# 禁词表与 AI 味儿特征（中英）

> `de-ai-flavor` 按需参考（L3）。何时加载：生成任何去味约束 / 改写文本前，按输入语言取对应清单。

## 语言处理规则

1. **检测输入语言**：若输入主要为中文 → 套用中文禁词表 + 中文模板；主要为英文 → 套用英文禁词表 + 英文模板。
2. **混合文本**：中英夹杂时，两套禁词表同时生效；改写时保持各自语言的自然语域，不要机器直译。
3. **指定语言**：用户明确说"用英文去味 / humanize in English"时，即使素材是中文，也按目标语言产出并套用对应禁词表。
4. **不要逐字翻译禁词**：中英文 AI 味儿的"套路词"不同（中文重抽象大词与客套，英文重 buzzword 与 hedge filler），按各自清单处理，不要互相套用。

## 五组 AI 味儿特征 → 替代写法（中英对照）

| AI 味儿 | 人味儿替代 | AI flavor (EN) | Human alternative (EN) |
|---|---|---|---|
| 套话开场（"在当今…时代"） | 直接切入要点 | "In today's fast-paced world" / "It is important to note" | Get to the point |
| 虚词堆叠（无实质的 可能/或许 垫词） | 删无实质垫词；表达真实不确定时保留，并明说"未确认" | "might" / "perhaps" used as padding | Drop padding; keep when expressing real uncertainty; say "unverified / TBD" if unsure |
| 三段式结构（首先/其次/最后） | 按逻辑推进，不强制套路 | "First… Second… Finally" as forced skeleton | Order by logic, not by formula |
| 抽象大词（赋能/打造/闭环） | 具体动作 + 对象 | "leverage" / "seamless" / "robust" / "empower" / "ecosystem" | Concrete action + object |
| 无立场无细节 | 有观点、有证据、有温度 | passive voice, no stance, no specifics | Stance + evidence + specifics |

## 中文禁词表（可直接复制）

```
禁止以下表达，出现即重写：
- 套话开场/收尾：在当今…时代、在…背景下、随着…的发展、众所周知、不容忽视、值得注意、总而言之、总的来说、综上所述
- 虚词堆叠：可能、或许、在一定程度上、似乎、某种意义上、毋庸置疑、不可否认
- 强制三段式连接词作为结构骨架：首先/其次/最后、第一/第二/第三（除非内容确需枚举）
- 抽象大词：赋能、打造、闭环、抓手、打通、全生命周期、一站式、生态、沉淀、裂变、组合拳、保驾护航、颗粒度、可视化
- 助手腔客套：很高兴为您提供帮助、作为 AI / 作为一个人工智能、如果您还有其他问题、随时告诉我、请问还有什么可以帮您、希望这个回答对您有帮助
```

## English banned list（可直接复制）

```
Forbid the following; rewrite on appearance:
- Cliche openers/closers: "In today's fast-paced world", "In the ever-evolving landscape of", "It is important to note that", "It is worth mentioning", "In conclusion", "To summarize", "At the end of the day"
- Hedge filler: "might", "perhaps", "to some extent", "arguably", "it could be said that", "one could argue", "somewhat", "relatively"
- Forced structure: "First… Second… Finally" used as a skeleton (unless the content truly enumerates)
- Buzzwords: "leverage", "seamless", "robust", "delve", "navigate", "empower", "unlock", "game-changer", "synergy", "ecosystem", "streamline", "holistic", "cutting-edge", "best-in-class", "move the needle", "circle back", "deep dive", "low-hanging fruit"
- Assistant pleasantries: "I'd be happy to help", "Great question", "As an AI / as a language model", "Let me know if you have any questions", "Hope this helps", "Feel free to ask"
```

---
**执行要点**
- 触发：生成去味约束 / 改写文本前。
- 必须动作：按目标语言取对应清单；中英混用两套同时生效。
- 禁止：逐字互译禁词；把表达真实不确定的虚词一律删除。
- 停止条件：选中的清单与目标语言一致，且已排除保真护栏保护项（见 `references/01-fidelity-guardrails.md`）。
