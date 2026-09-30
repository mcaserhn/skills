# AI 时代 SDLC 阶段与核心交付物（定制扩展）

> 三态标注：**待验证**（AI 提议，需人类验证）。本文为定制扩展，非 SPP R4.3 原文。
> 冲突时以主协议为准。
> 来源：研究报告《AI-Era-SDLC-Methodology-Research》（资料库「了解 spp-source-principle 原理」页，2026-09-29 会话产出；入库批准：用户 2026-09-29）。
> 依据：Anthropic《AI-native SDLC playbook》(2026-08)、OpenAI《Harness engineering》、DORA 2025、GitHub Spec Kit / AWS Kiro 官方文档。检索时点 2026-09-29。
> 与 references/13 的关系：13 号管「研发阶段 → SPP 条款」映射；本文件管「研发阶段 → 核心交付物」定义。互补不重叠。

## 一、核心变化

传统 SDLC 假设「写代码是最慢最贵的一步」。Agentic coding 使 build 坍缩到小时级后：瓶颈移至 Plan / Review-Test / Deploy（人类速度环节）；逐行人工审查与全量委员会审批失效。治理目标不变，**执行方式改为「机器可执行门禁 + 人类守门」**。流程从线性管线变为循环：每阶段提交一个版本化、机器可执行且人可读的 artifact，其验收触发下一阶段。

## 二、六阶段 × 核心交付物

| 阶段 | 传统交付物 | AI-era 交付物 | SPP 对接点 |
|---|---|---|---|
| Plan（意图） | PRD、会议纪要、签核记录 | **intent.md**：AI 从原始素材合成，人类（product owner）批准后才进入下一阶段 | 承重课题触发 §5.4 课题共构；产出对齐 §5.4.5 课题说明书 |
| Design（规格） | 分析师 spec | **spec.md**（含 Non-goals、验收标准可测试化）+ **constitution.md**（项目宪法：测试标准/性能预算/风格/红线） | §11.6 被引用原理核实写入 constitution 段；三态标注沿用 §10.1 |
| Build（实现） | 手写代码+后补文档 | **plan.md**（批准后实现）；代码+测试由 agent 生成；**AGENTS.md / CLAUDE.md** 持有机构知识（≤1 页，重复犯两次的错误入册） | plan mode ≈ S1/S2 的 Discovery Gate；§11.5 禁止推测性测量适用于「实现完成」声明 |
| Test（验证） | QA 门禁、覆盖率 | **evals 套件**（20–50 个真实任务回归，护栏变更即触发）；事故永久转为回归用例；mutation testing 防永绿测试 | 验证证据必须实贴输出（§11.5）；测试也是规格（三态中的「已确认」证据） |
| Deploy（发布） | 全量人工评审 | **REVIEW.md**（定义 AI 对 PR 的检查遍数）+ 分层审批：低爆炸半径+测试过→自动；受监管/高风险/核心架构→人类终审；hooks 为程序化门 | §13 不可逆操作分阶段；references/13 Coding 专属承重清单（migration/契约/生产配置） |
| Maintain（运营） | 人工盯生产、ticket | 监控 agent 超界起草**新 intent.md** 回环 | 回环产物重新进入承重判定（§11.1） |

## 三、横切层：Agent 上下文资产（新增一类持久交付物）

| 资产 | 内容 | 维护纪律 |
|---|---|---|
| AGENTS.md / CLAUDE.md | 构建/测试命令、代码风格、工作流规则、禁改区、三档边界（Always do / Ask first / Never do） | ≤1 页；祈使句；约定变更同一提交内更新；短小准确 > 冗长半失效 |
| constitution.md | 项目级不可协商原则 | 变更须经人类批准（管理决策） |
| skills | 重复流程的过程性知识（按需加载，不占每会话上下文） | 一再复用同一提示词/纠正同一流程 → 沉淀为 skill |
| hooks 配置 | 必须无例外的规则（保护文件、发布授权、拒绝读凭证） | 机械化执行，不靠提示词 |
| evals 套件 | 20–50 个真实任务回归集 | 护栏每次变更即跑；事故入库 |

## 四、与 SPP 条款映射速查

| 交付物 | 生成前 | 生成时 | 验收时 |
|---|---|---|---|
| intent.md | §11.1 承重判定 | §5.4 共构（单问串行） | 人类批准=管理决策 |
| spec.md | §11.6 原理核实 | §3.3 证据不足禁止补齐 | Non-goals/验收可测试性检查 |
| plan.md | §6 三轴判定 | §7 Gate（S2/S3 WAIT FOR HUMAN） | 影响面/风险/兼容性复核 |
| 代码+测试 | §13 不可逆项识别 | P4 验证闭环、§11.5 证据陈述 | `assets/ai-output-verification-checklist.md` 验收清单 + §12 排他反证 |
| 发布 | §13 分阶段 | hooks 强制门 | 实施后验收关闭证据链 |

## 五、复审与停止条件（§15.3 第 4 问）

本框架被实战验证有效（§18.3）且与主协议无冲突后，可评估合并回 references/ 通用层。
建议 6 个月后复审（参照 TW Radar 节奏）；期间若 Anthropic / OpenAI / DORA 官方方法论发生结构性更新，提前触发复审。

---

## 执行要点（AI 路由）

- **触发：** AI 辅助开发课题需要确定各阶段交付物或产物形态时。
- **必须动作：** 按阶段对照表定位当前产物；新产物回环时重新触发承重判定；上下文资产变更视为受控项。
- **禁止：** 不得跳过 spec 直接生成承重代码；不得以「agent 已生成」替代验收；不得将低风险自动通过策略套用在不可逆操作上。
- **停止条件：** 阶段产物验收完成或人类叫停；框架被验证有效且可合并时复审。
- **交叉引用：** 编码工作流执行 → `assets/spec-driven-workflow-template.md`；产出验收 → `assets/ai-output-verification-checklist.md`；阶段→条款映射 → `references/13-coding-and-product-lifecycle.md`。
