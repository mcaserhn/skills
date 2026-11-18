# 04 · 文档名称方案（DocName v1.0）

> **文档性质**：方案正文。规定文档名称的取值体系、书写形态与 AI 自动选名规则。
> **权威来源**：`aden-naming-standard` v1.4 正文（§4.3 / §5.1–§5.7 / 附录 A）与其研究底稿 `docs/11`（§2.1 / §2.6 / §5.3 / §5.6）。本文**不改写**上游条款，只做"形态澄清 + 取值汇总 + 自动选名决策"。冲突时以上游正文为准。
> **要解决的双需求**：① ADEN 组织工作 —— 沿用集团既有受控词表与命名式；② 本课题六类场景 —— 复用同一骨架、扩展取值、AI 按场景自动选名。
> **状态**：v1.0 · Draft · 2026-11-18。

---

## 1. 核心发现：受控值有两形态

上游规范存在一处**未被显式命名的事实**（底稿 §2.6 原文 + 规范 §4.3-4 / §5.2 共同蕴涵）：

> **受控值在注册表里是一种写法，进入文件名时是另一种写法。两者一一映射，不是二选一。**

| 形态 | 定义 | 用在 | 例 |
| --- | --- | --- | --- |
| **词典形**（Lexical Form） | 受控词表登记的自然语言写法，供人读、供检索 | 注册表、正文引用、登记表 | `Information Note`、`10_Server` |
| **载体形**（Carrier Form） | 按字符纪律转换后的写法，供文件名使用 | 文件名、目录名（`output/` 等受管辖产物） | `InformationNote`、`10Server` |

### 1.1 转换规则（词典形 → 载体形）

1. **段间**用连字符 `-`（唯一分隔符）；
2. **段内分词靠大小写**：每个词首字母大写、其余小写（底稿 §2.6-2、规范 §4.3-2）；
3. 去掉词典形中的**空格**与**下划线**；
4. **不应**在段内额外插入连字符（规范 §5.2 明令）。

### 1.2 三种写法的定性

| 写法 | 定性 | 依据 |
| --- | --- | --- |
| `InformationNote` | ✅ **正确**（载体形） | 段内大小写分词，无空格无下划线 |
| `Information-Note` | ❌ 错误 | 段内插连字符，违反 §5.2；**lint 的建议形式在此处是 bug** |
| `Information Note` | △ 仅词典形 | 文件名中新产物禁用空格（§4.3-3）；存量按 §1.3 豁免 |

> **校验器现状**：JS 与 Python 两个 lint 都只查"禁用字符是否出现"，没有"段值必须取受控值"的校验。所以连写能通过 = 它字符合规，**不是**侥幸；而 lint 对空格/下划线的"建议形式"（换成连字符）在本规范下是错的。升级 lint 属上游资产变更，须另行决策（见 §6）。

---

## 2. 文档名称统一式

沿用上游 §5.1，一个字不改：

```
[组织前缀]-[文档类型]-[域]-[主体]-[版本][-状态][-语言][.扩展名]
```

各段取值来源：

| 段 | 必填 | 取值来源 | 本文章节 |
| --- | --- | --- | --- |
| 组织前缀 | 应填 | §3.1 | ADEN 既有 2 值 + 本地扩展 2 值 |
| 文档类型 | 宜填 | §3.2 | ADEN 既有 5 类 + 本课题扩展 8 类 |
| 域 | 宜填 | §3.3 | ADEN 既有 9 域 + 本课题扩展 6 域码 |
| 主体 | 应填 | 自由文本，段内首字母大写（载体形规则） | — |
| 版本 | 宜填 | `-vX.Y`，第三段仅不兼容修订 | 上游 §5.4 |
| 状态 | 宜填 | 五值受控，置于版本之后 | 上游 §5.6 / 本文 §3.4 |
| 语言 | 可选 | `-zh` / `-en`，仅双语并存时 | 上游 §5.7 |

> **目录例外**：`docs/`、`context/`、`app/`、`tools/`、`config/`、`.tmp/` 下的文件名不适用本式（上游 §1.2-6/7）；六段骨架目录名 `00-Ingest` 等按 USP v1.1 `docs/01`。

---

## 3. 受控取值总表

标注来源：`【ADEN】`=集团既有，工作场景必须用；`【本地】`=本课题扩展 Draft，见 `docs/02`。

### 3.1 组织前缀

| 词典形 | 载体形 | 来源 | 适用 |
| --- | --- | --- | --- |
| `AGI` | `AGI` | 【ADEN】 | 基础设施类文档 |
| `ADEN` | `ADEN` | 【ADEN】 | 合同与记录类 |
| `PERS` | `PERS` | 【本地】 | 个人事务 |
| `FAM` | `FAM` | 【本地】 | 家庭事务（含子女教育科研） |

### 3.2 文档类型（13 类）

**ADEN 既有 5 类**（底稿 §2.1，工作场景优先）：

| 词典形 | 载体形 | 中文 | 用什么时候 |
| --- | --- | --- | --- |
| `Exploratory Study` | `ExploratoryStudy` | 预研报告 | 技术预研、可行性研究 |
| `Information Note` | `InformationNote` | 信息说明/操作指引 | 说明、指引、盘点记录 |
| `Position Note` | `PositionNote` | 立场说明 | 观点、方案比选结论 |
| `Group Standard` | `GroupStandard` | 集团标准 | 正式发布级规范 |
| `Group Service` | `GroupService` | 集团服务 | 政策类 |

**本课题扩展 8 类**（【本地】Draft）：

| 词典形 | 载体形 | 中文 | 用什么时候 |
| --- | --- | --- | --- |
| `Research Proposal` | `ResearchProposal` | 课题/科研立项书 | 开题、立项 |
| `Literature Review` | `LiteratureReview` | 文献综述 | 文献梳理 |
| `Research Note` | `ResearchNote` | 科研笔记 | 实验记录、随记 |
| `Experiment Report` | `ExperimentReport` | 实验/验证报告 | 实验结果、测试报告 |
| `Career Plan` | `CareerPlan` | 发展规划 | 专业方向、路径规划 |
| `Skill Spec` | `SkillSpec` | 技能/Agent 契约 | skill、Agent、Harness 规格 |
| `Requirement Spec` | `RequirementSpec` | 需求规格 | 软件或业务逻辑需求 |
| `Inventory Report` | `InventoryReport` | 盘点报告 | 系统盘点、资产清单 |

### 3.3 域

**ADEN 既有 9 技术域**（底稿 §2.3，载体形去下划线）：

| 词典形 | 载体形 | 词典形 | 载体形 |
| --- | --- | --- | --- |
| `00_FrontEnd` | `00FrontEnd` | `50_Backup&Recovery` | `50BackupRecovery` |
| `10_Server` | `10Server` | `60_Shared Folder` | `60SharedFolder` |
| `20_Networking` | `20Networking` | `70_Office365` | `70Office365` |
| `30_Monitor&Log` | `30MonitorLog` | `80_Patch` | `80Patch` |
| `40_Security&Compliance` | `40SecurityCompliance` | — | — |

> **`&` 的处理**：词典形里的 `&` 是英文连接符，载体形中去掉（不是换成 `And`）——`30MonitorLog` 而非 `30MonitorAndLog`。这是"去非字母数字符号"的直接结果，保持词典形与载体形可机械互推。

**本课题扩展 6 域码**（【本地】Draft，单词无空格，载体形=词典形）：`Software` / `BusinessLogic` / `Reverse` / `AgentCraft` / `Academic` / `Career`

### 3.4 状态后缀（五值，不扩展）

`-Draft` → `-Review` → `-Approved` → `-Signed` → `-Retired`（上游 §5.6，置于版本之后）。沿用，散词一律禁止。

---

## 4. AI 按场景自动选名决策表

AI **不应即席造词**（底稿 §5.6 R-AB-6）。按以下四步查表，每步只从受控值里选；判不了就问用户。

### 4.1 第一步：组织前缀

| 条件 | 选值 |
| --- | --- |
| ADEN 组织工作产物（受管辖文档） | `AGI`（基础设施）/ `ADEN`（合同、记录、业务） |
| 个人事务 | `PERS` |
| 家庭 / 子女教育科研 | `FAM` |

### 4.2 第二步：文档类型（按产物性质）

| 产物性质 | 优先选 | 备选 |
| --- | --- | --- |
| 立项、开题 | `ResearchProposal` | `ExploratoryStudy` |
| 文献梳理 | `LiteratureReview` | `InformationNote` |
| 实验记录、随笔 | `ResearchNote` | — |
| 测试 / 实验结果 | `ExperimentReport` | `InformationNote` |
| 需求规格 | `RequirementSpec` | `InformationNote` |
| 系统盘点 | `InventoryReport` | `InformationNote` |
| skill / Agent / Harness 规格 | `SkillSpec` | `GroupStandard` |
| 发展规划、路径 | `CareerPlan` | `PositionNote` |
| 预研、可行性 | `ExploratoryStudy` | — |
| 操作指引、说明 | `InformationNote` | — |
| 方案比选、立场 | `PositionNote` | — |
| 正式发布规范 | `GroupStandard` | — |
| 政策类 | `GroupService` | — |

> **优先级规则**：工作场景**先**在 ADEN 5 类里找，找不到才用扩展 8 类。避免本地取值侵蚀集团词表。

### 4.3 第三步：域

| 场景 | 选值 | 说明 |
| --- | --- | --- |
| 软件开发全流程 | `Software` | 本课题域码 |
| 业务逻辑需求 | `BusinessLogic` | 本课题域码 |
| 盘点逆向复刻 | `Reverse` | 本课题域码 |
| 技能/Agent 打造 | `AgentCraft` | 本课题域码 |
| 课题调研 | `Academic` | 本课题域码 |
| 专业与科研规划 | `Career` | 本课题域码 |
| ADEN 基建工作（服务器/网络等） | `10Server` 等 9 域载体形 | 集团技术域 |

### 4.4 第四步：状态（随六段骨架推进）

| 当前阶段 | 默认状态 | 说明 |
| --- | --- | --- |
| `00-Ingest` / `10-Analyze` / `20-Build` | `-Draft` | 草稿 |
| `30-Verify` | `-Review` | 评审中 |
| `40-Deliver` | `-Approved` | 定稿交付 |
| 正式签署后 | `-Signed` | — |
| 退役 | `-Retired` | — |

> 同一版本不应存在两种状态文件并存；状态推进**覆盖**旧文件，不另存副本（上游 §5.6）。

### 4.5 组装与输出

1. 取四段受控值 + 主体（自由，段内首字母大写）+ 版本；
2. 按 §1.1 把各受控段转为**载体形**；
3. 段间用 `-` 连接，扩展名前用 `.`；
4. 跑 lint 校验；不合规按清单改，**不凭手感**。

**完整示例**：

| 场景（§4.3） | 产物 | 输出文件名 |
| --- | --- | --- |
| 软件开发 | 客户门户需求规格 | `ADEN-RequirementSpec-Software-客户门户-v1.0-Draft.md` |
| ADEN 基建·服务器运维 | 服务器操作指引 | `AGI-InformationNote-10Server-服务器巡检-v1.0-Approved.md` |
| 课题调研 | 儿子方向立项 | `FAM-ResearchProposal-Academic-儿子方向初探-v0.1-Draft.md` |
| 技能打造 | 上下文持久化规格 | `ADEN-SkillSpec-AgentCraft-上下文持久化-v1.3-Approved.md` |
| 软件开发 | 系统盘点 | `AGI-InventoryReport-Software-系统盘点-v1.0-Review.md` |

> **域字段随场景走，不按笼统的"ADEN 工作"套用**：第 1、5 行均为"软件开发"场景，故域取 `Software`；第 2 行场景是服务器运维，命中 §4.3 第 7 行"ADEN 基建工作（服务器/网络等）"，故域取 `10Server`；第 3、4 行各按其课题域码。场景栏写明具体场景，域的来源即可逐行追溯。

---

## 5. 与三层治理的接缝

| 层 | 本文贡献 |
| --- | --- |
| 命名层（上游） | §1 双形态澄清 + §3 取值总表 —— **不改上游，只消歧** |
| 结构层（`docs/01`） | §4.4 状态随六段推进 —— 文档名称与阶段骨架对齐 |
| 识别层（`AGENTS.md` + skill） | §4 决策表 —— AI 读场景声明即可自动选名 |

**skill 的职责**：`universal-doc-framework`（通用文档骨架与规范）与本方案配合 —— 生成骨架时按 §4 选名；方案正文留在本文，skill 只引用不复制（对齐"规则单一权威"）。

---

## 6. 已知边界与待办

| # | 事项 | 处置 |
| --- | --- | --- |
| 1 | lint 的"建议形式"在空格/下划线处给出连字符，与 §5.2 冲突 | 属上游资产，**不擅改**；升级 lint 须另行决策 |
| 2 | `&` 在载体形中去掉（`30MonitorLog`），需确认是否可读 | 本文按"去非字母数字"处理；如需保留应走 §9.3 登记 |
| 3 | 本地扩展取值（PERS/FAM/8 类/6 域）为 Draft | 见 `docs/02`；升级须走上游 §9.3 |
| 4 | 主体段含中文时首字母大写规则不适用 | 中文主体保持自然书写（同 `docs/03` §5 注） |

---

## 修订记录

| 版本 | 日期 | 变更 | 作者 |
| --- | --- | --- | --- |
| v1.0 | 2026-11-18 | 首次成文：双形态机制、统一命名式、13 类文档类型 + 4 前缀 + 15 域取值总表、AI 四步决策表、与三层治理接缝 | — |
