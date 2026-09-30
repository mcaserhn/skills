# 反向保护清单（英文 · 不作为改写理由）

> `de-ai-flavor` 按需参考（L3）。**何时加载：任何英文改写动作开始前先读本文件。**
> **性质**：以下特征**看着像 AI 味，实测站不住**，**不得据此改写**。本清单与改写规则同为**硬约束**，不是参考——它的作用是防止"越改越不像人"。
> **来源**：S1 = Reinhart et al., PNAS 122(8) e2422455122 (2025)（HAP-E 平行语料 33.5M 词）；S4 = Wikipedia:Signs of AI writing（WikiProject AI Cleanup）。
> **适用范围**：**仅英文**。第 1–5 条的观察基于维基百科语境（百科体、25 年编辑语料），**其他体裁未经同等验证**，作方向性提示而非铁律；第 6–7 条为跨体裁语料测量。本清单不与中文规则互推——中文侧见 `references/06-do-not-change.md`。

## 核心风险

执行者若按"AI 味 = 华丽、正式、无重复、无 hedge"的直觉去改，会把**人类的自然特征当成 AI 味删掉**——结果**比不改更不像人**。而且**两个方向都会翻车**：把 `used` 改成 `utilized` 是在**制造** AI 味。

## A. 人类更常用的写法（实测 · 不得删改）

| # | 特征 | 证据 |
|---|---|---|
| 1 | **简单的 is / has 短语**（`there is a`、`it has a`） | S4：人类 25 年编辑语料中更常见。**不要为"生动"把 `is` 换成 `serves as` / `represents`——后者才是 AI 特征，见 `references/07-en-syntax-and-structure.md` 第 5 条** |
| 2 | **普通动词而非"高级"同义词** | S4：`wrote`（≠ `authored`）、`moved`（≠ `relocated`）、`used`（≠ `utilized`）、`tried`（≠ `attempted`）、`died`（≠ `passed away`）均为人类更常用。**把 `used` 改成 `utilized` 是制造 AI 味** |
| 3 | **最高级与确定性陈述**（`one of the best`、`is the only`、`was the first`） | S4：人类更常用。不得因"太绝对"而软化——作者要下判断就让他下 |
| 4 | **Hedging qualifiers 与 intensifiers**（`very`、`perhaps`、`tends to`） | S4 明确引用 S1 的 HAP-E 结论：**人类更常用**。与 `references/02-banned-words-and-patterns.md` 把 hedge 降为"仅提示"同向，且是第二个独立来源 |
| 5 | **孤立的冗词结构**（`as a result of`、`in order to`、`all of the`、`a part of`、`the fact that`） | S4：列为人类更常见。⚠️ **百科体观察，其他体裁未验证**——不要主动扩用 |
| 6 | **无施事被动语态**（`it is believed that`、`was determined by`） | S1（HAP-E）：AI ≈0.5×，**人类多用 2 倍**。2026-09-30 从 `references/02-banned-words-and-patterns.md` 五组特征表摘出移入 |
| 7 | **脏话与粗俗语** | S1（HAP-E）：AI 使用比人类低 **100 倍以上**。不要"净化"原文的粗俗表达 |

## B. 非 AI 信号（维基专门列为无效，含子节 `WP:AIELEVAR`）

| # | 特征 | 说明 |
|---|---|---|
| 8 | **词汇多样性 / elegant variation** | S4 列为**非** AI 信号（老模型带 repetition penalty 才会换词）。原文另注：非英语母语者（如意大利语教学）也习惯避免重复词。**且与 `references/02-banned-words-and-patterns.md` "禁同义词机械替换"同向** |
| 9 | **语感类的"像 AI"印象** | S4 的 Ineffective indicators 一节明确列出三项无效指标：**完美语法**（专业写作者亦然）、**"bland / robotic" 的语感**、**"fancy / academic / formal" 的语感**。原文特别澄清：AI 偏好的是**一批特定词**，这个相关性**不延伸到所有正式文风** |

## C. 无效判据（不得单独作为改写依据）

| # | 特征 | 说明 |
|---|---|---|
| 10 | **孤立出现的转折词**（`Additionally` / `Consequently` / `Notably`） | S4：只有**少数**几个转折词被证实被 AI 过用，且人类议论文同样这么写、许多体例指南也接受。**判据是密度，不是出现**——与 `references/02-banned-words-and-patterns.md` "rewrite on density" 一致 |
| 11 | **无来源陈述** | S4：57 万+ 维基条目待补引用，且大多数**早于 LLM**。反过来说，现代 AI 常带引用（未必准确）。出处问题走 `references/01-fidelity-guardrails.md` 第 6 条，不属去味 |

## D. 唯一需要看上下文的一条

**12. 弯引号 / 直引号。**

ChatGPT（2025 年中起）与 DeepSeek 倾向使用弯引号（`"…"` `'…'`）与弯撇号（`'`）；**Gemini 与 Claude 通常不用**。

但**弯引号本身不能证明 LLM 使用**，因为它有太多非 AI 来源：Microsoft Word 的 smart quotes 自动转换、macOS / iOS 的系统默认、LanguageTool 一类语法工具、Chicago 体例的出版作品、引用工具复制网页标题中的弯引号。

- **不得机械替换**（会把正规排版产物改坏）。
- 只有**同一文档内混用弯直引号**（且非用户自己输入习惯）才算弱信号。

## 使用纪律

- **风格文档优先**：若目标风格文档（写作风格指南、`language-DNA.md` 一类）与本清单冲突，以风格文档为准。
- **判据是可定位的触发标记 + 密度，不是频率印象**：不要按"某个模型的味"去套判断；同一特征在不同模型量级差异极大（HAP-E 实测 downtoner 方向随模型反转）。
- **体裁服从**：学术、新闻、公文不必强加口语；对话体、文学体裁按原有风格，不统一改写。
- **不在范围内**：文章框架（标题层级 / 章节顺序 / 段落顺序 / 列表 / 表格 / 引用 / 代码块位置）；代码块与外语段落；引文；对话与引语内部。
- **附：格式与残留标记不属本清单**——那些（裸露 markup、emoji 当格式符、粗体滥用、破折号过密、标题式大写、弯引号清扫等）是**真信号**，走 `references/09-format-and-artifacts.md`。本清单只保护**语言层**的人类特征。

> 与 `references/07-en-syntax-and-structure.md` 的关系：**07 说"改什么"，本文件说"什么绝不改"。** 两者冲突时——例如 07 第 5 条可能诱使你改掉一个正常的 `is`——**以本文件为准**（保留）。

---
**执行要点**
- **触发**：任何英文改写 / 去味动作开始前。
- **必须动作**：对已列入本清单的 12 项，**逐字保留**；有风格文档时先读并以其为准；第 12 条须先判断生成渠道。
- **禁止**：以"太简单 / 太正式 / 有重复 / 有 hedge / 有被动 / 有最高级"为由删改；把 `used` 一类普通动词"升级"为 `utilized` 一类；用本清单的推论改写中文文本。
- **停止条件**：确认本次改动**未触及**本清单任一项，方可输出。
