# Spec-Driven 编码工作流模板（定制扩展 · SDD × SPP 融合）

> 三态标注：**待验证**（AI 提议，需人类验证）。本文为定制扩展，非 SPP R4.3 原文。冲突时以主协议为准。
> 来源：资料库 draft-02（「了解 spp-source-principle 原理」页，2026-09-29 会话产出；入库批准：用户 2026-09-29）。
> 依据：GitHub Spec Kit 官方文档、AWS Kiro、Anthropic《AI-native SDLC playbook》、OpenAI Codex Best Practices。检索时点 2026-09-29。
> 定位：`assets/prd-template.md` 是产品文档层模板；本文件是编码执行层工作流模板（对接 GitHub Spec Kit / AWS Kiro / Claude Code plan mode 的通用形态）。

## 定位与档位

SDD 四段：**Specify → Plan → Tasks → Implement（含 Verify）**。每段产出被下一段消费的 artifact，agent 不得跳段直接写代码。

按 S 轴分档（对齐 §9 反过度设计）：

- **轻量档（S0/S1、一句话能说清 diff 的改动）**：只填 §A 的 Goal/Non-goals/验收三行，直接实现。
- **完整档（S2/S3、多文件、承重项）**：四段全走，plan.md 须经人类批准（Gate）。

## 与既有 FDD / TDD 模板的关系（分层，不替代）

- **FDD / TDD = 完整档设计文档**（承重、正式交付、S2/S3）：展开 A 轴映射（§6.2）、原理核实（§11.6）、排他反证（§12）、不可逆分阶段（§13）。见 `assets/fdd-template.md`、`assets/tdd-template.md`。
- **本模板 = 编码执行工作流**（每任务级、轻量）：对上述条款只做引用，不展开。
- **升级路径**：S0/S1 用本模板轻量档直接走；触发 S2/S3 或需正式设计交付物时，SPEC 对齐 FDD、PLAN 展开为 TDD 后再进入实现。
- 关系链：课题说明书 → intent.md → PRD → FDD → TDD → 本模板（SPEC→PLAN→TASKS→VERIFY）→ 验收清单（`assets/ai-output-verification-checklist.md`）。

## §A SPEC · 规格模板

```markdown
# Spec · [功能名]
> 三态：本文各节标注 已确认 / 待验证 / 管理决策

## 0. 目标（对齐 §5.4.5 课题说明书）
Goal：一句话——做什么、为谁、成功长什么样
Users：谁用
Out of Scope（非目标）：本期不做什么——非目标是刹住 agent 过度实现的刹车，禁止省略

## 1. 需求（EARS 可选：WHEN…/IF…THEN… the system SHALL…）
| 编号 | 需求 | 三态 | 依据 |
|---|---|---|---|

## 2. 边界与约束
API Contract：
Edge Cases：
禁改区（protected paths / 不可破坏的兼容性）：

## 3. 验收标准（必须可转化为测试）
Given [上下文] When [动作] Then [可观察结果]

## 4. 被引用原理（§11.6；无则标 N/A）
关键主张（含反直觉部分）：
核实来源：
```

## §B PLAN · 技术方案模板

```markdown
# Plan · [功能名]
影响面（文件/模块/接口）：
方案与权衡（≥1 个替代方案，说明取舍）：
风险与兼容性影响：
测试计划（对齐 §A3 验收标准）：
Open Questions（未决，禁止以确定性语气填补，§5.5）：
【S2/S3：本节经人类批准后方可进入实现——Gate】
```

## §C TASKS · 任务拆解模板

```markdown
# Tasks · [功能名]
| # | 任务 | 依赖 | 验证点（每任务自带） |
|---|---|---|---|
（依赖排序；每任务必须有可运行验证点：测试/构建/linter/截图对比）
```

## §D IMPLEMENT & VERIFY · 实现与验证规则

1. **验证闭环**：给 agent 一个它能运行的 pass/fail 检查（测试套件/构建退出码/linter/输出与 fixture 对比）。没有检查时，人是验证环——不可接受。
2. **证据而非断言**（§11.5）：完成的声明必须附测试输出/命令返回/截图；禁止「应该可以了」。
3. **跑偏即丢弃**：agent 方向错误时整体丢弃重述需求，优于在错误输出上打补丁。
4. **spec 随代码演进**：实现中发现规格不成立时，回到 §A 修改 spec 并留痕，禁止在代码里静默绕开（§11.6.5 精神）。
5. **验收**：对照 §A3 逐项核对 + `assets/ai-output-verification-checklist.md`（安全门/排他反证/不可逆项）。

## 与 SPP 条款对应速查

| SDD 段 | SPP 条款 |
|---|---|
| SPEC §0 目标/非目标 | §5.4.5 课题说明书、§3.1 目标原则 |
| SPEC §4 被引用原理 | §11.6（含替换测试） |
| PLAN | §6 三轴、§7 Gate（S2/S3 WAIT FOR HUMAN） |
| TASKS 验证点 | §11.5 证据要求 |
| VERIFY | §12 排他反证、§13 不可逆分阶段、§16 输出前检查 |

---

## 执行要点（AI 路由）

- **触发：** AI agent 辅助编码、且改动超出「一句话能说清的 diff」时。
- **必须动作：** 先 SPEC 后实现；非目标必填；每个任务带验证点；完成声明附实际执行证据。
- **禁止：** 跳段直接写代码；省略非目标；以聊天记录代替 spec 作为源真相；S2/S3 未经 plan 批准进入实现。
- **停止条件：** 验收标准逐项核销或人类叫停。
- **交叉引用：** 阶段产物定义 → `references/14-ai-era-sdlc-deliverables.md`；产出验收 → `assets/ai-output-verification-checklist.md`。
