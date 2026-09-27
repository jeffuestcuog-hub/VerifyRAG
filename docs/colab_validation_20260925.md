# Colab and OpenRouter validation record — 25 September 2026

This record separates the original live outputs, later validator development and work that still requires human review.

## Environment and inputs

- Platform: Google Colab CPU runtime.
- Model: `openai/gpt-4o-mini` through OpenRouter.
- Candidate archive SHA-256: `EB144F291904F3D6681DA06362C82AE90AAC3AA61DFEFD7393774FA0025E1C84`.
- Colab project root: `/content/verifyrag_v3_workspace/VerifyRAG`.
- Live development run: `/content/verifyrag_v3_workspace/VerifyRAG/results/20260925T142018102794Z_development_live`.
- Development dataset SHA-256: `45ea3a4a02f81bfb469acc63301cee8d9f6f8286454febfa9eb9f1174f98eaef`.
- The API key was read from Colab Secrets through `google.colab.userdata`; it was not printed or written to the project.

The uploaded archive passed all 27 tests that existed at that point. The grounded prompt was then tightened in the Colab copy before the paid run to require literal API spelling and quoted identifier support. The current repository adds quote-alignment, class-scope checks and four further tests; it now passes 31 tests. The current corpus hash is different because deterministic `scope` metadata was added, while chunk IDs, source text and rankings remain unchanged.

## Paid calls and measured usage

The user authorised one smoke request and up to 24 development requests. Exactly 25 calls were made, with no automatic retries.

| Batch/method | Calls | Tokens | Provider-reported cost (USD) | Original status summary |
|---|---:|---:|---:|---|
| Smoke: BM25+LLM | 1 | 3,456 | 0.00059625 | Rejected by evidence validation |
| Plain LLM | 8 | 1,720 | 0.00077820 | 8 answered |
| BM25+LLM | 8 | 25,434 | 0.00427995 | 1 answered, 7 abstained |
| Hybrid+LLM | 8 | 23,816 | 0.00349590 | 0 answered, 8 abstained |
| **Total** | **25** | **54,426** | **0.00915030** | — |

For the 24-call development run, median/p95 end-to-end latency was 2,400.9/4,778.0 ms for plain LLM, 2,121.9/5,027.9 ms for BM25+LLM and 2,601.9/4,937.2 ms for hybrid+LLM. Provider and network conditions can change these figures.

The original strict validator rejected most grounded drafts because the model copied the correct documentation prose but removed source-comment prefixes and line breaks. It also correctly caught wrong or unquoted class-qualified identifiers. Raw responses, usage, provider metadata, retrieval IDs and validation errors were retained in `results/20260925T142018102794Z_development_live/records_compact.json`. Full retrieved text was omitted from this compact copy because it is reconstructible from the pinned corpus.

## Post-hoc validator development

No further API call was made. The saved raw responses were rechecked after two bounded changes:

1. A formatting-only aligner maps a provider quote back to one unique exact source span. It preserves case, spelling and punctuation, and rejects ellipses and ambiguous matches.
2. Each claim is checked independently. Invalid claims are removed; a response is shown only when at least one claim remains valid. Qualified `Class::method` names must agree with deterministic enclosing-class metadata.

| Method | Answerable drafts accepted | Unsupported cases abstained |
|---|---:|---:|
| BM25+LLM | 5/6 (83.3%) | 2/2 (100%) |
| Hybrid+LLM | 6/6 (100%) | 2/2 (100%) |

These are automated provenance outcomes on development data, not semantic correctness. A disclosed AI-assisted source comparison rated the post-hoc hybrid output correct-and-usable on 5/6 cases (83.3%) and plain LLM on 2/6 (33.3%). The remaining hybrid case became incomplete after the validator removed a wrong class-qualified claim. The review is stored as `preliminary_ai_source_review.csv`; it is not human or independent domain validation.

## Evidence boundaries

- The original frozen v2 confirmation result remains 4/6 appropriate abstentions (66.7%). A later 6/6 regression on that now-exposed set is tuning evidence.
- The 80% numerical goal is met only by the disclosed post-hoc development review. The pre-registered human-reviewed confirmation target remains unverified.
- Automated quote and identifier checks do not prove entailment or technical correctness.
- A student and domain-aware peer should complete the blank review worksheet before presenting a final correctness claim.
