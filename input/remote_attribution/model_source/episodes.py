from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import torch


def _as_numpy_labels(labels: np.ndarray | torch.Tensor) -> np.ndarray:
    if isinstance(labels, torch.Tensor):
        return labels.detach().cpu().numpy()
    return np.asarray(labels)


@dataclass
class DenseEpisodeBatch:
    support_x: torch.Tensor
    support_y: torch.Tensor
    query_x: torch.Tensor
    query_y: torch.Tensor | None
    class_ids: torch.Tensor
    gene_permutation: torch.Tensor | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to(self, device: str | torch.device) -> "DenseEpisodeBatch":
        return DenseEpisodeBatch(
            support_x=self.support_x.to(device=device, dtype=torch.float32),
            support_y=self.support_y.to(device=device, dtype=torch.long),
            query_x=self.query_x.to(device=device, dtype=torch.float32),
            query_y=(
                None
                if self.query_y is None
                else self.query_y.to(device=device, dtype=torch.long)
            ),
            class_ids=self.class_ids.to(device=device, dtype=torch.long),
            gene_permutation=(
                None
                if self.gene_permutation is None
                else self.gene_permutation.to(device=device, dtype=torch.long)
            ),
            metadata=dict(self.metadata),
        )

    @property
    def num_classes(self) -> int:
        return int(self.class_ids.numel())

    @property
    def support_size(self) -> int:
        return int(self.support_y.numel())

    @property
    def query_size(self) -> int:
        return 0 if self.query_y is None else int(self.query_y.numel())


def stratified_label_split(
    labels: np.ndarray | torch.Tensor,
    *,
    val_fraction: float,
    seed: int,
    min_train_per_class: int = 1,
    min_val_per_class: int = 1,
) -> tuple[np.ndarray, np.ndarray]:
    if not 0.0 < float(val_fraction) < 1.0:
        raise ValueError("val_fraction must be strictly between 0 and 1.")

    labels_np = _as_numpy_labels(labels)
    rng = np.random.RandomState(seed)
    train_indices: list[int] = []
    val_indices: list[int] = []
    for class_id in sorted(np.unique(labels_np).tolist()):
        class_indices = np.flatnonzero(labels_np == class_id)
        if class_indices.size < (min_train_per_class + min_val_per_class):
            raise ValueError(
                f"Class {class_id} has only {class_indices.size} examples; "
                "cannot satisfy the requested stratified split."
            )
        permuted = rng.permutation(class_indices)
        n_val = int(round(class_indices.size * float(val_fraction)))
        n_val = max(int(min_val_per_class), n_val)
        n_val = min(class_indices.size - int(min_train_per_class), n_val)
        val_indices.extend(permuted[:n_val].tolist())
        train_indices.extend(permuted[n_val:].tolist())
    return np.asarray(sorted(train_indices), dtype=np.int64), np.asarray(
        sorted(val_indices), dtype=np.int64
    )


def sample_support_indices_by_class(
    labels: np.ndarray | torch.Tensor,
    class_ids: np.ndarray | torch.Tensor,
    *,
    k_support: int,
    seed: int,
) -> dict[int, np.ndarray]:
    if int(k_support) < 1:
        raise ValueError("k_support must be at least 1.")
    labels_np = _as_numpy_labels(labels)
    class_ids_np = _as_numpy_labels(class_ids)
    rng = np.random.RandomState(seed)
    output: dict[int, np.ndarray] = {}
    for class_id in class_ids_np.tolist():
        class_indices = np.flatnonzero(labels_np == class_id)
        if class_indices.size < int(k_support):
            raise ValueError(
                f"Class {class_id} has {class_indices.size} cells but k_support="
                f"{k_support} was requested."
            )
        chosen = np.sort(rng.choice(class_indices, size=int(k_support), replace=False))
        output[int(class_id)] = chosen.astype(np.int64, copy=False)
    return output


class BalancedEpisodeSampler:
    def __init__(
        self,
        matrix: np.ndarray,
        labels: np.ndarray | torch.Tensor,
        *,
        seed: int,
        anonymous_genes: bool = False,
        obs_names: np.ndarray | None = None,
    ):
        matrix_np = np.asarray(matrix)
        if matrix_np.ndim != 2:
            raise ValueError("matrix must have shape [cells, genes].")
        labels_np = _as_numpy_labels(labels).astype(np.int64, copy=False)
        if labels_np.ndim != 1 or labels_np.shape[0] != matrix_np.shape[0]:
            raise ValueError("labels must be a 1D array aligned with matrix rows.")

        self.matrix = matrix_np
        self.labels = labels_np
        self.obs_names = None if obs_names is None else np.asarray(obs_names)
        self.class_ids = np.asarray(sorted(np.unique(labels_np).tolist()), dtype=np.int64)
        self.indices_by_class = {
            int(class_id): np.flatnonzero(labels_np == class_id).astype(np.int64)
            for class_id in self.class_ids.tolist()
        }
        self.rng = np.random.RandomState(seed)
        self.anonymous_genes = bool(anonymous_genes)

    @property
    def num_genes(self) -> int:
        return int(self.matrix.shape[1])

    def sample_episode(
        self,
        *,
        k_support: int,
        q_query: int | str,
        class_ids: np.ndarray | torch.Tensor | None = None,
        query_seed: int | None = None,
    ) -> DenseEpisodeBatch:
        if class_ids is None:
            class_ids_np = self.class_ids
        else:
            class_ids_np = _as_numpy_labels(class_ids).astype(np.int64, copy=False)
        if class_ids_np.ndim != 1 or class_ids_np.size < 2:
            raise ValueError("Episodes require at least 2 classes.")

        rng = self.rng if query_seed is None else np.random.RandomState(int(query_seed))
        support_rows: list[int] = []
        support_labels: list[int] = []
        query_rows: list[int] = []
        query_labels: list[int] = []

        for local_class_index, class_id in enumerate(class_ids_np.tolist()):
            class_indices = self.indices_by_class[int(class_id)]
            if q_query == "all":
                required = int(k_support) + 1
            else:
                required = int(k_support) + int(q_query)
            if class_indices.size < required:
                raise ValueError(
                    f"Class {class_id} has {class_indices.size} cells but episode "
                    f"requires at least {required}."
                )
            permuted = rng.permutation(class_indices)
            support_idx = permuted[: int(k_support)]
            if q_query == "all":
                query_idx = permuted[int(k_support) :]
            else:
                query_idx = permuted[int(k_support) : int(k_support) + int(q_query)]
            support_rows.extend(support_idx.tolist())
            support_labels.extend([local_class_index] * int(support_idx.size))
            query_rows.extend(query_idx.tolist())
            query_labels.extend([local_class_index] * int(query_idx.size))

        support_x = torch.as_tensor(
            self.matrix[np.asarray(support_rows, dtype=np.int64)],
            dtype=torch.float32,
        )
        query_x = torch.as_tensor(
            self.matrix[np.asarray(query_rows, dtype=np.int64)],
            dtype=torch.float32,
        )

        gene_permutation = None
        if self.anonymous_genes:
            permutation = rng.permutation(self.num_genes).astype(np.int64, copy=False)
            gene_permutation = torch.as_tensor(permutation, dtype=torch.long)
            support_x = support_x.index_select(1, gene_permutation)
            query_x = query_x.index_select(1, gene_permutation)

        metadata = {
            "support_obs_names": None,
            "query_obs_names": None,
            "raw_class_ids": class_ids_np.tolist(),
        }
        if self.obs_names is not None:
            metadata["support_obs_names"] = self.obs_names[
                np.asarray(support_rows, dtype=np.int64)
            ].tolist()
            metadata["query_obs_names"] = self.obs_names[
                np.asarray(query_rows, dtype=np.int64)
            ].tolist()

        return DenseEpisodeBatch(
            support_x=support_x,
            support_y=torch.as_tensor(support_labels, dtype=torch.long),
            query_x=query_x,
            query_y=torch.as_tensor(query_labels, dtype=torch.long),
            class_ids=torch.arange(class_ids_np.size, dtype=torch.long),
            gene_permutation=gene_permutation,
            metadata=metadata,
        )

    def build_support_query_batch(
        self,
        *,
        support_indices_by_class: dict[int, np.ndarray],
        query_matrix: np.ndarray,
        query_labels: np.ndarray | torch.Tensor,
        query_obs_names: np.ndarray | None = None,
        query_seed: int | None = None,
    ) -> DenseEpisodeBatch:
        ordered_classes = np.asarray(
            sorted(int(class_id) for class_id in support_indices_by_class),
            dtype=np.int64,
        )
        support_rows: list[int] = []
        support_labels: list[int] = []
        raw_to_local = {int(class_id): idx for idx, class_id in enumerate(ordered_classes)}
        for class_id in ordered_classes.tolist():
            support_indices = np.asarray(
                support_indices_by_class[int(class_id)], dtype=np.int64
            )
            support_rows.extend(support_indices.tolist())
            support_labels.extend([raw_to_local[int(class_id)]] * support_indices.size)

        support_x = torch.as_tensor(
            self.matrix[np.asarray(support_rows, dtype=np.int64)],
            dtype=torch.float32,
        )
        query_x = torch.as_tensor(np.asarray(query_matrix), dtype=torch.float32)
        query_labels_np = _as_numpy_labels(query_labels).astype(np.int64, copy=False)
        mapped_query_labels = torch.as_tensor(
            [raw_to_local[int(value)] for value in query_labels_np.tolist()],
            dtype=torch.long,
        )

        rng = self.rng if query_seed is None else np.random.RandomState(int(query_seed))
        gene_permutation = None
        if self.anonymous_genes:
            permutation = rng.permutation(self.num_genes).astype(np.int64, copy=False)
            gene_permutation = torch.as_tensor(permutation, dtype=torch.long)
            support_x = support_x.index_select(1, gene_permutation)
            query_x = query_x.index_select(1, gene_permutation)

        metadata = {
            "support_obs_names": None,
            "query_obs_names": None,
            "raw_class_ids": ordered_classes.tolist(),
        }
        if self.obs_names is not None:
            metadata["support_obs_names"] = self.obs_names[
                np.asarray(support_rows, dtype=np.int64)
            ].tolist()
        if query_obs_names is not None:
            metadata["query_obs_names"] = np.asarray(query_obs_names).tolist()

        return DenseEpisodeBatch(
            support_x=support_x,
            support_y=torch.as_tensor(support_labels, dtype=torch.long),
            query_x=query_x,
            query_y=mapped_query_labels,
            class_ids=torch.arange(ordered_classes.size, dtype=torch.long),
            gene_permutation=gene_permutation,
            metadata=metadata,
        )
