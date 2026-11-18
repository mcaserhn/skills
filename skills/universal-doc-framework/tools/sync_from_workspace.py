#!/usr/bin/env python3
"""从开发样板工作区同步规范正文与工具到本 skill 包（维护者用）。

普通用户不需要运行本脚本；安装后的 skill 已自包含全部资产。

用法：
    python tools/sync_from_workspace.py --workspace /path/to/样板工作区 [--check]
    UDF_WORKSPACE=/path/to/样板工作区 python tools/sync_from_workspace.py [--check]

--check 只按归一化后的内容（行尾统一 LF）比较，不写文件；发现差异或缺失时退出码为 1。
默认模式按源文件覆盖包内副本并统一写 LF，不删除多余文件，不改动 SKILL.md/README.md 等包内自有文件。
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)

DOC_FILES = [
    "01-universal-folder-structure.md",
    "02-naming-extension-registry.md",
    "03-scenario-profiles.md",
    "04-document-naming-scheme.md",
    "05-naming-system.md",
]
TOOL_FILES = ["scaffold.py", "structure_lint.py"]


def pairs(workspace: str) -> list[tuple[str, str]]:
    result = []
    for name in DOC_FILES:
        result.append((
            os.path.join(workspace, "docs", name),
            os.path.join(SKILL_ROOT, "docs", name),
        ))
    for name in TOOL_FILES:
        result.append((
            os.path.join(workspace, "tools", name),
            os.path.join(SKILL_ROOT, "tools", name),
        ))
    return result


def content(path: str) -> bytes:
    """读取文件并把行尾归一化为 LF。

    开发样板工作区在 Windows 上是 CRLF；发布包统一存 LF，可避免整文件伪漂移，
    也保证带 shebang 的 Python 工具在 Linux/macOS 上可直接执行。
    """
    with open(path, "rb") as f:
        data = f.read()
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="同步开发样板工作区到本 skill 包")
    ap.add_argument("--workspace", default=os.environ.get("UDF_WORKSPACE", ""),
                    help="开发样板工作区根目录（或设环境变量 UDF_WORKSPACE）")
    ap.add_argument("--check", action="store_true", help="只检查漂移，不写文件")
    args = ap.parse_args()

    if not args.workspace or not os.path.isdir(args.workspace):
        print("error: 未找到开发样板工作区；用 --workspace 指定或设置 UDF_WORKSPACE",
              file=sys.stderr)
        return 2

    problems = 0
    for src, dst in pairs(os.path.abspath(args.workspace)):
        rel = os.path.relpath(dst, SKILL_ROOT).replace("\\", "/")
        if not os.path.isfile(src):
            print(f"[MISSING] 源文件不存在: {src}")
            problems += 1
            continue
        if not os.path.isfile(dst):
            if args.check:
                print(f"[DRIFT] 包内缺失: {rel}")
                problems += 1
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "wb") as f:
                f.write(content(src))
            print(f"[ADDED] {rel}")
            continue
        if content(src) == content(dst):
            print(f"[OK] {rel}")
            continue
        if args.check:
            print(f"[DRIFT] 内容不同: {rel}")
            problems += 1
            continue
        with open(dst, "wb") as f:
            f.write(content(src))
        print(f"[UPDATED] {rel}")

    if args.check:
        print(f"\n检查完成：{problems} 项漂移")
        return 1 if problems else 0
    print("\n同步完成（未删除任何文件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
