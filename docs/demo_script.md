# VerifyRAG video narration

Target length: about 5 minutes 40 seconds. Speak at a normal pace and pause when a result appears.

## 0:00–0:30 | Introduction

Hello, my name is Zihan Gao, and this is VerifyRAG, my PE6201 course project. I built it for verification engineers who need to check UVM APIs while developing a testbench. A general chatbot may use the wrong release or answer without enough evidence. VerifyRAG therefore uses one pinned source version, shows its citations, and refuses questions outside the available evidence.

## 0:30–1:00 | Architecture and design change

The corpus contains 24 files from Accellera UVM 2020.3.1, divided into 349 deterministic chunks. Each chunk keeps its commit, checksum, file name and line range. I originally planned to use embeddings and a vector database. I changed to BM25 and TF-IDF because exact UVM names work well with lexical retrieval, and the result is cheaper and easier to inspect.

## 1:00–1:35 | Fresh public Colab run

The public notebook was rerun in Colab on 28 September. All 31 tests passed. They check source integrity, provenance, version boundaries, citation alignment and refusal rules. The run also confirmed 349 chunks from 24 source files. These tests show that the programmed checks work. They do not prove that every generated answer is correct.

## 1:35–2:20 | Offline evidence and refusals

This first example uses the offline path, so it makes no model request. The question asks about configuration database tracing. The result shows an exact source excerpt, says that tracing is off by default, and gives the source file and line range. This is an evidence preview rather than a generated answer. The next case asks for an exact fault in a private scoreboard without providing code or logs, so the system abstains. It also refuses a request to reveal hidden instructions or an API key.

## 2:20–2:55 | Retrieval results

On six answerable development questions, BM25 ranked a labelled passage first in five cases and within the top five in all six. TF-IDF and the hybrid ranker placed it first in four cases and within the top five in all six. BM25 reached an MRR at five of 0.9167, while the other two reached 0.8333. These are retrieval measurements on a small development set. They are not answer-accuracy scores.

## 2:55–3:35 | Fresh paid smoke test

For this requested rerun, both paid switches were temporarily enabled and the OpenRouter key was loaded from Colab Secrets. The key was never printed or stored in a code cell. The smoke test made one request with GPT-4o mini. It used 3,539 tokens and cost 0.00059745 US dollars. The validator accepted the answer and its citation, but the answer only said that tracing is off by default. It did not explain how to enable tracing. This is a useful failure case: a valid citation does not guarantee that a two-part question was answered completely.

## 3:35–4:20 | Fresh paid comparison

The development comparison made 24 additional calls. It used 51,153 tokens, cost 0.00848985 dollars, and completed without an API error. Hybrid RAG answered five of the six supported cases and refused both unsupported cases. BM25 RAG answered four of six and also refused both unsupported cases. The plain model returned an answered status for all eight cases and produced no system-level abstention.

The automatic five-out-of-six result is coverage, not correctness. In an AI-assisted comparison against the prepared reference answers, I judged four of the six hybrid answers complete. One supported event question was refused, and one two-part sequence question omitted the rule that delays are not allowed between start_item and finish_item. This was not independent human review.

Including the smoke test, the fresh run made 25 paid calls, used 54,692 tokens, and cost 0.00908730 US dollars. I reset both paid switches to false after the run.

## 4:20–4:50 | Target and frozen confirmation result

My target was at least 80 percent correct-and-usable answers and 80 percent appropriate abstention. In the frozen 20-case confirmation run, BM25 found a labelled passage within five results for all 14 answerable questions. However, the original boundary logic refused only four of six unsupported questions, or 66.7 percent, so it missed the safety target. Later fixes passed all six exposed cases, but that is regression evidence because those questions were no longer blind.

## 4:50–5:25 | Limits

The main risk is a fluent answer attached to real but incomplete evidence. Exact quotations and citation checks reduce this risk, but an engineer still has to judge whether the evidence supports the whole answer. The prototype cannot inspect a private DUT, run a simulator, cover every UVM release or approve sign-off. Private RTL and logs remain outside the hosted-model scope.

## 5:25–5:50 | Conclusion and disclosure

In summary, VerifyRAG is an evidence navigator for one pinned UVM release. The public repository includes the code, corpus, tests, unsuccessful cases and evaluation records. I used generative AI during research, coding, test design and editing. I kept the failed and incomplete results, and I did not present the automated checks as human-validated accuracy. Thank you.

## Five lines to practise

1. Hit at five is a retrieval metric, not answer accuracy.
2. The fresh paid run made twenty-five calls and cost 0.00908730 US dollars.
3. Hybrid answered five out of six supported cases, but this is an automated status result.
4. My AI-assisted completeness check accepted four out of six hybrid answers; it was not independent human review.
5. The frozen confirmation run achieved four out of six appropriate abstentions, below the 80 percent target.
