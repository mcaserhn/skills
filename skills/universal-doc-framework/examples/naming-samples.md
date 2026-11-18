# 命名示例对照

本文件只展示命名规则，文件名本身不作为产物命名范例。合规示例均经 `aden-naming-standard` v1.4 的 `naming-lint.js` 验证。

## 合规示例

| 场景 | 产物 | 文件名 |
| --- | --- | --- |
| 软件开发 | 客户门户需求规格 | `ADEN-RequirementSpec-Software-客户门户-v1.0-Draft.md` |
| ADEN 基建·服务器运维 | 服务器操作指引 | `AGI-InformationNote-10Server-服务器巡检-v1.0-Approved.md` |
| 课题调研 | 儿子方向立项 | `FAM-ResearchProposal-Academic-儿子方向初探-v0.1-Draft.md` |
| 技能打造 | 上下文持久化规格 | `ADEN-SkillSpec-AgentCraft-上下文持久化-v1.3-Approved.md` |
| 软件开发 | 系统盘点 | `AGI-InventoryReport-Software-系统盘点-v1.0-Review.md` |

要点：

- 文档类型与域段用**载体形**：`InformationNote`、`10Server`、`RequirementSpec`，段内靠大小写分词，不加连字符。
- 域段随**具体场景**选：软件开发用 `Software`，服务器运维才用 `10Server`。
- 阶段不写进文件名，由所在目录定位（如 `00-Ingest/`）。
- 状态只用 `-Draft / -Review / -Approved / -Signed / -Retired` 五值，置于版本之后。

## 不合规示例（仅作反例，勿用于文件名）

| 反例 | 问题 | 正确写法 |
| --- | --- | --- |
| `ADEN-Information-Note-10Server-巡检-v1.0-Draft.md` | 段内插连字符，违反上游 §5.2 | `ADEN-InformationNote-10Server-巡检-v1.0-Draft.md` |
| `ADEN-Information Note-10Server-巡检-v1.0-Draft.md` | 段内有空格 | 同上 |
| `ADEN-RequirementSpec-10_Server-客户门户-v1.0-Draft.md` | 文件名内用下划线且域不符场景 | `ADEN-RequirementSpec-Software-客户门户-v1.0-Draft.md` |
| `ADEN-RequirementSpec-Software-客户门户-v1.0-Final.md` | `Final` 不是受控状态值 | `...-v1.0-Approved.md` |
| `AGI-InformationNote-00-Ingest-需求访谈-v1.0-Draft.md` | 阶段段写进文件名，占了域段位置 | 放进 `00-Ingest/`，域段取受控域码 |

> 上游 lint 对空格/下划线的「建议形式」会给出 `Information-Note`，该建议违反 §5.2，属上游资产缺陷，不照抄。详见 `docs/04` §1.2 与 §6。
