#!/usr/bin/env python3
"""Index the complete frozen paper export without executing its builders.

The JSON preserves source documentation and observed schemas separately from the
editorial disposition. --check regenerates in memory and never writes files.
"""
from __future__ import annotations
import argparse
import ast
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT.parent / 'paper_export_20261011'
OUTPUT = ROOT / 'evidence/export_index.json'
INDEX_MD = ROOT / 'notes/export_index.md'
DISPOSITION_MD = ROOT / 'notes/export_disposition.md'
BLOCKS = {
 'fig1': ('Model, simulator and training lineage', 'main; appendix; later Methods', 'Report architecture and training exposure now; reserve code-level construction and training details for Methods.'),
 'fig2': ('Gene-view and transcriptome-width comparisons', 'main; appendix', 'Quantify paired gene-width benefits and losses; preserve support-draw uncertainty and alternate views.'),
 'fig3': ('Transfer of the cellular prior to tabular models', 'main; appendix', 'Report matched-parent adaptation gains, support-budget dependence and negative transfer; retain generic-table tradeoffs.'),
 'fig4': ('Biological benchmark and model context', 'main; appendix', 'Populate the main performance table and complete panel-level appendix; distinguish declared series from post hoc diagnostics.'),
 'fig5': ('Gene-deletion attribution, fidelity and cost', 'main; appendix; later Methods', 'Report validated fidelity and stability with restricted validation scope; distinguish measured, inferred and hypothetical timing routes.'),
 'fig6': ('Operator and task-mixture ablations', 'main; appendix', 'Report all three operator arms, the failed prespecified test, later paired comparisons and probability-quality tradeoffs.'),
 'fig7': ('Simulator realism against public biological references', 'main; appendix', 'Quantify alignment and remaining discrepancy descriptively; calibration references are not independent validation.'),
 'supp_exposure': ('Pretraining-exposure qualifications', 'main; appendix', 'Qualify benchmark interpretation with public pretraining exposure and uncertain exact-cell overlap.'),
 'supp_prior_ablation': ('Ten-candidate prior screen and hard-tier checks', 'main; appendix', 'Report the positive filtering result alongside all neutral, rejected, unresolved and untestable candidates.'),
 'supp_rosmap': ('Provisional ROSMAP aggregates and label issues', 'main (provisional); appendix; later Methods', 'Keep provisional status explicit; no final biological claim before label corrections and the controlled-data analysis.'),
 'supp_stored_zeros': ('Stored-zero and reconstructed-count sensitivity', 'appendix', 'Retain exploratory sensitivity and support-replacement checks without changing the primary benchmark input.'),
 'supp_taskmix_tradeoff': ('Task-mixture checkpoint and gene-view tradeoffs', 'appendix', 'Preserve checkpoint/view confounding and unequal sampling; not an isolated causal gene-view comparison.'),
 'glossary': ('Model, panel, metric and vocabulary definitions', 'provenance; later Methods', 'Resolve the harmonized identifiers and metric meanings used by every evidence table.'),
}
BUILD_BLOCKS = {
 'ablations': ['fig6', 'supp_prior_ablation', 'supp_taskmix_tradeoff'],
 'benchmark': ['fig4', 'supp_exposure'],
 'knockout': ['fig5'],
 'scaling_transfer': ['fig2', 'fig3'],
 'method_realism_misc': ['fig1', 'fig7', 'supp_stored_zeros', 'supp_rosmap', 'glossary'],
 'assemble': list(BLOCKS), 'finalize': list(BLOCKS),
}
MAIN_SELECTIONS = {
 'fig1__facts.csv': 'Simulator components, synthetic-only weight training and episode/input contract.',
 'fig1__lineage.csv': 'Reference-model parameters, dataset banks, scheduled/loss-bearing episodes and prior-version exposure.',
 'fig2__cases.csv': 'Three-draw benchmark means, gene-view means and released-model declines; keep the twenty-draw analysis distinct.',
 'fig2__cells.csv': 'Paired twenty-draw gene-width gains and PBMC one-shot losses with correctly labelled intervals.',
 'fig3__arms.csv': 'Released starting points and cellular/adaptation budgets, including generic replay.',
 'fig3__paired.csv': 'Matched-parent adaptation gains by support budget and the fine-PBMC ten-support decline.',
 'fig3__generic_tables_cases.csv': 'TabICLv2 generic-table degradation after cellular adaptation; four tables and five split seeds.',
 'fig4__cases.csv': 'Conventional LDA comparison and declared benchmark series with model-specific input routes.',
 'fig4__panels.csv': 'Panel definitions, supports, query population and primary input conventions.',
 'fig4__methods.csv': 'Comparator identities, training/exposure context, selected representations and classifier choices.',
 'fig4__default_series.csv': 'Declared series and exposure marks underlying the overview; not a new performance observation.',
 'fig5__cases.csv': 'Six-case/two-model validation scope, correctly predicted cells and full-precision attribution.',
 'fig5__fidelity_by_case.csv': 'Within-cell correlation fidelity and relative error, summarized at the case/model level.',
 'fig5__marker_ranks.csv': 'Illustrative IL7R and NKG7 ranking statements within the evaluated class-margin rankings.',
 'fig5__deletion_curves.csv': 'PBMC top-50 query-gene deletion versus random expressed-gene margin reversals.',
 'fig5__stability.csv': 'Top-20 class-gene overlap across support configurations; not context-independent importance.',
 'fig5__cost_by_route.csv': 'Provisional O05 runtime/forward-equivalent statement; measured and extrapolated components remain explicit.',
 'fig6__operator_readings.csv': 'No-operator/diagonal/full endpoints and later twenty-draw descriptive decomposition.',
 'fig6__operator_paired_by_view.csv': 'Paired full-versus-none and full-versus-diagonal gains and intervals at fine-PBMC B100.',
 'fig6__operator_n3_test_wide.csv': 'Failed prespecified coarse-PBMC harm test, separate from the later descriptive analysis.',
 'fig6__taskmix_paired.csv': 'One-shot gains on four panels and higher-support negative-log-likelihood tradeoffs.',
 'fig6__taskmix_stream_composition.csv': 'Unequal cells per update in the learnable-versus-standard task-mixture comparison.',
 'fig7__sim_vs_real_summary.csv': 'Strongest-marker fold change and task-easiness discrepancy relative to the calibration references.',
 'supp_exposure__panel_chances.csv': 'Qualifications concerning possible exact-cell pretraining exposure.',
 'supp_exposure__study_exposure.csv': 'Qualifications concerning PBMC and held-out cortex study overlap in pretraining.',
 'supp_prior_ablation__outcomes.csv': 'Ten-candidate screen, retained learnable-task filter, rejected gene-absence candidate and nonpositive outcomes.',
 'supp_prior_ablation__replicates.csv': 'Three task-stream effects underlying the retained proxy result; not model-seed replication.',
 'supp_prior_ablation__thresholds.csv': 'Frozen retention/noise and predictive-log-loss guard thresholds for the prior campaign.',
 'supp_rosmap__auc.csv': 'Provisional O02 donor-level AUC and corrected repeated-split interval; pending label audit and rerun.',
 'supp_rosmap__label_issues.csv': 'Reason O02 remains provisional; no completed or independent disease validation.',
}

NO_INFERENCE = ('Never treat query cells, heterogeneous benchmark panels or different model checkpoints as independent training replicates. '
                'Every trained model has one model seed. Three support draws are descriptive values/ranges; 10/20 draws allow the documented paired t intervals. '
                'Three task streams share a model seed; kidney draws are donor-held-out folds; attribution ranges and timings are not confidence intervals.')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def tidy(s):
    return re.sub(r'\s+', ' ', s).strip()


def dictionary_entries(text):
    parts = re.split(r'^### `(data/[^`]+)`\s*$', text, flags=re.M)
    result = {}
    for name, section in zip(parts[1::2], parts[2::2]):
        # Stop before the next block introduction, which is not this file's data.
        section = re.split(r'^## ', section, maxsplit=1, flags=re.M)[0].strip()
        first_table = re.search(r'^\| column \|', section, re.M)
        preamble = section[:first_table.start()] if first_table else section
        columns = {}
        for line in section.splitlines():
            m = re.match(r'^\| `([^`]+)` \| (.*?) \| (.*?) \|$', line)
            if m and not re.fullmatch(r'[a-f0-9]{64}', m[2].strip('`')):
                columns[m[1]] = {'meaning_and_unit': m[2], 'documented_values': m[3]}
        def field(labels):
            for label in labels:
                m = re.search(r'(?:\*\*)?' + label + r'[:.]?(?:\*\*)?\s*(.*?)(?=\n\s*\n|\n- |\n\*\*|$)', preamble, re.I | re.S)
                if m:
                    return tidy(m[1])
            return ''
        content = field(['One row is', 'Content'])
        if not content:
            paras = [tidy(p) for p in preamble.split('\n\n') if p.strip() and not p.strip().startswith(('Rows:', '**Changed', '**Operator', '**A8d', '- '))]
            content = paras[0] if paras else tidy(preamble)
        sources = []
        for line in section.splitlines():
            m = re.match(r'\| `([^`]+)` \| `([a-f0-9]{64})` \| ([\d,]+) \|', line)
            if m:
                sources.append({'path': m[1], 'sha256': m[2], 'bytes': int(m[3].replace(',', ''))})
            else:
                m = re.search(r'`([^`]+)` sha256 `([a-f0-9]{64})`', line)
                if m:
                    sources.append({'path': m[1], 'sha256': m[2]})
        result[name] = {
            'anchor': 'DATA_DICTIONARY.md#' + name.replace('/', '').replace('.', ''),
            'line': text[:text.find('### `' + name + '`')].count('\n') + 1,
            'unit_of_analysis': content,
            'derivation': field(['How it was derived', 'How derived', 'Derived from']),
            'intervals': field(['Intervals', 'Legitimate intervals']),
            'preamble': preamble.strip(),
            'columns': columns,
            'upstream_sources': sources,
        }
    assert len(result) == 115, f'Expected 115 documented data files, found {len(result)}'
    return result


def role_for_data(name):
    tail = name.split('__', 1)[1]
    if name == 'fig5__cells.csv':
        return 'case-level or finer observations'
    if name.startswith('glossary__'):
        return 'glossary'
    if tail.endswith('_wide.csv'):
        return 'wide convenience view'
    if any(x in tail for x in ['facts', 'architecture_modules', 'lineage', 'training_stream', 'stream_composition', 'arms', 'methods', 'caveats', 'panels', 'thresholds', 'label_issues', 'statistics', 'library_column_use', 'arm_differences', 'hard_tier_tasks']):
        return 'design, definition or provenance facts'
    if any(x in tail for x in ['summary', 'means', 'cells.csv', 'paired_by_view', 'paired.csv', 'trajectory.csv', 'outcomes', 'replicates', 'shrink', 'stability', 'fidelity_by_case', 'fidelity_by_class', 'real_by', 'best_per_family', 'default_series', 'figure_marks', 'domain_shares', 'panel_chances', 'study_exposure']):
        return 'derived summary or comparison'
    if any(x in tail for x in ['cases', 'pairs', 'by_cell', 'sim_units', 'donor_deltas', 'deletion_curves', 'top_genes', 'marker_ranks']):
        return 'case-level or finer observations'
    return 'documented diagnostic or auxiliary measurement'


def disposition(name, block, role):
    base = BLOCKS[block]
    if block == 'glossary':
        return 'provenance; later Methods', base[2]
    if block == 'supp_rosmap':
        return 'main (provisional); appendix; later Methods', base[2] + ' Retained in bold red as O02 in main Results.'
    filename = Path(name).name
    if filename in MAIN_SELECTIONS:
        destination = 'main (provisional); appendix; later Methods' if filename == 'fig5__cost_by_route.csv' else 'main; appendix'
        return destination, MAIN_SELECTIONS[filename] + ' Other rows remain supporting evidence; this designation does not promote the whole file to main-text results.'
    if filename == 'fig2__cases_cellpfn_later_states.csv':
        return 'appendix', 'Later-state trajectories have checkpoint/view-dependent draw counts and unequal exposure; do not interpret them as a clean gene-view contrast.'
    if filename == 'fig2__inputs_and_cost.csv':
        return 'appendix; later Methods', 'Input dimensions and recorded timing/memory diagnostics support scope checks; shared-GPU timings do not establish a matched-compute advantage.'
    if 'wide convenience' in role:
        return 'provenance', 'Convenience reshape; use its long-format parent for claims and do not count it as independent evidence.'
    if any(x in name for x in ['ko_pairs_by_cell', 'ko_pairs_by_class', 'fidelity_by_cell', 'top_genes', 'deletion_curves', 'sim_units', 'hard_tier_cases', 'hard_tier_tasks', 'trajectory_cases']):
        return 'provenance; appendix', 'Retain exhaustive underlying observations for verification; summarize them in the appendix rather than printing all rows. ' + base[2]
    if any(x in name for x in ['cost_dsloo_vs_kumo', 'cost_kumo_estimated', 'cost_by_route', 'cost_measured']):
        return 'appendix; later Methods', 'Separate measured times from extrapolated/inferred and paper-only routes; final runtime claims remain unresolved.'
    if any(x in name for x in ['posthoc_diagnostics', 'generic_tables', 'cases_other_views', 'p1_arm_differences', 'gradient_diagnostics', 'kumo_gene_coverage', 'scanvi_training_budget']):
        return 'appendix', 'Supporting or post hoc diagnostic; label its status and do not substitute it for the declared primary comparison.'
    if block == 'fig1' and any(x in name for x in ['architecture_modules', 'training_stream']):
        return 'appendix; later Methods', 'Use verified parameter/training facts as needed now; detailed architecture and stream construction await the Methods code audit.'
    return 'appendix', 'Supporting observations, derived summaries or definitions for this block; no separately selected main-text anchor. ' + base[2]


def blocks_for(path, text=''):
    if path.startswith('data/'):
        return [Path(path).name.split('__')[0]]
    matches = {b for b in BLOCKS if re.search(r'(?<![a-z0-9])' + re.escape(b) + r'(?:__|\b)', path + '\n' + text)}
    if matches:
        return sorted(matches)
    for part in Path(path).parts:
        if part in BUILD_BLOCKS:
            return BUILD_BLOCKS[part]
        stem = Path(part).stem.split('__')[0]
        if stem in BUILD_BLOCKS:
            return BUILD_BLOCKS[stem]
    return list(BLOCKS)


def nondata_role(path):
    if 'expected_before_' in path:
        return 'historical validation freeze', 'historical', 'Superseded expected values; retain the change history and never cite as current results.'
    if path.endswith('patch_figures_a8d_refresh.py'):
        return 'retired patch script', 'historical', 'Retired text patch retained as provenance; not the current assembly path and must not be rerun.'
    if 'expected_changes' in path:
        return 'refresh change audit', 'provenance', 'Explains transitions between frozen expected-value sets; use current checks/expected.csv for validation.'
    if path.startswith(('sections/', 'dictionary/')):
        return 'builder source document' if path.endswith('.md') else 'builder model registry', 'provenance; later Methods', 'Builder parts may retain pre-harmonization identifiers/checksums; current FIGURES.md, DATA_DICTIONARY.md and data/ govern manuscript facts.'
    if path.startswith('checks/') or Path(path).name.startswith(('check_', 'check.', 'checks.', 'verify_','server_verification','server_check')) or path == 'CHECKS.md':
        return 'validation record or checker', 'provenance', 'Reproducibility and source consistency check; no independent experimental replication.'
    if path.endswith('.py') or path.endswith('.sh'):
        return 'builder or transformation script', 'provenance; later Methods', 'Static source inspection only; server-dependent builders are not executed and do not replace the source-code Methods audit.'
    if path.endswith('.json') and ('_registry/' in path or '/sources/' in path or '.record.' in path):
        return 'builder provenance registry', 'provenance', 'Describes derivation and server inputs; output checksums may predate harmonization and are not current file identities.'
    if path.endswith(('.json', '.txt')):
        return 'builder log or constants', 'provenance', 'Builder metadata and recorded diagnostics; distinguish recorded counts from current observed file counts.'
    if path.endswith('.csv'):
        return 'provenance mapping or registry', 'provenance', 'Source mapping, transformations or builder validation; current harmonized data supply manuscript values.'
    if path == 'MANIFEST.sha256':
        return 'source checksum manifest', 'provenance', 'Frozen export file identities; the separate manuscript export_manifest.csv also covers this manifest itself.'
    if path in {'FIGURES.md', 'DATA_DICTIONARY.md'}:
        return 'current interpretation and schema', 'main; appendix; later Methods', 'Primary narrative/schema companion for current harmonized data; preserve caveats and file-specific qualifications.'
    if path == 'STATUS.md':
        return 'readiness and open-issue record', 'provenance; later Methods', 'Readiness context, not a replacement for current data and refreshed figure/dictionary entries.'
    if path == 'CHANGELOG.md':
        return 'refresh history and issue resolution', 'provenance', 'Records corrections and remaining limitations, including the A8d and operator refreshes.'
    if path == 'build/knockout/README.md':
        return 'builder instructions and validation scope', 'provenance; later Methods', 'Documents the attribution export and server verification requirements; current FIGURES.md governs result interpretation.'
    if path == 'README.md':
        return 'export navigation and conventions', 'provenance', 'Entry point and conventions; a few historical counts/status descriptions are superseded by current data.'
    raise AssertionError('Unclassified file: ' + path)


def csv_profile(raw, docs=None):
    reader = csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    columns = reader.fieldnames or []
    seen = {c: collections.Counter() for c in columns}
    n = 0
    for row in reader:
        assert None not in row, 'Malformed CSV row'
        n += 1
        for c in columns:
            seen[c][row[c] or ''] += 1
    profiles = []
    for c in columns:
        counts = seen[c]
        vals = sorted(x for x in counts if x != '')
        obj = {'name': c, 'missing': counts.get('', 0), 'distinct_nonempty': len(vals)}
        if docs:
            obj.update(docs.get(c, {}))
        if len(vals) <= 30:
            obj['values'] = vals
        else:
            nums = []
            try:
                nums = [float(v) for v in vals]
            except ValueError:
                pass
            if nums:
                obj['numeric_range'] = [min(nums), max(nums)]
            else:
                obj['examples'] = vals[:3]
        profiles.append(obj)
    raw_status = {c: dict(sorted(v.items())) for c, v in seen.items() if re.search(r'(?:status|decision|outcome|verdict|test_label|readiness)', c)}
    coverage_names = {'model_id','model_a','model_b','panel','label_set','support_per_class','gene_view','metric','unit','draw','draw_kind','n_draws','n_replicates','replicate','checkpoint_update','interval','interval_kind','aggregation','mean_kind','timing_context','cost_kind','estimate_kind','arm','training_seeds','task_draw_replicates','task_stream_seed','model_seed'}
    coverage = {c: p for c, p in zip(columns, profiles) if c in coverage_names}
    return {'rows': n, 'columns': columns, 'column_profiles': profiles, 'coverage': coverage, 'raw_status_counts': raw_status}


def python_profile(text):
    tree = ast.parse(text)
    defs = [{'name': n.name, 'line': n.lineno, 'docstring': ast.get_docstring(n)} for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    calls = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            name = ast.unparse(n.func)
            if re.search(r'(read|write|open|load|dump|save|to_csv|glob|replace|unlink|mkdir|copy|sha256|run|check_call)', name, re.I):
                calls.append({'line': n.lineno, 'call': ast.get_source_segment(text, n)[:500]})
    strings = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    path_strings = sorted(set(s for s in strings if len(s) < 1000 and re.search(r'\.(csv|json|md|py|sha256|npz|pt|gz|yaml|txt)(?:$|[#:/])', s)))
    return {'docstring': ast.get_docstring(tree), 'definitions': defs, 'io_calls': sorted(calls, key=lambda x:x['line']), 'path_literals': path_strings, 'inspection': 'AST parsed; source read; no execution'}


def links_in(text, files):
    links = set()
    for f in files:
        if f in text or Path(f).name in text:
            links.add(f)
    return sorted(links)


def fallback_intervals(path, block, role):
    if block == 'fig5':
        return 'No confidence intervals supported. One value per case/model; ranges are descriptive, class/cell/gene quantities are nested, timings are single runs (DATA_DICTIONARY.md: Which intervals are legitimate).'
    if block in {'glossary', 'supp_exposure'} or role == 'design, definition or provenance facts':
        return 'Not applicable to definitions, design facts or exposure assessments; any reported exposure bands are source assessments, not computed sampling confidence intervals.'
    if block == 'fig4':
        return 'Three support draws per PBMC/Zebra condition are descriptive points/ranges; kidney draws are donor-held-out folds. Do not infer uncertainty across heterogeneous panels or models (DATA_DICTIONARY.md: Which intervals are legitimate).'
    if block == 'fig3':
        return 'Use the parent case table and exact draw/run filters. Three draws are descriptive; stage0_efast has 10 or 5 draws. Kumo-small task-stream replicates share one model seed. No interval across panels or support budgets (DATA_DICTIONARY.md: fig3__cases.csv).'
    if block == 'fig2':
        return 'Use the parent case table and exact draw-set filters: CellPFN commonly 20 support draws, baselines 3; later states have view/checkpoint-dependent counts. Pair gene views by draw; no interval across panels or over an overall model mean (DATA_DICTIONARY.md: fig2__cases.csv).'
    return 'File-specific interval not separately stated; use its dictionary preamble and the export-wide legitimate-interval rules. No interval is inferred by this index.'


def data_readiness(path, profile):
    if 'supp_rosmap__' in path:
        return {'state': 'provisional', 'reason': 'Label fixes pending; nonfinal report aggregates only, regardless of a numeric value being present.'}
    if any(x in path for x in ['cost_dsloo_vs_kumo', 'cost_kumo_estimated', 'cost_by_route', 'cost_measured']):
        return {'state': 'qualified', 'reason': 'Measured/inferred/estimated timing routes must remain separate; no completed end-to-end runtime claim.'}
    if 'posthoc' in path or 'supp_taskmix_tradeoff' in path:
        return {'state': 'exploratory', 'reason': 'Post hoc or checkpoint/view-confounded diagnostic; usable with explicit qualification.'}
    if 'supp_prior_ablation' in path:
        return {'state': 'mixed outcomes', 'reason': 'Preserve KEEP/NEUTRAL/DROP/UNRESOLVED/NOT_TESTABLE outcomes and replicate-specific coverage; lack of evidence is not a zero effect.'}
    if path.startswith('data/fig7'):
        return {'state': 'descriptive', 'reason': 'Public reference statistics were used in calibration; synthetic units are nested within banks and no inferential test is supported.'}
    if 'n3_' in path or 'prereg_' in path:
        return {'state': 'prespecified test', 'reason': 'Preserve the original failed operator test. PBMC uses donor enumeration with approximate 80% coverage; Zebra uses a 95% donor bootstrap within study. These intervals condition on fixed support draws and one model seed.'}
    return {'state': 'usable with recorded limitations', 'reason': 'Follow row-level status and dictionary interval rules; present estimates only for evaluated cells and maintain model/input restrictions.'}


def build():
    files = sorted(p.relative_to(EXPORT).as_posix() for p in EXPORT.rglob('*') if p.is_file())
    assert len(files) == 288, f'Export inventory changed: {len(files)} files'
    raw = {f: (EXPORT / f).read_bytes() for f in files}
    texts = {f: b.decode('utf-8-sig') for f, b in raw.items()}
    dd = dictionary_entries(texts['DATA_DICTIONARY.md'])
    manifest = {r['source'].split('/',1)[1]:r['sha256'] for r in csv.DictReader((ROOT / 'evidence/export_manifest.csv').open())}
    assert set(manifest) == set(files), 'Original export manifest coverage changed'
    registries = {}
    json_docs = {f:json.loads(texts[f]) for f in files if f.endswith('.json')}
    for path, obj in json_docs.items():
        if '/_registry/' in path:
            registries[obj['file']] = (path, obj)
    records = []
    for f in files:
        digest = sha(raw[f])
        assert manifest[f] == digest, f'Frozen source modified: {f}'
        block_ids = blocks_for(f, texts[f] if not f.endswith('.csv') else '')
        record = {'path': f, 'bytes': len(raw[f]), 'sha256': digest, 'file_type': Path(f).suffix[1:], 'blocks': block_ids,
                  'source_integrity': 'matches original evidence/export_manifest.csv', 'related_export_files': links_in(texts[f], files) if not f.endswith('.csv') else [],
                  'raw_status_counts': {}, 'replication_policy': NO_INFERENCE}
        if f.startswith('data/'):
            doc = dd[f]
            block = block_ids[0]
            role = role_for_data(Path(f).name)
            destination, reason = disposition(f, block, role)
            record.update({'role':role, 'purpose':doc['unit_of_analysis'], 'authority':'current harmonized data',
                           'manuscript_destination':destination, 'disposition_reason':reason, 'selected_main_anchor':MAIN_SELECTIONS.get(Path(f).name), 'dictionary':doc,
                           'unit_of_analysis':doc['unit_of_analysis'], 'aggregation':doc['derivation'],
                           'interval_definition':doc['intervals'] or fallback_intervals(f, block, role),
                           'readiness':data_readiness(f, None)})
            record.update(csv_profile(raw[f],doc['columns']))
            record['replication'] = {'observed_dimensions': {k:v for k,v in record['coverage'].items() if k in {'draw','draw_kind','n_draws','n_replicates','replicate','training_seeds','task_draw_replicates','model_seed','task_stream_seed'}}, 'interpretation': record['interval_definition'], 'limit': NO_INFERENCE}
            assert set(record['columns']) <= set(doc['columns']), f'Undocumented columns: {f}: {set(record["columns"])-set(doc["columns"])}'
            if f in registries:
                registry_path, registry = registries[f]
                record['builder_registry'] = {'path':registry_path, 'record':registry,
                    'checksum_status':'matches current file' if registry.get('sha256') == digest else 'historical builder checksum; current export checksum takes precedence'}
                record['unit_of_analysis'] = registry.get('grain') or record['unit_of_analysis']
                record['aggregation'] = registry.get('derivation') or record['aggregation']
                # Current dictionary refresh text takes precedence over registry prose.
                if not doc['intervals']:
                    record['interval_definition'] = registry.get('intervals') or record['interval_definition']
            record['replication']['interpretation'] = record['interval_definition']
            record['related_export_files'] = sorted(set(links_in(doc['preamble'], files)) - {f})
            record['provenance_records'] = [p for p,t in texts.items() if p.startswith('build/') and p.endswith(('.json','.csv')) and (f in t or Path(f).name in t)]
        else:
            role, destination, reason = nondata_role(f)
            record.update({'role':role, 'manuscript_destination':destination, 'disposition_reason':reason,
                'authority':'historical only' if destination == 'historical' else ('current narrative/schema' if f in {'FIGURES.md','DATA_DICTIONARY.md'} else 'context, provenance or validation'),
                'unit_of_analysis':'not an experimental observation', 'aggregation':'not applicable', 'interval_definition':'not applicable',
                'readiness':{'state':'historical' if destination == 'historical' else 'reference material', 'reason':reason}})
            if f.endswith('.csv'):
                record.update(csv_profile(raw[f]))
                record['purpose'] = role + ': ' + Path(f).stem.replace('_', ' ')
            elif f.endswith('.json'):
                obj = json_docs[f]
                record['json_keys'] = list(obj) if isinstance(obj,dict) else []
                record['json_type'] = type(obj).__name__
                record['json_items'] = len(obj) if isinstance(obj,(dict,list)) else 1
                record['purpose'] = role + ': ' + Path(f).stem.replace('_',' ')
                record['json_content'] = obj
            elif f.endswith('.py'):
                profile = python_profile(texts[f])
                record['code_inspection'] = profile
                record['purpose'] = tidy(profile['docstring']) if profile['docstring'] else role + ': ' + Path(f).stem.replace('_',' ') + '; definitions: ' + ', '.join(x['name'] for x in profile['definitions'][:8])
            elif f.endswith('.sh'):
                record['purpose'] = role + ': ' + str(Path(f).parent) + ' / ' + Path(f).stem.replace('_',' ')
                record['shell_commands'] = [{'line':i+1,'text':line} for i,line in enumerate(texts[f].splitlines()) if line.strip() and not line.lstrip().startswith('#')]
                record['code_inspection'] = {'inspection':'Every command read and indexed; not executed'}
            elif f.endswith('.md'):
                record['headings'] = [{'line':i+1,'text':line} for i,line in enumerate(texts[f].splitlines()) if re.match(r'^#{1,6} ',line)]
                record['purpose'] = record['headings'][0]['text'].lstrip('# ') if record['headings'] else role
                record['introductory_context'] = '\n'.join(texts[f].splitlines()[:20])
            elif f.endswith('.txt'):
                record['purpose'] = role + ': ' + Path(f).stem.replace('_',' ')
                record['log_content'] = texts[f]
            else:
                record['purpose'] = 'Frozen sha256 file identity manifest'
                record['checksum_entries'] = len(texts[f].splitlines())
        records.append(record)
    data = [r for r in records if r['path'].startswith('data/')]
    assert len(data) == 115
    summary = {'file_count':len(records),'bytes':sum(r['bytes'] for r in records),
               'types':dict(sorted(collections.Counter(r['file_type'] for r in records).items())),
               'data_files':len(data),'data_rows':sum(r['rows'] for r in data),
               'csv_files':sum(r['file_type']=='csv' for r in records),'dictionary_coverage':'115/115 complete ordered schemas',
               'code_inspection': 'All 58 Python files parsed as AST; all 7 shell files indexed without execution',
               'manifest_integrity':'288/288 original source hashes match'}
    result = {'schema_version':1,'source_export':'../paper_export_20261011','coverage':summary,
              'authority_order':['current data/ with FIGURES.md and DATA_DICTIONARY.md refresh notes','CHANGELOG.md and STATUS.md for readiness and unresolved issues','builder parts and registries for derivation and server provenance','historical freezes and retired scripts for history only'],
              'replication_policy':NO_INFERENCE,'blocks':{k:{'purpose':v[0],'destinations':v[1],'reason':v[2]} for k,v in BLOCKS.items()},
              'known_documentation_drift':['build/assemble/renames.csv contains 582 rows, not the stale README count of 578.',
                 'checks/ablations__comparisons.csv contains 5,086 rows, not the stale changelog count of 5,081.',
                 'Some README status descriptions retain the earlier 2026-10-11 date although the operator refresh is 2026-10-13.',
                 'Builder output hashes may predate harmonization; original manuscript export_manifest.csv and current bytes govern identity.'],
              'files':records}
    return result


def markdown(result):
    s = result['coverage']
    lines = ['# Complete paper-export index','',f"The frozen export contains **{s['file_count']} files ({s['bytes']:,} bytes)**, including **{s['data_files']} data tables with {s['data_rows']:,} rows**. Every file has one record in [the machine-readable index](../evidence/export_index.json). All original export-manifest hashes match.",'',
     'The index records purpose, authority, disposition, actual schema and value coverage, raw status counts, replication/interval rules, dictionary anchors, source checksums and related files. Python sources were parsed as ASTs and their definitions, path literals and I/O calls inspected; shell commands, JSON records, Markdown headings, logs and checksum files were read. Builders were not executed.','',
     '## Authority and use','',
     'Use current harmonized `data/`, `FIGURES.md` and the refreshed `DATA_DICTIONARY.md` for results. Read `CHANGELOG.md` and `STATUS.md` for readiness. Original builder parts explain derivation but may retain old identifiers or checksums. Historical expected-value freezes and the retired A8d figure patch are not current evidence.','',
     NO_INFERENCE,'',
     'Run `python scripts/index_export.py --check` for a read-only check of coverage, hashes, schemas and both generated notes. Run without `--check` only to regenerate the three owned index artifacts.','',
     '## Evidence blocks','', '| Block | Data files | Rows | Purpose |', '|---|---:|---:|---|']
    data = [r for r in result['files'] if r['path'].startswith('data/')]
    for b,v in BLOCKS.items():
        rs=[r for r in data if r['blocks']==[b]]
        lines.append(f"| `{b}` | {len(rs)} | {sum(r['rows'] for r in rs):,} | {v[0]} |")
    lines += ['', '## Documentation discrepancies', ''] + ['- '+x for x in result['known_documentation_drift']]
    lines += ['', '## Every export file', '', 'Paths link to the immutable source export. Experimental row counts are observations at the documented grain, not a count of independent replications. The JSON contains the full schema and source-level detail omitted from this navigational table.', '']
    for top in ['root','data','build','checks','dictionary','sections']:
        rs=[r for r in result['files'] if ('root' if '/' not in r['path'] else r['path'].split('/')[0])==top]
        lines += [f'### {top}', '', '| File | Rows/items | Role and purpose | Destination |','|---|---:|---|---|']
        for r in rs:
            purpose=tidy(r['purpose']).replace('|',' / ')
            if len(purpose)>240:purpose=purpose[:237]+'…'
            count=r.get('rows',r.get('json_items','—'))
            lines.append(f"| [{r['path']}](../../paper_export_20261011/{r['path']}) | {count} | **{r['role']}**: {purpose} | {r['manuscript_destination']} |")
        lines.append('')
    disposition_lines=['# Evidence disposition for quantitative Wave 1','',
     'This document allocates every export block. The per-file decisions and reasons are in [export_index.json](../evidence/export_index.json); the complete navigational inventory is [export_index.md](export_index.md). A file can support more than one destination. Figure production and code-level Methods remain later waves.','',
     '| Evidence block | Destination | Editorial decision |','|---|---|---|']
    for b,v in BLOCKS.items():disposition_lines.append(f'| `{b}`: {v[0]} | {v[1]} | {v[2]} |')
    disposition_lines += ['', '## Rules for retaining or excluding detail','',
     '- Main Results report numerical effect sizes and the important negative outcomes; the appendix holds the full benchmark and ablation matrices, input variants and sensitivity checks.',
     '- Case-, cell- and gene-level arrays remain machine-readable source evidence. Their summaries enter the appendix; printing every underlying observation would obscure the experimental unit.',
     '- Wide-format copies are convenience views of the long-format parents and are not additional evidence.',
     '- Supporting diagnostics never overwrite the declared benchmark. This includes post hoc standardized embeddings, alternate feature views, reconstructed counts and hard-tier subgroup checks.',
     '- The failed prespecified operator test remains visible separately from later twenty-draw descriptive estimates. The prespecified PBMC donor-enumeration interval has approximate 80% coverage; the Zebra donor-bootstrap interval has 95% coverage.',
     '- The ten-candidate prior campaign retains all verdicts, noise bands and task-stream replicates, including A8d proxy-headroom failure, the two-replicate hard tier and its authorized skipped-task deviation.',
     '- Task-mixture improvements accompany negative-log-likelihood tradeoffs and unequal cells per update; generic-table degradation accompanies biological transfer gains.',
     '- ROSMAP aggregates remain in the main text only as bold-red provisional O02, with supporting appendix detail. Attribution timing likewise remains provisional O05; estimates and hypothetical routes are not completed measurements.',
     '- Simulator realism is descriptive and uses calibration references. Unit counts differ by statistic and synthetic observations may share a bank.',
     '- Every non-data file has a provenance, historical or later-Methods role; no file is left unclassified. Source hashes and source folders remain unchanged.', '']
    return '\n'.join(lines), '\n'.join(disposition_lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Verify existing index and notes without writing')
    args=parser.parse_args()
    result=build()
    index_md, disposition_md=markdown(result)
    outputs={OUTPUT:json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n', INDEX_MD:index_md, DISPOSITION_MD:disposition_md}
    if args.check:
        differences=[str(p.relative_to(ROOT)) for p,t in outputs.items() if not p.exists() or p.read_text()!=t]
        if differences:
            print('Index missing or stale: '+', '.join(differences),file=sys.stderr)
            return 1
    else:
        for path,text in outputs.items():path.write_text(text)
    print(json.dumps({'mode':'check' if args.check else 'write',**result['coverage']},sort_keys=True))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
