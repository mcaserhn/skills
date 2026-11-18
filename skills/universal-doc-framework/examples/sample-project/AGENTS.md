# 示例项目 · 项目契约

> 静态声明。动态状态从 `.workbuddy/context/task_state.json` 读取，不写在本文件。

## 场景声明

```yaml
scenario: Software
mix_mode: single
active_phase: 00-Ingest
```

## 骨架说明

本项目采用 USP v1.1 六段骨架（`docs/01-universal-folder-structure.md`），由 `scenario: Software` 投影：

- `00-Ingest` 输入 — 需求收集
- `10-Analyze` 分析 — 设计
- `20-Build` 构建 — 开发
- `30-Verify` 验证 — 测试 + UAT
- `40-Deliver` 交付 — 上线
- `50-Sustain` 沉淀 — 运维复盘、迭代

当前阶段：`00-Ingest`。

## 命名规范

- 命名式：`aden-naming-standard` v1.4 §5.1
- 命名体系全景：`docs/05-naming-system.md`（9 类对象，AI 按对象类型选式）
- 文档名称方案：`docs/04-document-naming-scheme.md`（双形态 + 选名表）
- 结构规范：USP v1.1（docs/01）
- 扩展取值：docs/02（本地 Draft）
- 状态后缀：只用 §5.6 五值

## 状态读取指令

动态状态从 `.workbuddy/context/task_state.json` 读取；本文件只放静态声明。

---
生成于 2026-11-18 · scaffold.py · USP v1.1
