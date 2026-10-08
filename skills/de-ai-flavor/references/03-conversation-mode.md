# 对话模式（常驻 system）

> `de-ai-flavor` 按需参考（L3）。何时加载：需要配置"对话人格"，或解释对话场景为何必须常驻。

对话里的 AI 味儿额外来自三处：**客套开场/收尾、过度展开+反问、默认助手腔**。把对应语言的常驻人格放进 system，所有对话自动去味 —— 可复制片段见 `assets/persona-zh-system.md`、`assets/persona-en-system.md`。

> 跨语言提示：虚词类（可能 / 或许、might / perhaps 等）仅当作为填充套话时禁用；若作者确在表达不确定或附带条件（见 `references/01-fidelity-guardrails.md` 第 3 条），必须保留，不得改写为确定语气。

关键技巧（中英通用）：**把文档的"改写 pass"压缩进每轮** —— 在 system 加一句"输出最终回复前先自查是否出现套话/客套/虚词，若有则重写后再输出"（英文："before outputting, self-check for clichés / pleasantries / filler and rewrite if found"）。

---
**执行要点**
- 触发：对话场景需要去味。
- 必须动作：把常驻人格放进 system（不要放用户消息，会被每轮稀释）。
- 禁止：只在当前用户消息里临时加约束，却期望跨轮持久生效。
- 停止条件：system 常驻人格已就位，且含跨语言虚词保护提示。
