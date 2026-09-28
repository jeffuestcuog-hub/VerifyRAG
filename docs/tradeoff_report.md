# VerifyRAG: Business and Technical Trade-off Analysis

**Current position.** I built VerifyRAG as a small evidence navigator for UVM questions. In a fresh Colab run on 28 September 2026, all 31 tests passed and the hybrid system answered five of six supported development questions while refusing both unsupported questions. A stricter AI-assisted review found only four of the six hybrid answers complete. The project therefore shows useful retrieval and refusal behaviour, but it does not establish the 80% answer-quality target.

## 1. Problem and significance (15%)

The intended user is a verification engineer checking how a UVM API behaves while writing or debugging a testbench. A plausible answer from the wrong release can waste time or weaken a check. VerifyRAG uses one pinned UVM release and links its output to source lines. If the available evidence is outside scope or insufficient, it refuses or shows the source text for inspection.

I did not conduct interviews or a timed user study, so I make no claim about adoption, time saved, willingness to pay or return on investment. A later study could give engineers matched tasks using ordinary search and VerifyRAG, then compare correctness, completion time and source-checking time.

Accellera and Verification Academy already provide searchable UVM documentation [1, 3]. Synopsys describes a retrieval-based verification copilot, while Siemens and Cadence offer broader AI-assisted verification tools [4, 5, 6]. My contribution is narrower: a reproducible prototype with fixed public sources, inspectable citations, repeatable tests and retained failures. It does not cover private designs, all SystemVerilog or simulator-specific behaviour.

## 2. Business and technical trade-offs (25%)

My proposal assumed embeddings and a vector database. After building the corpus, I chose in-memory BM25 and sparse TF-IDF. The 349 chunks contain exact identifiers such as `uvm_config_db`, so lexical retrieval is cheap, transparent and fast enough. The hybrid ranker combines BM25 and TF-IDF with reciprocal-rank fusion. This avoids embedding charges and external corpus transfer, although it can miss strongly paraphrased questions.

A plain model cannot guarantee that it is using the selected UVM release. Fine-tuning would need labelled data and would make attribution harder, while an agent loop would add complexity to a one-step lookup. I kept retrieval, validation and evaluation in local Python and used `openai/gpt-4o-mini` through OpenRouter only for optional answer generation.

The corpus pins 24 Accellera files from UVM 2020.3.1 commit `78c06547a2a0a29b3dc9dcafae62b75b2ff61544` and records checksums, file names and line links [2]. This makes the evidence reproducible, but also fixes the coverage to an older and incomplete source set. Supporting another release requires a separate corpus and regression run [1].

Offline preview has no token charge and keeps the question local. Hosted generation sends the question and public source excerpts to a provider, so private RTL and logs are outside scope. The fresh 25-call run used 54,692 tokens and cost USD 0.00908730. This small API bill does not include engineering time, hosting, maintenance or expert review.

## 3. Implementation and evaluation evidence (35%)

The program retrieves five chunks. Offline mode shows the top two as an evidence preview. Hosted mode requests structured claims. A claim is kept only when it cites a retrieved chunk and its quotation aligns to one exact source span. UVM identifiers must occur in that chunk, and a class-qualified method must match the class scope. These checks verify provenance; they do not prove that the interpretation is complete.

In the 28 September Colab rerun, all 31 tests passed. The corpus contained 349 chunks from 24 source files. On six answerable development questions, BM25 reached 5/6 Hit@1, 6/6 Hit@5 and 0.9167 MRR@5. TF-IDF and hybrid each reached 4/6, 6/6 and 0.8333. This is a small development set, and Hit@5 measures whether a labelled passage was retrieved rather than whether a generated answer was correct.

I set targets of at least 80% correct-and-usable answers, ten percentage points above the same-model baseline, and 80% appropriate abstention. In the frozen 20-case confirmation run, retrieval placed a labelled passage within five results for all 14 answerable cases, but the original boundary logic refused only 4/6 unsupported cases, or 66.7%. Later changes passed all six exposed cases, but those checks are regression evidence because the cases were no longer blind.

The fresh paid comparison made 24 development calls without an API error. The plain comparator returned an answered status for all eight cases. BM25 plus LLM answered 4/6 supported cases and refused 2/2 unsupported cases. Hybrid plus LLM answered 5/6 and refused 2/2. These are system statuses after format, citation and identifier checks.

I then compared the outputs with the prepared references and cited UVM excerpts. This AI-assisted check rated 2/6 plain, 3/6 BM25 and 4/6 hybrid answers complete and usable. Hybrid refused one supported event question, and its answer about `start_item` and `finish_item` allowed randomisation but omitted that delay is forbidden between the calls. Because 4/6 is 66.7%, the fresh result did not meet the 80% answer-quality target. This review was not independent human validation.

The separate smoke question exposed the same distinction. Its citation passed, but the answer stated only that tracing is off by default and omitted how to enable it. The smoke call used 3,539 tokens and cost USD 0.00059745. Together with the development comparison, the fresh run made 25 calls, used 54,692 tokens and cost USD 0.00908730.

To reproduce the non-paid checks from the repository root:

```bash
python scripts/build_corpus.py
python scripts/evaluate.py --split development
python -m unittest discover -s tests -v
```

## 4. Demonstration, risks and limits (25%)

My demonstration shows a supported question with a commit-linked excerpt, a request lacking private evidence, an instruction-override attempt, the retrieval table and the fresh paid summary. It also shows the incomplete smoke answer. Keeping this failure visible is useful because a valid citation can still support only part of an answer.

The main remaining risk is a fluent interpretation attached to real but insufficient evidence. Exact quotations, source hashes and class scopes reduce that risk, but a domain-aware reviewer must still judge meaning and usefulness. Other limits are stale sources, lexical misses, provider disclosure, false refusals and over-reliance. VerifyRAG cannot compile a testbench, inspect an unseen DUT, diagnose a proprietary simulator or approve sign-off. Before a pilot, I would use a larger frozen benchmark and blinded review by verification engineers.

I used generative AI during research, coding, test design and editing. The final Colab run was checked on 28 September, the failed and incomplete cases were retained, and automated statuses were kept separate from correctness claims. The detailed assistance record is included in `docs/AI_USE.md`.

## References

1. [Accellera UVM downloads](https://www.accellera.org/downloads/standards/uvm)
2. [Accellera UVM 2020.3.1 source tree](https://github.com/accellera-official/uvm-core/tree/2020.3.1)
3. [Verification Academy search](https://verificationacademy.com/search/) and [UVM 1.2 reference](https://verificationacademy.com/verification-methodology-reference/uvm/docs_1.2/html/menu.html)
4. [Synopsys.ai Copilot assistants](https://www.synopsys.com/blogs/chip-design/synopsys-ai-copilots-chip-design.html)
5. [Siemens Questa One Agentic Toolkit](https://www.siemens.com/en-gb/products/ic/questa-one/agentic-toolkit/)
6. [Cadence Verisium platform](https://www.cadence.com/en_US/home/tools/system-design-and-verification/ai-driven-verification.html)
7. [OpenRouter GPT-4o-mini model page](https://openrouter.ai/openai/gpt-4o-mini)
8. [OpenRouter structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs) and [usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting)
