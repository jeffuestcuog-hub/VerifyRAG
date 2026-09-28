# Public Colab rerun on 28 September 2026

This record documents the fresh run used in the final report. It separates system status,
retrieval performance and answer completeness.

## Integrity and offline checks

- 31 tests passed.
- The corpus contained 349 chunks from 24 source files.
- BM25 reached 5/6 Hit@1, 6/6 Hit@5 and 0.9167 MRR@5.
- TF-IDF and hybrid each reached 4/6 Hit@1, 6/6 Hit@5 and 0.8333 MRR@5.

## Paid calls

| Part | Calls | Total tokens | Provider cost USD |
|---|---:|---:|---:|
| Smoke test | 1 | 3,539 | 0.00059745 |
| Development comparison | 24 | 51,153 | 0.00848985 |
| **Combined** | **25** | **54,692** | **0.00908730** |

All 24 development calls completed without an API error.

| Method | Supported answered | Unsupported abstained |
|---|---:|---:|
| Plain LLM | 6/6 | 0/2 |
| BM25 plus LLM | 4/6 | 2/2 |
| Hybrid plus LLM | 5/6 | 2/2 |

These are automated system statuses. The smoke answer passed citation validation but omitted how
to enable tracing. A separate AI-assisted reference comparison accepted 2/6 plain, 3/6 BM25 and
4/6 hybrid answers as complete and usable. It was not independent human review.

The paid switches were reset to `False` after the run. The saved evidence is stored with the
submission materials as `VerifyRAG_paid_run_20260928.zip` and a downloaded notebook with outputs.
