# 03 · 场景投影与落地指南（USP-GUIDE v1.1）

> **文档性质**：指南。场景取值投影与操作步骤，不含规则（见 `docs/01`）与注册字段（见 `docs/02`）。
> **上游**：`aden-naming-standard` v1.4 + `docs/01-universal-folder-structure.md` v1.1。
> **状态**：v1.1 · Draft · 2026-11-18。

---

## 1. 六类场景的六段投影

下表把六类场景映射到同一骨架。**列对齐六段；某段无内容时留空，不强行填充**（`docs/01` §3.3）。

| 场景代码 | 场景名 | 00-Ingest | 10-Analyze | 20-Build | 30-Verify | 40-Deliver | 50-Sustain |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Academic` | 课题调研 | 选题、文献、资料 | 研究框架、方法 | 调研执行、初稿 | 论证、评审 | 报告定稿 | 知识沉淀、后续选题 |
| `BusinessLogic` | 业务逻辑需求调研 | 干系人、现状流程 | 流程建模、拆解 | 业务规则规格 | 业务评审确认 | 需求基线 | 规则复用、变更跟踪 |
| `Software` | 软件系统开发全流程 | 需求收集 | 设计 | 开发 | 测试 + UAT | 上线 | 运维复盘、迭代 |
| `Reverse` | 盘点+逆向+复刻 | 资产盘点 | 逆向解析、架构还原 | 复刻实现 | 对齐验证 | 交付切换 | 差异台账、复用件 |
| `AgentCraft` | 技能/Agent/Harness | 用例与边界收集 | 契约设计 | 实现与打磨 | 评测与回归 | 发布 | 版本迭代、经验库 |
| `Career` | 专业方向与科研规划 | 方向情报、兴趣与能力盘点 | 路径规划、目标拆解 | 计划执行、材料准备 | 阶段评审、答辩预演 | 定稿提交 | 定期复盘、方向校准 |

> 场景代码取 `docs/02` §5 的域码，不是新增代码。

---

## 2. 单一场景落地步骤

以"课题调研"为例：

```
1. 在项目根放 AGENTS.md，scenario: Academic，声明六段映射与当前阶段
2. 建六个一级目录，空段放 README.md 说明原因
3. 把 context-persistence 引擎部署到 .workbuddy/context/ 并 init
4. 每个新产物按命名式命名，套 docs/02 中 Academic 域的扩展取值
5. 每回合末用 context-persistence capture；收尾 flush
6. 生成后跑 tools/structure_lint.py 做一次自检
```

---

## 3. 混合场景落地步骤

混合场景**先判据再动手**（`docs/01` §4.2）：

```
判据：两条工作流是否共享同一份输入与结论？
  ├─ 是 → 同一实例，不同阶段 → 直接填对应段，用文档类型受控值区分
  └─ 否 → 并行实例 → 每个实例建 W<nn>-<主体> 目录，内嵌完整六段
                    实例之间在 50-Sustain 建交叉引用台账
```

**示例**：一个项目同时含"软件系统开发"与"业务逻辑需求调研"，两者输入不同、结论各自成线 → 并行实例：

```
<项目根>/
├── AGENTS.md              scenario: Software + BusinessLogic
├── W01-CustomerPortal/
│   ├── 00-Ingest/ … 50-Sustain/
├── W02-BusinessRules/
│   ├── 00-Ingest/ … 50-Sustain/
└── 50-Sustain/            ← 根级沉淀层：实例间交叉引用台账
```

> 注意：并行实例时，根级 `50-Sustain` 与各实例内的 `50-Sustain` 职责不同 —— 根级管**跨实例**复用，实例内管**本实例**复盘。`docs/01` §3.1 对根级骨架的定义仍成立。

**一次生成（1.1.1 起）**：`scaffold.py` 的 `--instance` 可重复，格式 `<Wnn-主体>:<场景码>`。根级建共享六段，每个实例目录内嵌完整六段：

```bash
SKILL_DIR=<本 skill 根目录绝对路径>
python "$SKILL_DIR/tools/scaffold.py" <项目根> --scenario Software \
  --name "客户门户" --mix parallel \
  --instance W01-CustomerPortal:Software \
  --instance W02-BusinessRules:BusinessLogic
```

`--phases` 只作用于根级；实例内始终完整六段。给 `--instance` 时即使没写 `--mix parallel` 也自动按并行处理。

**两步法兜底（旧版本或手工补建）**：先建根级，再对每个实例目录各跑一次脚手架 ——

```bash
python "$SKILL_DIR/tools/scaffold.py" <项目根> --scenario Software --mix parallel
python "$SKILL_DIR/tools/scaffold.py" <项目根>/W01-CustomerPortal --scenario Software --name "客户门户"
python "$SKILL_DIR/tools/scaffold.py" <项目根>/W02-BusinessRules --scenario BusinessLogic --name "业务规则"
```

只写 `--mix parallel` 而不建实例目录时，脚本会在 `AGENTS.md` 与输出里留下兜底提示；`structure_lint.py` 给出 `§4.2` WARN，不硬判违规。

---

## 4. AGENTS.md 声明模板

```markdown
# <项目名> · 项目契约

## 场景声明
scenario: <Academic|BusinessLogic|Software|Reverse|AgentCraft|Career>
mix_mode: <single|parallel>
active_phase: <00-Ingest|10-Analyze|20-Build|30-Verify|40-Deliver|50-Sustain>

## 骨架说明
本项目采用 USP v1.1 六段骨架：
- 00-Ingest 输入 — <本项目具体放什么>
- 10-Analyze 分析 — <…>
- 20-Build 构建 — <…>
- 30-Verify 验证 — <…>
- 40-Deliver 交付 — <…>
- 50-Sustain 沉淀 — <…>

当前阶段：<段码+中文>，进入依据：<完成判据>

## 命名规范
- 命名式：aden-naming-standard v1.4 §5.1
- 结构规范：USP v1.1（docs/01）
- 本项目使用的扩展取值：<从 docs/02 列出用到的值>
- 状态后缀：只用 §5.6 五值

## 状态读取指令
动态状态（目标/进度/子目标/待决问题）从 .workbuddy/context/task_state.json 读取。
本文件只放静态声明，不写 time/progress/status。
```

**字段纪律**：`active_phase` 是唯一允许写"当前进度"的字段，且它是**静态快照**（场景切换时才改）。逐轮进度仍由 `task_state.json` 承载 —— 两者不重复。

---

## 5. 文件命名示例

套用上游 §5.1 命名式 `[组织前缀]-[文档类型]-[域]-[主体]-[版本][-状态][-语言][.ext]`。
**文档类型/域段用载体形**（段内大小写分词、去空格去下划线），详见 `docs/04-document-naming-scheme.md` §1：

| 场景 | 示例文件名 | 说明 |
| --- | --- | --- |
| 课题调研 | `PERS-ResearchProposal-Academic-儿子专业方向初探-v0.1-Draft.md` | 个人域，科研文档类型，Academic 域码 |
| 需求规格 | `AGI-RequirementSpec-Software-客户门户需求-v1.0-Review.docx` | 工作场景，上游组织前缀 |
| 技能规格 | `ADEN-SkillSpec-AgentCraft-上下文持久化-v1.3-Approved.md` | 集团资产，扩展文档类型 |
| 复盘记录 | `FAM-InformationNote-Career-学年规划复盘-v1.0-Draft.md` | 家庭域，用上游既有文档类型 |
| 双语并存 | `AGI-InformationNote-Software-系统盘点-v1.0-Approved-en.md` | 仅双语时加语言段 |

**注意**：示例中的中文主体段首字母概念不适用（中文无大小写），按上游 §4.3-2"宜每部分仅首字母大写"的精神，中文主体保持自然书写即可。

---

## 6. 与 context-persistence 的接缝

本规范的结构层与 `context-persistence` 技能的分工：

| 维度 | 本规范（USP） | context-persistence |
| --- | --- | --- |
| 管什么 | 目录长什么样、文件叫什么 | 任务状态怎么跨会话续上 |
| 静态前缀 | `AGENTS.md`（场景声明） | SOUL/IDENTITY/USER（身份） |
| 动态状态 | 不提供 | `task_state.json`（SSOT） |
| 日志 | 不提供 | journal/ 日志层 |
| 接缝 | `AGENTS.md` 指明状态文件位置 | 引擎读 `task_state.json` |

**组合用法**：AI 进项目 → 读 `AGENTS.md` 得静态骨架 → 跑 `context_manager.py layout` 得动态状态栏 → 按命名式写产物 → 收尾 `flush`。

---

## 7. 常见误用

| 误用 | 正确做法 |
| --- | --- |
| 为每个场景复制一套六段目录 | 一套骨架 + 场景投影（`docs/01` §4.2） |
| 把进度写进 `AGENTS.md` | 写进 `task_state.json` |
| 用 `Final` / `Done` / `最终版` 做状态 | 只用 §5.6 五值 |
| 科研产物挂 `AGI-` 前缀 | 用 `PERS-` / `FAM-`（`docs/02` §2） |
| 拿本地 Draft 域码当集团受控值 | 本地用途，升级须走 §9.3 |
| 校验器跑不通就凭手感判合规 | 只报"校验未完成" |

---

## 修订记录

| 版本 | 日期 | 变更 | 作者 |
| --- | --- | --- | --- |
| v1.0 | 2026-11-18 | 首次成文：六类场景投影、单一/混合落地步骤、AGENTS.md 模板、命名示例、引擎接缝、常见误用 | — |
| v1.1 | 2026-11-18 | §3 补 `scaffold.py --instance` 一次生成法与两步法兜底；明确 `--phases` 只作用于根级、实例内始终完整六段；声明 parallel 而无实例目录时由校验器给 WARN。条款实质未变 | — |
