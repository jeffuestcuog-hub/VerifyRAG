# VerifyRAG 精简录屏操作与中英对照口播主稿

建议成片：4分40秒至5分钟

正式口播：只念英文；中文仅用于理解
Colab：`https://colab.research.google.com/github/jeffuestcuog-hub/VerifyRAG/blob/main/VerifyRAG_Colab.ipynb`

## 录制前

1. 只保留GitHub和已保存结果的Colab两个标签页。
2. 关闭Secrets侧栏、邮箱、聊天和书签栏。
3. 不要刷新Colab，不要点击“全部运行”；两个付费开关保持`False`。
4. 浏览器缩放约90%，先做15秒试录。

## 1  0:00–0:20  项目介绍

**展示**  GitHub仓库顶部，显示`VerifyRAG`、`Public`和README标题。画面停稳，不滚动。

**English**

Hello, my name is Zihan Gao. VerifyRAG is my PE6201 course project for verification engineers who need to check UVM APIs. It uses one pinned UVM release, shows source evidence and refuses questions outside that evidence.

**中文**

大家好，我是Gao Zihan。VerifyRAG是我的PE6201课程项目，面向需要核对UVM API的验证工程师。它使用一个固定的UVM版本，展示原始证据，并拒绝证据范围外的问题。

## 2  0:20–0:45  方案取舍

**展示**  在README按`Ctrl + F`搜索`Architecture`，停在架构图。

**English**

The corpus contains 24 Accellera UVM 2020.3.1 files and 349 deterministic chunks. I replaced the proposed vector database with BM25 and TF-IDF because exact UVM identifiers suit lexical retrieval. This is cheaper and easier to reproduce, although it may miss heavily paraphrased questions.

**中文**

语料包含Accellera UVM 2020.3.1的24个文件和349个文本块。我把原计划的向量数据库改为BM25和TF-IDF，因为精确的UVM标识符适合词法检索。这样成本更低、更容易复现，但可能漏掉大幅改写的问题。

## 3  0:45–1:10  测试结果

**展示**  切到Colab第2节，显示`Ran 31 tests`、`OK`、349 chunks、24 files和固定commit。

**English**

The public notebook was rerun on 28 September. All 31 tests passed and confirmed 349 chunks from 24 source files. The tests cover source integrity, version boundaries, citation alignment and refusal rules. They verify the programmed checks, not answer correctness.

**中文**

公开笔记本于9月28日重新运行。31项测试全部通过，并确认349个文本块来自24个源文件。测试覆盖来源完整性、版本边界、引用对齐和拒答规则，但不代表答案正确。

## 4  1:10–1:40  离线证据与拒答

**展示**  Colab第3节：先显示支持问题的证据、文件和行号，再滚到两个`Status: abstained`。

**English**

The offline path makes no model request. A supported question returns an exact source excerpt with its file and line range. It is an evidence preview, not a generated answer. Requests for missing private evidence or hidden credentials are refused instead of being answered from guesswork.

**中文**

离线路径不会请求模型。支持问题返回带文件和行号的原始摘录，它是证据预览，不是生成答案。对于缺失的私人证据或隐藏凭据请求，系统会拒答而不是猜测。

## 5  1:40–2:00  检索指标

**展示**  Colab第4节，使BM25、TF-IDF和Hybrid三行同时可见。

**English**

On six answerable development questions, BM25 reached five out of six at Hit at one and six out of six at Hit at five. TF-IDF and hybrid reached four out of six and six out of six. These are retrieval results, not answer accuracy.

**中文**

在六个可回答问题中，BM25的Hit@1为5/6，Hit@5为6/6；TF-IDF和Hybrid分别为4/6和6/6。这些是检索结果，不是答案正确率。

## 6  2:00–2:35  付费烟雾测试

**展示**  Colab第6节最新烟雾输出，显示`Status: answered`、3,539 tokens、USD 0.00059745和引用。

**English**

The OpenRouter key was loaded only from Colab Secrets. The GPT-4o mini smoke test used 3,539 tokens and cost 0.00059745 US dollars. Its citation passed, but the answer only said tracing is off by default and omitted how to enable it. A valid citation therefore does not guarantee a complete answer.

**中文**

OpenRouter密钥只从Colab Secrets加载。GPT-4o mini烟雾测试使用3,539 tokens，费用为0.00059745美元。引用通过了检查，但答案只说追踪默认关闭，没有说明怎样开启。因此引用有效不代表答案完整。

## 7  2:35–3:30  付费对比与目标

### 画面一  2:35–3:00

**展示**  滚到`FRESH PAID RUN - 28 September 2026`，显示24 calls、Hybrid 5/6和2/2，以及总计25 calls、54,692 tokens、USD 0.00908730。

**English**

The development comparison made 24 calls with no API error. Hybrid answered five of six supported cases and refused both unsupported cases. BM25 answered four of six and also refused both. Including the smoke test, the fresh run made 25 calls, used 54,692 tokens and cost 0.00908730 US dollars.

**中文**

开发集对比进行了24次调用，没有API错误。Hybrid回答5/6个支持问题并拒绝2/2个不支持问题；BM25分别为4/6和2/2。包括烟雾测试，本次复跑共25次调用、54,692 tokens，费用为0.00908730美元。

### 画面二  3:00–3:30

**展示**  回到README，搜索`14/14`，停在冻结确认集说明。

**English**

Five out of six is an automated status, not correctness. My AI-assisted reference check accepted only four of six hybrid answers as complete, so the fresh run did not prove the 80 percent quality target. The frozen confirmation run also refused only four of six unsupported cases, or 66.7 percent.

**中文**

5/6只是自动状态，不是正确率。AI辅助参考复核只认定4/6个Hybrid答案完整，因此本次运行没有证明达到80%的质量目标。冻结确认运行也只拒绝了4/6个不支持问题，即66.7%。

## 8  3:30–3:55  风险与限制

**展示**  在README搜索`Limits`并停在该段。

**English**

The main risk is a fluent answer supported by real but incomplete evidence. Source checks reduce this risk, but an engineer must still judge the meaning. VerifyRAG cannot inspect a private DUT, run a simulator, cover every UVM release or approve sign-off.

**中文**

主要风险是流畅答案可能只得到真实但不完整的证据支持。来源检查可以降低风险，但仍需工程师判断含义。VerifyRAG不能检查私人DUT、运行仿真、覆盖所有UVM版本或批准签核。

## 9  3:55–4:20  结论与AI说明

**展示**  打开`docs/AI_USE.md`，再切回仓库顶部。说完后停两秒再结束录制。

**English**

VerifyRAG is an evidence navigator for one pinned UVM release. The repository includes the code, corpus, tests, failures and evaluation records. I used generative AI during research, coding, testing and editing, and documented that assistance. I kept incomplete results and did not present automated checks as human-validated accuracy. Thank you.

**中文**

VerifyRAG是针对一个固定UVM版本的证据导航工具。仓库包含代码、语料、测试、失败案例和评估记录。我在研究、编码、测试和编辑中使用了生成式AI，并记录了相关协助。我保留了不完整结果，也没有把自动检查描述成人工验证的正确率。谢谢。

## 录完只检查六项

1. 成片约4分40秒至5分钟，开头10秒内出现姓名、课程和项目名。
2. 每段口播与指定画面对应，滚动时不要说下一段。
3. 画面包含31项测试、两个拒答、检索表、烟雾测试和付费汇总。
4. 不要把Hit@5、5/6或引用通过说成答案正确率。
5. 画面中没有API key、Secrets侧栏、邮箱或聊天。
6. 上传后用无痕窗口测试链接，再填入`04_GitHub_and_Video_Links.txt`。
