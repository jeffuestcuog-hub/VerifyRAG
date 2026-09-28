# Authorship and AI assistance disclosure

Project owner: Gao Zihan. Course: PE6201, individual End-of-Course Project.

The original VerifyRAG proposal and domain framing were supplied in the owner's existing course
materials. In this session Codex assisted with requirements analysis, public-source discovery,
software implementation, test/evaluation scaffolding, offline execution, and report/demo drafts.
Parallel AI agents helped implement the engine, draft evaluation labels, and check source evidence.
After the v2 code/corpus freeze, a context-isolated AI task was restricted to the pinned corpus
and raw sources to author the confirmation set; it did not inspect the engine, earlier labels or
outputs. Codex performed the mechanical preflight and one frozen offline run, preserved both missed
abstentions, and updated the report without changing the evaluated engine.

On 25 September 2026, Codex operated the owner's Google Colab session to upload the project,
rerun the then-current 27 tests, reproduce the offline development evaluation and, after explicit
owner authorisation, make one paid smoke request plus 24 paid development requests through
OpenRouter. The stored API secret was read through Colab Secrets and was not printed or saved.
Codex retained compact raw-response and usage records, diagnosed false rejections caused by
comment-line formatting, implemented source-aligned quote recovery and class-scope checks, added
four tests, and revalidated the saved responses without further API calls. The current 31 tests
pass. Codex also prepared a clearly labelled AI-assisted source comparison; it is not human review.

On 27 September 2026, the owner opened the notebook in Colab and reproduced the workflow. That
run is retained as historical evidence, including a false smoke-test abstention.

On 28 September 2026, after the owner explicitly authorised new OpenRouter charges, Codex operated
the open Colab session for a fresh public-notebook check. Both paid switches were enabled for the
run and reset to `False` afterwards. The OpenRouter secret was read only through Colab Secrets and
was not printed or stored in a code cell. The run completed 25 paid calls with no API error, used
54,692 tokens and cost USD 0.00908730. The saved evidence includes the per-case records and a
notebook copy with outputs. Codex also compared the outputs with the prepared references. That
AI-assisted check rated 4/6 hybrid answers complete; it is not independent human review.

The owner has reproduced the notebook workflow but has **not yet completed** domain review of every
answer or obtained peer validation. No independent human correctness score is claimed. The owner
should still check the final first-person design statements and be able to explain them before
submission.

All imported UVM source is attributed in `THIRD_PARTY_NOTICES.md`. Existing A1/A2 results were not
relabelled as VerifyRAG evidence. Model-generated output is identified as such; offline evidence
previews and automated citation checks are not represented as measured LLM correctness.

## Owner contribution log (complete truthfully)

| Date | Work actually performed | Evidence | Decision I can explain |
|---|---|---|---|
| Pending | Review scope and source version | Own notes | Why this scope |
| 27-28 Sep 2026 | Ran and inspected the Colab notebook | Downloaded notebooks and preserved run evidence | Tests passed; fresh smoke citation passed but its answer was incomplete |
| Pending | Review domain labels and answers with a peer | Named review worksheet | Why an answer is correct |
| 28 Sep 2026 | Revised the final report against the fresh results | Final report and change record | Why automated status and answer completeness differ |
| Pending | Record personal demonstration | Video URL | Risks and limits |
