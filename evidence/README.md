# Saved paid-run evidence

`paid_run_20260928/` contains the sanitised records downloaded from the fresh public-notebook run on
28 September 2026:

- `run_manifest.json`: run configuration and identifiers;
- `summary.json` and `fresh_paid_run_summary.json`: aggregate status, usage and cost;
- `records.jsonl`: per-case retrieved evidence, model output and validation status;
- `live_progress.jsonl`: append-only progress captured during the run;
- `human_review.csv`: review worksheet retained with the run.

The run made 25 paid calls without an API error, used 54,692 tokens and reported a total OpenRouter
cost of USD 0.00908730. The files contain no OpenRouter credential. Automated status and the saved
AI-assisted comparison are evidence about the development run; they are not independent human
correctness labels. See `../docs/colab_validation_20260928.md` and
`../docs/evaluation_protocol.md` for interpretation limits.
