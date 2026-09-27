# VerifyRAG video script

This is a rehearsal script for a five-to-six-minute recording. Speak naturally and change any
wording that you would not normally use. Keep the Colab Secrets panel closed. The demonstration
uses saved outputs, so it does not need another paid API call.

## Before recording

- Open `README.md`, `VerifyRAG_Colab.ipynb`, and the saved results folder.
- Collapse long installation and code cells in Colab.
- Keep the cells showing the 31 tests, offline metrics, saved paid comparison, and smoke-test
  refusal visible.
- Check that no API key or personal browser tab is on screen.
- Practise once with a timer. Aim for five to six minutes.

## 0:00-0:35 | Problem and intended user

**Show:** the project title and the first section of `README.md`.

**Say:**

“My project is VerifyRAG. I built it for a verification engineer who needs to check UVM API
behaviour while writing or debugging a testbench. General chatbots can give a fluent answer from
the wrong UVM version, so my system only returns a generated answer when it can connect each claim
to the selected source code. Otherwise, it refuses or shows local evidence for inspection.”

## 0:35-1:15 | What I built and why

**Show:** the architecture section of `README.md`, then `data/source_manifest.json`.

**Say:**

“The corpus contains 24 files from the Accellera UVM 2020.3.1 source tree. It is pinned to one
commit, and I record file checksums and source-line links. My proposal originally mentioned
embeddings and a vector database. After building the corpus, I changed to BM25 and TF-IDF because
this small technical corpus contains exact identifiers such as `uvm_config_db`. The lexical methods
are cheaper and easier to inspect. I use OpenRouter and GPT-4o-mini only for optional answer
generation.”

## 1:15-2:05 | Reproducible local evidence

**Show:** the notebook output that ends with `Ran 31 tests` and `OK`, followed by the development
retrieval table.

**Say:**

“I reran the notebook in Colab on 27 September. All 31 tests passed. On the six answerable
development questions, BM25 found a labelled passage first in five cases and within the top five in
all six cases. TF-IDF and the hybrid method also found a labelled passage within the top five in all
six. These are retrieval results. They do not prove that a generated answer is correct.”

## 2:05-2:55 | Supported and unsupported questions

**Show:** one saved local answer for `How do I use uvm_config_db get and set?`, including its source
path and quote. Then show the unsupported API and wrong-version cases.

**Say:**

“For this supported question, the local mode retrieves the original source text and shows where it
came from. This is an evidence preview rather than an LLM answer. For a nonexistent API or a request
for another UVM version, the system refuses. The version and scope checks are implemented in code;
they are not only a warning in the interface.”

## 2:55-3:45 | Validation and an honest failure

**Show:** the saved 25 September paid comparison, then the 27 September smoke-test output.

**Say:**

“In hosted mode, the model must return structured claims. Each claim needs a retrieved chunk and a
quote that can be aligned to one exact source span. UVM identifiers must appear in that source, and
a class-qualified method must match the class scope.

The saved 25 September development batch used 25 calls, 54,426 tokens and cost about 0.0092 US
dollars. After a bounded alignment fix, the validator accepted six out of six hybrid drafts for the
answerable development questions and refused both unsupported questions. An AI-assisted source
review rated five of the six hybrid answers correct and usable, compared with two of six for the
plain model. This is development evidence, not independent human accuracy.

The later smoke test is a useful failure. It used 3,543 tokens and cost 0.00035025 dollars, but the
validator rejected the draft and the system abstained on a supported question. This shows that a
strict guardrail can also remove a useful answer.”

## 3:45-4:35 | Target, limits, and risk

**Show:** the frozen confirmation summary and the limitations section of the report.

**Say:**

“My target was at least 80 percent correct-and-usable answers and 80 percent appropriate
abstention. The frozen 20-case confirmation run retrieved a labelled passage within five results for
all 14 answerable questions, but the original boundary logic refused only four of the six unsupported
questions. Later changes passed all six exposed refusal cases, but I treat that as regression
evidence because those cases are no longer blind.

The main remaining risk is a fluent interpretation attached to real but insufficient evidence.
Exact quotes and source checks reduce that risk, but a verification engineer still needs to judge
the meaning. The prototype cannot inspect a private DUT, run a simulator, or approve sign-off.”

## 4:35-5:20 | Cost, deployment, and conclusion

**Show:** the repository file list and the three reproduction commands in the report or `README.md`.

**Say:**

“Offline retrieval has no token charge and keeps the question local. Hosted generation sends the
question and public source excerpts to a provider, so private RTL and logs are outside this
prototype’s scope. Before a real pilot, I would use a larger frozen benchmark and blinded review by
verification engineers.

In summary, VerifyRAG is a small evidence navigator for one pinned UVM release. Its strongest result
is reproducibility: the corpus, tests, saved failures and evaluation files are included in the
repository. Its main limitation is that citation checks do not replace engineering judgement.”

## 5:20-5:35 | Disclosure

**Show:** `docs/AI_USE.md`.

**Say:**

“I used generative AI during research, coding, test design and editing. I checked the final Colab run,
kept the failed cases, and documented the assistance in the repository. I have not presented the
AI-assisted labels as independent human review.”

## Final recording check

- The first ten seconds include your name, course, and project title.
- The recording shows the working notebook, source evidence, one refusal, metrics, and one failure.
- Every number spoken matches the final report.
- No secret, email inbox, or unrelated browser tab is visible.
- The uploaded video opens in a private/incognito window without requesting access.
