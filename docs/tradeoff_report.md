# VerifyRAG: Business and Technical Trade-off Analysis

**Current position.** I built VerifyRAG as a small evidence finder for UVM questions. On 27 September 2026, all 31 tests passed and each retriever found a labelled passage within five results for all six answerable development questions. A paid smoke question ended in a false abstention after the validator rejected the model draft. The prototype is an evidence navigator, not a replacement for engineering judgement.

## 1. Problem and significance (15%)

The intended user is a verification engineer checking how a UVM API behaves while writing or debugging a testbench. A plausible but wrong answer can waste time or weaken a check. VerifyRAG returns a short answer only when it can connect each claim to the selected UVM release; otherwise, it refuses or shows source text for inspection.

I did not run interviews or a timed user study, so I make no claim about time saved, adoption, willingness to pay or return on investment. A later study could give engineers matched tasks using ordinary search and VerifyRAG, then record correctness, completion time and source-checking time.

Accellera and Verification Academy already provide searchable UVM documentation [1, 3]. Synopsys describes a retrieval-based verification copilot, while Siemens and Cadence offer wider AI-assisted verification tools [4, 5, 6]. My contribution is narrower: an inspectable prototype with fixed public sources, repeatable tests and visible failures. It does not cover private designs, all SystemVerilog or simulator-specific behaviour.

## 2. Business and technical trade-offs (25%)

My proposal assumed embeddings and a vector database. After building the corpus, I chose in-memory BM25 and sparse TF-IDF. The 349 chunks often contain exact API names such as `uvm_config_db`, so lexical retrieval is cheap, inspectable and fast enough. The hybrid ranker combines both methods with reciprocal-rank fusion. This avoids embedding charges and external corpus transfer, although it may miss heavy paraphrasing.

A plain model cannot guarantee that it uses the chosen UVM release. Fine-tuning needs labelled data and makes attribution harder, while an agent loop adds complexity to a one-step task. I kept retrieval, validation and evaluation in local Python and used `openai/gpt-4o-mini` through OpenRouter only for optional generation.

The corpus pins 24 Accellera files from UVM 2020.3.1 commit `78c06547a2a0a29b3dc9dcafae62b75b2ff61544` and records checksums and line links [2]. This makes citations reproducible but coverage old and incomplete. The interface labels its version and rejects other releases. Adding 2020.3.2 requires a new corpus and regression run [1].

Offline preview has no token cost and keeps the question local. Hosted generation sends the question and public excerpts to a provider, so private RTL and logs are outside scope. The recorded 25-call batch used 54,426 tokens and cost USD 0.00915030. This excludes engineering time, hosting, maintenance and review.

## 3. Implementation and evaluation evidence (35%)

The program retrieves five chunks. Offline mode shows the top two as an evidence preview. Hosted mode requests structured claims. A claim is kept only if it cites a retrieved chunk and a quote aligned to one exact source span. UVM identifiers must occur in that chunk, and a qualified method must match its class. These checks verify provenance, not entailment.

On the 27 September Colab rerun (`20260927T090146780914Z`), all 31 tests passed. BM25 reached 5/6 Hit@1, 6/6 Hit@5 and 0.9167 MRR@5. TF-IDF and hybrid each reached 4/6, 6/6 and 0.8333. Median time was 1.23 ms for BM25, 1.05 ms for TF-IDF and 3.24 ms for hybrid. The set is small, and Hit@5 measures retrieval rather than correctness.

I set a target of at least 80% correct-and-usable answers, ten points above the same-model baseline, and 80% appropriate abstention. The frozen 20-case v2 run found a correct passage for 14/14 answerable cases but refused only 4/6 unsupported cases. Later changes reached 6/6, but the exposed set now provides regression evidence rather than a new blind result.

The saved 25 September development run contains eight outputs for each of plain LLM, BM25 plus LLM and hybrid plus LLM. The first validator rejected correct quotes when the model removed source-comment prefixes or changed line wrapping. Rechecking the saved responses after a bounded alignment fix accepted 5/6 BM25 and 6/6 hybrid drafts; both rejected 2/2 unsupported questions. No extra API calls were used for that recheck.

An AI-assisted source comparison rated hybrid 5/6 correct and usable against 2/6 for the plain model. The 83.3% versus 33.3% result is development evidence, not independent human review. The remaining hybrid answer became incomplete after the validator removed a wrong class-qualified claim.

The 27 September smoke test used 3,543 tokens and cost USD 0.00035025, but the draft failed citation or identifier checks, causing a false abstention. The next 24-call batch completed, but its result folder was not embedded in the downloaded notebook. I therefore report no new accuracy or cost total from it.

To reproduce the non-paid checks from the repository root:

```bash
python scripts/build_corpus.py
python scripts/evaluate.py --split development
python -m unittest discover -s tests -v
```

## 4. Demonstration, risks and limits (25%)

My demonstration shows a supported question with a commit-linked source, a request lacking private evidence and an instruction-override attempt. It also includes the ranking results, saved paid comparison and rejected smoke question. Strict validation can prevent a wrong claim but also reduce usefulness.

The hardest remaining failure is a fluent interpretation attached to real but insufficient evidence. Exact quotes, source hashes and class scopes reduce this risk, but only a domain-aware reviewer can judge meaning and usefulness. Other limits are stale sources, lexical misses, provider disclosure, false refusals and over-reliance. VerifyRAG cannot compile a testbench, inspect an unseen DUT, diagnose a proprietary simulator or approve sign-off. I would require a larger frozen benchmark and a blinded review by verification engineers before a pilot.

I used generative AI during research, coding, test design and editing. I checked the final Colab run myself on 27 September and retained the failed cases. I have not presented the AI-assisted labels as independent human review. The detailed assistance record is included with the project in `docs/AI_USE.md`.

## References

1. [Accellera UVM downloads](https://www.accellera.org/downloads/standards/uvm)
2. [Accellera UVM 2020.3.1 source tree](https://github.com/accellera-official/uvm-core/tree/2020.3.1)
3. [Verification Academy search](https://verificationacademy.com/search/) and [UVM 1.2 reference](https://verificationacademy.com/verification-methodology-reference/uvm/docs_1.2/html/menu.html)
4. [Synopsys.ai Copilot assistants](https://www.synopsys.com/blogs/chip-design/synopsys-ai-copilots-chip-design.html)
5. [Siemens Questa One Agentic Toolkit](https://www.siemens.com/en-gb/products/ic/questa-one/agentic-toolkit/)
6. [Cadence Verisium platform](https://www.cadence.com/en_US/home/tools/system-design-and-verification/ai-driven-verification.html)
7. [OpenRouter GPT-4o-mini model page](https://openrouter.ai/openai/gpt-4o-mini)
8. [OpenRouter structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs) and [usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting)
