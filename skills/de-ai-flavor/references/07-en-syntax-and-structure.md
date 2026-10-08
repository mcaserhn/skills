# 篇章与句法层规则（英文）

> `de-ai-flavor` 按需参考（L3）。何时加载：对**英文**文本做去味时，在词汇层禁词表（`references/02-banned-words-and-patterns.md`）之外，按本清单逐项检查句法 / 篇章痕迹。
> **适用范围（重要）**：本清单来自**英文对照语料与英文社区样本**，仅适用于英文文本。**不得顺推至中文**——中文侧见 `references/05-zh-syntax-and-structure.md`，其结论同样不得推回本清单。两侧是各自独立成立的证据，不是互为译文。
> **来源**：S1 = Reinhart et al., *Do LLMs write like humans? Variation in grammatical and rhetorical styles*, PNAS 122(8) e2422455122 (2025)；arXiv:2410.16107（HAP-E 平行语料 33.5M 词 / 6 体裁 / 8 来源，Biber 67 特征逐项检验）。**S1′ = 本地独立复算**（2026-09-30，取用 S1 公开的 Biber 特征计数 `hf/3792`，人类基准 = chunk-2，配对 n=8,290，6 模型 × 6 体裁；五个关键倍数复现误差 <1%）。S4 = Wikipedia:Signs of AI writing（WikiProject AI Cleanup，社区共识）。S1 的全文本、特征、解析与复现代码公开（`hf/3770`、`hf/3792`、`hf/3793`、`OSF 7MRQN`）。
> **证据等级**：第 1–4 条 🟢 同行评审（倍数为 **GPT-4o**，已本地复算）；第 5 条 🟢（S1′ 复算：`be` 作主动词 0.63× / d=−0.83）；第 6 条 🟢（Kobak 互证）；第 7–10 条 🟡 社区共识。
> **特征口径（2026-09-30 核对）**：本文件的倍数对应 Biber 特征编号（`f_14` / `f_25` / `f_29` / `f_64` 等），定义以 S1 作者开源的 **`pseudobibeR`**（R 包，MIT，CRAN；S1 数据页确认即此包所算）为准，已**逐条比对源码**而非注释。核出一处结构错配：第 3 条原写「名词性 `That … is …` 从句作主句主语」，而 `f_29` 实为 **that 关系从句**（`the dog [that bit me]`），已更正。本地以 Python + spaCy 复刻该口径，并在 HAP-E 全文（人类 chunk-2 vs gpt-4o，n=960）上与官方 Biber 计数**逐文档比对**：六项句法特征 r = 0.975–0.997，比值几乎重合（`f_25` 5.09 vs 官方 5.08）——口径等价，可供我们自己的语料使用。
> **倍数怎么用（重要）**：下表倍数是 **GPT-4o 单点值**，跨 6 模型差异极大（例：现在分词从句 0.94–5.27）。**只作方向性依据，不是阈值**——判据始终是触发标记 + 密度。
> **配套**：反向保护清单（看着像 AI 味、实测站不住、**不得据此改写**）见 `references/08-en-do-not-change.md`——**先读它**。

## 核心判断

**与中文侧不同：英文的区分力在词汇层和句法层同时很强。**

| | 中文（`references/05-zh-syntax-and-structure.md`） | 英文（本文件） |
|---|---|---|
| 词汇层 | 痕迹**弱**——区分力集中在篇章层 | 痕迹**强**——倍数达 100×+（camaraderie 162×、tapestry 155×） |
| 句法 / 篇章层 | **强**（R = 1.8–9.4） | **强**（GPT-4o 2–5×，d 最高 1.38；跨 6 模型 0.94–5.27） |

所以中文"篇章层独强、词汇层不必重看"的结论**不能套用到英文**——英文两层都要过。

另一条与中文同向的结论：差异**来自指令微调，不来自训练语料**。

本地复算（67 特征平均偏离 |log₂ R|）：基座 llama-3-8B **0.294** / 70B **0.254**，指令版 8B **0.501** / 70B **0.458**，gpt-4o **0.711** 最高。**instruct / base = 1.71×（8B）、1.80×（70B）**，且 70B 并不比 8B 更接近人类。**基础模型最接近人类**。

以现在分词的梯度可直接看出（基座 → 指令 → 对齐）：

```
llama-3-8B (base)     0.94×  ← 等于人类
llama-3-70B (base)    1.02×  ← 等于人类
llama-3-8B-Instruct   2.24×
llama-3-70B-Instruct  2.61×
gpt-4o-mini           4.81×
gpt-4o                5.27×
```

这解释了为什么"换个大模型"解决不了 AI 味——问题出在对齐之后，不出在规模。

## 改写规则（按证据强度排序）

倍数与 d 值来自 S1（并经 S1′ 本地复算校验），均为 **GPT-4o vs 人类的比值**。**这些数字只作方向性依据，不是判据阈值**——判据始终是下面的**触发标记 + 密度**。跨模型差异见文件头的「倍数怎么用」。

### 1. 现在分词状语从句（5.3× / d=1.38）🟢

挂一个 `-ing` 短语给句子加一层"意义升华"，删掉后信息不减。英文侧证据最强的一项，也最容易被忽略——它读起来很顺。

**位置**：S4 明确指出最常见的位置是**句尾**（"attaching a present participle ('-ing') phrase at the end of sentences"，并引 S1 为据）。Biber 特征 `f_25` 的机器判据是**紧随标点之后的 `VBG` 状语 / 补语从句**（`advcl` / `ccomp`）——该判据同时涵盖句首（`[Stuffing his mouth with cookies], Joe ran out.`）与句中，因此**不要只查句尾**。

- **触发标记**：`highlighting / underscoring / emphasizing / reflecting / demonstrating / showcasing / ensuring / allowing for / paving the way for` + 名词短语，位于句尾（最常见）、句首或句中，且删掉后句子信息不减。
- **改法**：删掉该短语。若它确实带了信息，改成独立句子并把内容说具体（不得新增原文没有的信息）。
- **不改**：分词短语确实承担信息（交代结果、原因、方式）时；技术文档里描述伴随动作的常规写法。
- ❌ The update ships next week, highlighting our commitment to reliability.
  ✅ The update ships next week.
- ❌ Highlighting our commitment to reliability, the update ships next week.
  ✅ The update ships next week.
- ❌ The pilot cut handling time by half, underscoring the value of automation.
  ✅ The pilot cut handling time by half.

### 2. 名词化堆叠（2.1× / d=1.23）🟢

把动作写成抽象名词，动词被挤掉。单看一句不算问题，成段出现就是机器骨架。

- **触发标记**：`the implementation of` / `the utilization of` / `the optimization of` / `the facilitation of` / `the enhancement of` + 名词；或一句里出现两个以上 `-tion / -ment / -ness / -ity` 抽象名词。`f_14` 的机器判据即后缀 `-tion(s) / -ment(s) / -ness(es) / -ity|ities` 加词性 `NOUN`，另有停用词表排除。
- **改法**：恢复动词。`the implementation of the policy` → `implementing the policy`。
- **不改**：该名词是领域术语且无自然动词形式（`authentication`、`compliance`）；标题、字段名、代码标识符。
- ❌ The optimization of the deployment process resulted in the reduction of downtime.
  ✅ We optimized the deployment process, and downtime dropped.

### 3. that 关系从句作从句主语（2.6× / d=0.77）🟢

名词短语后面挂 `that` 引导的关系从句，`that` 在从句里作主语，把主语拉长、真正的谓语被推后——信息挤进名词短语的一种表现。

**先分清结构**：Biber 特征 `f_29` 的定义是 **that 关系从句**（`the dog [that bit me]`：`that` 前接名词性词、`that` 自身充当 `nsubj`）。它**不是** `That … is …` 那种名词性从句作主句主语——后者的 `that` 是 `mark`，不计入本特征。别把两者混为一谈；`It is important that…` 之类属词汇层空话，走 `references/02-banned-words-and-patterns.md`。

- **触发标记**：`the X that [动词] …` 结构密集出现，尤其当**句子主语被关系从句拉长、谓语被推后**（`The change that reduced the error rate most was …`）。
- **改法**：把关系从句拆成独立句，或把从句内容提到主位。`The change that reduced the error rate most was the retry cap` → `The retry cap reduced the error rate most`。
- **不改**：关系从句是不可省的限定，用来区分多个对象（`the clause that applies to EU customers`）；定义、法条、字段名。
- ❌ The change that reduced the error rate most was the retry cap.
  ✅ The retry cap reduced the error rate most.

### 4. 短语并列（1.9× / d=0.81）🟢

同类短语成对并置（`f_64` 判据：名词、形容词、动词、副词四类中任一类以 `and` 相连），两侧信息往往重叠，实际只占一格的量。

- **触发标记**：`both X and Y` / `X and Y` 式同义堆叠（`thorough, detailed, and comprehensive`）在全文多次出现。
- **改法**：删掉**无信息**的那一侧，保留信息量最大的一项。不得为"读起来更完整"补新词。
- **不改**：两侧都承担不同信息且不可省（`read and write access`）；法律、财务、配置项等必须完整列出的场合。
- ❌ The report is thorough, detailed, and comprehensive.
  ✅ The report is detailed.

### 5. 回避系词（0.63× / d=−0.83）🟢

用 `serves as / stands as / marks / functions as / constitutes` 代替 `is / are`，把简单判断说成"具有某种地位"。

**HAP-E 复算（S1 + S1′）**：`be` 作主动词（`f_19`）GPT-4o 仅为人类的 **0.63×**（d=−0.83，本清单最强效应之一）——AI 少用约 37% 的简单 `is / are`。S4 的人类特征节独立佐证同一方向：人类 25 年编辑语料中 `there is a` / `it has a` 这类**简单系词短语**的出现频率高于 AI 文本。即 AI 回避的是系词本身，不只是这几个替身词。

- **触发标记**：`serves as a` / `stands as a` / `marks a` / `constitutes a` + 名词，而换成 `is a` 意思完全不变。
- **改法**：换回 `is / are`，或直接写它做了什么。
- **不改**：`represent` 确指法律或代理意义上的"代表"；`function as` 确指"充当某功能"且有对照物时。**且不得反向**：不要为"更生动 / 更简练"把正常的 `is` / `has` 升级成 `serves as` / `represents` / `constitutes`——`references/08-en-do-not-change.md` 第 1 条：简单系词是**人类更常用**，把它换掉是在**制造** AI 味。
- ❌ The dashboard serves as the central hub for all metrics.
  ✅ The dashboard holds all metrics.

### 6. 空转意义强调（🟡 维基 ＋ 🟢 Kobak）🟢

一整句在强调"这件事很重要"，却不说重要在哪。

- **触发标记**：`is a testament to` / `underscores the importance of` / `reflects a broader` / `in an evolving landscape` / `marks a key turning point` / `leaves an indelible mark` / `speaks to the`。
- **改法**：删整句；若后文确接了具体事实，只删强调壳、保留事实。
- **不改**：后面确实跟着具体结论或数据时——那是正常过渡，只处理空转的那半句。
- ❌ The migration succeeded, underscoring the importance of early planning.
  ✅ The migration succeeded.

### 7. 否定平行（🟡 维基）

`not just X but also Y` / `not X but Y` / `Y rather than X`——先立一个读者并没有的误解，再推翻它。与中文 `references/05-zh-syntax-and-structure.md` 第 1 条「翻案腔」同构，但**在英文侧是独立证据**，不是中文规则的翻译。

- **触发标记**：全文出现 ≥2 次，或作为段首句 / 结尾句出现。清单只是举例，同一动作换任何字面都要处理。
- **改法**：直接从正面下判断——先给判断，再给依据。
- **不改**：单次出现且确在区分两个真实选项（`read-only rather than read-write`）；技术对照说明。
- ❌ This isn't just a migration, it's a rethink of the architecture.
  ✅ The migration also changes the architecture.

### 8. 提纲式结尾（🟡 维基）

末尾以空转段收尾，宣布"挑战仍在，前路可期"，或列出 `Challenges and Legacy` 一类只有标题没有内容的章节。

- **触发标记**：`Despite these challenges…` / `Challenges and Legacy` / `Future Outlook` / `Conclusion` 类小标题或空转收尾段。
- **改法**：删掉空转段。若原文确有下一步计划，保留该段并把已写出的内容写具体（**不得新增原文没有的计划、日期、负责人**）。
- **不改**：正式报告体例确有「结论 / 下一步」章节，且其中写了具体内容。
- ❌ Despite these challenges, the path forward is promising.
  ✅ （删掉；若原文已写了具体计划，直接写那项计划）

### 9. 模糊归属（🟡 维基）

`experts argue` / `industry reports suggest` / `observers have noted` / `studies show`——不指明是谁。

- **触发标记**：无来源的群体归属，且全文无脚注、链接或具名机构。
- **改法**：按保真护栏处理（`references/01-fidelity-guardrails.md` 第 6 条）——**保留归属与论断**，必要时在正文外标注"缺来源"；**不得只删归属让无源论断变成裸事实**。
- **不改**：原文给了来源、链接或具名机构时。
- ❌ Industry reports suggest adoption is accelerating.
  ✅ Industry reports suggest adoption is accelerating.（保留，标注"缺来源"，待作者补充）

### 10. 三段式密度（🟡 维基）

不是"看到三就改"。单组三项并列是正常修辞，维基实证有人把它当铁律，结果把人类特征删掉了。

- **触发标记**：**几乎每段**都出现三组并列；或 `First… Second… Finally` 作为通篇小标题骨架。
- **改法**：能概括就别逐项列；必须保留三项以上时，**改变其中一项的句法**，不让它们排成同一结构。不得删除必要项。
- **不改**：单组三项（不是判据）；材料本身必须完整列出（法规、配置项、财务科目）；编号承担指代（"see item 3"）。
- ❌ `## First, find where the ambiguity lives` / `## Second, write the requirement as six modules`
  ✅ `## Find where the ambiguity lives` / `## Write the requirement as six modules`

## 验收（改写后逐项复查）

- 每一处改动都能明确对应**本文件某条编号规则**或 `references/02-banned-words-and-patterns.md` 禁词表；指不出对应规则的改动**必须撤销**。
- 改动**未落在** `references/01-fidelity-guardrails.md` 第 1.1 节的四类上下文边界上（标题 / 专有名词本身 / 元语言指称 / 引文与对话内部）。
- 所有**未命中规则的句子逐字保留**；未顺便润色相邻文字。
- **没有**用同义词机械替换命中项（维基实证：把 `delve` 批量换成 `look into` 反而制造新痕迹）。
- **没有**按中文清单改英文，也没有按本文件的倍数去改中文。
- 改写后**每个实词都能在原文指出出处**；姓名、数字、日期、引语、来源、因果，任一指不出出处者**必须撤销**。
- 原文标题层级、章节顺序、段落数量与顺序、列表 / 表格 / 引用 / 代码块位置**完全保留**。
- 交付前另跑一遍 `references/09-format-and-artifacts.md`（格式与残留标记清扫，中英共用）。

---
**执行要点**
- **触发**：对英文文本做去味 / 改写时（词汇层之外的结构层检查）。
- **必须动作**：按倍数由高到低逐项检查；命中即按"改法"处理，改动限于解决命中问题的最小范围；先读 `references/08-en-do-not-change.md` 排除保护项。
- **禁止**：改动未命中规则的文字；动文章框架；用同义词替换命中项；把中文规则翻译过来套用；把本文件的倍数当作其他体裁（商务邮件 / IT 方案 / 汇报 / 幻灯片）的判据阈值；改标题 / 专有名词本身 / 引文，或一段在**讨论**某词而非**使用**某词的文字（见 `references/01-fidelity-guardrails.md` 第 1.1 节）。
- **停止条件**：全部未命中规则的句子逐字保留、每处改动可指向具体规则、实词可溯源——三条同时满足方可输出。
