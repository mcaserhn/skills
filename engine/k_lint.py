#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""k_lint.py — 知识面（K 面）一致性自检器（基线附录 A-11 的最小落地）

用途：K 面「改完即跑」的自检闸门。**只读**，不改任何文件。
对齐 StreamLens 的 ctx-lint 思路，覆盖 A-11 列出的四类 + 本项目实测出的两个漂移源：

  C1 清单条数与基线一致  附录 A 与概览 §10 的条目数（及文中「N 条清单」声称）必须相等
  C2 引用断链            K 面文档里反引号包住的 *.(md|json|jsonl|py) 路径是否真实存在
  C3 章节编号            §N / §N.M 引用能否在任一 K 面文档中落到实际标题
  C4 承重数字时效         标了「实测 / 快照 / 盘点 / 口径」的日期是否已过期（默认 > 7 天告警）
  C5 体积预算            各 K 面文件是否超上限
  C6 概览待决数一致性     概览 §9「唯一待决」声称 vs SSOT open_questions 实际条数

背景：这层校验器本身就是本项目的核心命题 —— **「存在 ≠ 可达」**。
  「改完即自检」长期只是文档里的一句话，从没有一个会亮红灯的东西把它接住。
  2026-10-13 的合规审计（F2/F3）证明：没有这层，概览清单会停在 v1.0 的 9 条、
  glossary 会把「脚本支持」写成「已挂点」，而无人察觉。

用法：
  python .workbuddy/context/k_lint.py [--ws <项目根>] [--out <文件>]
退出码：0 = 无 ERROR（可有 WARN）；1 = 存在 ERROR。
仅依赖 Python 标准库。
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import sys

# ------------------------- 配置（K 面文件清单与预算） -------------------------
# 基线的口径是「K 面在标准里只受三条约束，不约束文件个数与命名」——
# 故此处显式列出**本项目自有**的 K 面文件；换项目时改这一段即可。
K_FILES: list[str] = [
    "PROJECT-OVERVIEW.md",
    "cross_model_context_persistence_design.md",
    "context-system-baseline/CONTEXT-SYSTEM-BASELINE.md",
    "context-system-baseline/WORKBUDDY-DEPLOYMENT.md",
    ".workbuddy/context/glossary.md",
]

# 体积预算（KB，告警阈值，刻意留余量；超限不代表错，只提示该收敛或下沉）
SIZE_BUDGET_KB: dict[str, int] = {
    "PROJECT-OVERVIEW.md": 24,                                        # 导读，应保持 5 分钟可读
    "cross_model_context_persistence_design.md": 64,                  # 机制规格（含实测与路线图）
    "context-system-baseline/CONTEXT-SYSTEM-BASELINE.md": 32,         # 通用基线
    "context-system-baseline/WORKBUDDY-DEPLOYMENT.md": 32,            # 落地手册
    ".workbuddy/context/glossary.md": 24,                             # 符号登记处
}
TOTAL_BUDGET_KB = 200

STALENESS_DAYS = 7          # 承重数字超过此天数未复测 → 告警

# C4 只盯「当前承重数字」所在的快照段——否则会把历史版本注记 / 复盘日期一并捞出（噪声）。
# 依据 A-11 与合规审计 F4：「体量快照处」加 as-of 与失效条件。
SNAPSHOT_SECTIONS: list[tuple[str, str]] = [
    ("cross_model_context_persistence_design.md", r"^##\s*19\."),
    ("PROJECT-OVERVIEW.md", r"^##\s*8\."),
]

# C2：L0（~/.workbuddy/）下、不在本仓库的常见文件名——反引号引用它们不算断链
L0_NAMES = {
    "SOUL.md", "IDENTITY.md", "USER.md", "MEMORY.md",
    "settings.json", "context_hook.py", "project.txt", "output_mode.txt",
}

SSOT_REL = ".workbuddy/context/task_state.json"
BASELINE_REL = "context-system-baseline/CONTEXT-SYSTEM-BASELINE.md"
OVERVIEW_REL = "PROJECT-OVERVIEW.md"


# ------------------------- 小工具 -------------------------
class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warns: list[str] = []
        self.infos: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warns.append(msg)

    def info(self, msg: str) -> None:
        self.infos.append(msg)


def _read(p: pathlib.Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def _section(text: str, start_re: str, stop_re: str) -> str:
    """截取从 start_re 命中的标题行起、到下一个 stop_re 标题行之前的正文。"""
    lines = text.splitlines()
    out: list[str] = []
    started = False
    s = re.compile(start_re)
    e = re.compile(stop_re)
    for ln in lines:
        if not started:
            if s.search(ln):
                started = True
                out.append(ln)
            continue
        if e.search(ln):
            break
        out.append(ln)
    return "\n".join(out)


def _norm(p: pathlib.Path) -> str:
    return p.as_posix()


# ------------------------- C1 清单条数一致性 -------------------------
ITEM_RE = re.compile(r"^-\s*\[ \]\s*\*\*(\d+)\*\*", re.M)


def _count_items(block: str) -> list[int]:
    return [int(n) for n in ITEM_RE.findall(block)]


def check_list_count(root: pathlib.Path, rep: Report) -> None:
    base_path = root / BASELINE_REL
    ov_path = root / OVERVIEW_REL
    base = _read(base_path)
    ov = _read(ov_path)
    if not base or not ov:
        rep.warn(f"C1 跳过：找不到 {BASELINE_REL} 或 {OVERVIEW_REL}")
        return

    base_block = _section(base, r"^##\s*附录\s*A", r"^##\s")
    ov_block = _section(ov, r"^##\s*10\.", r"^##\s")
    base_items = _count_items(base_block)
    ov_items = _count_items(ov_block)

    canonical = len(base_items) or max(ov_items, default=0)
    if not base_items:
        rep.err(f"C1 基线附录 A 未解析出任何条目（预期形如 `- [ ] **1** ...`）")
    if not ov_items:
        rep.err(f"C1 概览 §10 未解析出任何条目")

    if base_items and ov_items:
        if len(base_items) != len(ov_items):
            rep.err(f"C1 清单条数不一致：基线附录 A = {len(base_items)} 条，"
                    f"概览 §10 = {len(ov_items)} 条（应相等）")
        if base_items != list(range(1, len(base_items) + 1)):
            rep.err(f"C1 基线附录 A 编号不连续/重复：{base_items}")
        if ov_items != list(range(1, len(ov_items) + 1)):
            rep.err(f"C1 概览 §10 编号不连续/重复：{ov_items}")

    # 文中「N 条清单」之类的声称，必须等于规范条数
    claim_re = re.compile(r"(\d+)\s*条\s*清单|清单\D{0,12}?(\d+)\s*条")
    for label, text in ((BASELINE_REL, base), (OVERVIEW_REL, ov)):
        for m in claim_re.finditer(text):
            n = int(m.group(1) or m.group(2))
            if canonical and n != canonical:
                line_no = text[:m.start()].count("\n") + 1
                rep.err(f"C1 {label}:{line_no} 声称「{n} 条清单」，"
                        f"而规范条数为 {canonical} 条")


# ------------------------- C2 引用断链 -------------------------
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
PATHISH_RE = re.compile(r"^[\w./-]+\.(?:md|json|jsonl|py|txt)$")
_SKIP_SUBSTR = ("<", ">", "{", "}", "*", "…", "~", "YYYY", "N-", "路径", " ")


def _looks_external(token: str) -> bool:
    # 明显指向别的项目/外部命名空间的反引号路径（本项目不校验）
    return token.startswith("StreamLens/") or token.startswith("docs/12")


def check_refs(root: pathlib.Path, rep: Report) -> None:
    basenames = {p.name for p in root.rglob("*") if p.is_file()}
    top_dirs = {d.name for d in root.iterdir() if d.is_dir()}
    for rel in K_FILES:
        p = root / rel
        if not p.exists():
            continue
        doc_dir = p.parent
        text = _read(p)
        for m in BACKTICK_RE.finditer(text):
            token = m.group(1).strip()
            if any(s in token for s in _SKIP_SUBSTR):
                continue
            if not PATHISH_RE.match(token):
                continue
            if token.startswith("/") or _looks_external(token):
                continue
            if "/" not in token and token in L0_NAMES:
                continue  # L0（~/.workbuddy/）文件，不在本仓库，非断链
            # 首段目录不在本仓库 → 视为 L0 / 相对 / 外部引用，不校验
            seg = token.split("/")[0]
            if "/" in token and seg not in top_dirs and not (doc_dir / seg).exists():
                continue
            # 解析：repo 根 → 文档所在目录 → 全库按文件名兜底
            cand = [root / token, doc_dir / token]
            ok = any(c.exists() for c in cand)
            if not ok and pathlib.Path(token).name in basenames:
                ok = True
            if not ok:
                line_no = text[:m.start()].count("\n") + 1
                sev = "err" if token.startswith((".workbuddy/", "context-system-baseline/")) else "warn"
                getattr(rep, sev)(
                    f"C2 {rel}:{line_no} 引用断链（未找到）：`{token}`")


# ------------------------- C3 章节编号 -------------------------
SEC_RE = re.compile(r"^#{2,4}\s+(\d+(?:\.\d+)?)[\.\s]", re.M)
REF_RE = re.compile(r"§\s*(\d+(?:\.\d+)?)")


def _headings(text: str) -> set[str]:
    return set(SEC_RE.findall(text))


def check_sections(root: pathlib.Path, rep: Report) -> None:
    all_heads: set[str] = set()
    texts: dict[str, str] = {}
    for rel in K_FILES:
        p = root / rel
        if p.exists():
            t = _read(p)
            texts[rel] = t
            all_heads |= _headings(t)
    int_parts = {h.split(".")[0] for h in all_heads}
    for rel, text in texts.items():
        for m in REF_RE.finditer(text):
            ref = m.group(1)
            if ref in all_heads or ref.split(".")[0] in int_parts:
                continue
            line_no = text[:m.start()].count("\n") + 1
            rep.warn(f"C3 {rel}:{line_no} 章节引用 §{ref} 在任一 K 面文档中无对应标题")


# ------------------------- C4 承重数字时效 -------------------------
DATE_RE = re.compile(r"20\d\d-\d\d-\d\d")


def check_staleness(root: pathlib.Path, rep: Report) -> None:
    """C4：只校验「当前承重数字」所在快照段的 as-of 日期（见 SNAPSHOT_SECTIONS）。"""
    today = datetime.date.today()
    for rel, heading_re in SNAPSHOT_SECTIONS:
        p = root / rel
        if not p.exists():
            rep.warn(f"C4 快照文件缺失：{rel}")
            continue
        text = _read(p)
        block = _section(text, heading_re, r"^##\s")
        if not block:
            rep.warn(f"C4 快照段未找到：{rel}（{heading_re}）")
            continue
        dates: list[datetime.date] = []
        for dm in DATE_RE.finditer(block):
            try:
                dates.append(datetime.date.fromisoformat(dm.group(0)))
            except ValueError:
                continue
        if not dates:
            rep.warn(f"C4 {rel} 快照段缺 as-of 日期（A-11 要求承重数字带 as-of 与失效条件）")
            continue
        newest = max(dates)
        age = (today - newest).days
        if age > STALENESS_DAYS:
            rep.warn(f"C4 {rel} 承重数字已过期：as-of {newest.isoformat()}"
                     f"（{age} 天前 > {STALENESS_DAYS} 天）→ 回跑 measure_context.py 复测")
        else:
            rep.info(f"C4 {rel} 承重数字 as-of {newest.isoformat()}（{age} 天前，未过期）")


# ------------------------- C5 体积预算 -------------------------
def check_size(root: pathlib.Path, rep: Report) -> None:
    total = 0
    for rel in K_FILES:
        p = root / rel
        if not p.exists():
            rep.warn(f"C5 缺失 K 面文件：{rel}")
            continue
        n = p.stat().st_size
        total += n
        rep.info(f"C5 {rel}: {n:,} B")
        budget = SIZE_BUDGET_KB.get(rel)
        if budget and n > budget * 1024:
            rep.warn(f"C5 {rel} 超预算：{n:,} B > {budget} KB（考虑收敛措辞或下沉到 docs/）")
    rep.info(f"C5 K 面合计：{total:,} B")
    if total > TOTAL_BUDGET_KB * 1024:
        rep.warn(f"C5 K 面合计超预算：{total:,} B > {TOTAL_BUDGET_KB} KB")


# ------------------------- C6 概览待决数 vs SSOT -------------------------
def check_open_questions(root: pathlib.Path, rep: Report) -> None:
    """C6：概览 §9 声明的待决数 vs SSOT open_questions 实际条数。"""
    ov_path = root / OVERVIEW_REL
    ssot_path = root / SSOT_REL
    if not ov_path.exists() or not ssot_path.exists():
        return
    ov = _read(ov_path)
    sec9 = _section(ov, r"^##\s*9\.", r"^##\s")
    if not sec9:
        return
    claimed = None
    if "唯一待决" in sec9:
        claimed = 1
    else:
        m = re.search(r"待决问题\s*(\d+)\s*项", sec9)
        if m:
            claimed = int(m.group(1))
    if claimed is None:
        rep.info("C6 概览 §9 未声明待决数，跳过")
        return
    try:
        ssot = json.loads(_read(ssot_path))
        oq = ssot.get("task", {}).get("open_questions", [])
    except Exception:
        rep.warn("C6 SSOT 无法解析，跳过")
        return
    if len(oq) != claimed:
        rep.warn(f"C6 概览 §9 声明待决 {claimed} 项，但 SSOT open_questions 实为 {len(oq)} 项："
                 f"需么精简 SSOT、要么改写概览措辞（一事实一权威处）")


# ------------------------- 主流程 -------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(add_help=True, description="K 面一致性自检（只读）")
    ap.add_argument("--ws", default=".", help="项目根（默认当前目录）")
    ap.add_argument("--out", default="", help="把报告写入文件（UTF-8）")
    args, _ = ap.parse_known_args(argv)

    root = pathlib.Path(args.ws).resolve()
    rep = Report()

    check_list_count(root, rep)     # C1
    check_refs(root, rep)           # C2
    check_sections(root, rep)       # C3
    check_staleness(root, rep)      # C4
    check_size(root, rep)           # C5
    check_open_questions(root, rep)  # C6

    L: list[str] = []
    L.append("== K 面一致性自检 ==")
    L.append(f"项目根：{_norm(root)}")
    L.append("")
    if rep.errors:
        L.append(f"[ERROR] {len(rep.errors)} 项：")
        for e in rep.errors:
            L.append(f"  ✗ {e}")
        L.append("")
    if rep.warns:
        L.append(f"[WARN] {len(rep.warns)} 项：")
        for w in rep.warns:
            L.append(f"  ! {w}")
        L.append("")
    if not rep.errors and not rep.warns:
        L.append("✓ 全部检查通过（无 ERROR / 无 WARN）")
        L.append("")
    L.append(f"小结：ERROR {len(rep.errors)} · WARN {len(rep.warns)}")
    text = "\n".join(L)

    if args.out:
        pathlib.Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
