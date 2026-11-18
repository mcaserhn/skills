# 变更记录

## v1.1.0 — 2026-11-18

首个自包含分发版本。从此前仅含 `SKILL.md` 的薄入口升级为完整技能包。

- 包内收录结构规范与命名体系正文 `docs/01`–`05`（USP v1.1 / DocName v1.0 / NamingSystem v1.0）。
- 包内收录 `tools/scaffold.py` 与 `tools/structure_lint.py`，安装后不依赖宿主工作区绝对路径。
- 新增 `tools/sync_from_workspace.py`，支持 `--check` 漂移检查与按源同步。
- 新增 `examples/sample-project/` 与 `examples/naming-samples.md`。
- `SKILL.md` 从「指向样板工作区」改为「指向包内资产」，补齐依赖声明与失败分支。
- 修复此前复检发现的 9 类偏差：全仓版本指针统一 USP v1.1、校验顺序、引擎文件名、载体形示例、交叉引用、前缀计数、大小写与错字等。
