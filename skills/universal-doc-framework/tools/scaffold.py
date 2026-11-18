#!/usr/bin/env python3
"""USP scaffold — 按 USP v1.1 生成一个新项目骨架。

纯 Python 3 标准库，无第三方依赖。用法：

    python scaffold.py <目标目录> --scenario Software [--name 项目名] [--mix single|parallel]
                       [--phases 00,10,20] [--with-context]
                       [--instance W01-Career:Career --instance W02-AgentCraft:AgentCraft]

行为纪律：
- 只创建不存在的对象；已存在的一律跳过并报告，绝不覆盖（对齐 §1.3 存量豁免）。
- 生成的骨架含六段目录 + 每段 README + 根 AGENTS.md / README.md。
- --instance 可重复，格式 `<Wnn-主体>:<场景码>`；根级建共享六段，每个实例目录内嵌完整六段（docs/01 §4.2）。
- 不给 --instance 但 --mix parallel 时只建根级骨架，并在 AGENTS.md 与输出里给出两步法兜底提示。
- --with-context 时在输出中提示需部署 context-persistence 引擎；本脚本不自动初始化（部署走该 skill 的 engine/DEPLOY.md）。
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date

PHASES = [
    ("00", "Ingest", "输入", "收集原始材料：选题、文献、干系人、现状资产、用例边界"),
    ("10", "Analyze", "分析", "建模、拆解、逆向解析、路径规划、框架设计"),
    ("20", "Build", "构建", "写出产物：代码、规格、报告初稿、复刻实现、科研执行"),
    ("30", "Verify", "验证", "测试、评审、对齐校验、UAT、答辩预演"),
    ("40", "Deliver", "交付", "上线、发布、提交、归档、定稿"),
    ("50", "Sustain", "沉淀", "复盘、经验库、复用资产、版本迭代、持续跟踪"),
]

SCENARIOS = {
    "Academic": ("选题、文献、资料", "研究框架、方法", "调研执行、初稿", "论证、评审", "报告定稿", "知识沉淀、后续选题"),
    "BusinessLogic": ("干系人、现状流程", "流程建模、拆解", "业务规则规格", "业务评审确认", "需求基线", "规则复用、变更跟踪"),
    "Software": ("需求收集", "设计", "开发", "测试 + UAT", "上线", "运维复盘、迭代"),
    "Reverse": ("资产盘点", "逆向解析、架构还原", "复刻实现", "对齐验证", "交付切换", "差异台账、复用件"),
    "AgentCraft": ("用例与边界收集", "契约设计", "实现与打磨", "评测与回归", "发布", "版本迭代、经验库"),
    "Career": ("方向情报、能力盘点", "路径规划、目标拆解", "计划执行、材料准备", "阶段评审、答辩预演", "定稿提交", "定期复盘、方向校准"),
}

INSTANCE_NAME_RE = re.compile(r"^W\d{2}-[A-Za-z0-9][A-Za-z0-9-]*$")

PHASE_README = """# {code}-{eng} · {zh}

**语义**：{semantic}

**本项目在这段放什么**：{mapping}

**完成判据**（USP v1.1 §3.1）：{criterion}

**命名**：套 `aden-naming-standard` §5.1；用 `{code}-{eng}` 段码定位。

> 空段应保留本 README 并说明原因（§3.3）。
"""

CRITERIA = [
    "输入清单登记完毕，来源可追溯",
    "分析结论成文，关键假设显式标注",
    "产物达到可验证状态",
    "验证记录齐备，缺陷有归属",
    "交付物有版本与状态，接收方确认",
    "可复用项已登记，回流到相关段",
]

AGENTS_TMPL = """# {name} · 项目契约

> 静态声明。动态状态从 `.workbuddy/context/task_state.json` 读取，不写在本文件。

## 场景声明

```yaml
scenario: {scenario}
mix_mode: {mix}
active_phase: {active}
```

## 骨架说明

本项目采用 USP v1.1 六段骨架（`docs/01-universal-folder-structure.md`），由 `scenario: {scenario}` 投影：

{phase_lines}

当前阶段：`{active}`。
{instance_section}
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
生成于 {today} · scaffold.py · USP v1.1
"""

ROOT_README_TMPL = """# {name}

由 USP v1.1 脚手架生成。场景 `{scenario}`，模式 `{mix}`。

| 文件 | 作用 |
| --- | --- |
| `AGENTS.md` | AI 入口：场景声明与骨架说明 |
| `00-Ingest/` … `50-Sustain/` | 六段骨架 |
| `docs/`（可选） | 规范正文（复制自样板工作区或引用外部；本脚本不自动创建） |
| `.workbuddy/context/` | context-persistence 动态状态 |

{instance_list}
生成于 {today}。
"""


def write_new(path: str, content: str, created: list, skipped: list) -> None:
    """只写新文件；已存在则跳过，不覆盖。"""
    if os.path.exists(path):
        skipped.append(os.path.relpath(path, os.getcwd()))
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    created.append(os.path.relpath(path, os.getcwd()))


def build_one(target: str, scenario: str, name: str, mix: str, phases: set,
              with_context: bool, instance_section: str = "",
              instance_list: str = "") -> tuple[list, list]:
    """在一处目标目录建一套六段骨架；返回 (新建, 跳过)，不自行打印。"""
    os.makedirs(target, exist_ok=True)
    created, skipped = [], []

    mapping = SCENARIOS[scenario]
    active = min(phases) if phases else "00"
    active_dir = next((f"{c}-{e}" for c, e, _, _ in PHASES if c == active), "00-Ingest")

    phase_lines = "\n".join(
        f"- `{code}-{eng}` {zh} — {mapping[i]}" for i, (code, eng, zh, _) in enumerate(PHASES)
    )
    today = date.today().isoformat()

    write_new(os.path.join(target, "AGENTS.md"),
              AGENTS_TMPL.format(name=name, scenario=scenario, mix=mix, active=active_dir,
                                 phase_lines=phase_lines, today=today,
                                 instance_section=instance_section), created, skipped)
    write_new(os.path.join(target, "README.md"),
              ROOT_README_TMPL.format(name=name, scenario=scenario, mix=mix, today=today,
                                      instance_list=instance_list), created, skipped)

    for i, (code, eng, zh, semantic) in enumerate(PHASES):
        d = os.path.join(target, f"{code}-{eng}")
        if not os.path.isdir(d):
            os.makedirs(d, exist_ok=True)
            created.append(os.path.relpath(d, os.getcwd()))
        else:
            skipped.append(os.path.relpath(d, os.getcwd()))
        if phases and code not in phases:
            reason = f"（本项目未启用该阶段，{scenario} 场景在此阶段无内容）"
        else:
            reason = ""
        write_new(os.path.join(d, "README.md"),
                  PHASE_README.format(code=code, eng=eng, zh=zh, semantic=semantic,
                                      mapping=mapping[i] + reason, criterion=CRITERIA[i]),
                  created, skipped)

    if with_context:
        ctx = os.path.join(target, ".workbuddy", "context")
        if os.path.isdir(ctx):
            skipped.append(os.path.relpath(ctx, os.getcwd()))
        else:
            created.append(os.path.relpath(ctx, os.getcwd()) + "/  (请在其中部署 context-persistence 引擎并 init)")

    return created, skipped


def build(target: str, scenario: str, name: str, mix: str, phases: set,
          with_context: bool, instances: list[tuple[str, str]]) -> int:
    if scenario not in SCENARIOS:
        print(f"error: 未知场景 {scenario!r}，可选：{', '.join(SCENARIOS)}", file=sys.stderr)
        return 2

    created, skipped = [], []
    instance_section, instance_list = "", ""

    if instances:
        rows = ["", "## 并行实例", "", "| 实例目录 | 场景 | 职责 |", "|---|---|---|"]
        for d, s in instances:
            rows.append(f"| `{d}` | `{s}` | {SCENARIOS[s][0]} |")
        rows.append("")
        rows.append("> 根级六段承载共享输入与跨实例沉淀；各实例内嵌完整六段（docs/01 §4.2）。实例目录已由本脚本生成。")
        # 末尾留空行，避免引用块与后续标题粘连
        instance_section = "\n".join(rows) + "\n"
        instance_list = "\n".join(
            f"- `{d}` （`{s}`）：内嵌完整六段" for d, s in instances
        ) + "\n"
    elif mix == "parallel":
        instance_section = "\n".join([
            "", "## 并行实例", "",
            "> 本声明为并行模式，但尚未生成 `W<nn>-<主体>` 实例目录。",
            "> 兜底做法：对每个实例目录再跑一次 scaffold.py ——",
            '> `python scaffold.py <root>/W01-<主体> --scenario <场景> --name "<实例名>"`',
            "> 或改用 `--instance W01-<主体>:<场景>` 一次生成。",
            "",
        ])
        instance_list = "> 并行实例目录未生成；见 AGENTS.md「并行实例」节的两步法兜底。\n"

    c, s = build_one(target, scenario, name, mix, phases, with_context,
                     instance_section, instance_list)
    created += c
    skipped += s

    for d, inst_scenario in instances:
        inst_name = d.split("-", 1)[1] if "-" in d else d
        c, s = build_one(os.path.join(target, d), inst_scenario, inst_name,
                         "single", set(), False)
        created += c
        skipped += s

    active = min(phases) if phases else "00"
    active_dir = next((f"{c}-{e}" for c, e, _, _ in PHASES if c == active), "00-Ingest")
    print(f"scaffold ok: {target}")
    print(f"  scenario={scenario}  mix={mix}  active={active_dir}")
    if instances:
        print(f"  实例 {len(instances)} 个：" + ", ".join(d for d, _ in instances))
    elif mix == "parallel":
        print("  [WARN] mix=parallel 未生成实例目录；AGENTS.md 已写入两步法兜底，或用 --instance")
    print(f"  新建 {len(created)} 项，跳过 {len(skipped)} 项（存量不覆盖）")
    for p in created:
        print(f"  + {p}")
    for p in skipped:
        print(f"  = {p}  [已存在，跳过]")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="USP v1.1 项目骨架生成器")
    ap.add_argument("target", help="目标目录（不存在则创建）")
    ap.add_argument("--scenario", required=True, choices=list(SCENARIOS), help="场景类型")
    ap.add_argument("--name", default=None, help="项目名（默认取目录名）")
    ap.add_argument("--mix", default="single", choices=["single", "parallel"], help="单一/混合场景")
    ap.add_argument("--phases", default=None, help="只启用指定段，逗号分隔，如 00,10,20（默认全段）")
    ap.add_argument("--with-context", action="store_true", help="声明需要 context-persistence 状态层")
    ap.add_argument("--instance", action="append", default=[], metavar="Wnn-主体:场景",
                    help="并行实例，可重复；每个实例内嵌完整六段（如 W01-Career:Career）")
    args = ap.parse_args()

    instances, seen = [], set()
    for raw in args.instance:
        if ":" not in raw:
            print(f"error: --instance 格式应为 <Wnn-主体>:<场景码>，收到 {raw!r}", file=sys.stderr)
            return 2
        d, s = (x.strip() for x in raw.split(":", 1))
        if not INSTANCE_NAME_RE.match(d):
            print(f"error: 实例目录名 {d!r} 应为 W<nn>-<主体>，两位数字、连字符、无空格下划线", file=sys.stderr)
            return 2
        if s not in SCENARIOS:
            print(f"error: 实例 {d!r} 的场景 {s!r} 未知，可选：{', '.join(SCENARIOS)}", file=sys.stderr)
            return 2
        if d in seen:
            print(f"error: 实例目录名重复 {d!r}", file=sys.stderr)
            return 2
        seen.add(d)
        instances.append((d, s))

    mix = "parallel" if instances else args.mix
    if instances and args.mix == "single":
        print("info: 提供 --instance 时自动按 parallel 处理", file=sys.stderr)

    phases = set()
    if args.phases:
        phases = {p.strip().zfill(2) for p in args.phases.split(",") if p.strip()}
        bad = phases - {c for c, _, _, _ in PHASES}
        if bad:
            print(f"error: 未知段码 {sorted(bad)}", file=sys.stderr)
            return 2

    name = args.name or os.path.basename(os.path.normpath(args.target))
    return build(os.path.abspath(args.target), args.scenario, name, mix,
                 phases, args.with_context, instances)


if __name__ == "__main__":
    sys.exit(main())
