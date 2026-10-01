# VerifyRAG data guide

This directory contains the public UVM source snapshot, the deterministic retrieval corpus and the
question sets used for evaluation. It contains no private RTL, simulator log or API credential.

## Data map

| Path | Contents | How it is used |
|---|---|---|
| `raw/` | 24 selected source files from Accellera UVM 2020.3.1, plus the upstream licence, notice and deviation record | Authoritative input text for chunk construction |
| `source_manifest.json` | Source version, commit-linked paths and SHA-256 values | Provenance and integrity check |
| `corpus.jsonl` | 349 deterministic chunks with IDs, source paths, line ranges, text, version and URLs | BM25, TF-IDF and hybrid retrieval input |
| `eval/development.jsonl` | 8 development cases: 6 answerable and 2 expected abstentions | Tuning, debugging and paid method comparison |
| `eval/exploratory_test_v1.jsonl` | 20 cases exposed during development | Regression diagnostics only |
| `eval/confirmation_test.jsonl` | 20 cases: 14 answerable and 6 expected abstentions | Original frozen confirmation run; later runs are exposed regression evidence |

## Provenance and reproducibility

The snapshot is pinned to Accellera commit
`78c06547a2a0a29b3dc9dcafae62b75b2ff61544` from release `2020.3.1`. The manifest records the
retained files and their hashes. Recreate the source snapshot with:

```bash
python scripts/fetch_corpus.py
python scripts/build_corpus.py
```

The first command requires network access. Corpus construction is deterministic and runs offline
after the source files are present. Raw files and evaluation labels must not be placed in the
retrieval index except through the documented corpus builder.

## Record schemas

Each corpus row includes a stable chunk ID, title, source path, source line range, version, commit
URL and exact text. Each evaluation row includes the question, split, expected behaviour,
answerability, reference source/chunk, evidence terms and a source-checked reference answer. Empty
source fields on an abstention case mean that the requested claim is outside the loaded corpus.

The labels were AI-authored and source-checked. They are not an independent human benchmark. Read
[`../docs/evaluation_protocol.md`](../docs/evaluation_protocol.md) before interpreting a score.

## Results and retained evidence

Timestamped offline and hosted results are under `../results/`. The sanitised raw files from the
28 September paid run are under `../evidence/paid_run_20260928/`; the executed notebook also retains
the visible summaries. Generated status, citation validation, retrieval metrics and AI-assisted
completeness labels are reported separately from human correctness.

## Known limitations

- The corpus is a selected source-code/comment subset, not the complete IEEE standard or Cookbook.
- The development and confirmation sets are small and do not establish broad UVM coverage.
- Later use of an exposed set is regression evidence, not a new blind confirmation result.
- Hit@5 establishes retrieval of an annotated passage, not technical correctness or completeness.
