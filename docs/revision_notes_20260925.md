# Revision notes — 25 September 2026

- Reproduced the offline workflow in a Google Colab CPU runtime.
- Confirmed all 27 then-current automated tests pass in Colab; the revised local project now passes 31.
- Reproduced the development-set ranking metrics and recorded Colab-specific latency.
- Checked one supported question and two refusal paths offline.
- After explicit owner authorisation, ran one paid smoke request and 24 paid development requests
  with `openai/gpt-4o-mini` through OpenRouter; measured total cost was USD 0.00915030.
- Preserved compact raw responses, retrieval identifiers, validation outcomes, usage and provider metadata.
- Found that the strict validator rejected correct prose when a model removed source-comment line
  prefixes; added bounded source alignment that returns only exact source spans.
- Added enclosing-class metadata and qualified-method checks after the live output confused
  `uvm_config_db` with `uvm_config_db_options`.
- Revalidated the saved responses without new API calls: hybrid automated acceptance was 6/6 on
  answerable development cases and refusal was 2/2 on unsupported cases.
- Added an explicitly non-human preliminary source comparison: hybrid 5/6 correct-and-usable versus
  plain LLM 2/6. The pre-registered human confirmation target remains pending.
- Updated the notebook upload path so a pre-uploaded `VerifyRAG.zip` or `VerifyRAG_public.zip` can be reused safely.
- Added the Colab evidence and corpus hash to the trade-off report.
- Kept the original failed 4/6 confirmation result visible; later 6/6 regression is labelled exposed tuning evidence.
