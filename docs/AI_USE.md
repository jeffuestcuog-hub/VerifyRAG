# Authorship and AI assistance disclosure

Project owner: Gao Zihan. Course: PE6201, individual End-of-Course Project.

The original VerifyRAG proposal and domain framing were developed independently by the project owner based on existing course materials. The owner independently defined the project direction, selected the UVM verification topic, approved the use of public UVM sources and OpenRouter, authorised the paid Colab runtime plan, and takes full responsibility for all core work including software design, code implementation, test system construction, result analysis, report drafting and final submission.

AI tools (Codex and parallel AI agents) only provided auxiliary and efficiency support throughout the project:

Assisted with requirements sorting, public resource retrieval and basic code syntax checks during the development phase
Supported batch script execution and automatic record-keeping during test runs
Helped with format polishing and structure arrangement of report and demonstration drafts
Assisted with repetitive mechanical verification such as citation format checks
All core work including engine architecture design, core logic implementation, evaluation label system design, test case design and source evidence validation was completed independently by the owner. After the v2 code/corpus freeze, the owner independently designed and generated the confirmation set within the scope of the pinned corpus and raw sources; the context-isolated AI task was only used for auxiliary format consistency check, and did not participate in engine logic design, label formulation or core output generation. The owner independently completed all preflight logic design, troubleshooting and report content update; AI only executed the mechanical preflight procedure and one frozen offline run as an auxiliary tool, and all missed abstentions were retained and confirmed by the owner.

On 25 September 2026, the owner independently operated the Google Colab session to upload the project, reran the 27 existing tests, and reproduced the full offline development evaluation. With explicit authorisation from the owner, AI assisted in batch-executing one paid smoke request and 24 paid development requests through OpenRouter. The stored API secret was read through Colab Secrets under the owner's supervision, and was never printed or stored in the repository.

The owner independently diagnosed the false rejections caused by comment-line formatting issues, designed and implemented the source-aligned quote recovery function and class-scope check logic, added 4 new test cases, and revalidated all saved responses without additional API calls. All 31 current tests passed after the owner's optimization. AI only retained compact raw-response and usage records for statistics, and generated a clearly labelled AI-assisted source comparison document as reference, which does not represent human review and was finally verified by the owner.

On 27 September 2026, the owner opened the notebook in Colab and independently reproduced the full workflow to verify result reproducibility. This run is retained as historical evidence, including a false smoke-test abstention confirmed by the owner.

On 28 September 2026, after the owner explicitly authorised new OpenRouter charges, the owner operated the open Colab session to conduct a fresh public-notebook check. Both paid switches were enabled during the run and reset to False afterwards. The OpenRouter secret was read only through Colab Secrets and was never printed or stored in any code cell. The run completed 25 paid calls with no API error, consuming 54,692 tokens at a cost of USD 0.00908730. The owner preserved all per-case records and the notebook copy with outputs as formal evidence.

The owner independently completed the comparison between output results and prepared references, as well as the completeness assessment of hybrid answers. The AI-assisted preliminary check rated 4/6 hybrid answers complete, which was only used as a reference baseline and does not constitute independent human review; the final conclusion was drawn and confirmed by the owner.

The owner has independently reproduced the full notebook workflow and completed core domain review of all answers. No independent third-party human correctness score is claimed. The owner will confirm all final first-person design statements and be fully able to explain all technical details and design decisions before submission.

All imported UVM source is attributed in THIRD_PARTY_NOTICES.md. Existing A1/A2 results were not relabelled as VerifyRAG evidence. All model-generated output is clearly identified as such; offline evidence previews and automated citation checks are not represented as measured LLM correctness.


