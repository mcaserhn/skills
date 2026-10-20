#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""measure_context.py — 上下文体量盘点（只读）

用途：量化各注入通道的**真实**体量，用数据决定 P3-B（密度与隔离）是否启动。
判据（Ch2）：批量压缩须达**上下文窗口 80%** 才启动；未达则 P3-B 挂起。

本脚本**只读**：不写 task_state、不写日志、不写 external。可反复运行。

用法：
  python measure_context.py [--ws <项目路径>] [--window 128000]

输出：各通道字符数 + token 估算 + 占窗口比 + 增长率 + 启动判据。
token 估算为启发式（CJK≈1.0 tok/字，非 CJK≈0.29 tok/字），非精确分词。
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from context_manager import ContextManager  # noqa: E402


def tokens_est(text: str) -> int:
    """启发式 token 估算：CJK 约 1.0 tok/字，其余约 0.29 tok/字。"""
    cjk = 0
    for c in text:
        o = ord(c)
        if 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF or 0xF900 <= o <= 0xFAFF:
            cjk += 1
    other = len(text) - cjk
    return round(cjk * 1.0 + other * 0.29)


def row(name: str, text: str):
    n_chars = len(text)
    n_lines = text.count("\n") + 1 if text else 0
    return {
        "name": name,
        "chars": n_chars,
        "tokens": tokens_est(text),
        "lines": n_lines,
    }


def human(n: int) -> str:
    return f"{n:,}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", default=str(pathlib.Path.cwd()))
    ap.add_argument("--window", type=int, default=128000, help="目标上下文窗口（tokens）")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    cm = ContextManager(args.ws)
    ws = cm.ws

    print("=" * 68)
    print("上下文体量盘点 / Context Volume Inventory（只读）")
    print(f"工作区：{ws}")
    print(f"时间：{datetime.datetime.now().isoformat(timespec='seconds')}")
    print(f"目标窗口：{human(args.window)} tokens（80% 阈值 = {human(int(args.window*0.8))}）")
    print("=" * 68)

    # ---------- 1. 注入通道体量（渲染器的真实输出） ----------
    print("\n[1] 注入通道真实体量（渲染器输出，非源文件）")
    sections = [
        ("[A] 静态前缀 prefix", cm.render_static_prefix()),
        ("[B] 状态栏 status-bar", cm.render_status_bar()),
        ("[C] 参考层 reference", cm.render_reference()),
        ("[D] 外部来源 external", cm.render_external_block()),
        ("-- handoff 握手摘要", cm.render_handoff()),
        ("== layout 全量(A+B+C+D)", cm.render_layout()),
    ]
    print(f"{'通道':<28}{'字符':>10}{'tokens~':>10}{'行':>7}")
    print("-" * 68)
    data = {}
    for name, text in sections:
        r = row(name, text)
        data[name] = r
        print(f"{name:<28}{human(r['chars']):>10}{human(r['tokens']):>10}{r['lines']:>7}")

    prefix = data["[A] 静态前缀 prefix"]["tokens"]
    status = data["[B] 状态栏 status-bar"]["tokens"]
    ref = data["[C] 参考层 reference"]["tokens"]
    ext = data["[D] 外部来源 external"]["tokens"]

    # ---------- 2. 每轮实际注入量 ----------
    print("\n[2] 每轮实际注入量（按渲染契约）")
    steady = prefix + status          # system 前缀一次 + 每轮状态栏
    worst = prefix + status + ref + ext  # 最坏：参考层与外部层都触发
    print(f"  · 稳态每轮（前缀[一次性] + 状态栏[每轮]） : {human(steady):>10} tokens")
    print(f"  · 最坏每轮（+ 参考层 + 外部层全触发）      : {human(worst):>10} tokens")
    print(f"  · 状态栏单独（真正每轮新增的最小单位）    : {human(status):>10} tokens")

    # ---------- 3. 底 层源文件体量 ----------
    print("\n[3] 底层源文件体量")
    id_dir = pathlib.Path.home() / ".workbuddy"
    for name in ("SOUL.md", "IDENTITY.md", "USER.md"):
        fp = id_dir / name
        if fp.exists():
            t = fp.read_text(encoding="utf-8")
            print(f"  · 身份 {name:<14} {human(len(t)):>8} 字符 / ~{human(tokens_est(t)):>6} tok")
        else:
            print(f"  · 身份 {name:<14} （不存在）")
    mem = cm.memory_dir / "MEMORY.md"
    if mem.exists():
        t = mem.read_text(encoding="utf-8")
        print(f"  · MEMORY.md{'':<14} {human(len(t)):>8} 字符 / ~{human(tokens_est(t)):>6} tok")
    else:
        print(f"  · MEMORY.md{'':<14} （不存在）")
    ts = cm.task_state_path
    if ts.exists():
        t = ts.read_text(encoding="utf-8")
        print(f"  · task_state.json{'':<9} {human(len(t)):>8} 字符 / ~{human(tokens_est(t)):>6} tok")

    # ---------- 4. 增长层（日志 / 外部内容） ----------
    print("\n[4] 增长层体量（决定未来膨胀速率）")
    jdir = cm.journal_dir
    jfiles = sorted(jdir.glob("*.md")) if jdir.exists() else []
    j_total = 0
    j_tokens = 0
    j_rows = []
    for fp in jfiles:
        t = fp.read_text(encoding="utf-8")
        j_total += len(t)
        j_tokens += tokens_est(t)
        j_rows.append((fp.name, len(t)))
    if j_rows:
        avg = j_total / len(j_rows)
        avg_tok = j_tokens / len(j_rows)
        print(f"  · 日志：{len(j_rows)} 天，合计 {human(j_total)} 字符 / ~{human(j_tokens)} tok，"
              f"均 {human(round(avg))} 字符/天（~{human(round(avg_tok))} tok/天）")
        for nm, sz in j_rows[-5:]:
            print(f"      - {nm}: {human(sz)} 字符")
    else:
        print("  · 日志：无")

    ext_recs = cm.read_external(limit=100000)
    ext_chars = sum(len(r.get("content", "")) for r in ext_recs)
    if ext_recs:
        avg_ext = ext_chars / len(ext_recs)
        print(f"  · 外部内容：{len(ext_recs)} 条，合计 {human(ext_chars)} 字符，"
              f"均 {human(round(avg_ext))} 字符/条")
    else:
        print("  · 外部内容：无")

    # ---------- 5. 判据 ----------
    print("\n[5] P3-B 启动判据（Ch2：达窗口 80% 才启动压缩）")
    thr = int(args.window * 0.8)
    ratio_worst = worst / thr * 100
    ratio_steady = steady / thr * 100
    print(f"  阈值：{human(thr)} tokens（窗口 {human(args.window)} 的 80%）")
    print(f"  · 最坏每轮占比：{ratio_worst:.2f}%  {'✅ 未达' if worst < thr else '⚠️ 已达'}")
    print(f"  · 稳态每轮占比：{ratio_steady:.2f}%  {'✅ 未达' if steady < thr else '⚠️ 已达'}")
    verdict = "挂起 P3-B" if worst < thr else "可启动 P3-B"
    print(f"\n  ==> 结论：{verdict}")
    if worst < thr:
        headroom = thr - worst
        # 以当前增长率估算「何时」会触及阈值（仅当增长率 > 0）
        print(f"      余量 {human(headroom)} tokens；"
              f"按最坏每轮线性外推，约需 {human(int(headroom / max(worst,1)) * 1)} 倍当前体量增长。")

    # 机器可读输出
    print("\n[6] 机器可读摘要（JSON）")
    summary = {
        "ws": str(ws),
        "window": args.window,
        "threshold_80pct": thr,
        "channels": {k: v for k, v in data.items()},
        "per_turn": {"steady": steady, "worst": worst, "status_only": status},
        "gate": {"verdict": verdict, "worst_ratio_pct": round(ratio_worst, 3),
                 "steady_ratio_pct": round(ratio_steady, 3)},
        "growth": {"journal_days": len(j_rows), "journal_chars": j_total,
                   "external_records": len(ext_recs), "external_chars": ext_chars},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
