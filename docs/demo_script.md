# VerifyRAG concise English narration

The matching screen actions and Chinese translation are in `VIDEO_RECORDING_GUIDE_zh.md`.

## 0:00–0:20  Project

Hello, my name is Zihan Gao. VerifyRAG is my PE6201 course project for verification engineers who need to check UVM APIs. It uses one pinned UVM release, shows source evidence and refuses questions outside that evidence.

## 0:20–0:45  Design

The corpus contains 24 Accellera UVM 2020.3.1 files and 349 deterministic chunks. I replaced the proposed vector database with BM25 and TF-IDF because exact UVM identifiers suit lexical retrieval. This is cheaper and easier to reproduce, although it may miss heavily paraphrased questions.

## 0:45–1:10  Tests

The public notebook was rerun on 28 September. All 31 tests passed and confirmed 349 chunks from 24 source files. The tests cover source integrity, version boundaries, citation alignment and refusal rules. They verify the programmed checks, not answer correctness.

## 1:10–1:40  Offline evidence

The offline path makes no model request. A supported question returns an exact source excerpt with its file and line range. It is an evidence preview, not a generated answer. Requests for missing private evidence or hidden credentials are refused instead of being answered from guesswork.

## 1:40–2:00  Retrieval

On six answerable development questions, BM25 reached five out of six at Hit at one and six out of six at Hit at five. TF-IDF and hybrid reached four out of six and six out of six. These are retrieval results, not answer accuracy.

## 2:00–2:35  Smoke test

The OpenRouter key was loaded only from Colab Secrets. The GPT-4o mini smoke test used 3,539 tokens and cost 0.00059745 US dollars. Its citation passed, but the answer only said tracing is off by default and omitted how to enable it. A valid citation therefore does not guarantee a complete answer.

## 2:35–3:00  Paid comparison

The development comparison made 24 calls with no API error. Hybrid answered five of six supported cases and refused both unsupported cases. BM25 answered four of six and also refused both. Including the smoke test, the fresh run made 25 calls, used 54,692 tokens and cost 0.00908730 US dollars.

## 3:00–3:30  Targets

Five out of six is an automated status, not correctness. My AI-assisted reference check accepted only four of six hybrid answers as complete, so the fresh run did not prove the 80 percent quality target. The frozen confirmation run also refused only four of six unsupported cases, or 66.7 percent.

## 3:30–3:55  Limits

The main risk is a fluent answer supported by real but incomplete evidence. Source checks reduce this risk, but an engineer must still judge the meaning. VerifyRAG cannot inspect a private DUT, run a simulator, cover every UVM release or approve sign-off.

## 3:55–4:20  Conclusion

VerifyRAG is an evidence navigator for one pinned UVM release. The repository includes the code, corpus, tests, failures and evaluation records. I used generative AI during research, coding, testing and editing, and documented that assistance. I kept incomplete results and did not present automated checks as human-validated accuracy. Thank you.
