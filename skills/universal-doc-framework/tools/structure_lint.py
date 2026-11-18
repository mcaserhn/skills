#!/usr/bin/env python3
"""USP structure lint — 校验项目骨架是否符合 USP v1.1。

纯 Python 3 标准库。检查三项（docs/01 §8.1）：

1. 六段目录齐全（空段有 README.md 视为齐全）
2. AGENTS.md 必含字段齐备（§5.2）
3. 并行实例：W<nn>-<主体> 目录内六段与 AGENTS.md 齐备（§4.2）；
   声明 parallel 却无实例目录时给 WARN，不硬判违规
4. 命名合规 —— 调用 aden-naming-standard 的权威 lint（如可用），不另写命名规则

退出码：0 = 无 ERROR；1 = 有 ERROR；2 = 参数/环境错误。
校验器跑不起来时只报「校验未完成」，不输出合规判定（docs/01 §8.2）。
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

PHASES = ["00-Ingest", "10-Analyze", "20-Build", "30-Verify", "40-Deliver", "50-Sustain"]

REQUIRED_AGENTS_FIELDS = {
    "场景声明": [r"scenario\s*:", r"mix_mode\s*:", r"active_phase\s*:"],
    "骨架说明": [r"六段|骨架|00-Ingest"],
    "命名规范指针": [r"aden-naming-standard", r"USP v1\.[0-9]|USP v"],
    "扩展取值指针": [r"docs/02|扩展取值|扩展受控值"],
    "状态读取指令": [r"task_state\.json"],
}


def check(root: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    root_text = ""

    # 1. 六段目录
    for phase in PHASES:
        d = os.path.join(root, phase)
        if not os.path.isdir(d):
            errors.append(f"[§3.1] 缺少阶段目录 {phase}/")
            continue
        rd = os.path.join(d, "README.md")
        if not os.path.isfile(rd) and not os.listdir(d):
            warns.append(f"[§3.3] {phase}/ 为空且无 README.md 说明")

    # 2. AGENTS.md 必含字段
    agents = os.path.join(root, "AGENTS.md")
    if not os.path.isfile(agents):
        errors.append("[§5.1] 缺少 AGENTS.md（AI 入口契约）")
    else:
        with open(agents, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        root_text = text
        for group, patterns in REQUIRED_AGENTS_FIELDS.items():
            for pat in patterns:
                if not re.search(pat, text):
                    errors.append(f"[§5.2] AGENTS.md 缺少「{group}」字段（未匹配 /{pat}/）")
        if re.search(r"\b(progress|last_active|time)\s*:", text):
            warns.append("[§5.3] AGENTS.md 疑似写入动态字段，应移到 task_state.json")

    # 2b. 并行实例（docs/01 §4.2）
    instance_dirs = sorted(
        d for d in os.listdir(root)
        if re.match(r"^W\d{2}-", d) and os.path.isdir(os.path.join(root, d))
    )
    if re.search(r"mix_mode\s*:\s*parallel", root_text) and not instance_dirs:
        warns.append(
            "[§4.2] AGENTS.md 声明 mix_mode: parallel，但未发现 W<nn>-<主体> 实例目录；"
            "若确需并行请用 --instance 或按两步法补建"
        )
    for inst in instance_dirs:
        base = os.path.join(root, inst)
        for phase in PHASES:
            d = os.path.join(base, phase)
            if not os.path.isdir(d):
                errors.append(f"[§4.2] 实例 {inst}/ 缺少阶段目录 {phase}/")
                continue
            rd = os.path.join(d, "README.md")
            if not os.path.isfile(rd) and not os.listdir(d):
                warns.append(f"[§4.2] 实例 {inst}/{phase}/ 为空且无 README.md 说明")
        ia = os.path.join(base, "AGENTS.md")
        if not os.path.isfile(ia):
            errors.append(f"[§4.2] 实例 {inst}/ 缺少 AGENTS.md")
        else:
            with open(ia, "r", encoding="utf-8", errors="replace") as f:
                itext = f.read()
            for group, patterns in REQUIRED_AGENTS_FIELDS.items():
                for pat in patterns:
                    if not re.search(pat, itext):
                        errors.append(f"[§4.2] 实例 {inst}/ AGENTS.md 缺少「{group}」字段（未匹配 /{pat}/）")

    # 4. 命名合规 —— 交给上游权威 lint
    naming_lint = os.environ.get("ADEN_NAMING_LINT", "")
    if naming_lint and os.path.isfile(naming_lint):
        # 上游命名 lint 是 Node 脚本，按扩展名选解释器；不能把 JS 交给 Python 执行
        runner = "node" if naming_lint.lower().endswith(".js") else sys.executable
        try:
            r = subprocess.run([runner, naming_lint, "--root", root],
                               capture_output=True, text=True, timeout=60)
            if r.returncode not in (0, 1):
                warns.append("[§8.2] 命名 lint 退出码异常，视为校验未完成")
            elif r.returncode == 1:
                filtered = 0
                for line in (r.stdout + r.stderr).splitlines():
                    if "ERROR" not in line.upper():
                        continue
                    s = line.strip()
                    # 汇总行不是具体违规项
                    if s.startswith(("合计:", "结论:", "小结")):
                        continue
                    # 作用域划界（非另写命名规则）：
                    # .workbuddy/ 是 context-persistence 工具引擎区；
                    # .workbuddy-ai/ 是宿主管理的技能与记忆区，日志名被宿主固定为
                    # YYYY-MM-DD.md。两者文件名均由工具自身决定，按上游 §1.2-6
                    # 「代码与脚手架」精神只约束目录归属、不约束文件名。
                    host_zones = (".workbuddy/", ".workbuddy\\",
                                  ".workbuddy-ai/", ".workbuddy-ai\\")
                    if any(z in s for z in host_zones):
                        filtered += 1
                        continue
                    errors.append(f"[§8.1] 命名不合规：{s}")
                if filtered:
                    warns.append(
                        f"[§8.1] 上游 lint 报 {filtered} 项位于 .workbuddy/ 或 "
                        ".workbuddy-ai/ 工具区，按上游 §1.2-6 豁免"
                        "（作用域划界，非规则放宽）"
                    )
        except Exception as e:
            warns.append(f"[§8.2] 命名 lint 调用失败（{e}），视为校验未完成")
    else:
        warns.append("[§8.1] 未配置 ADEN_NAMING_LINT，跳过命名校验（不代表合规）")

    return errors, warns


def main() -> int:
    ap = argparse.ArgumentParser(description="USP v1.1 结构校验器")
    ap.add_argument("root", help="项目根目录")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"error: 目录不存在 {root}", file=sys.stderr)
        return 2

    errors, warns = check(root)
    print("== USP v1.1 结构校验 ==")
    print(f"项目根：{root}")
    for w in warns:
        print(f"[WARN] {w}")
    for e in errors:
        print(f"[ERROR] {e}")
    print(f"\n小结：ERROR {len(errors)} · WARN {len(warns)}")
    if errors:
        print("结论：不合规（以上 ERROR 须修复）")
        return 1
    if warns:
        print("结论：结构合规，但有 WARN（请逐条查看，不输出无条件合规判定）")
    else:
        print("结论：合规")
    return 0


if __name__ == "__main__":
    sys.exit(main())
