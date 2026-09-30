# 禁词表与 AI 味儿特征（中英）

> `de-ai-flavor` 按需参考（L3）。何时加载：生成任何去味约束 / 改写文本前，按输入语言取对应清单。
> **证据分级**：中文词汇层为 🟡 经验共识（2026-09-30 依据中文对照语料做过一次校准，见文末「校准说明」）；英文清单为 ⚪ 待验证（**无对照语料数据**，属经验清单）。
> **层次边界**：本文件的禁词清单是**词汇层**约束；**篇章 / 句法层**痕迹另见 `references/05-zh-syntax-and-structure.md`（中文），**反向保护清单**（不得据此改写的项）见 `references/06-do-not-change.md`。

## 语言处理规则

1. **检测输入语言**：若输入主要为中文 → 套用中文禁词表 + 中文模板；主要为英文 → 套用英文禁词表 + 英文模板。
2. **混合文本**：中英夹杂时，两套禁词表同时生效；改写时保持各自语言的自然语域，不要机器直译。
3. **指定语言**：用户明确说"用英文去味 / humanize in English"时，即使素材是中文，也按目标语言产出并套用对应禁词表。
4. **不要逐字翻译禁词**：中英文 AI 味儿的"套路词"不同（中文重抽象大词与客套，英文重 buzzword 与 hedge filler），按各自清单处理，不要互相套用。

## 五组 AI 味儿特征 → 替代写法（中英对照）

| AI 味儿 | 人味儿替代（中文） | AI flavor (EN) | Human alternative (EN) |
|---|---|---|---|
| 套话开场（"在当今…时代"） | 直接切入要点 | "In today's fast-paced world" / "It is important to note" | Get to the point |
| 确定语气空转词（毋庸置疑/不可否认） | 删空话，或给出依据 | "It goes without saying" / "needless to say" | Drop it, or give the basis |
| 序数词当小标题（一、二、三通篇编号） | 删编号，保留小标题原文 | "First… Second… Finally" as a forced skeleton | Order by logic, not by formula |
| 抽象大词（赋能/打造/闭环） | 具体动作 + 对象 | "leverage" / "seamless" / "robust" / "empower" / "ecosystem" | Concrete action + object |
| 无立场无细节 | 有观点、有证据、有温度 | passive voice, no stance, no specifics | Stance + evidence + specifics |

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

> 证据等级 ⚪ 待验证：英文侧**无对照语料数据**，以下为经验清单。中文语料的统计结论不得反向套用到英文（见 `references/06-do-not-change.md`）。

```
Forbid the following; rewrite on appearance:
- Cliche openers/closers: "In today's fast-paced world", "In the ever-evolving landscape of", "It is important to note that", "It is worth mentioning", "In conclusion", "To summarize", "At the end of the day"
- Hedge filler: "might", "perhaps", "to some extent", "arguably", "it could be said that", "one could argue", "somewhat", "relatively"
- Forced structure: "First… Second… Finally" used as a skeleton (unless the content truly enumerates)
- Buzzwords: "leverage", "seamless", "robust", "delve", "navigate", "empower", "unlock", "game-changer", "synergy", "ecosystem", "streamline", "holistic", "cutting-edge", "best-in-class", "move the needle", "circle back", "deep dive", "low-hanging fruit"
- Assistant pleasantries: "I'd be happy to help", "Great question", "As an AI / as a language model", "Let me know if you have any questions", "Hope this helps", "Feel free to ask"
```

## 校准说明（2026-09-30）

依据中文对照语料研究（283 万字 / 629 篇 = 300 生成 + 329 人类，5 个模型；来源 `lieflat-less-ai-tone`，MIT，证据等级「高质量外部证据 · 待独立验证」），对原词汇表做两处修订：

1. **「虚词堆叠」修订**：删「可能 / 或许」必删项——实测方向相反（AI 偏少），且与原护栏"真实不确定须保留"内部矛盾。保留「毋庸置疑 / 不可否认」等**确定语气空转词**（属相反问题：以确定语气说空话）。
2. **「三段式」修订**：靶子由**正文连接词**改为**序数词当小标题**——正文连接词实测无差别（R≈1.0），小标题编号才有模板感（R=3.1）。

配套新增篇章 / 句法层清单（`references/05-zh-syntax-and-structure.md`）与反向保护清单（`references/06-do-not-change.md`）。

---
**执行要点**
- 触发：生成去味约束 / 改写文本前。
- 必须动作：按目标语言取对应清单；中英混用两套同时生效；中文改写时，词汇层（本文件）+ 篇章层（`references/05-zh-syntax-and-structure.md`）**都要过**。
- 禁止：逐字互译禁词；把表达真实不确定的虚词（可能/或许）机械删除；据中文统计结论改动英文清单。
- 停止条件：选中的清单与目标语言一致，且已排除保真护栏保护项（`references/01-fidelity-guardrails.md`）与反向保护清单（`references/06-do-not-change.md`）中的项。
