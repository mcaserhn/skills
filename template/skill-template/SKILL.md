---
name: skill-template
description: >
  <One sentence: what this skill does.> Use when <trigger scenario>.
  NOT for <excluded scenario>.
license: MIT
metadata:
  version: "0.1.0"
  status: experimental
---

# <Skill title>

## 定位 / Positioning

<This skill solves <problem>. It does not solve <non-goal>.>

## 何时触发 / When to trigger

- <Scenario 1>
- <Scenario 2>
- NOT for: <excluded scenario>

## 执行流程 / How it runs

1. ...
2. ...
3. ...

## 路由表 / Routing table

| 触发场景 | 读取 |
|---|---|
| <Scenario> | `references/<file>.md` |
| <Scenario needing a template> | `assets/<file>.md` |

## 输出前检查 / Pre-output checklist

- [ ] ...
- [ ] ...
