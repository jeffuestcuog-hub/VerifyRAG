# Submission review notes — 16 September 2026

## What was revised

- Replaced unverified first-person implementation claims with project-level, evidence-based wording.
- Connected each design choice to a trade-off: lexical retrieval, no agent loop, local versus hosted generation, fixed source version and build-versus-rent boundaries.
- Added the missing citation for structured output and provider usage accounting, and dated the model-price assumption.
- Kept development, exposed exploratory and frozen confirmation evidence separate.
- Reported the missed safety target exactly: 4/6 appropriate abstentions (66.7%) against an 80% target.
- Explained the two frozen failure modes and the lack of a semantic relevance threshold.
- Clarified that Hit@5, exact quotes and identifier checks do not establish answer correctness or entailment.
- Revised the demo and self-appraisal prompts to use the recorded success and failure evidence.
- Confirmed the report remains below the 1,200-word limit: 1,109 words before references using the repository count.

## Evidence deliberately left incomplete

- Live OpenRouter output, measured token cost and plain-model-versus-RAG answer comparison.
- Student and domain-peer correctness, usability and citation-entailment review.
- User-study evidence for time savings, willingness to pay or ROI.
- Student-recorded demonstration, GitHub publication and university upload.

These items require real execution or personal authorship. They must not be replaced with invented results.

## Final student review

Before submission, read the report aloud and make sure every sentence is something you can explain.
Record your own reproduction run and contribution in `docs/AI_USE.md`. If you perform the live or
human evaluation, update the report with actual numerators, denominators, model identifier, run ID
and reviewer details; otherwise keep the stated limitations.
