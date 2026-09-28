# Submission evidence checklist

This checklist records the evidence prepared in the repository. It does not claim that the files
have already been uploaded to NTULearn.

**Current NTULearn deadline checked on 28 September 2026:** 4 October 2026, 11:59 PM (UTC+8).

| Deliverable / evidence | Status | Location / action |
|---|---|---|
| Individual topic and original problem | Complete | VerifyRAG; original course proposal retained separately |
| One-page problem statement | Complete | Final PDF in the submission folder |
| Trade-off analysis, maximum 1,200 words | Complete; about 1,095 words before references | `tradeoff_report.md`, editable DOCX and final PDF |
| First-person authorship and limitations | Reviewed | `tradeoff_report.md`, `AI_USE.md` |
| Source corpus, licence and fixed version | Complete | `data/source_manifest.json`, `data/raw/` |
| Local reproduction | Complete | CLI instructions, Colab notebook and 31 passing tests |
| Retrieval baseline comparison | Complete on small development and confirmation sets | `results/`, notebook outputs |
| Frozen confirmation evidence | Preserved | Original v2: 14/14 Hit@5; 4/6 unsupported cases refused |
| Later guardrail regression | Preserved and labelled as exposed data | 6/6 unsupported cases refused; not treated as a new blind result |
| Fresh hosted-model comparison | Complete for 28 September development run | 24 calls, 51,153 tokens, USD 0.00848985; zero API errors |
| Fresh paid smoke test | Preserved as an incomplete answer | 1 call, 3,539 tokens, USD 0.00059745; citation passed but enablement step was omitted |
| Fresh paid-run total | Complete and retained | 25 calls, 54,692 tokens, USD 0.00908730 |
| Correctness and usability review | Preliminary only | AI-assisted source review: hybrid 4/6, BM25 3/6, plain 2/6; human review pending |
| Fresh evidence archive | Complete | `evidence/VerifyRAG_paid_run_20260928.zip` and downloaded notebook with outputs |
| Credential handling | Complete for public package | API key kept in Colab Secrets; package scanned |
| GitHub repository | Published and publicly accessible | https://github.com/jeffuestcuog-hub/VerifyRAG |
| Recorded working demo | Script complete; recording pending | `demo_script.md` |
| Repository and video links | Repository complete; video pending | Add the accessible video URL before NTULearn upload |
| NTULearn submission | Pending | Read current View instructions, upload, reopen files, save receipt |

## Final checks before submission

1. Read the current NTULearn **View instructions** page and follow its exact file/link format.
2. Record the demonstration using the saved evidence; do not rerun the paid cells for the video.
3. Test the video link in a private/incognito window.
4. Read the final report personally and confirm that every first-person statement is accurate.
5. Upload before 4 October 2026, 11:59 PM (UTC+8), reopen each submitted item, and save the receipt.

## Evidence limits

- The course files require a problem statement, a trade-off analysis of no more than 1,200 words,
  working code in GitHub, and a recorded presentation/demo.
- No independent domain-expert review has been completed.
- Hit@5 measures retrieval of an annotated passage, not answer correctness.
- The AI-assisted development review is clearly labelled and is not human ground truth.
- The fixed five-minute duration found in the course outline applies to another assessment. The
  five-to-six-minute project script is a practical recommendation unless NTULearn states otherwise.
