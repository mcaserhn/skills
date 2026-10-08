---
name: de-ai-flavor
description: Remove "AI flavor" (AI 味儿) from LLM outputs in both conversational replies and document generation, for Chinese AND English text. Covers word-level banned lists plus parallel Chinese and English discourse/syntax rules, per-language do-not-change protection lists, format / markup-artifact cleanup, a forensic scoring rubric (AI-check) with a protected-items audit, and a deterministic Python linter. Use when the user complains about AI-sounding text, wants human-like writing, asks to humanize / de-AI-flavored content, asks "does this sound AI?" or wants the text scored and linted.
description_zh: "去除 LLM 输出的 AI 味儿（中文+英文）：覆盖对话与文档生成，含中英双语禁词表、中文篇章/句法层规则（11 项）、英文篇章/句法层规则（10 项）、中英各自的反向保护清单、格式与残留标记清扫、常驻人设 system 片段、文档模板、保真护栏（白名单默认/实词溯源/情态条件保护）；并含取证打分（AI-check 十类信号 0–30 分，附保护项复核）与确定性 Python linter（规则编号直挂 02/05/07/09，只报不改，可进 CI）"
description_en: "Strip AI-sounding tone from LLM output in chat and documents, in Chinese and English, with bilingual banned-word lists, parallel Chinese and English discourse/syntax rules, per-language do-not-change lists, format and markup-artifact cleanup, persona system snippets, doc templates, whitelist-first fidelity guardrails, a forensic scoring rubric (AI-check, 10 signals / 30 points, with a protected-items audit), and a deterministic stdlib-only Python linter keyed to the skill's own rule IDs."
version: 1.6.2
status: stable
license: MIT
allowed-tools: Read,Write,Edit,Grep,Bash
display_name: "de-ai-flavor"
display_name_en: "de-ai-flavor"
visibility: "user"
---

# De-AI-Flavor（去 AI 味儿 · 中英双语）

支持 **中文** 与 **英文** 两种场景的去味。原理与管线一致；**词汇层、篇章层、反向清单按语言各自成文，不跨语言套用**（分派见「加载路由表」）。

## 何时使用

- 用户抱怨文本"有 AI 味儿""太机器""像 ChatGPT 写的" / "too robotic" / "sounds like AI"
- 需要"写得像人""humanize""去 AI 化"
- 配置一个不该像助手的对话人格（system prompt），中文或英文
- 生成复盘、方案、汇报、邮件等文档时想去掉套话
- 用户问"这段像 AI 写的吗 / 打个分 / 给我个取证分析" / "does this sound AI?" → 走**取证打分**（`references/10-ai-check-forensics.md`）
- 需要**可重复、可进 CI** 的机械检查 → 跑**确定性 linter**（`scripts/ai_pattern_lint.py`）

## 核心原理（统一，中英文通用）

AI 味儿不是语法错误，而是模型"最大化先验概率"下的**默认安全分布**——稳妥、平衡、不犯错的套话。去味的本质，是用约束把分布拉向**具体、有主见、有依据**的表达。

三件套：**约束（禁词 / 负面指令） + 素材（真实数据 / 引语 / 案例） + 具体性（每论点带数字或动作）**。

两类场景共用同一原理，差异只在**约束注入的位置**：

| 场景 | 注入方式 | 能否跑改写 pass |
|------|---------|----------------|
| 文档生成 | 一次性写进当次 prompt | 可以（独立改写轮） |
| 对话输出 | 常驻 system prompt（每轮会重置焦点） | 压缩为"输出前自查" |

## 加载路由表（先判语言，再按需加载）

**先判语言，再决定读哪些文件。** 中文专用与英文专用的规则**不交叉加载**——既省上下文，也避免误用。

| 文件 | 层 | 语言 | 何时读 |
|---|---|---|---|
| `references/01-fidelity-guardrails.md` | 保真护栏 | 共用 | **任何改写 / 去味 / 审稿前必读**；与禁词冲突时以它为准 |
| `references/02-banned-words-and-patterns.md` | 词汇层 | 中 / 英分表 | 语言判定后取对应表；含语言门控细则 |
| `references/05-zh-syntax-and-structure.md` | 篇章 / 句法（11 项） | **zh only** | 中文文本 |
| `references/06-do-not-change.md` | 反向保护（10 项） | **zh only** | 中文**改写前先读**——"绝不改什么"比"改什么"更该先看 |
| `references/07-en-syntax-and-structure.md` | 篇章 / 句法（10 项，按 HAP-E 倍数排序） | **en only** | 英文文本 |
| `references/08-en-do-not-change.md` | 反向保护（12 项） | **en only** | 英文**改写前先读** |
| `references/09-format-and-artifacts.md` | 格式 / 残留标记 | 共用 | **交付前必跑**（残留标记零假阳性） |
| `references/03-conversation-mode.md` | 对话常驻 | 共用 | 配置不该像助手的 system prompt |
| `references/04-doc-pipeline-and-faq.md` | 管线 / 参数 / 校验 / 版本 | 共用 | 生成文档、长文去味；需参数说明、校验方法、FAQ、证据源与版本沿革 |
| `references/10-ai-check-forensics.md` | 评估层（判断性） | 共用 | 用户问"像不像 AI / 打个分 / 取证分析" |
| `scripts/ai_pattern_lint.py` | 评估层（机械性） | 共用 | 要可重复、可进 CI 的检查；**改完复跑**验证 |
| `assets/persona-zh-system.md` / `assets/persona-en-system.md` / `assets/doc-template-zh.md` / `assets/doc-template-en.md` | 人设片段 + 文档模板 | zh / en | 人设可直接复制进 system prompt；模板用于文档定向阶段（完整 + 极简） |

四条纪律：

1. **检测输入语言** → 按上表分派。英文文本**不读** 05 / 06；中文文本**不读** 07 / 08。
2. **用户指定语言** → 按目标语言产出并分派，与素材语言无关。
3. **不逐字互译禁词** → 中文重抽象大词与客套，英文重 buzzword 与固定句式，各按各的清单。
4. **结论不跨语言** → 中英两侧证据**彼此独立，不得互推**：中文"篇章层独强、词汇层痕迹弱"，英文"词汇层与句法层同时很强"（词汇 100×+，句法 2–5×、d 最高 1.38）。故 05 与 07 **各自独立成立，不是互为译文**。

> **打分前先跑脚本**：`--show-protected` 拿到排除清单，再按 `references/10-ai-check-forensics.md` 写报告；报告里的 `保护项复核` 一节**必填**。

## 评估层：取证打分 + 确定性 linter（**只诊断，不改写**）

去味是"改"，评估是"判"。两者是**两条独立通道**——评估结论本身**不是**改写理由，只有落到 01/02/05/07/09 的具体条目上，改动才成立。

| 能力 | 性质 | 位置 | 什么时候用 |
|---|---|---|---|
| **取证打分**（AI-check） | 判断性 · 十类信号 / 30 分 | `references/10-ai-check-forensics.md` | 用户问"像不像 AI""打个分""取证分析"；交付前要可复核的诊断报告 |
| **确定性 linter** | 机械性 · 正则可判定子集 | `scripts/ai_pattern_lint.py` | 需要可重复、可进 CI 的检查；改完复跑验证 |

```bash
python3 scripts/ai_pattern_lint.py draft.md            # 人读报告，退出码 0/1
python3 scripts/ai_pattern_lint.py --json draft.md     # 机器可读
python3 scripts/ai_pattern_lint.py --list-rules        # 规则编号 → 本 skill 文件对照
```

常用选项：`--lang zh|en` 指定语言、`--threshold N` 改密度阈值、`--show-protected` 列永不报的排除清单。

三条硬规矩：

1. **规则编号直挂本 skill**：linter 的每条命中都标 `02-*` / `05-*` / `07-*` / `09-*`，**不引用任何外部检测器的私有编号**。命中即可回溯到具体文件具体条目。
2. **反向保护清单是硬排除**：`references/06-do-not-change.md` / `references/08-en-do-not-change.md` 里的项（被动语态、hedge、问句、比喻、单组三项、词汇多样性、简单 is/has、普通动词……）**永不判为命中**。通用 AI 检测器会把它们报成 AI 味——那是**本 skill 与它们的根本分歧**（详见 `references/10-ai-check-forensics.md` 第 1 节）。
3. **只报不改**：linter **不提供任何自动改写 / 同义词替换功能**。`references/02-banned-words-and-patterns.md` 明令禁止机械换词——把 `delve` 批量换成 `look into` 是制造新痕迹。

> **两者不一致时**：脚本命中但按报告判为保护项 → **以报告为准**；报告命中但脚本无输出 → 属判断性信号，须给原文片段作证。

## 保真护栏（精简版 · 优先于任何禁词）

去味是把表达变自然，**不是改变事实或作者意图**。冲突时保真优先。

1. **白名单默认（最高优先级）**：只改禁词表 / 改写规则**明确列出**的问题，**未命中者逐字保留**；命中者仅改解决该问题所必需的部分。对是否命中没把握 → **保持原文**。
2. **实词溯源**：改写后**每个实词都要能在原文指出出处**；指不出来即新增，**必须撤销**。不得新增原文没有的细节；不得删减限定词与让步（"可能 / 通常 / 在某些情况下 / 据说"）。
3. **情态 / 条件 / 承诺不可改写**："可能"≠"必然"；"可以"≠"会"；否定只排除一种原因，不能改肯定。
4. **抽象可保留**：原文只谈潜力 / 目标 / 作用时可仍抽象；不得为"更具体"补事实或把"有望改善"改成"已实现改善"。
5. **代码块逐字保留**：程序代码不进去味编辑（除非用户点名改注释文字）。
6. **来源不可删**：未指明来源的归属默认保留，必要时标注"缺来源"；不得只删归属让无源论断变裸事实。
7. **编辑幅度档位（可选覆盖）**：默认即白名单；`in-place` / `bounded` / `structural` **仅在用户显式指定**时启用。
8. **只标问题（审稿）**：用户要求时只引片段 + 说问题，不交替换全文、不评分。
9. **样本覆盖规则**：用户给了写作样本 / 风格文档时，**样本优先于本 skill 全部规则**（含禁词表与中文破折号条）。样本怎么用破折号，就按样本的密度用。

> **四条上下文级边界**（不算命中，逐字保留）：**标题**（含小标题、文件名、图表题）、**专有名词**本身（产品名 / 人名 / 机构名 / 标准号）、**元语言指称**（一段在**讨论**某个词而非**使用**它）、**引文与对话内部**。

## 输出前自查（中英通用）

给最终文本前自查一遍：

- 是否出现套话开场 / 收尾、助手腔客套、以确定语气说空话（"毋庸置疑""it is undeniable that"）？→ 有则重写。
- **中文**文本是否过了篇章层（段首零回指 / 冒号空转 / 拟人喻体 / 翻案腔 / 破折号 / 翻译腔等 11 项）？→ 未过则回看 `references/05-zh-syntax-and-structure.md`。
- **英文**文本是否过了篇章层（分词状语从句 / 名词化 / that 关系从句 / 回避系词 / 空转意义强调 / 否定平行 / 提纲式结尾 / 模糊归属 / 三段式密度等 10 项）？→ 未过则回看 `references/07-en-syntax-and-structure.md`。
- 是否误改了**对应语言的反向保护清单**里的项（中文：问句 / 比喻 / 句内排比 / 被动句 / 正文连接词；英文：简单 is-has / 普通动词 / 最高级 / hedge / 被动 / 脏话 / 词汇多样性）？→ 改了则**撤回**。
- **交付前是否扫过格式与残留标记**（`[cite: 1]` / `oai_citation` / `turn0search0` / 粗体滥用 / 标题层级 / 弯引号）？→ 未扫则补 `references/09-format-and-artifacts.md`。
- 若本次是在**改一篇已有文件**：改完是否复跑 `scripts/ai_pattern_lint.py`，确认密度下降且**未引入新命中**？→ 未跑则补跑。
- 朗读一遍：拗口、排比堆砌、一听像营销 / PR 文案的 → 重写。

**保真四查**（凡有改动就逐条过，全文即上一节）：逐字保留 / 实词溯源 / 不改事实·情态·条件 / 四条上下文级边界；外加禁**同义词机械替换**（`references/02-banned-words-and-patterns.md`）。任一不过即**撤回**。

## 来源与许可

- **独立实现**：未复制任何第三方源码；每条判据都挂本 skill 自己的文件与条目编号。**许可 MIT，作者 Stanley Hao。**
- **借鉴来源**（均 MIT，只借结构，未复制文字）：`shuorenhua`（保真护栏）、`lieflat-less-ai-tone`（中文篇章层与反向清单）、`harshaneel/humanize` 的 `ai-check` 与 `shir-danishyar/humanize` 的 linter（评估层骨架）、`blader/humanizer`（上下文级排除、样本优先）。**判据按本 skill 语料逐条重校，与来源并不一致**——外部判为 AI 信号的 hedge / 被动 / em dash / 词汇多样性，在本 skill 是受保护的人类特征。
- **证据基础**：英文侧依 Reinhart et al., PNAS 122(8) e2422455122 (2025)（HAP-E 平行语料，数据 `hf/3770` / `hf/3792`）+ **本地独立复算**（配对 n=8,290）；中文侧依 283 万字对照语料统计（**外部证据，未经独立复算**）；格式层依 *Wikipedia:Signs of AI writing*（社区共识）。分级 🟢 复算 / 官方 · 🟡 社区共识 · ⚪ 待验证。
- **已知局限与完整沿革**：HAP-E 六体裁**不含商务邮件 / IT 方案 / 汇报 / 幻灯片**，倍数只作方向性依据；linter 只覆盖机械可判定子集——详见 `references/10-ai-check-forensics.md` 第 7 / 8 节。证据源与逐版沿革见 `references/04-doc-pipeline-and-faq.md`。
