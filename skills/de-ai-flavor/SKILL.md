---
name: de-ai-flavor
description: Remove "AI flavor" (AI 味儿) from LLM outputs in both conversational replies and document generation, for Chinese AND English text. Covers word-level banned lists plus parallel Chinese and English discourse/syntax rules, per-language do-not-change protection lists, and format / markup-artifact cleanup. Use when the user complains about AI-sounding text, wants human-like writing, or asks to humanize / de-AI-flavored content in either language.
description_zh: "去除 LLM 输出的 AI 味儿（中文+英文）：覆盖对话与文档生成，含中英双语禁词表、中文篇章/句法层规则（11 项）、英文篇章/句法层规则（10 项）、中英各自的反向保护清单、格式与残留标记清扫、常驻人设 system 片段、文档模板、保真护栏（白名单默认/实词溯源/情态条件保护）"
description_en: "Strip AI-sounding tone from LLM output in chat and documents, in Chinese and English, with bilingual banned-word lists, parallel Chinese and English discourse/syntax rules, per-language do-not-change lists, format and markup-artifact cleanup, persona system snippets, doc templates, and whitelist-first fidelity guardrails."
version: 1.5.0
status: stable
license: MIT
allowed-tools: Read,Write,Edit,Grep
display_name: "de-ai-flavor"
display_name_en: "de-ai-flavor"
visibility: "user"
---

# De-AI-Flavor（去 AI 味儿 · 中英双语）

支持 **中文** 与 **英文** 两种场景的去味。原理与管线一致；**词汇层、篇章层、反向清单按语言各自成文，不跨语言套用**（分派见「语言门控」）。

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

## 三个层次（中英各自都要过，互补不替代）

| 层次 | 覆盖 | 文件 | 证据等级 |
|---|---|---|---|
| **词汇层** | 套话、确定语气空转词、抽象大词、助手腔（中英） | `references/02-banned-words-and-patterns.md` | 中文 🟡 经验共识 / 英文 ⚪ 待验证 |
| **篇章 / 句法层（中文）** | 段首回指、冒号空转、拟人喻体、翻案腔等 11 项 | `references/05-zh-syntax-and-structure.md` | 🟢 语料验证（待独立验证） |
| **篇章 / 句法层（英文）** | 句尾分词、名词化、回避系词、否定平行等 10 项 | `references/07-en-syntax-and-structure.md` | 🟢 同行评审 + 🟡 社区共识 |
| **格式 / 残留标记层** | 机器残留标记、粗体滥用、标题层级、弯引号等 | `references/09-format-and-artifacts.md` | 🟢 残留标记零假阳性 |

> **两侧结论不同，不可互推**：中文是"**篇章层独强、词汇层痕迹弱**"；英文是"**词汇层与句法层同时很强**"（词汇倍数达 100×+，句法 2–5× 且效应量大，d 最高 1.38）。所以两套篇章层文件**各自独立成立**，不是互为译文——英文文本不得套中文清单，反之亦然。
>
> 另有**反向保护清单**（看着像 AI 味、实测站不住、**不得改写**）：中文见 `references/06-do-not-change.md`，英文见 `references/08-en-do-not-change.md`——**改写前先读对应语言那一份**。

## 语言门控（按语言分派加载）

**先判语言，再决定读哪些文件。** 中文专用与英文专用的规则不交叉加载——既省上下文，也避免误用。

| 输入语言 | 词汇层 | 篇章 / 句法层 | 反向清单 | 格式层 |
|---|---|---|---|---|
| **中文** | `references/02-banned-words-and-patterns.md` 中文表 | `references/05-zh-syntax-and-structure.md` | `references/06-do-not-change.md` | `references/09-format-and-artifacts.md` |
| **英文** | `references/02-banned-words-and-patterns.md` 英文表 | `references/07-en-syntax-and-structure.md` | `references/08-en-do-not-change.md` | `references/09-format-and-artifacts.md` |
| **中英混排** | 两表同时生效 | 05 + 07 **都读** | 06 + 08 **都读** | 09（共用） |

1. **检测输入语言** → 按上表分派。英文文本**不要**读 05 / 06；中文文本**不要**读 07 / 08。
2. **用户指定语言** → 按目标语言产出并分派，与素材语言无关。
3. **不要逐字互译禁词** → 中文重抽象大词与客套，英文重 buzzword 与固定句式，各按各的清单。
4. **结论不跨语言** → 05 是中文语料结论、07 是英文语料结论，**互为独立证据，不得互推**。中文"词汇层不重要"不得套到英文；英文"被动语态是正常写法"也不得套到中文（中文侧另有独立判断）。

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

| 需要做什么 | 读取文件 | 语言 |
|---|---|---|
| 完整保真规则 / 白名单默认 / 实词溯源 / 编辑幅度档位 / 审稿模式 | `references/01-fidelity-guardrails.md` | 共用 |
| 中英禁词表 / 五组 AI 味儿特征对照 / 语言门控细则 | `references/02-banned-words-and-patterns.md` | 共用 |
| 配置对话常驻人格（原理 + 技巧） | `references/03-conversation-mode.md` | 共用 |
| 文档四阶段管线 / 可调参数 / 校验 / 常见误区 / 版本 | `references/04-doc-pipeline-and-faq.md` | 共用 |
| **格式与残留标记清扫（交付前必跑）** | `references/09-format-and-artifacts.md` | 共用 |
| **中文篇章 / 句法层规则（11 项，含触发标记与改法）** | `references/05-zh-syntax-and-structure.md` | **zh only** |
| **中文反向保护清单（看着像 AI 味、实测站不住，不得改写）** | `references/06-do-not-change.md` | **zh only** |
| **英文篇章 / 句法层规则（10 项，按 HAP-E 倍数排序）** | `references/07-en-syntax-and-structure.md` | **en only** |
| **英文反向保护清单（不得改写）** | `references/08-en-do-not-change.md` | **en only** |
| 中文常驻人格（可直接复制） | `assets/persona-zh-system.md` | zh |
| English persona（copy-paste） | `assets/persona-en-system.md` | en |
| 中文文档模板（完整 + 极简） | `assets/doc-template-zh.md` | zh |
| English doc template（full + minimal） | `assets/doc-template-en.md` | en |

> **改写前先读反向清单**：中文 → `references/06-do-not-change.md`；英文 → `references/08-en-do-not-change.md`。它们说"什么绝不改"，比"改什么"更该先看。
>
> **交付前跑格式清扫**：`references/09-format-and-artifacts.md`（中英共用，机器残留标记零假阳性）。

## 输出前自查（中英通用）

在给出最终文本前自查一遍：

- 是否出现套话开场 / 收尾、助手腔客套、确定语气空转词？→ 有则重写。
- **中文**文本是否过了篇章层（段首零回指 / 冒号空转 / 拟人喻体 / 翻案腔 / 破折号 / 翻译腔等 11 项）？→ 未过则回看 `references/05-zh-syntax-and-structure.md`。
- **英文**文本是否过了篇章层（句尾分词 / 名词化 / 回避系词 / 空转意义强调 / 否定平行 / 提纲式结尾 / 模糊归属 / 三段式密度等 10 项）？→ 未过则回看 `references/07-en-syntax-and-structure.md`。
- 是否误改了**对应语言的反向保护清单**里的项（中文：问句 / 比喻 / 句内排比 / 被动句 / 正文连接词；英文：简单 is-has / 普通动词 / 最高级 / hedge / 被动 / 脏话 / 词汇多样性）？→ 改了则**撤回**。
- **交付前是否扫过格式与残留标记**（`[cite: 1]` / `oai_citation` / `turn0search0` / 粗体滥用 / 标题层级 / 弯引号）？→ 未扫则补 `references/09-format-and-artifacts.md`。
- 是否用**同义词机械替换**了命中项（如 `delve` → `look into`）？→ 是则撤销——那是新痕迹，不是去味。
- 每处改动是否都能**指向具体规则**？未命中规则的句子是否**逐字保留**？→ 否则撤回该改动。
- 改写后**每个实词能否在原文指出出处**？→ 指不出来的新增**必须撤销**。
- 去味后是否改变了事实、情态、条件、归属、数字、完成状态？→ 改了则撤回该改动。
- 朗读一遍：拗口、排比堆砌、一听像营销 / PR 文案的 → 重写。

## 来源与许可

- 本 skill 为独立实现，未复制第三方源码。v1.2.0「保真护栏」的编辑哲学借鉴自开源项目 **shuorenhua（说人话，MIT License）**；v1.4.0 新增的**中文篇章 / 句法层规则**与**反向保护清单**改写自开源项目 **`lieflat-less-ai-tone`（MIT License）**，其规则基于 283 万字对照语料统计（**证据等级：高质量外部证据 · 待独立验证**）。评测数据以原作者自述为准。
- v1.5.0 新增的**英文篇章 / 句法层规则**、**英文反向保护清单**与**格式 / 残留标记清扫**，依据 **Reinhart et al., "Do LLMs write like humans? Variation in grammatical and rhetorical styles", PNAS 122(8) e2422455122 (2025)**（HAP-E 平行语料 33.5M 词，数据与复现代码公开：`hf/3770`、`hf/3792`、`OSF 7MRQN`）与 **Wikipedia:Signs of AI writing**（WikiProject AI Cleanup，社区共识）。同轮按实测**修正**三处既有英文规则：被动语态摘出、hedge 降级为提示、判据改为密度。
- **已知局限**：HAP-E 的 6 体裁（学术 / 博客 / 小说 / 新闻 / 口语 / 影视剧本）**不含商务邮件、IT 方案与汇报、幻灯片**，其倍数只作方向性依据；中文语料未公开、不可核验。两侧定量结论均**未在本 skill 自建语料上复算**（待办 P2）。
- 许可证：MIT。作者 Stanley Hao。
