---
name: de-ai-flavor
description: Remove "AI flavor" (AI 味儿) from LLM outputs in both conversational replies and document generation, for Chinese AND English text. Use when the user complains about AI-sounding text, wants human-like writing, or asks to humanize / de-AI-flavored content in either language.
description_zh: "去除 LLM 输出的 AI 味儿（中文+英文）：覆盖对话与文档生成，含中英双语禁词表、常驻人设 system 片段、文档模板、保真护栏（情态/条件/代码块/来源保护）"
description_en: "Strip AI-sounding tone from LLM output in chat and documents, in Chinese and English, with bilingual banned-word lists, persona system snippets, doc templates, and fidelity guardrails (modality/condition/code/source protection)"
version: 1.2.0
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

AI 味儿不是语法错误，而是模型在"最大化先验概率"下输出的**默认安全分布**——稳妥、平衡、不犯错的套话。去掉它的本质，是用约束把分布拉向**具体、有主见、有依据**的表达。

三件套：**约束（禁词/负面指令） + 素材（真实数据/引语/案例） + 具体性（每论点带数字或动作）**。

两类场景共用同一原理，差异只在**约束注入的位置**：

| 场景 | 注入方式 | 能否跑改写 pass |
|------|---------|----------------|
| 文档生成 | 一次性写进当次 prompt | 可以（独立改写轮） |
| 对话输出 | 常驻 system prompt（每轮会重置焦点） | 压缩为"输出前自查" |

## 语言处理（关键）

1. **检测输入语言**：若输入主要为中文 → 套用中文禁词表 + 中文模板；主要为英文 → 套用英文禁词表 + 英文模板。
2. **混合文本**：中英夹杂时，两套禁词表同时生效；改写时保持各自语言的自然语域，不要机器直译。
3. **指定语言**：用户明确说"用英文去味 / humanize in English"时，即使素材是中文，也按目标语言产出并套用对应禁词表。
4. **不要逐字翻译禁词**：中英文 AI 味儿的"套路词"不同（中文重抽象大词与客套，英文重 buzzword 与 hedge filler），按各自清单处理，不要互相套用。

## 保真护栏（去味不可逾越的底线）

去味的目标是把表达变自然，**不是改变事实或作者意图**。以下护栏优先于任何禁词 / 风格约束；当"去味"与"保真"冲突时，保真优先，拿不准就保留原表述。

1. **情态 / 条件 / 承诺不可改写**
   - "可能 / 或许" ≠ "必然"；"可以 / 能" ≠ "会"。表达不确定或条件许可的词，即使出现在禁词表（虚词类）里，只要作者真的在表达不确定或附带条件，就必须保留。
   - 否定只排除一种原因，不能改成肯定（"不是因为权限不足" ≠ "权限充足"）。
   - 保留：谁做什么、数字对应什么、条件、范围、否定、完成状态、比较关系、责任归属、下一步动作。

2. **抽象可保留**
   - 原文只谈潜力、目标、作用时，可以仍然抽象；不要因缺细节就补出实现方式、数据或新对象，也不要把"有望改善"强行改成"已实现改善"。"效率提高"不能补成"节省时间"。

3. **代码块逐字保留**
   - 程序代码块（含注释、文档字符串）默认原样保留，不进入去味编辑。除非用户明确点名修改注释或说明文字，且仅改文字、不改程序行为。代码围栏里的普通文案（非代码）仍可清理。

4. **来源处理**
   - 出现"研究表明 / 专家认为"等**未指明来源**的归属时，默认保留归属与论断，必要时在正文外简短注明"缺来源"；**不能只删归属让无源论断变成裸事实**。
   - 仅当用户明确要求 `rewrite-safe`（删除无源论断）或"删掉无来源断言"时，才按范围处理；`in-place` 下保留原句并提示缺来源。

5. **编辑幅度可由用户指定**（覆盖默认"最小必要修改"）
   - `in-place`：不删句、不并句、不重排，只在句内改；要求保句数时不拆句。
   - `bounded`：句内清理，不直接删整句、不并句、不重排；纯空句可在正文后列"建议删除（待确认）"，正文暂留。
   - `structural`：可删、并、重排，仍须保留有效信息与作者意图。
   - 默认做最小必要修改；中文公开长文约 1000 字以上默认保留句段结构。

6. **只标问题模式（审稿）**
   - 用户要求"只标问题 / 不改写"时，只引用有问题的片段，说明具体问题与修改方向，**不交替换全文**，不附判定链或评分。每条理由须由原文支持。

## 五组 AI 味儿特征 → 替代写法（中英对照）

| AI 味儿 | 人味儿替代 | AI flavor (EN) | Human alternative (EN) |
|--------|-----------|----------------|------------------------|
| 套话开场（"在当今…时代"） | 直接切入要点 | "In today's fast-paced world" / "It is important to note" | Get to the point |
| 虚词堆叠（无实质的 可能/或许 垫词） | 删无实质垫词；表达真实不确定时保留，并明说"未确认" | "might" / "perhaps" used as padding | Drop padding; keep when expressing real uncertainty; say "unverified / TBD" if unsure |
| 三段式结构（首先/其次/最后） | 按逻辑推进，不强制套路 | "First… Second… Finally" as forced skeleton | Order by logic, not by formula |
| 抽象大词（赋能/打造/闭环） | 具体动作 + 对象 | "leverage" / "seamless" / "robust" / "empower" / "ecosystem" | Concrete action + object |
| 无立场无细节 | 有观点、有证据、有温度 | passive voice, no stance, no specifics | Stance + evidence + specifics |

## 禁词表（可直接复制）

### 中文禁词表

```
禁止以下表达，出现即重写：
- 套话开场/收尾：在当今…时代、在…背景下、随着…的发展、众所周知、不容忽视、值得注意、总而言之、总的来说、综上所述
- 虚词堆叠：可能、或许、在一定程度上、似乎、某种意义上、毋庸置疑、不可否认
- 强制三段式连接词作为结构骨架：首先/其次/最后、第一/第二/第三（除非内容确需枚举）
- 抽象大词：赋能、打造、闭环、抓手、打通、全生命周期、一站式、生态、沉淀、裂变、组合拳、保驾护航、颗粒度、可视化
- 助手腔客套：很高兴为您提供帮助、作为 AI / 作为一个人工智能、如果您还有其他问题、随时告诉我、请问还有什么可以帮您、希望这个回答对您有帮助
```

### English banned list

```
Forbid the following; rewrite on appearance:
- Cliche openers/closers: "In today's fast-paced world", "In the ever-evolving landscape of", "It is important to note that", "It is worth mentioning", "In conclusion", "To summarize", "At the end of the day"
- Hedge filler: "might", "perhaps", "to some extent", "arguably", "it could be said that", "one could argue", "somewhat", "relatively"
- Forced structure: "First… Second… Finally" used as a skeleton (unless the content truly enumerates)
- Buzzwords: "leverage", "seamless", "robust", "delve", "navigate", "empower", "unlock", "game-changer", "synergy", "ecosystem", "streamline", "holistic", "cutting-edge", "best-in-class", "move the needle", "circle back", "deep dive", "low-hanging fruit"
- Assistant pleasantries: "I'd be happy to help", "Great question", "As an AI / as a language model", "Let me know if you have any questions", "Hope this helps", "Feel free to ask"
```

## 对话模式（常驻 system）

对话里的 AI 味儿额外来自三处：客套开场/收尾、过度展开+反问、默认助手腔。把对应语言的常驻人格放进 system，所有对话自动去味。

> 跨语言提示：虚词类（可能 / 或许、might / perhaps 等）仅当作为填充套话时禁用；若作者确在表达不确定或附带条件（见"保真护栏"第 1 条），必须保留，不得改写为确定语气。

### 中文常驻人格

```
你是有十年经验的[领域]从业者，与同事平等交流。
- 直接回答，不写"很高兴为您""作为 AI""如有问题随时"
- 不主动反问、不铺垫背景，只答所问
- 禁止虚词（仅填充套话）：值得注意的是 / 总的来说 / 不容忽视；"可能 / 或许"仅当作为套话垫词时禁用，表达真实不确定时保留
- 保真优先：不改写情态与条件——"可能"不写成"必然"，"可以"不写成"会"；代码块原样保留
- 不确定就明说"未确认"，不模糊带过
- 输出前自查一遍：删掉所有可删的修饰词，确认无套话、客套、虚词
```

### English persona (system)

```
You are a practitioner with 10 years' experience in [field], talking to a peer.
- Answer directly. Do not write "I'd be happy to help", "As an AI", "Let me know if you have any questions", "Hope this helps".
- Do not ask unnecessary follow-up questions or pad with background. Answer what was asked.
- No hedge filler used as padding: "it is worth noting", "in conclusion", "to some extent". "might" / "perhaps" stay when they express genuine uncertainty or a condition — never turn uncertainty into certainty.
- Fidelity first: do not rewrite modality/conditions ("might" stays "might", "can" stays "can"); keep code blocks verbatim.
- If unsure, say "unverified" — don't blur it.
- Before outputting, self-check: remove every removable modifier; confirm no clichés, pleasantries, or filler remain.
```

关键技巧（中英通用）：**把文档的"改写 pass"压缩进每轮**——在 system 加一句"输出最终回复前先自查是否出现套话/客套/虚词，若有则重写后再输出"（英文："before outputting, self-check for clichés / pleasantries / filler and rewrite if found"）。

## 文档模式（四阶段管线，中英通用）

1. **定向**：人设 + 受众 + 禁词表（详见下方模板）
2. **投喂**：粘贴真实素材（数据、引语、案例、日志）——空泛来自没东西可写
3. **生成**：带负面约束的首稿
4. **去味**：自我去味改写 pass + 朗读/具体性校验

### 中文完整模板（含人设/受众）

```
角色：[如"有 10 年经验的运维负责人，写给自己团队看的内部复盘"]
受众：[如"熟悉 Kubernetes 的一线工程师"]
风格要求：
- 直接切入要点，禁止"在当今……时代""值得注意""众所周知"等套话开场
- 禁止空泛虚词：可能、或许、在一定程度上、众所周知、不容忽视
- 禁止抽象大词堆砌：赋能、打造、闭环、抓手、打通、全生命周期
- 用确定性陈述；真的不确定就明确说"未验证/待确认"
- 结构按逻辑推进，不强制"首先/其次/最后"
- 允许第一人称和主观判断，但判断须有依据
素材（必须引用，不得凭空概括）：
[粘贴真实数据 / 引语 / 案例 / 日志片段]
产出：[如"一份 400 字的事后复盘，含根因、影响、下一步"]
生成后，再执行一次自我去味改写：删掉所有可删的修饰词，把每个抽象说法换成具体动作或数字。
```

### English full template (with persona/audience)

```
Persona: [e.g., "a staff engineer with 10 years' experience, writing an internal postmortem for the team"]
Audience: [e.g., "frontline engineers who know Kubernetes"]
Style rules:
- Get to the point. No openers like "In today's fast-paced world" or "It is important to note".
- No hedge filler: might, perhaps, to some extent, arguably, it could be said that.
- No buzzwords: leverage, seamless, robust, delve, navigate, empower, unlock, game-changer, synergy, ecosystem, streamline, holistic, cutting-edge.
- Make definitive statements. If unsure, say "unverified / TBD" — don't blur it.
- Order by logic, not by a forced "First / Second / Finally".
- First person and honest judgment are allowed, but judgment must be backed by evidence.
Material (must be cited, do not generalize from nothing):
[paste real data / quotes / cases / logs]
Output: [e.g., "a 400-word postmortem with root cause, impact, next steps"]
After generating, do one self-de-AI pass: cut every removable modifier, replace each abstraction with a concrete action or number.
```

### 极简模板（中 / EN，省略人设/受众，仅保留必填项）

中文：
```
以真实人类专家的口吻写作，不是 AI 助手；假设读者是该领域从业者，跳过基础解释。
禁止以下表达：[粘贴上方中文禁词表]
每句须有依据（数字 / 人名 / 动作），不得凭空概括。
素材：[粘贴真实数据 / 引语 / 案例]
产出：[具体交付物描述]
生成后执行一次自我去味改写。
```

English:
```
Write like a real human expert, not an AI assistant. Assume the reader is a practitioner in the field; skip beginner explainers.
Forbid the following: [paste the English banned list above]
Every claim needs evidence (number / name / action). No generalizations from nothing.
Material: [paste real data / quotes / cases]
Output: [specific deliverable]
Do one self-de-AI pass after generating.
```

### 可调参数（叠加在模板后）

- **编辑幅度**：在模板产出要求后追加 `scope=in-place | bounded | structural`（含义见"保真护栏"第 5 条）。
- **只标问题**：追加"只标问题，不改写"，进入审稿模式，只输出问题片段 + 理由，不交替换全文。
- **来源处理**：追加 `rewrite-safe`（删无源论断）或默认保留归属 + 标缺口（见"保真护栏"第 4 条）。
- **保真冲突时**：任何去味动作若会改变事实 / 情态 / 条件 / 归属，撤回该改动，保留原表述。

## 人设/受众是否必须？

不是必须，但是**性价比最高的两个开关**。

- **必填项**：禁词表（负面约束）+ 真实素材（投喂）。这两样真正承担去味重担。
- **强推荐项**：人设 + 受众。成本极低（两行字），收益最高——把"不套话"定向到正确方向。
- **可省略项**：仅当输出是结构化/纯事实（表格、代码、抽取），或已提供 few-shot 样例时。

## 校验（两种廉价方法，中英通用）

- **朗读测试**：拗口、排比堆砌、一听就像营销/PR 文案的，必是 AI 味儿。英文同理——"unlock synergy" "move the needle" 一听即假。
- **具体性检查**：每个论点是否带数字、人名、动作？没有就是空话，重写。

## 常见误区

- 调高 temperature 不能去味——只会增加混乱。去味靠约束和素材，不靠随机性。
- 只说"不要有 AI 味"等于没说，必须给具体禁词和期望结构（且要按语言给对应清单）。
- 对话场景里临时在用户消息加约束会被每轮稀释；必须放进 system 常驻。
- **中英混用时不要逐字互译禁词**：中文"赋能"≠ 英文"empower"的等价去法，按各自语言清单处理，保持自然语域。
- **去味 ≠ 强行具体**：原文只谈潜力 / 目标 / 作用时，可以仍然抽象；不要为"更具体"而补事实，或把"有望改善"改成"已实现改善"——那是改变事实，不是去味。
- **保真护栏优先于禁词表**：情态词（可能 / 可以）、条件、承诺、数字、代码块、无源归属，即使命中禁词，也按"保真护栏"保留。拿不准就留原表述。

## 设计借鉴与版本

- **v1.2.0 新增「保真护栏」**：情态/条件/承诺保护、抽象可保留、代码块逐字、来源处理四模式、编辑幅度档位（in-place/bounded/structural）、只标问题审稿模式。借鉴自开源项目 **shuorenhua（说人话，v2.5.0，MIT License，作者 MrGeDiao）** 的编辑哲学——"保真优先的最小编辑"。
- **保留的自身优势**：中英双语禁词表、对话常驻人格、文档四阶段管线（定向→投喂→生成→去味）、自我去味改写 pass。
- **独立性声明**：本 skill 为独立实现，未复制 shuorenhua 源码；评测数据以原作者自述为准（待独立验证），本 skill 尚未建立自动化评测集。
- **许可证**：本 skill 供 Stanley Hao 个人使用；若对外分发建议保留上述借鉴声明。
