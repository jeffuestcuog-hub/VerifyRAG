# VerifyRAG English narration

Use this file for English-only practice. The timing, screen actions and Chinese translation are in `VIDEO_RECORDING_GUIDE_zh.md`. The wording below matches that master guide.

## 0:00–0:25  Project and user

Hello, my name is Zihan Gao, and this is VerifyRAG, my PE6201 course project. I built it for verification engineers who need to check UVM API behaviour while developing a testbench. The system uses one pinned UVM release, shows the source behind its answers, and refuses questions that are outside the available evidence.

## 0:25–0:55  Architecture and design change

The corpus contains 24 files from Accellera UVM 2020.3.1, divided into 349 deterministic chunks. I originally proposed embeddings and a vector database. After building the corpus, I changed to BM25 and TF-IDF because exact UVM identifiers work well with lexical retrieval. This design is inexpensive, reproducible and easier to inspect, although it may miss strongly paraphrased questions.

## 0:55–1:25  Tests and reproducibility

The public notebook was rerun in Colab on 28 September. All 31 tests passed, and the run confirmed 349 chunks from 24 source files. The tests cover source integrity, version boundaries, citation alignment and refusal rules. They show that the programmed checks work; they do not prove that every generated answer is correct.

## 1:25–2:00  Offline evidence and refusals

This supported example uses the offline path, so it makes no model request and has no API cost. The result shows an exact source excerpt, its file and its line range. It is an evidence preview rather than a generated answer. The next two examples ask for private evidence that was not supplied and for hidden instructions or a credential. In both cases, the system abstains instead of inventing an answer.

## 2:00–2:30  Retrieval results

On six answerable development questions, BM25 ranked a labelled passage first in five cases and within the top five in all six. TF-IDF and the hybrid method ranked it first in four cases and within the top five in all six. BM25 reached an MRR at five of 0.9167. These are retrieval measurements on a small development set, not answer-accuracy scores.

## 2:30–3:10  Paid smoke test

For the fresh paid check, the OpenRouter key was loaded from Colab Secrets and was never printed or stored in a code cell. The smoke test used GPT-4o mini, 3,539 tokens and 0.00059745 US dollars. The validator accepted the citation, but the answer only said that tracing is off by default. It did not explain how to enable tracing. This failure shows that a valid citation does not guarantee a complete answer.

## 3:10–3:35  Fresh paid comparison

The development comparison made 24 additional calls with no API error. Hybrid RAG answered five of six supported cases and refused both unsupported cases. BM25 RAG answered four of six and also refused both unsupported cases. Including the smoke test, the fresh run made 25 calls, used 54,692 tokens and cost 0.00908730 US dollars.

## 3:35–4:05  Target and frozen confirmation

The five-out-of-six figure is an automated status, not correctness. My AI-assisted reference check accepted four of six hybrid answers as complete, so the fresh run did not prove the 80 percent answer-quality target. In the frozen confirmation run, retrieval reached 14 out of 14 at Hit at five, but the original boundary logic refused only four of six unsupported cases, or 66.7 percent. That also missed the 80 percent safety target.

## 4:05–4:40  Risks and limits

The main risk is a fluent interpretation attached to real but incomplete evidence. Exact quotations and source checks reduce that risk, but an engineer still has to judge whether the evidence supports the whole answer. VerifyRAG cannot inspect a private DUT, run a simulator, cover every UVM release or approve sign-off. Private RTL and logs are outside the hosted-model scope.

## 4:40–5:15  Conclusion and disclosure

In summary, VerifyRAG is an evidence navigator for one pinned UVM release. The public repository includes the code, corpus, tests, failed cases and evaluation records. I used generative AI during research, coding, test design and editing, and the assistance is documented here. I kept the failed and incomplete results and did not present automated checks as human-validated accuracy. Thank you.
