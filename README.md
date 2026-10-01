# VerifyRAG

**Versioned UVM evidence for digital verification engineers.**

PE6201 individual End-of-Course Project (44%). Project owner: Gao Zihan.

## Status

Working local retrieval/evidence prototype with an OpenRouter grounded-generation client.
A fresh public-Colab check completed on 28 September 2026. The current code passes 31 tests. The
fresh run made 25 paid calls without an API error, and hybrid RAG answered 5/6 supported development
questions while refusing 2/2 unsupported questions. A stricter AI-assisted review found 4/6 hybrid
answers complete, so the run does **not** establish the 80% answer-quality target. Independent
third-party domain review remains pending. A 5:11 screen-recorded demonstration is public, but the
camera-visible replacement requested in the final course clarification still needs to be recorded.
See [Chinese starting guide](docs/START_HERE_zh.md) and [evidence status](docs/submission_checklist.md).

## Product definition

| Item | Definition |
|---|---|
| **Persona** | A digital-verification engineer checking the behaviour, scope or version of a UVM API while writing or debugging a testbench. |
| **Input** | A natural-language UVM/SystemVerilog question and the supported source version (`2020.3.1`). Private RTL, logs and simulator state are outside scope. |
| **Output** | Either an offline evidence preview, an optional model-generated answer with source-aligned claims, or an explicit abstention. Every accepted claim retains a chunk ID, file, line range and commit-linked URL. |
| **External intelligence** | Optional `openai/gpt-4o-mini` generation through OpenRouter. Retrieval, validation and evaluation remain local Python code. |

### Targeted and reached metrics

| Measure | Target | Reached | Interpretation |
|---|---:|---:|---|
| Human-reviewed correct-and-usable answers | >=80% and >=10 percentage points above the same-model plain baseline | Not independently measured; AI-assisted development comparison: hybrid 4/6 (66.7%), plain 2/6 (33.3%) | Quality target remains unproven. |
| Appropriate-abstention recall | >=80% | Frozen confirmation: 4/6 (66.7%) | Target missed. The later 6/6 result used exposed cases and is regression evidence only. |
| Retrieval Hit@5 | Diagnostic, no correctness target | Development BM25 6/6; frozen confirmation 14/14 | Shows evidence retrieval, not answer correctness. |
| Reproducibility checks | All automated checks pass | 31/31 tests; 24 source files; 349 chunks | Confirms programmed contracts and corpus integrity. |
| Hosted-run cost and reliability | Record every call, error, token and returned cost | 25 calls; 0 API errors; 54,692 tokens; USD 0.00908730 | Measured development-run cost, excluding engineering and review effort. |

## Run in one minute

Python 3.10+; core workflow has no third-party package dependencies. From this folder:

```bash
python -m verifyrag "How do I use uvm_config_db get and set?"
python -m verifyrag "Explain uvm_config_db for UVM 1.2" --version 1.2
python scripts/evaluate.py --split development
python -m unittest discover -s tests -v
```

Default output is **EVIDENCE PREVIEW**: it retrieves original excerpts and provides immutable
source links. It does not pretend to be a model-generated answer. Open `VerifyRAG_Colab.ipynb`
for the guided workflow, including a live model section that you run explicitly.

## Generate an answer with a model

Set `OPENROUTER_API_KEY` in the runtime environment or Colab Secrets, and provide the model ID:

```bash
python -m verifyrag "What does uvm_object clone do?" --mode openrouter --model openai/gpt-4o-mini
python scripts/evaluate.py --split development --live --model openai/gpt-4o-mini
```

These commands make paid API requests. The evaluation compares plain LLM, BM25+LLM and hybrid+LLM
and makes up to three requests per case. There are no automatic retries. Missing credentials or
provider failures are recorded as errors, not substituted with invented output. Keys are read
from the environment, never saved in source files. Use only public course questions: the API
receives your query and the selected public source excerpts. It is not configured for company IP.

## Architecture

```text
Pinned public UVM sources -> checksum verification -> chunks + line/version provenance
Question -> version/scope checks -> BM25 / TF-IDF / RRF hybrid retrieval
         -> offline evidence preview OR OpenRouter structured claims
         -> chunk-ID / source-aligned quote / class-scope checks -> cited output or abstention
Frozen evaluation cases -> raw records + retrieval metrics + blank expert-review worksheet
```

The vectors in this first version are **sparse lexical TF-IDF**, not pretrained semantic embeddings.
Hybrid means reciprocal-rank fusion of two lexical rankings. This revises the proposal's rented
embedding plan for a simple reproducible baseline. It cannot establish an advantage over MiniLM
or other dense retrieval without a separate experiment. There is no agent loop: the task is
document-grounded QA, with at most one model request per answer.

## Data and reproducibility

- 24 selected source files from official `accellera-official/uvm-core`, tag `2020.3.1`.
- Commit: `78c06547a2a0a29b3dc9dcafae62b75b2ff61544`.
- 349 deterministic source chunks; IDs, line ranges, version and commit links travel with each chunk.
- Source code/comment corpus, not the complete IEEE standard or an entire UVM Cookbook.
- The release is pinned for reproducibility; **it is not claimed to be the latest release**.
- `data/source_manifest.json` records provenance and SHA-256 for every retained source file.
- `data/raw/LICENSE.txt`, `NOTICE.txt`, `README.md`, `DEVIATIONS.md` preserve upstream notices/context.
- Restore the public source snapshot: `python scripts/fetch_corpus.py` (network required).
- Rebuild deterministic chunks: `python scripts/build_corpus.py` (offline).

Do not edit raw files or labels after looking at final test results. If you change chunking or
retrieval after examining the test set, call those results exploratory and obtain a new test set.

## Evaluation

Read [evaluation protocol](docs/evaluation_protocol.md). The development set supports configuration
work. The former test set was exposed during QA and is now `exploratory_test_v1`; its before/after
results are regression diagnostics. A fresh confirmation set was authored after the v2 freeze and
run once. Separate AI authorship does not imply independent human or domain-expert validation.

```bash
# Already run once under the recorded freeze; repeat only as a reproduction audit:
python scripts/evaluate.py --split confirmation_test
```

The recorded frozen confirmation run is `results/20260915T161112734734Z_confirmation_test_offline`.
BM25 found an annotated passage in the top five for 14/14 answerable cases. Offline boundary
behaviour answered 14/14 answerable cases and abstained on 4/6 expected-abstention cases, missing
the pre-registered 80% safety target. Later guardrail changes make that set exposed; its 6/6
regression is tuning evidence and is not a replacement confirmation result.

The paid development run and exact cost record are documented in
[`docs/colab_validation_20260925.md`](docs/colab_validation_20260925.md). The original validator
over-rejected comment-wrapped quotes. Rechecking the saved responses after a bounded formatting
alignment accepted 5/6 BM25 and 6/6 hybrid answerable drafts, with both methods refusing 2/2
unsupported cases. A disclosed AI-assisted source comparison rated hybrid 5/6 (83.3%) versus
plain LLM 2/6 (33.3%) correct-and-usable. This is post-hoc development evidence; human/domain
confirmation remains pending.

The fresh 28 September rerun is documented in
[`docs/colab_validation_20260928.md`](docs/colab_validation_20260928.md). Its smoke test used 3,539
tokens and cost USD 0.00059745. The 24-call development comparison used 51,153 tokens and cost
USD 0.00848985. Combined, the run used 54,692 tokens and cost USD 0.00908730. Hybrid's automated
status was 5/6 supported answers and 2/2 unsupported refusals, but the AI-assisted completeness
check accepted 4/6. The difference is retained as evidence that citation validation does not
guarantee a complete answer.

Every run saves input/code hashes, timestamped per-case retrieved chunk IDs, latencies, generated/preview
outputs, usage if returned by the provider, and a blank `human_review.csv`. Hit@5 measures whether
at least one annotated relevant passage was retrieved. It does not measure factual correctness,
complete multi-document support, or useful engineering advice. Report errors and abstentions
alongside answer quality; never drop failed model calls from the denominator.

## Limits

This assistant cannot compile a testbench, debug an unseen design, approve silicon sign-off, prove
a claim from mere identifier occurrence, or guarantee prompt-injection resistance. Exact citations
can coexist with incorrect interpretation. Pattern checks can miss novel private-context or
instruction-override wording, and offline mode has no semantic relevance threshold. A DV engineer
must review recommendations before use. Unsupported versions abstain. Company source uploads and
simulator execution are outside scope.

## Repository map

| Folder/file | Purpose |
|---|---|
| `verifyrag/` | Retrieval, model client, deterministic checks and CLI |
| `data/README.md` | Data provenance, schemas, rebuild steps and limitations |
| `data/raw/`, `source_manifest.json`, `corpus.jsonl` | Original public source and reproducible index inputs |
| `data/eval/` | Development, exposed exploratory, and once-run frozen confirmation questions |
| `evidence/paid_run_20260928/` | Sanitised raw records from the fresh paid run; no credential is included |
| `scripts/` | Fetch, chunk, evaluate and calculate scenario costs |
| `results/` | Genuine run records and blank review sheets |
| `tests/` | Source integrity and guardrail contract tests |
| `docs/tradeoff_report.md` | English report source; about 1,178 words before references |
| `output/VerifyRAG_Tradeoff_Report_Final.docx` | Editable final report matching the submitted PDF content |
| `docs/colab_validation_20260925.md` | Colab run, paid usage, post-hoc validation and evidence boundaries |
| `docs/colab_validation_20260928.md` | Fresh public-Colab rerun, paid usage and completeness limits |
| `docs/demo_script.md` | Narration and live demonstration outline |
| `docs/VIDEO_RECORDING_GUIDE_zh.md` | Bilingual narration with matching screen actions |
| `docs/AI_USE.md` | Authorship and assistance disclosure |

Upstream files retain their Apache-2.0 license. See [third-party notices](THIRD_PARTY_NOTICES.md).
The student's new work has no additional public distribution license assigned in this draft.
