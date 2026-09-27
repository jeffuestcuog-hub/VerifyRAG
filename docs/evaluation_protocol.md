# VerifyRAG evaluation protocol

## Scope and provenance

The evaluation concerns documentation assistance over the selected, pinned Accellera UVM 2020.3.1 source corpus. It does not establish that generated SystemVerilog compiles, that a DUT is correct, or that advice applies to a different UVM or simulator version.

The initial question and reference-answer files were authored by a separate AI agent that read the source corpus, without running the retrieval engine or seeing its answers. This is independent task authorship within the same AI-assisted project. It is **not** a human-authored benchmark, a different-model evaluation, or an externally validated test set. Shared model blind spots remain possible.

Source comments and executable implementation were used to check factual support. The original source paths, version, line ranges, and commit-linked URLs are preserved in `data/corpus.jsonl`. No results or success claims are implied by the existence of these labels.

## Files and roles

| File | Cases | Permitted use |
|---|---:|---|
| `data/eval/development.jsonl` | 8: 6 answerable, 2 abstention | Prompt design, retrieval settings, threshold selection, and debugging |
| `data/eval/exploratory_test_v1.jsonl` | 20: 14 answerable, 6 abstention | Exposed during development QA; exploratory only, never a held-out result |
| `data/eval/confirmation_test.jsonl` | 20: 14 answerable, 6 abstention | Original v2 frozen run preserved; later runs are exposed regression/tuning evidence |

Answerable questions cover API use, method behavior, and realistic debugging misconceptions. Abstention questions cover unsupported versions, attempts to disclose hidden instructions or credentials, nonexistent APIs, unsupported vendor details, missing private-project evidence, and future-release claims. These are deliberately selected small cases, not a representative sample of all verification-engineering work.

The development and test files contain distinct questions. Some source classes occur in more than one split because the product answers questions about a shared documentation corpus; this is question-level separation, not a claim of unseen-document generalization. Reference answers, labels, and questions must not be included in the retrieval index or model context at inference time. The first test file was accidentally displayed by a broad QA text search before its run, so it was renamed `exploratory_test_v1.jsonl` without changing its hash. The fresh confirmation set was authored only after the system configuration was frozen.

That original procedure is recorded in `config/evaluation_freeze_v2.json` and `config/confirmation_run_v2.json`. The confirmation dataset SHA-256 is `afa3deb8238ce328dc3fa08b11e9fc5447b61ade1e958738e430128a60b7bc17`; its only frozen run is `20260915T161112734734Z`. Later guardrail and validator changes mean subsequent runs on this file are regression evidence, not confirmation evidence.

## Label schema

Each JSONL record contains:

- `id`, `split`, `question`, `version`, and `category` for stable identification and grouping.
- `answerable` and `expected_behavior`: whether a grounded answer is supported in the loaded corpus or the system should abstain.
- `expected_sources`: exact repository-relative source paths.
- `expected_chunk_ids`: independently checked sufficient passages. When several IDs are listed, **any one** is an acceptable retrieval hit; they are alternative supporting passages, not a requirement to retrieve every ID. Questions were designed to have a sufficient single passage, avoiding hidden multi-document requirements.
- `evidence_terms`: literal symbols or phrases in the supporting source. These help audit retrieval and provenance; keyword occurrence is not a semantic correctness label.
- `reference_answer` and `reason`: the supported conclusion and why the label was assigned.

For abstention cases the source, chunk, and evidence-term lists are empty. This means the requested claim is not supported within scope, not that the real-world question is necessarily impossible to answer from other evidence.

## Freeze and run order

1. Check label syntax, chunk existence, source/version agreement, and literal evidence against the corpus. These are data-integrity checks, not system evaluation.
2. Record SHA-256 hashes of both label files and the corpus **before any retrieval or answer-generation run**. Keep the files and hashes in version control. The initial files were created before the evaluation author ran any system evaluation.
3. Use only the development and explicitly labelled exploratory splits to choose retrieval parameters, prompt wording, abstention rules, model settings, and reporting logic. Log the final configuration and code hashes before a fresh author creates or runs the confirmation set.
4. Run the same frozen confirmation questions through all comparison methods. Preserve every output, retrieved chunk, citation, status, latency, token count, model identifier, and error. Keep failures and abstentions in the denominator.
5. Do not tune on confirmation scores. If outcomes drive a change, label that set as exposed and create a new independently authored confirmation set for any later confirmatory claim. A repeat run on an exposed set is a regression check.
6. If a genuine gold-label error is discovered, preserve the original labels/results, document the source-supported correction, version and rehash the labels, and rerun all methods consistently. Do not silently alter a label to match a favored output.

## Comparison design

Compare a simple keyword/document-search baseline with the proposed retrieval approach on the same corpus and questions. Separate retrieval quality from generated-answer quality. An offline extractive response can demonstrate retrieval and provenance, but it must be reported as extractive behavior rather than a live LLM result. Only include a live model comparison when an actual model call was made and its run records were captured.

Keep retrieval cutoffs and abstention settings fixed before the confirmation run. Report the exact settings. If comparing model-backed variants, use the same question set and record any differences in supplied context or prompting. Do not give the gold answer to the answering model.

## Metrics and their limits

Report counts with their denominators, not percentages alone. The exposed exploratory set has 20 cases, so one case changes its overall rate by five percentage points; the fresh confirmation set will also be small. Report answerable and abstention subsets separately.

### Retrieval

- **Hit@k:** among answerable questions, the fraction with at least one `expected_chunk_ids` passage in the top k. State k. This is a passage-level hit; a matching source filename alone is insufficient.
- **Reciprocal rank:** reciprocal of the rank of the first gold passage, or zero when no gold passage is returned within the evaluated cutoff. Average over answerable questions and state the cutoff.
- Inspect retrieval misses for genuinely sufficient passages omitted from the initial gold set; any label correction must follow the versioned procedure above.

### Answers, citations, and abstention

- **Answer correctness:** a human reviewer judges whether the response answers the question correctly and respects its version and scope. Reference-answer wording need not be copied.
- **Citation validity:** cited identifiers exist and resolve to the claimed source/version. This can be checked automatically.
- **Citation support:** the cited passages actually support the substantive claims. This requires semantic review; valid IDs and matching keywords do not establish support.
- **Coverage:** answered cases divided by all cases. Also report the abstention rate.
- **Appropriate abstention recall:** expected-abstention cases on which the system abstains, divided by all expected-abstention cases.
- **Abstention precision:** expected-abstention cases among all system abstentions. State separately how many answerable questions were unnecessarily refused.
- **Selective answer accuracy:** correct answers among cases the system answered, based on human review. Pair this with coverage so refusing everything cannot appear successful.
- **Counterfactual usefulness of abstention:** to assess whether a refused case would otherwise have been answered wrongly, save an unreleased candidate answer from a documented diagnostic mode and have a human judge it. Report this measure only if that extra procedure was actually performed. Retrieval confidence or the expected-abstention label alone cannot establish the counterfactual.

Evidence-term matches and agreement with `expected_behavior` may be reported as automated diagnostic measures. They must not be relabeled as human answer accuracy, groundedness, or a successful factual evaluation.

### Cost and runtime

Report measured latency and actual calls/tokens for completed live runs. An estimate must be labeled an estimate and show the model price assumptions and date. Offline retrieval runtime is not API latency, and zero paid calls do not establish zero production cost. Record errors, retries, and refused cases alongside successful calls.

## Student and domain-peer validation still required

Before relying on this evaluation in the final course report, the student and a domain-aware peer should independently inspect every question, the gold passages, and the reference answer. Record reviewer identity or role, date, changes, disagreements, and their resolution. Until that happens, report the labels as **AI-authored, source-checked, not human-validated**.

For answer-quality assessment, those reviewers should judge saved outputs without knowing which method produced each answer where practical. Record correctness, unsupported claims, citation support, and whether abstention was useful. Use a second reviewer to resolve disagreements. A model judge, if added, is another system component; calibrate it against these human labels and report its precision and recall before using its scores as evidence.

The initial protocol leaves these human assessments pending. Do not invent reviewer participation, successful compilation, real user time savings, expert acceptance, or live API results.
