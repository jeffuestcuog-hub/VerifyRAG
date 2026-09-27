# VerifyRAG: primary-source research and bounded claims

Checked on **15 September 2026**. This is supporting research, not an evaluation report. Product descriptions below are vendor statements; they are not independently reproduced performance results. No interviews, customer adoption, time savings, paid model calls, or successful API completions are claimed.

## 1. Existing alternatives and project positioning

| Existing alternative | Evidence from its official source | Implication for VerifyRAG (project inference) |
|---|---|---|
| Accellera UVM reference material | Accellera publishes UVM reference implementations and class references. Its downloads page lists UVM 2020-3.1 (August 2024) and the newer 2020-3.2 (August 2026). [Accellera UVM downloads](https://www.accellera.org/downloads/standards/uvm) | Direct reading and browser text search form a meaningful low-cost baseline. Freeze the project to 2020.3.1 for reproducibility and label that version everywhere; do not describe the corpus as the latest UVM. |
| Verification Academy | The site provides search with topic and content filters, and a navigable UVM 1.2 reference, including a configuration-database page. [Academy search](https://verificationacademy.com/search/), [UVM 1.2 menu](https://verificationacademy.com/verification-methodology-reference/uvm/docs_1.2/html/menu.html), [configuration database](https://verificationacademy.com/verification-methodology-reference/uvm/docs_1.2/html/files/base/uvm_config_db-svh.html) | VerifyRAG should be compared against ordinary documentation lookup. Its scoped proposition is question-to-evidence retrieval within a named source version. Academy's broader learning material is useful but is not automatically part of the project corpus; UVM 1.2 pages must not be cited as 2020.3.1 evidence. |
| Synopsys.ai Copilot Knowledge Assistant | Synopsys describes an available knowledge assistant using commercial/open LLMs and proprietary RAG pipelines to answer questions and supply contextual guidance across its EDA stack, including verification. [Synopsys Copilot assistants](https://www.synopsys.com/blogs/chip-design/synopsys-ai-copilots-chip-design.html) | This is the closest conceptual commercial alternative. Domain-specific RAG for verification is already established; do not claim the concept is novel. A defensible student contribution is a small, inspectable implementation and reproducible evaluation over public UVM material. |
| Siemens Questa One Agentic Toolkit | Siemens describes a gateway and planning, design, verification, debug and closure agents integrated with its verification environment. [Questa One Agentic Toolkit](https://www.siemens.com/en-gb/products/ic/questa-one/agentic-toolkit/) | This has a much broader workflow scope. VerifyRAG answers documentation questions; it does not run simulation, close coverage, debug waveform databases, or sign off RTL. No comparative productivity or feature-superiority claim is supported here. |
| Cadence Verisium | Cadence describes AI applications for verification management, regression failure triage, debugging and root-cause analysis, using multi-run verification data. [Verisium platform](https://www.cadence.com/en_US/home/tools/system-design-and-verification/ai-driven-verification.html) | An adjacent industrial alternative demonstrates that AI-supported verification is an active product category. VerifyRAG's public-document scope cannot establish equivalence to commercial design-data analysis. |

**Proposed positioning:** VerifyRAG is an educational, version-pinned UVM documentation assistant with inspectable retrieved passages and source links, a local retrieval mode, and optional hosted answer generation. Its contribution is an evaluated implementation and explicit failure analysis. It makes no first-in-market, state-of-the-art, or commercial-readiness claim. Absence of a feature from a vendor webpage is not evidence that the product lacks it.

## 2. Design tradeoffs to explain in the report

These are engineering rationales to test, not measured findings.

| Decision | Expected benefit | Limitation / evidence needed |
|---|---|---|
| Pin 24 selected source files from Accellera's `2020.3.1` tag at commit `78c06547a2a0a29b3dc9dcafae62b75b2ff61544` | Stable passages and source-line citations make runs easier to audit. [Official source tree](https://github.com/accellera-official/uvm-core/tree/2020.3.1) | A selected subset is not complete UVM or SystemVerilog coverage. Questions outside this subset need an explicit insufficient-evidence outcome. The file count and commit are project configuration and must be confirmed by the local corpus manifest. |
| Local BM25 and TF-IDF retrieval, with a hybrid option | No paid embedding service; retrieval is inspectable and suited to exact API identifiers. | Both are lexical methods. Their combination is not dense semantic retrieval and may still miss paraphrases. Measure whether hybrid actually improves on either component; do not assume it does. |
| Optional hosted generation after retrieval | A language model may combine passages into a readable explanation. | Readability and schema validity do not prove factual support. Inspect each claim against the cited passage, handle invalid citations, and evaluate abstentions. |
| Preserve a local evidence-only mode | A reproducible retrieval demonstration can run without an API key. | An evidence-only result is not an LLM-generated answer and cannot establish generation quality, API latency, or model cost. Report its results separately. |
| Limited context, explicit evidence IDs and versioned links | Reduces the amount of text a reviewer must inspect and enables citation validation. | Top-k truncation can omit the answer. A valid evidence ID can still accompany an unsupported statement; citation existence and answer support are separate checks. |

## 3. Verified OpenRouter model listing and pricing

The public [GPT-4o-mini endpoint listing](https://openrouter.ai/api/v1/models/openai/gpt-4o-mini/endpoints) was retrieved through the web tool on 15 September 2026. It listed model `openai/gpt-4o-mini` with these routes:

| Provider route | Input USD / 1M tokens | Output USD / 1M tokens | Cached-input USD / 1M tokens |
|---|---:|---:|---:|
| `openai` | 0.15 | 0.60 | 0.075 |
| `azure` | 0.15 | 0.60 | 0.075 |
| `azure/swedencentral` | 0.165 | 0.66 | 0.0825 |

The routes listed a 128,000-token context and 16,384 maximum completion tokens, plus `response_format` and `structured_outputs`. This establishes public catalog availability, not successful authenticated inference. The [model page](https://openrouter.ai/openai/gpt-4o-mini) corroborates the base per-million pricing. Prices are a dated snapshot, not a permanent tariff. Selected facts are recorded in `config/model_pricing.json`; no full provider-response archive or paid response was captured.

For an **illustrative, uncached** request with 3,000 input tokens and 500 output tokens, the base token-only estimate is `(3000 × 0.15 + 500 × 0.60) / 1,000,000 = USD 0.00075`. Those token counts are assumptions, not measured VerifyRAG usage. A 100-question scenario would be USD 0.075 under those same assumptions. This excludes retries, routing variation, hosting, acquisition charges/taxes, maintenance and human review; it is not a cost-savings result.

## 4. Official API guidance for implementation

- Send a JSON `POST` to `https://openrouter.ai/api/v1/chat/completions` with a bearer API key, explicit `model`, `messages`, and a bounded token limit. Non-streaming text is under `choices[0].message.content`; also inspect `finish_reason` and error fields. [OpenRouter API reference](https://openrouter.ai/docs/api_reference/overview)
- Request `response_format.type = "json_schema"`, a named `json_schema`, `strict: true`, and a schema with required fields and `additionalProperties: false`. Support is endpoint-specific. Set `provider.require_parameters = true`; still validate returned JSON and citation membership locally. Schema conformance does not establish factual accuracy. [Structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs)
- Provider selection can vary. `provider.only` restricts providers, `allow_fallbacks` controls fallback and `max_price` can reject unaffordable routes. Record the actual returned model/provider where present. [Provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)
- Record response ID, `usage.prompt_tokens`, `usage.completion_tokens`, `usage.total_tokens`, and `usage.cost` when supplied. Cost is documented as account credits/amount charged; do not silently relabel missing usage as zero. Usage is automatically included for non-streaming responses; `usage.include` and `stream_options.include_usage` are deprecated. Keep a locally calculated USD estimate distinct from provider-reported cost. [Usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting)

**Suggested response contract (project design):** an answer string, a list of evidence IDs, and an insufficient-evidence flag. Validate types and required fields; reject evidence IDs that were not supplied to the model. Treat source passages as data, not instructions. Keep credentials in the environment; do not include them in logs or the submission. Hosted mode sends the question and retrieved excerpts to the configured service; local mode does not perform hosted inference.

## 5. Business hypotheses and a validation plan

No customer research has been performed for this document. These are proposed hypotheses for later validation.

| Hypothesis | Proposed validation | What may be claimed now |
|---|---|---|
| Students and junior verification engineers spend effort locating reliable UVM API explanations. | Recruit consenting participants with recorded experience levels; observe them answering realistic tasks through documentation search. Ask where they lose time. | A plausible target-user assumption, not a measured pain point. |
| Versioned citations improve users' ability to check an answer. | Compare answer-only and answer-plus-evidence conditions; assess supported-answer accuracy and successful source verification. | A design objective, not established user trust. |
| VerifyRAG can reduce documentation lookup time without reducing correctness. | Counterbalance comparable question sets between ordinary search and VerifyRAG; collect task time, correctness, source verification and failures. Report participant count and uncertainty. | A testable value proposition, not time savings or return on investment. |
| A small local index and optional low-cost generation suit education or a small team's pilot. | Measure local resource use and actual API usage; interview potential users about access restrictions, budget and deployment needs. | A proposed deployment scenario, not willingness to pay or demand. |

Do not replace human validation with invented interviews, fabricated survey percentages, synthetic testimonials, vendor productivity figures, or extrapolated annual savings. If human testing has not occurred by submission, present it as future work. A commercial pilot would additionally need corpus access rights, data-handling approval, maintainability, version-update policy and support arrangements.
