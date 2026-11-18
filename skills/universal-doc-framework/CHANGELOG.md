# 变更记录

## v1.1.2 — 2026-11-18

划清「骨架」与「内容」的职责，防止脚手架预置未经共构的内容（由 Zoho 课题实战触发）。

- **新增 `place_doc.py`**：产物落位器。受控值白名单校验 type/domain/prefix/status/phase，按 `docs/04` §2 统一式组装载体形文件名，状态按段位推导；**只建元数据头 + 空章节骨架，绝不写内容**，幂等不覆盖。
- **SKILL.md 新增 §4.3.1 硬纪律**：脚手架只建空骨架、不预置内容文档；doc-framework 管语法（名字/段位），SPP 等内容技能管语义（写什么/凭什么）。§4.3.2 给按需落位用法。
- **`docs/03` 升 v1.2，新增 §7 接缝**：SPP 产物→文档类型→默认段位映射表 + 典型工作流；原「常见误用」顺延为 §8。
- `sync_from_workspace.py` 把 `place_doc.py` 纳入同步清单。

## v1.1.1 — 2026-11-18

补齐混合场景实例目录的落地能力（由实战反馈触发）。

- `scaffold.py` 新增可重复的 `--instance <Wnn-主体>:<场景码>`：根级建共享六段，每个实例目录内嵌完整六段；`--phases` 只作用于根级。
- 不给 `--instance` 但写 `--mix parallel` 时，脚本在 `AGENTS.md` 与输出里保留两步法兜底提示（旧行为不破坏）。
- `structure_lint.py` 检查每个 `W<nn>-<主体>` 实例目录的六段与 `AGENTS.md` 字段；声明 parallel 却无实例目录时给 `§4.2` WARN，不硬判违规。
- `docs/03` 升 v1.1，补一次生成法与两步法兜底；`docs/01` §4.2 补落地提示；`SKILL.md` 同步工作流与版本号。
- 修正结构校验器有 WARN 时的结论文案，避免把非命名 WARN 说成「命名校验未完成」。
- `sync_from_workspace.py` 的比较与复制均把行尾归一化为 LF：消除 Windows CRLF 造成的整文件伪漂移，也保证包内工具的 shebang 在 Linux/macOS 可直接执行。
- 并行实例段落末尾补空行，避免 `AGENTS.md` / `README.md` 中引用块与后续标题粘连。

## v1.1.0 — 2026-11-18

首个自包含分发版本。从此前仅含 `SKILL.md` 的薄入口升级为完整技能包。

- 包内收录结构规范与命名体系正文 `docs/01`–`05`（USP v1.1 / DocName v1.0 / NamingSystem v1.0）。
- 包内收录 `tools/scaffold.py` 与 `tools/structure_lint.py`，安装后不依赖宿主工作区绝对路径。
- 新增 `tools/sync_from_workspace.py`，支持 `--check` 漂移检查与按源同步。
- 新增 `examples/sample-project/` 与 `examples/naming-samples.md`。
- `SKILL.md` 从「指向样板工作区」改为「指向包内资产」，补齐依赖声明与失败分支。
- 修复此前复检发现的 9 类偏差：全仓版本指针统一 USP v1.1、校验顺序、引擎文件名、载体形示例、交叉引用、前缀计数、大小写与错字等。
- 安装说明修正为集合仓库布局：从 `mcaserhn/skills` 克隆后拷贝 `skills/universal-doc-framework/`，而不是把整个仓库克隆成单个技能目录。
