from dataclasses import dataclass, field

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class PromptForwardOutput:
    z_q: torch.Tensor
    y_q: torch.Tensor
    protos: torch.Tensor
    classes: torch.Tensor
    logits: torch.Tensor | None = None
    proto_loss: torch.Tensor | None = None
    aux_losses: dict[str, torch.Tensor] = field(default_factory=dict)
    aux_metrics: dict[str, float] = field(default_factory=dict)
    debug_tensors: dict[str, torch.Tensor] = field(default_factory=dict)

    def __iter__(self):
        yield self.z_q
        yield self.y_q
        yield self.protos
        yield self.classes


def split_episode_support_query(labels, k_support, shuffle_support, device=None):
    if k_support < 1:
        raise ValueError("k_support must be at least 1.")

    episode_labels = labels.to(device=device or labels.device, dtype=torch.long)
    if episode_labels.ndim != 1:
        raise ValueError("labels must have shape [num_examples].")

    class_ids = torch.unique(episode_labels, sorted=True)
    support_indices_by_class = {}
    query_indices_by_class = {}
    is_query_example = torch.zeros_like(episode_labels, dtype=torch.bool)
    skipped_classes = []

    for class_id in class_ids:
        class_indices = (episode_labels == class_id).nonzero(as_tuple=True)[0]
        if shuffle_support and class_indices.numel() > 1:
            perm = torch.randperm(class_indices.numel(), device=class_indices.device)
            class_indices = class_indices.index_select(0, perm)

        if class_indices.numel() < k_support + 1:
            skipped_classes.append((int(class_id.item()), int(class_indices.numel())))
            continue

        class_value = int(class_id.item())
        support_indices = class_indices[:k_support]
        query_indices = class_indices[k_support:]
        support_indices_by_class[class_value] = support_indices
        query_indices_by_class[class_value] = query_indices
        is_query_example[query_indices] = True

    valid_class_ids = torch.tensor(
        sorted(support_indices_by_class),
        device=episode_labels.device,
        dtype=episode_labels.dtype,
    )
    if valid_class_ids.numel() < 2:
        raise ValueError(
            "Invalid episode: need at least 2 classes with "
            f"{k_support} supports and at least 1 query each; "
            f"got {valid_class_ids.numel()} valid classes out of {class_ids.numel()}. "
            f"Skipped classes: {skipped_classes}"
        )

    if not torch.any(is_query_example):
        raise ValueError(
            "Invalid episode: no query examples remain after filtering classes."
        )

    return (
        support_indices_by_class,
        query_indices_by_class,
        is_query_example,
        valid_class_ids,
    )


def split_support_for_calibration(
    support_indices_by_class,
    cal_frac,
    min_cal_per_class=1,
):
    support_proto_indices_by_class = {}
    support_cal_indices_by_class = {}

    for class_id, support_indices in support_indices_by_class.items():
        if support_indices.ndim != 1:
            raise ValueError("Support index tensors must be 1D.")
        n_support = int(support_indices.numel())
        if n_support == 0:
            raise ValueError(f"Class {class_id} has no support indices.")

        if n_support == 1:
            support_proto_indices_by_class[class_id] = support_indices
            support_cal_indices_by_class[class_id] = support_indices
            continue

        n_cal = max(int(min_cal_per_class), int(round(float(cal_frac) * n_support)))
        n_cal = max(1, min(n_support - 1, n_cal))
        support_proto_indices_by_class[class_id] = support_indices[:-n_cal]
        support_cal_indices_by_class[class_id] = support_indices[-n_cal:]

    return support_proto_indices_by_class, support_cal_indices_by_class


def build_attention_prototypes(
    z_all,
    support_indices_by_class,
    class_ids,
    dim,
    q_proj=None,
    k_proj=None,
    v_proj=None,
):
    if z_all.ndim != 2:
        raise ValueError("z_all must have shape [num_examples, dim].")
    if class_ids.ndim != 1:
        raise ValueError("class_ids must have shape [num_classes].")

    prototypes = []
    for class_id in class_ids:
        class_value = int(class_id.item())
        support_indices = support_indices_by_class.get(class_value)
        if support_indices is None or support_indices.numel() == 0:
            raise ValueError(f"Class {class_value} is missing support examples.")

        support_embeddings = z_all.index_select(0, support_indices)
        support_summary = support_embeddings.mean(dim=0, keepdim=True)
        query_token = q_proj(support_summary) if q_proj is not None else support_summary
        key_tokens = (
            k_proj(support_embeddings) if k_proj is not None else support_embeddings
        )
        value_tokens = (
            v_proj(support_embeddings) if v_proj is not None else support_embeddings
        )
        scale = key_tokens.size(-1) ** 0.5
        attention = torch.softmax(
            (query_token @ key_tokens.transpose(0, 1)) / scale,
            dim=-1,
        )
        prototypes.append((attention @ value_tokens).squeeze(0))

    return torch.stack(prototypes, dim=0)


class PromptEncoder(nn.Module):
    def __init__(self, gene_embed, cell_enc, dim=256, shuffle_support=True):
        super().__init__()
        self.gene_embed = gene_embed
        self.cell_enc = cell_enc
        self.shuffle_support = bool(shuffle_support)
        self.W_Q = nn.Linear(dim, dim, bias=False)
        self.W_K = nn.Linear(dim, dim, bias=False)
        self.W_V = nn.Linear(dim, dim, bias=False)

    def encode_cells(self, gene_ids, expr):
        token_sets = self.gene_embed(gene_ids, expr)
        return self.cell_enc(token_sets)

    def encode_dense(self, expr_matrix, gene_ids):
        tokens = self.gene_embed.forward_dense(gene_ids, expr_matrix)
        return self.cell_enc.forward_dense(tokens)

    def build_prototypes(self, z_all, support_indices_by_class, class_ids):
        return build_attention_prototypes(
            z_all,
            support_indices_by_class,
            class_ids,
            dim=z_all.size(-1),
            q_proj=self.W_Q,
            k_proj=self.W_K,
            v_proj=self.W_V,
        )

    def forward(self, gene_ids, expr, labels, k_support):
        if len(gene_ids) != len(expr):
            raise ValueError("gene_ids and expr must contain the same number of cells.")
        if len(gene_ids) != int(labels.numel()):
            raise ValueError("Batch size mismatch between inputs and labels.")

        z_all = self.encode_cells(gene_ids, expr)
        episode_labels = labels.to(device=z_all.device, dtype=torch.long)
        (
            support_indices_by_class,
            _query_indices_by_class,
            is_query_example,
            valid_class_ids,
        ) = split_episode_support_query(
            episode_labels,
            k_support=k_support,
            shuffle_support=self.shuffle_support,
            device=z_all.device,
        )
        protos = self.build_prototypes(z_all, support_indices_by_class, valid_class_ids)
        z_q = z_all[is_query_example]
        y_q = episode_labels[is_query_example]
        return PromptForwardOutput(
            z_q=z_q,
            y_q=y_q,
            protos=protos,
            classes=valid_class_ids.to(
                device=episode_labels.device,
                dtype=episode_labels.dtype,
            ),
        )


class GeneHashEmbed(nn.Module):
    def __init__(self, n_buckets=16384, d_emb=64):
        super().__init__()
        self.emb = nn.Embedding(n_buckets, d_emb)

    def forward(self, gene_ids, expr):
        if len(gene_ids) != len(expr):
            raise ValueError("gene_ids and expr must contain the same number of cells.")

        token_sets = []
        for cell_index, (g, e) in enumerate(zip(gene_ids, expr)):
            if g.ndim != 1 or e.ndim != 1:
                raise ValueError(
                    f"Cell {cell_index} must provide 1D gene_id and expr tensors."
                )
            if g.numel() == 0:
                raise ValueError(f"Cell {cell_index} has no genes.")
            if g.numel() != e.numel():
                raise ValueError(
                    f"Cell {cell_index} has mismatched gene_id/expr lengths: "
                    f"{g.numel()} vs {e.numel()}."
                )

            hashed_ids = torch.tensor(
                [
                    hash32(int(gene_id.item())) % self.emb.num_embeddings
                    for gene_id in g
                ],
                device=g.device,
                dtype=torch.long,
            )
            gene_vectors = self.emb(hashed_ids)
            expr_values = e.to(device=gene_vectors.device, dtype=gene_vectors.dtype)
            token_sets.append(
                torch.cat([gene_vectors, expr_values.log1p().unsqueeze(-1)], dim=1)
            )

        return token_sets

    def hash_gene_ids(self, gene_ids: torch.Tensor) -> torch.Tensor:
        if gene_ids.ndim != 1:
            raise ValueError("hash_gene_ids expects a 1D gene-id tensor.")
        hashed_ids = [
            hash32(int(gene_id.item())) % self.emb.num_embeddings for gene_id in gene_ids
        ]
        return torch.tensor(
            hashed_ids,
            device=gene_ids.device,
            dtype=torch.long,
        )

    def forward_dense(self, gene_ids: torch.Tensor, expr_matrix: torch.Tensor) -> torch.Tensor:
        if gene_ids.ndim != 1:
            raise ValueError("forward_dense expects gene_ids with shape [num_genes].")
        if expr_matrix.ndim != 2:
            raise ValueError(
                "forward_dense expects expr_matrix with shape [num_cells, num_genes]."
            )
        if expr_matrix.size(1) != gene_ids.numel():
            raise ValueError(
                "forward_dense gene_ids must align with expr_matrix gene dimension."
            )

        hashed_ids = self.hash_gene_ids(gene_ids.to(device=expr_matrix.device))
        gene_vectors = self.emb(hashed_ids)
        expr_values = expr_matrix.to(device=gene_vectors.device, dtype=gene_vectors.dtype)
        return torch.cat(
            [
                gene_vectors.unsqueeze(0).expand(expr_values.size(0), -1, -1),
                expr_values.log1p().unsqueeze(-1),
            ],
            dim=-1,
        )
