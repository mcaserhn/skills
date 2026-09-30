# 禁词表与 AI 味儿特征（中英）

> `de-ai-flavor` 按需参考（L3）。何时加载：生成任何去味约束 / 改写文本前，按输入语言取对应清单。
> **证据分级**：中文词汇层为 🟡 经验共识（2026-09-30 依据中文对照语料做过一次校准）；**英文词汇层仍为 ⚪ 待验证**（本表无对照语料支撑）；但**英文句法 / 篇章层已有 🟢 同行评审证据**，见 `references/07-en-syntax-and-structure.md`。校准与冲突处置见文末。
> **层次边界**：本文件是**词汇层**约束。**篇章 / 句法层**——中文见 `references/05-zh-syntax-and-structure.md`，英文见 `references/07-en-syntax-and-structure.md`；**反向保护清单**（不得据此改写的项）——中文见 `references/06-do-not-change.md`，英文见 `references/08-en-do-not-change.md`；**格式与残留标记清扫**（中英共用）见 `references/09-format-and-artifacts.md`。

## 语言处理规则

1. **检测输入语言**：若输入主要为中文 → 套用中文禁词表 + 中文模板；主要为英文 → 套用英文禁词表 + 英文模板。
2. **混合文本**：中英夹杂时，两套禁词表同时生效；改写时保持各自语言的自然语域，不要机器直译。
3. **指定语言**：用户明确说"用英文去味 / humanize in English"时，即使素材是中文，也按目标语言产出并套用对应禁词表。
4. **不要逐字翻译禁词**：中英文 AI 味儿的"套路词"不同（中文重抽象大词与客套，英文重 buzzword 与固定句式），按各自清单处理，不要互相套用。

## 五组 AI 味儿特征 → 替代写法（中英对照）

| AI 味儿 | 人味儿替代（中文） | AI flavor (EN) | Human alternative (EN) |
|---|---|---|---|
| 套话开场（"在当今…时代"） | 直接切入要点 | "In today's fast-paced world" / "It is important to note" | Get to the point |
| 确定语气空转词（毋庸置疑/不可否认） | 删空话，或给出依据 | "It goes without saying" / "needless to say" | Drop it, or give the basis |
| 序数词当小标题（一、二、三通篇编号） | 删编号，保留小标题原文 | "First… Second… Finally" as a forced skeleton | Order by logic, not by formula |
| 抽象大词（赋能/打造/闭环） | 具体动作 + 对象 | "leverage" / "seamless" / "robust" / "empower" / "ecosystem" | Concrete action + object |
| 无立场无细节 | 有观点、有证据、有温度 | vague stance, no specifics | Stance + evidence + specifics |

> **已摘出（2026-09-30）**：英文列此行原写作 `passive voice, no stance, no specifics`。依 HAP-E 平行语料（PNAS 2025）实测，**无施事被动 AI ≈0.5×，人类多用 2 倍**——被动语态不是 AI 痕迹，已移入反向保护清单 `references/08-en-do-not-change.md`。有证据的靶子只有"无立场、无细节"，三项已拆开。

## 中文禁词表（可直接复制）

```
禁止以下表达，出现即重写：
- 套话开场/收尾：在当今…时代、在…背景下、随着…的发展、众所周知、不容忽视、值得注意、总而言之、总的来说、综上所述
- 确定语气空转词（以确定语气说空话）：毋庸置疑、不可否认、不言而喻、毫无疑问
- 序数词当小标题：小标题以「一、二、三」通篇编号且连续 ≥3（正文连接词不在此列，详见 references/05 第 6 条）
- 抽象大词：赋能、打造、闭环、抓手、打通、全生命周期、一站式、生态、沉淀、裂变、组合拳、保驾护航、颗粒度、可视化
- 助手腔客套：很高兴为您提供帮助、作为 AI / 作为一个人工智能、如果您还有其他问题、随时告诉我、请问还有什么可以帮您、希望这个回答对您有帮助
```

**不再列为「必删」（实测方向相反或无差别，仅作提示，不得据此机械删除）**：

- **虚词 / 模糊限定**：「可能、或许、在一定程度上、某种意义上、似乎」——中文对照语料实测 AI 用得比人类**更少**（口语连接词 R=0.26、单字虚词 R=0.45），方向是"补"不是"删"；且表达真实不确定或条件许可时**一律保留**（见 `references/01-fidelity-guardrails.md` 情态保护条）。仅在它们作为**无实质垫词堆叠**、可删而不丢信息时，按"空话"处理。
- **正文连接词**：「首先 / 其次 / 最后」「第一 / 第二 / 第三」——实测**与人类写作无差别**，不是 AI 痕迹；只有充当**小标题编号**时才按上表"序数词当小标题"处理。

## English banned list（可直接复制）

> 证据等级 ⚪ 待验证：英文词汇层**无对照语料数据**，以下为经验清单（英文**句法层**另有 🟢 证据，见 `references/07-en-syntax-and-structure.md`）。中文语料的统计结论不得反向套用到英文（见 `references/08-en-do-not-change.md`）。

```
Rewrite on density, not on appearance. Act only when trigger markers cluster in one paragraph or across the whole text; a single occurrence is never a reason to touch a sentence.
Never fix a listed item by swapping in a synonym. A word being overused by AI does not mean its synonyms are: mechanically replacing "delve" with "look into" creates a new tell instead of removing one.
- Cliche openers/closers: "In today's fast-paced world", "In the ever-evolving landscape of", "It is important to note that", "It is worth mentioning", "In conclusion", "To summarize", "At the end of the day"
- Empty certainty (saying nothing, at full confidence): "It goes without saying", "needless to say", "it is undeniable that", "cannot be overstated", "there is no doubt that"
- Forced skeleton: "First… Second… Finally" used as a heading scheme, or a three-item list in nearly every paragraph (a single set of three is not a tell — see references/08-en-do-not-change.md)
- Buzzwords: "leverage", "seamless", "robust", "delve", "navigate", "empower", "unlock", "game-changer", "synergy", "ecosystem", "streamline", "holistic", "cutting-edge", "best-in-class", "move the needle", "circle back", "deep dive", "low-hanging fruit"
- Assistant pleasantries: "I'd be happy to help", "Great question", "As an AI / as a language model", "Let me know if you have any questions", "Hope this helps", "Feel free to ask"
```

**不再列为「必删」**（方向随模型而变，或证据不足——仅作提示，**不得据此改写**）：

- **Hedge / downtoner**：`might` / `perhaps` / `somewhat` / `relatively` / `arguably` / `to some extent` / `it could be said that` / `one could argue`。HAP-E 实测**方向随模型而变**——GPT-4o 过用、Llama 回避，不构成稳定判据；且表达真实不确定或条件许可时**一律保留**（见 `references/01-fidelity-guardrails.md` 情态保护条）。真靶子是**以确定语气说空话**，即上列 Empty certainty。
- **词汇多样性 / elegant variation**：为"换个说法"而轮换同义词是维基明确列出的**非** AI 信号，且与上一条"禁同义词机械替换"同向。详见 `references/08-en-do-not-change.md`。

> **时效警示**：本清单证据来自 2025–2026 的观察。词表会腐烂——`Wikipedia:Signs of AI writing` 按 GPT-4 / GPT-4o / GPT-5 **分代际**列出代表词，`delve` 在 2023–2024 被滥用后已于 2025 年急剧退潮。本清单须随版本复审（见 `references/04-doc-pipeline-and-faq.md` 版本节）。

## 校准说明（2026-09-30）

依据中文对照语料研究（283 万字 / 629 篇 = 300 生成 + 329 人类，5 个模型；来源 `lieflat-less-ai-tone`，MIT，证据等级「高质量外部证据 · 待独立验证」），对原词汇表做两处修订：

1. **「虚词堆叠」修订**：删「可能 / 或许」必删项——实测方向相反（AI 偏少），且与原护栏"真实不确定须保留"内部矛盾。保留「毋庸置疑 / 不可否认」等**确定语气空转词**（属相反问题：以确定语气说空话）。
2. **「三段式」修订**：靶子由**正文连接词**改为**序数词当小标题**——正文连接词实测无差别（R≈1.0），小标题编号才有模板感（R=3.1）。

配套新增篇章 / 句法层清单（`references/05-zh-syntax-and-structure.md`）与反向保护清单（`references/06-do-not-change.md`）。

### 英文侧校准（同日，依 HAP-E 平行语料 · PNAS 2025）

以 `Reinhart et al., "Do LLMs write like humans?", PNAS 122(8) e2422455122 (2025)` 的 33.5M 词平行语料（6 体裁 × 8 来源，Biber 66 特征）复核英文清单，发现**三处与实测不符**，已修订：

3. **「被动语态」摘出**：原五组特征表把 `passive voice` 列为 AI 味。实测无施事被动 **AI ≈0.5×、人类多用 2 倍**，方向相反；且与本 skill 中文 `references/06-do-not-change.md` 第 4 条"被动句不得改写"自相矛盾。已移入 `references/08-en-do-not-change.md`。
4. **「hedge filler」降级**：原清单"出现即重写"。实测 downtoner 方向**随模型而变**（GPT-4o 过用、Llama 回避），且与保真护栏情态保护条打架。降为**仅提示**，真靶子改为「以确定语气说空话」。
5. **判据改为密度 + 触发标记**：原为 "rewrite on appearance"，会诱发机械换同义词（维基实证有人把 `delve` 批量换成 `look into`，反而制造新痕迹）。已改为按密度判定，并新增明令：**不得用同义词机械替换**。

同轮新增英文专属两文件（`references/07-en-syntax-and-structure.md` 句法层 10 项 🟢 / `references/08-en-do-not-change.md` 反向清单），另立中英共用的 `references/09-format-and-artifacts.md` 格式与残留标记清扫。

> **证据强度差异（须知）**：中文侧结论基于**单一来源、语料未公开、不可核验**；英文侧基于**同行评审 + 数据与代码全公开可复算**（`hf/3770` 全文本、`hf/3792` Biber 特征、`hf/3793` spaCy 解析、`OSF 7MRQN` 复现代码）。英文侧数字更硬，但**体裁不匹配**——HAP-E 的 6 体裁为学术 / 博客 / 小说 / 新闻 / 口语 / 影视剧本，**不含商务邮件、IT 方案与汇报、幻灯片**，故其倍数只作**方向性依据**，不能直接当作判据阈值。

---
**执行要点**
- 触发：生成去味约束 / 改写文本前。
- 必须动作：按目标语言取对应清单；中英混用两套同时生效；**中英各自**都要过词汇层（本文件）+ 该语言自己的篇章层（中文 `references/05-zh-syntax-and-structure.md`，英文 `references/07-en-syntax-and-structure.md`）。
- 禁止：逐字互译禁词；把表达真实不确定的虚词 / hedge 机械删除；**用同义词机械替换**命中项；把篇章层规则跨语言套用（中文结论不得改英文，英文倍数不得改中文）；据单一来源的定量数字直接当判据阈值。
- 停止条件：选中的清单与目标语言一致，且已排除保真护栏保护项（`references/01-fidelity-guardrails.md`）与对应语言的反向保护清单（中文 `references/06-do-not-change.md` / 英文 `references/08-en-do-not-change.md`）中的项。
