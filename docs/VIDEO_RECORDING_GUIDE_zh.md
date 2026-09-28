# VerifyRAG 录屏操作与中英对照口播主稿

建议时长：5分10秒至5分40秒  
正式口播：只念英文  
中文用途：帮助理解和检查，不需要在视频中念出  
公开Colab：`https://colab.research.google.com/github/jeffuestcuog-hub/VerifyRAG/blob/main/VerifyRAG_Colab.ipynb`

## 录制前准备

1. 浏览器只保留GitHub和已经保存结果的Colab两个标签页。
2. 关闭邮箱、聊天、课程页面、书签栏和Colab Secrets侧栏。
3. 确认Colab中两个付费开关均为`False`。
4. 不要刷新Colab，不要点击“全部运行”，不要重新运行付费单元格。
5. 浏览器缩放设为90%左右，使结果表和标题完整显示。
6. 按`Win + G`打开Xbox Game Bar，打开麦克风，先做15秒试录。

## 要求与展示内容对应表

| 项目内容 | 视频中展示的位置 | 对应段落 |
|---|---|---:|
| 问题、用户和价值 | GitHub仓库顶部与README开头 | 1 |
| 技术方案和取舍 | README的Architecture | 2 |
| 实现与可复现性 | Colab第2节测试结果 | 3 |
| 支持问题和安全拒答 | Colab第3节离线示例 | 4 |
| 检索评估 | Colab第4节结果表 | 5 |
| 付费模型与真实失败 | Colab第6节烟雾测试 | 6 |
| 方法对比、成本和80%目标 | FRESH PAID RUN汇总与README确认集结果 | 7 |
| 风险、限制和结论 | README Limits与AI_USE | 8和9 |

## 逐段录制

### 1  0:00–0:25  项目和目标用户

**画面**  GitHub仓库首页顶部，同时显示`VerifyRAG`、`Public`、文件列表和README标题。

**操作**  开始录制后停两秒再说。此段不要滚动。

**English narration**

Hello, my name is Zihan Gao, and this is VerifyRAG, my PE6201 course project. I built it for verification engineers who need to check UVM API behaviour while developing a testbench. The system uses one pinned UVM release, shows the source behind its answers, and refuses questions that are outside the available evidence.

**中文对照**

大家好，我是Gao Zihan。这是我的PE6201课程项目VerifyRAG。它面向在开发测试平台时需要核对UVM API行为的验证工程师。系统只使用一个固定的UVM版本，展示答案背后的原始来源，并拒绝超出已有证据范围的问题。

### 2  0:25–0:55  架构和方案变化

**画面**  在GitHub页面按`Ctrl + F`，输入`Architecture`，按Enter后按Esc，停在架构图和后面的说明。

**操作**  画面停稳后再开始本段。说完后切换到Colab。

**English narration**

The corpus contains 24 files from Accellera UVM 2020.3.1, divided into 349 deterministic chunks. I originally proposed embeddings and a vector database. After building the corpus, I changed to BM25 and TF-IDF because exact UVM identifiers work well with lexical retrieval. This design is inexpensive, reproducible and easier to inspect, although it may miss strongly paraphrased questions.

**中文对照**

语料库包含Accellera UVM 2020.3.1的24个文件，并确定性地划分为349个文本块。我最初计划使用嵌入和向量数据库。建立语料后，我改用BM25和TF-IDF，因为精确的UVM标识符适合词法检索。这个方案成本低、容易复现和检查，但可能漏掉改写幅度很大的问题。

### 3  0:55–1:25  测试与可复现性

**画面**  在Colab左侧目录点击`2. Check the files and tests`，滚到输出末尾。

**必须显示**  `Ran 31 tests`、`OK`、`349 chunks from 24 corpus source files`和固定commit。

**English narration**

The public notebook was rerun in Colab on 28 September. All 31 tests passed, and the run confirmed 349 chunks from 24 source files. The tests cover source integrity, version boundaries, citation alignment and refusal rules. They show that the programmed checks work; they do not prove that every generated answer is correct.

**中文对照**

公开笔记本于9月28日在Colab中重新运行。31项测试全部通过，并确认语料包含来自24个源文件的349个文本块。这些测试覆盖来源完整性、版本边界、引用对齐和拒答规则。它们说明程序检查能够工作，但不能证明每个生成答案都正确。

### 4  1:25–2:00  离线证据和拒答

**画面**  点击`3. Try the offline path`。先停在支持问题的`Status: answered`、证据摘录、文件名和行号，再缓慢向下滚到两个`Status: abstained`示例。

**操作**  第一句对应支持问题；说到`The next two examples`时再滚到两个拒答结果。

**English narration**

This supported example uses the offline path, so it makes no model request and has no API cost. The result shows an exact source excerpt, its file and its line range. It is an evidence preview rather than a generated answer. The next two examples ask for private evidence that was not supplied and for hidden instructions or a credential. In both cases, the system abstains instead of inventing an answer.

**中文对照**

这个支持问题使用离线路径，因此不会请求模型，也没有API费用。结果展示原始代码摘录、文件和行号。它是证据预览，不是生成式答案。接下来的两个例子分别要求没有提供的私人证据，以及隐藏指令或凭据。系统都选择拒答，而不是编造答案。

### 5  2:00–2:30  检索结果

**画面**  点击`4. Measure retrieval on the development questions`，让BM25、TF-IDF和Hybrid三行结果同时可见。

**操作**  鼠标不要遮住数字。说完后滚到第6节。

**English narration**

On six answerable development questions, BM25 ranked a labelled passage first in five cases and within the top five in all six. TF-IDF and the hybrid method ranked it first in four cases and within the top five in all six. BM25 reached an MRR at five of 0.9167. These are retrieval measurements on a small development set, not answer-accuracy scores.

**中文对照**

在六个可回答的开发集问题中，BM25有五题把标注段落排在第一位，六题都排在前五位。TF-IDF和Hybrid有四题排在第一位，六题都排在前五位。BM25的MRR@5为0.9167。这些是小型开发集上的检索指标，不是答案正确率。

### 6  2:30–3:10  付费烟雾测试和不完整答案

**画面**  点击`6. Optional OpenRouter run`，停在最新烟雾测试输出。

**必须显示**  `Status: answered`、`3,539` tokens、`0.00059745` cost和引用信息。

**English narration**

For the fresh paid check, the OpenRouter key was loaded from Colab Secrets and was never printed or stored in a code cell. The smoke test used GPT-4o mini, 3,539 tokens and 0.00059745 US dollars. The validator accepted the citation, but the answer only said that tracing is off by default. It did not explain how to enable tracing. This failure shows that a valid citation does not guarantee a complete answer.

**中文对照**

在最新的付费检查中，OpenRouter密钥只从Colab Secrets加载，没有被打印或保存在代码单元格中。烟雾测试使用GPT-4o mini，共3,539 tokens，费用为0.00059745美元。验证器接受了引用，但答案只说追踪功能默认关闭，没有说明怎样开启。这个失败说明引用有效不代表答案完整。

### 7  3:10–4:05  付费对比、成本和80%目标

**画面一**  向下滚到`FRESH PAID RUN - 28 September 2026`汇总。

**必须显示**  `24 calls`、`51,153 tokens`、`USD 0.00848985`、Hybrid `5/6`和`2/2`，以及总计`25 calls`、`54,692 tokens`、`USD 0.00908730`。

**English narration for screen one**

The development comparison made 24 additional calls with no API error. Hybrid RAG answered five of six supported cases and refused both unsupported cases. BM25 RAG answered four of six and also refused both unsupported cases. Including the smoke test, the fresh run made 25 calls, used 54,692 tokens and cost 0.00908730 US dollars.

**中文对照**

开发集对比另外进行了24次调用，没有API错误。Hybrid RAG回答了六个支持问题中的五个，并拒绝了两个不支持问题。BM25 RAG回答了六个中的四个，也拒绝了两个不支持问题。包括烟雾测试，本次复跑共25次调用、54,692 tokens，费用为0.00908730美元。

**画面二**  切回GitHub README，按`Ctrl + F`搜索`14/14`，停在冻结确认集说明。

**English narration for screen two**

The five-out-of-six figure is an automated status, not correctness. My AI-assisted reference check accepted four of six hybrid answers as complete, so the fresh run did not prove the 80 percent answer-quality target. In the frozen confirmation run, retrieval reached 14 out of 14 at Hit at five, but the original boundary logic refused only four of six unsupported cases, or 66.7 percent. That also missed the 80 percent safety target.

**中文对照**

五比六只是自动状态，不是正确率。AI辅助参考答案复核只认定六个Hybrid答案中的四个完整，因此本次复跑没有证明达到80%的答案质量目标。在冻结确认运行中，检索的Hit@5为14/14，但原始边界逻辑只拒绝了六个不支持问题中的四个，即66.7%，同样没有达到80%的安全目标。

### 8  4:05–4:40  风险和限制

**画面**  在README按`Ctrl + F`搜索`Limits`，停在限制段落。

**English narration**

The main risk is a fluent interpretation attached to real but incomplete evidence. Exact quotations and source checks reduce that risk, but an engineer still has to judge whether the evidence supports the whole answer. VerifyRAG cannot inspect a private DUT, run a simulator, cover every UVM release or approve sign-off. Private RTL and logs are outside the hosted-model scope.

**中文对照**

主要风险是模型可能把流畅解释附在真实但不完整的证据上。精确引用和来源检查可以降低风险，但工程师仍需判断证据是否支持完整答案。VerifyRAG不能检查私人DUT、运行仿真、覆盖所有UVM版本或批准签核。私人RTL和日志不属于托管模型的使用范围。

### 9  4:40–5:15  结论和AI使用说明

**画面**  打开`docs/AI_USE.md`，显示标题和9月28日运行说明；最后切回仓库顶部。

**操作**  说完`Thank you`后停两秒，再按`Win + Alt + R`停止。

**English narration**

In summary, VerifyRAG is an evidence navigator for one pinned UVM release. The public repository includes the code, corpus, tests, failed cases and evaluation records. I used generative AI during research, coding, test design and editing, and the assistance is documented here. I kept the failed and incomplete results and did not present automated checks as human-validated accuracy. Thank you.

**中文对照**

总结来说，VerifyRAG是面向一个固定UVM版本的证据导航工具。公开仓库包含代码、语料、测试、失败案例和评估记录。我在研究、编码、测试设计和编辑过程中使用了生成式AI，相关协助记录在这里。我保留了失败和不完整结果，也没有把自动检查描述成人工验证的正确率。谢谢。

## 录制后检查

1. 成片控制在5分10秒至5分40秒。
2. 开头10秒内出现姓名、课程和项目名。
3. 每个口播段落都能看到上面指定的对应画面。
4. 画面必须包含31项测试、两个拒答、检索表、烟雾测试和FRESH PAID RUN汇总。
5. 不要把Hit@5、5/6自动状态或引用验证说成答案正确率。
6. 视频中不得出现API key、Secrets侧栏、邮箱或聊天页面。
7. 导出1080p MP4，用无痕窗口检查上传后的链接。
8. 将最终视频URL填写到`04_GitHub_and_Video_Links.txt`。
