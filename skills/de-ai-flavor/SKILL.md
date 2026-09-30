---
name: de-ai-flavor
description: Remove "AI flavor" (AI 味儿) from LLM outputs in both conversational replies and document generation, for Chinese AND English text. Covers word-level banned lists plus Chinese discourse/syntax rules and a do-not-change protection list. Use when the user complains about AI-sounding text, wants human-like writing, or asks to humanize / de-AI-flavored content in either language.
description_zh: "去除 LLM 输出的 AI 味儿（中文+英文）：覆盖对话与文档生成，含中英双语禁词表、中文篇章/句法层规则（11 项）、反向保护清单、常驻人设 system 片段、文档模板、保真护栏（白名单默认/实词溯源/情态条件保护）"
description_en: "Strip AI-sounding tone from LLM output in chat and documents, in Chinese and English, with bilingual banned-word lists, Chinese discourse/syntax rules, a do-not-change list, persona system snippets, doc templates, and whitelist-first fidelity guardrails with word-level provenance."
version: 1.4.0
status: stable
license: MIT
allowed-tools: Read,Write,Edit,Grep
display_name: "de-ai-flavor"
display_name_en: "de-ai-flavor"
visibility: "user"
---

# De-AI-Flavor（去 AI 味儿 · 中英双语）

支持 **中文** 与 **英文** 两种场景的去味。原理、管线完全一致，差异仅在禁词表与模板语言。

## 何时使用

- 用户抱怨文本"有 AI 味儿""太机器""像 ChatGPT 写的" / "too robotic" / "sounds like AI"
- 需要"写得像人""humanize""去 AI 化"
- 配置一个不该像助手的对话人格（system prompt），中文或英文
- 生成复盘、方案、汇报、邮件等文档时想去掉套话

## 核心原理（统一，中英文通用）

AI 味儿不是语法错误，而是模型在"最大化先验概率"下输出的**默认安全分布** —— 稳妥、平衡、不犯错的套话。去掉它的本质，是用约束把分布拉向**具体、有主见、有依据**的表达。

三件套：**约束（禁词 / 负面指令） + 素材（真实数据 / 引语 / 案例） + 具体性（每论点带数字或动作）**。

两类场景共用同一原理，差异只在**约束注入的位置**：

| 场景 | 注入方式 | 能否跑改写 pass |
|------|---------|----------------|
| 文档生成 | 一次性写进当次 prompt | 可以（独立改写轮） |
| 对话输出 | 常驻 system prompt（每轮会重置焦点） | 压缩为"输出前自查" |

## 两个层次（都要过，互补不替代）

| 层次 | 覆盖 | 文件 | 证据等级 |
|---|---|---|---|
| **词汇层** | 套话、确定语气空转词、抽象大词、助手腔（中英） | `references/02-banned-words-and-patterns.md` | 中文 🟡 经验共识 / 英文 ⚪ 待验证 |
| **篇章 / 句法层** | 段首回指、冒号空转、拟人喻体、翻案腔、破折号、翻译腔等 11 项（**仅中文**） | `references/05-zh-syntax-and-structure.md` | 🟢 语料验证（待独立验证） |

> **关键结论**：区分力最强的特征**集中在篇章 / 结构层，而非词汇层**。词汇层痕迹多半能被模型自身直觉处理，篇章层才是真盲区。另有一张**反向保护清单**（看着像 AI 味、实测站不住、**不得改写**）见 `references/06-do-not-change.md`。

## 语言处理（关键）

1. **检测输入语言** → 中文走中文禁词表 + 篇章层规则 + 中文模板；英文走英文禁词表 + 英文模板。
2. **中英夹杂** → 两套禁词表同时生效，各自保持自然语域，不要机器直译。
3. **用户指定语言** → 按目标语言产出，套用对应禁词表。
4. **不要逐字互译禁词** → 中文重抽象大词与客套，英文重 buzzword 与 hedge filler，各按各的清单。
5. **篇章层规则不跨语言** → `references/05-zh-syntax-and-structure.md` 是中文语料结论，**不得**据它改英文文本。

细则见 `references/02-banned-words-and-patterns.md`。

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

完整规则、清单与档位表见 `references/01-fidelity-guardrails.md`。

## 路由表（按需加载）

| 需要做什么 | 读取文件 |
|---|---|
| 完整保真规则 / 白名单默认 / 实词溯源 / 编辑幅度档位 / 审稿模式 | `references/01-fidelity-guardrails.md` |
| 中英禁词表 / 五组 AI 味儿特征对照 / 语言处理细则 | `references/02-banned-words-and-patterns.md` |
| **中文篇章 / 句法层规则（11 项，含触发标记与改法）** | `references/05-zh-syntax-and-structure.md` |
| **反向保护清单（看着像 AI 味、实测站不住，不得改写）** | `references/06-do-not-change.md` |
| 配置对话常驻人格（原理 + 技巧） | `references/03-conversation-mode.md` |
| 文档四阶段管线 / 可调参数 / 校验 / 常见误区 / 版本 | `references/04-doc-pipeline-and-faq.md` |
| 中文常驻人格（可直接复制） | `assets/persona-zh-system.md` |
| English persona（copy-paste） | `assets/persona-en-system.md` |
| 中文文档模板（完整 + 极简） | `assets/doc-template-zh.md` |
| English doc template（full + minimal） | `assets/doc-template-en.md` |

> 改写**中文**文本时，**先读 `references/06-do-not-change.md`（什么绝不改）**，再用 `references/02-banned-words-and-patterns.md` + `references/05-zh-syntax-and-structure.md`（改什么）逐项检查。

## 输出前自查（中英通用）

在给出最终文本前自查一遍：

- 是否出现套话开场 / 收尾、助手腔客套、确定语气空转词？→ 有则重写。
- 中文文本是否过了**篇章层**（段首零回指 / 冒号空转 / 拟人喻体 / 翻案腔 / 破折号 / 翻译腔等）？→ 未过则回看 `references/05-zh-syntax-and-structure.md`。
- 是否误改了**反向保护清单**里的项（问句 / 比喻 / 句内排比 / 被动句 / 正文连接词）？→ 改了则**撤回**。
- 每处改动是否都能**指向具体规则**？未命中规则的句子是否**逐字保留**？→ 否则撤回该改动。
- 改写后**每个实词能否在原文指出出处**？→ 指不出来的新增**必须撤销**。
- 去味后是否改变了事实、情态、条件、归属、数字、完成状态？→ 改了则撤回该改动。
- 朗读一遍：拗口、排比堆砌、一听像营销 / PR 文案的 → 重写。

## 来源与许可

- 本 skill 为独立实现，未复制第三方源码。v1.2.0「保真护栏」的编辑哲学借鉴自开源项目 **shuorenhua（说人话，MIT License）**；v1.4.0 新增的**中文篇章 / 句法层规则**与**反向保护清单**改写自开源项目 **`lieflat-less-ai-tone`（MIT License）**，其规则基于 283 万字对照语料统计（**证据等级：高质量外部证据 · 待独立验证**）。评测数据以原作者自述为准。
- 许可证：MIT。作者 Stanley Hao。
