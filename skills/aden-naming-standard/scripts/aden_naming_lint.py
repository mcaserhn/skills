#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aden_naming_lint.py — 依《ADEN 命名与标识规范》校验工作区产物命名（Python 装载版）。

**依据**：`references/12-aden-naming-and-identifier-standard.md`（v1.4，Stanley HAO 编制，
2026-10-12）。**底稿**：`references/11-...md`；**上游**：`references/10-...md`。
**移植自**：`scripts/naming-lint.js`（该规范的机器化落地，自带负向测试历史）。
**不重写规则** —— 条款号、正则、判定口径、豁免判据全部照搬，本文件只做**作用域**适配。

用法：
    python aden_naming_lint.py [--root <工作区>] [--profile generic|lab]
                               [--exempt-basis modified|created]
                               [--out FILE] [--csv FILE] [--all]
                               [--effective YYYY-MM-DD]

退出码：0 = 无 ERROR；1 = 有 ERROR；2 = 参数或路径错误。

**与 naming-lint.js 的分工**（务必知道自己在跑哪一个）：
  · `naming-lint.js` = **权威实现**。含全部检查：载体层 6 条 + 内容层补零 + §8.1 待登记
    代号交叉核对 + 文件名未登记缩写。Node 零依赖。**首选**。
  · 本文件 = **无 Node 环境时的子集**。覆盖载体层 6 条 + 内容层补零；**不含** §8.1
    待登记交叉核对与文件名缩写扫描（那两项未移植，不做半吊子重写）。
    在 `generic` profile 下，本文件与 JS 的 ERROR 数应一致 —— 若不一致，以 JS 为准。

────────────────────────────────────────────────────────────────────────────
作用域 profile（**只改作用域，不改条款**）

`generic`（默认）—— 与 `naming-lint.js` 的作用域逐条对齐，适用于目录语义与 StreamLens
一致的工作区（`app/ tools/ config/ .tmp/` + `docs/ context/ README.md AGENTS.md`）：
  · §1.2-6 代码与脚手架：`app/`、`tools/`、`config/`、`.tmp/` 下的文件 → 文件名不评判。
  · §1.2-7 项目本地文档：`docs/`（`NN-名称.md`）、`context/`、根级 `README.md` /
    `AGENTS.md` → §5 不适用，但 §4.3-3 通用字符纪律仍适用。
  · 受管辖（§5.1 适用）= 其余一切（`output/` 交付物、散落的 ADEN 文档名等）。

`lab` —— 科研工作区适配（目录语义与 StreamLens 不同）：
  · `lab/` 整棵子树 = 工程区；`other-archive/tooling-scratch/`、`outputs/_pdf_build/` = 工具目录。
  · `lab/README.md`、`lab/projects/**/{project.json,report.md}`、`lab/reviewers/`、
    `other-archive/README.md` = 项目本地文档。
  · 该工作区的脚本与机读数据散在 `outputs/` 下，故**按扩展名**（`CODE_EXT`）额外豁免。
  · 受管辖 = `outputs/` 与 `other-archive/` 下的交付物。

**两处装载层补充（显式声明，非新增条款）**：
  1. `skills/` 视同 §1.2-6 工程区 —— 理由同该条：技能目录是脚手架，其 `references/`
     里的 `NN-名称.md` 属项目本地编号体系，套 ADEN 命名式既表达不出也无人遵守。
  2. `.workbuddy-ai/` 与 `.workbuddy/` 同属平台框架写入（memory/context/journal），
     文件名由框架决定。JS 只排除了 `.workbuddy/memory/`，本文件一并排除 `.workbuddy-ai/`。

**判定口径**：
  · §1.3 存量豁免按 `--exempt-basis` 判：`modified`（默认，= JS 原口径，用 mtime）
    或 `created`（用创建时间；Windows 的 `st_ctime` 即创建时间，POSIX 上不是，
    在 POSIX 须改 `st_birthtime` 或外部清单）。两种口径在「先建后改」的文件上结论不同：
    mtime 口径会把它算作新产物，created 口径算存量 —— 这是**口径差异**，不是缺陷。
  · §10.2 只扫**新建**资产；存量标 `[豁免]` 只备案，不计入不合规统计。
  · §5.6 判状态看**段位置**、不看词本身；§7.2-8 规则陈述/引用/外部编号不判违规。
  · 审计产物自指：`output/audit/` 下的正文必须引用违规片段才能描述问题，内容层不扫。
"""
import argparse
import csv as _csv
import datetime
import os
import re
import sys

# ---------------------------------------------------------------- 作用域 profile
_EXCLUDE_COMMON = [
    re.compile(r"^node_modules/"),
    re.compile(r"^\.git/"),
    re.compile(r"__pycache__"),
]

# §1.2-6 按**扩展名**判源码/脚本/配置/机器数据（仅 lab profile 启用）：
#   源码脚本与机读注册表/中间数据沿用各自技术生态的命名约定，不套 ADEN 文档命名式。
CODE_EXT = {".py", ".js", ".ps1", ".json", ".jsonl", ".log", ".schema",
            ".yml", ".yaml", ".toml"}

_ROOT_SCRIPT = re.compile(r"^[^/]+\.(py|js|ps1)$")
_SKILLS = re.compile(r"^skills(/|$)")

PROFILES = {
    # 与 naming-lint.js 的作用域逐条对齐（StreamLens 同构工作区）
    "generic": dict(
        exclude=_EXCLUDE_COMMON + [
            re.compile(r"^\.workbuddy(-ai)?/memory/"),   # 平台：按日写日志，文件名由框架决定
            re.compile(r"^app/public/globals\.css$"),    # 资料库标准 UI 层，原样引用禁改
        ],
        # §1.2-6 工程区：只约束目录归属，不约束文件名
        code_scope=[
            re.compile(r"^(app|tools|config|\.tmp)(/|$)"),
            _ROOT_SCRIPT,
            _SKILLS,
        ],
        tool_scope=[],          # 工程区整目录已跳过，目录名无需另判
        code_ext=set(),         # generic 不做按扩展名的额外豁免（JS 亦无）
        # §1.2-7 项目本地文档：§5 不适用，§4.3-3 通用字符纪律仍适用
        doc_scope=[
            re.compile(r"^docs/"),
            re.compile(r"^context/"),
            re.compile(r"^README\.md$"),
            re.compile(r"^AGENTS\.md$"),
        ],
    ),
    # 科研工作区适配（目录语义与 StreamLens 不同）
    "lab": dict(
        exclude=_EXCLUDE_COMMON + [
            re.compile(r"^\.workbuddy(-ai)?/context/"),  # 平台：SSOT
            re.compile(r"^\.workbuddy(-ai)?/memory/"),
            re.compile(r"^outputs/_pdf_build/chrome_profile"),  # Chrome 构建缓存
        ],
        code_scope=[
            _ROOT_SCRIPT,
            re.compile(r"^lab(/|$)"),
            re.compile(r"^other-archive/tooling-scratch(/|$)"),
            re.compile(r"^outputs/_pdf_build(/|$)"),
            _SKILLS,
        ],
        tool_scope=[
            re.compile(r"^other-archive/tooling-scratch(/|$)"),
            re.compile(r"^outputs/_pdf_build(/|$)"),
        ],
        code_ext=CODE_EXT,
        doc_scope=[
            re.compile(r"^lab/README\.md$"),
            re.compile(r"^lab/projects/.+/project\.json$"),
            re.compile(r"^lab/projects/.+/report\.md$"),
            re.compile(r"^lab/reviewers(/|$)"),
            re.compile(r"^other-archive/README\.md$"),
            re.compile(r"^README\.md$"),
        ],
    ),
}

# 审计产物自指例外（§7.2-8 精神）：审计报告必须引用违规片段才能描述问题
CONTENT_SCAN_EXCLUDE = [re.compile(r"^output/audit/")]

in_scope = lambda rel, pats: any(p.search(rel) for p in pats)

# §5.6 明示的例外（**按段位置判，不按词本身**）：
# 「名称中作为**主体词**出现的同形词（`prototype` 设计文档、`archive` 目录）**不属**本条」。
# 故容器名里的 archive/archived 不判为状态后缀（负向测试：不豁免会把 `other-archive/`
# 误报，而它恰恰是 §5.6 点名豁免的形态）。
CONTAINER_NOUN = {"archive", "archived"}


# ---------------------------------------------------------------- 载体层规则（照搬 naming-lint.js）
def r_underscore(n):
    """§5.2 · §5.10-4 下划线分隔（前导下划线为排序习惯，正解是去掉）"""
    m = re.match(r"^_+", n)
    if m:
        return m.group(0), n[len(m.group(0)):] + "（去掉前导下划线）"
    if "_" in n:
        return "_", n.replace("_", "-")
    return None, None


def r_space(n):
    """§4.3-3 · §5.2 空格 / 全角"""
    if re.search(r"[ \u3000]", n):
        return "空格", re.sub(r"[ \u3000]", "-", n)
    if re.search(r"[\uFF01-\uFF5E]", n):
        return "全角", re.sub(r"[\uFF01-\uFF5E]",
                             lambda m: chr(ord(m.group(0)) - 0xFEE0), n)
    return None, None


def r_version(n):
    """§5.4 · 附录 A.6 版本号：受控形式仅 -vX.Y（小写 v、连字符、≥2 段）"""
    m = re.search(r"([-_. ]?)([vV])(\d+(?:\.\d+)*)", n)
    if not m:
        return None, None
    sep, letter, digits = m.group(1), m.group(2), m.group(3)
    if sep == "-" and letter == "v" and "." in digits:
        return None, None   # 合规
    fixed = re.sub(r"([-_. ]?)[vV](\d+(?:\.\d+)*)",
                   lambda mm: "-v" + (mm.group(2) if "." in mm.group(2)
                                      else mm.group(2) + ".0"), n)
    return m.group(0), fixed


def r_date(n):
    """§5.5 · 附录 A.7 日期：文件名段用 YYYYMMDD；期间段可 YYYY-MM；季度用大写 Q"""
    if re.search(r"\b20\d{2}Q[1-4]\b", n) and not re.search(r"\b20\d{2}-[qQ]\d", n):
        return None, None
    m = re.search(r"20\d{2}-[qQ]\d", n)
    if m:
        return m.group(0), re.sub(r"20(\d{2})-([qQ])(\d)", r"20\1Q\3", n)
    m = re.search(r"20\d{2}-\d{2}-\d{2}", n)
    if m:
        return m.group(0), re.sub(r"(20\d{2})-(\d{2})-(\d{2})", r"\1\2\3", n)
    return None, None


def r_status(n):
    """§5.6 · §5.10-1 状态/修订散词（看**段位置**，不看词本身）"""
    m = re.search(r"[-_](final|sample|prototype|previous|archive|archived|bkup|old"
                  r"|copy|updated|upd|ongoing|done|pre|post|draft\d|r\d+)(?=$|[-_.])",
                  n, re.I)
    if not m:
        return None, None
    if re.match(r"^-(Draft|Review|Approved|Signed|Retired)$", m.group(0)):
        return None, None
    # §5.6 例外：主体词形态（archive 目录等）不判
    if m.group(1).lower() in CONTAINER_NOUN:
        return None, None
    return m.group(0), "改用受控 5 值：-Draft / -Review / -Approved / -Signed / -Retired"


def r_lang(n):
    """§5.7 · 附录 A.5 语言段：受控 2 值 -zh / -en"""
    m = re.search(r"[-_](cn|ENG?|CN|EN|zh|中文)(?=[-_.]|$)", n)
    if not m:
        return None, None
    if m.group(1) in ("zh", "en"):
        return None, None
    return m.group(0), "受控 2 值：-zh / -en（小写）"


RULES = [
    ("下划线分隔",      "§5.2 · §5.10-4", r_underscore, True),
    ("空格 / 全角",     "§4.3-3 · §5.2",  r_space,      False),  # 通用字符纪律，doc_scope 也适用
    ("版本号写法",      "§5.4 · 附录 A.6", r_version,    True),
    ("日期形式",        "§5.5 · 附录 A.7", r_date,       True),
    ("状态 / 修订散词", "§5.6 · §5.10-1", r_status,     True),
    ("语言段写法",      "§5.7 · 附录 A.5", r_lang,       True),
]
SYS_ARTIFACT = re.compile(r"-CCNLT[A-Z]{3}-[A-Z]+")
SCRIPT_GEN_EXT = {".svg"}     # 由分析脚本生成，随脚本命名


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="目标工作区根（默认=当前目录）")
    ap.add_argument("--profile", default="generic", choices=sorted(PROFILES),
                    help="作用域 profile（默认 generic；只改作用域，不改条款）")
    ap.add_argument("--exempt-basis", default="modified",
                    choices=["modified", "created"],
                    help="§1.3 存量豁免判据（默认 modified，= naming-lint.js 原口径）")
    ap.add_argument("--out")
    ap.add_argument("--csv")
    ap.add_argument("--effective", default="2026-10-12")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    root = os.path.abspath(a.root) if a.root else os.getcwd()
    if not os.path.isdir(root):
        print(f"[FATAL] 目标工作区不存在：{root}", file=sys.stderr)
        return 2
    prof = PROFILES[a.profile]
    EXCLUDE, CODE_SCOPE = prof["exclude"], prof["code_scope"]
    TOOL_SCOPE, DOC_SCOPE = prof["tool_scope"], prof["doc_scope"]
    CODE_EXT_P = prof["code_ext"]
    EFFECTIVE = datetime.datetime.fromisoformat(a.effective + "T00:00:00")

    findings, scanned, skipped = [], 0, []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        for name, isdir in [(d, True) for d in dirs] + [(f, False) for f in files]:
            full = os.path.join(base, name)
            rel = os.path.relpath(full, root).replace("\\", "/")
            if in_scope(rel, EXCLUDE):
                continue
            # §1.2-6 豁免（目录归属已定，文件名不判）
            if in_scope(rel, CODE_SCOPE):
                skipped.append((rel, "§1.2-6 代码脚手架目录"))
                continue
            if not isdir and CODE_EXT_P and \
                    os.path.splitext(name)[1].lower() in CODE_EXT_P:
                skipped.append((rel, "§1.2-6 源码/配置/机读数据"))
                continue
            # §1.2-6 工程区的**目录名**也不判（它们是工作目录，不是文档）
            if isdir and TOOL_SCOPE and in_scope(rel + "/", TOOL_SCOPE):
                skipped.append((rel + "/", "§1.2-6 工具目录"))
                continue
            scanned += 1
            st = os.stat(full)
            # §1.3 存量豁免：口径见 --exempt-basis
            ts = st.st_mtime if a.exempt_basis == "modified" else st.st_ctime
            exempt = datetime.datetime.fromtimestamp(ts) < EFFECTIVE
            is_doc = in_scope(rel, DOC_SCOPE)

            if SYS_ARTIFACT.search(name):
                findings.append(dict(level="WARN", path=rel + ("/" if isdir else ""),
                                     clause="§1.4", rule="系统异常产物",
                                     frag=name, suggest="列为清理候选；删除前须人工比对确认",
                                     exempt=False))
                continue

            for rule, clause, fn, s5_only in RULES:
                if is_doc and s5_only:
                    continue          # §1.2-7：docs 类不适用 §5 专属规则
                frag, sug = fn(name)
                if frag is None:
                    continue
                findings.append(dict(
                    level="INFO" if exempt else "ERROR",
                    path=rel + ("/" if isdir else ""), clause=clause, rule=rule,
                    frag=frag, suggest=sug, exempt=exempt))

    # ---------- 内容层标识（§7.1）：序号应 ≥2 位补零 ----------
    TEXT_EXT = re.compile(r"\.(md|csv|txt)$")
    INTERNAL = ["BASE-M365", "BASE", "NFR", "INT", "EOD", "FR", "OP", "MD"]
    ID_RE = re.compile(r"(?<![\w-])(" + "|".join(INTERNAL) + r")-(\d{1,3})([a-z]?)(?![\wx-])")
    EVIDENCE_CITE = re.compile(r"引用原样|实际编码|勿改|原文为准|照抄|反例")
    content = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        for f in files:
            full = os.path.join(base, f)
            rel = os.path.relpath(full, root).replace("\\", "/")
            if in_scope(rel, EXCLUDE) or in_scope(rel, CODE_SCOPE):
                continue
            if in_scope(rel, CONTENT_SCAN_EXCLUDE):   # 审计产物自指例外
                continue
            if not TEXT_EXT.search(f) or os.path.getsize(full) > 400_000:
                continue
            try:
                text = open(full, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            bad = set()
            for line in text.split("\n"):
                if EVIDENCE_CITE.search(line):     # §7.2-8 规则陈述/引用不判违规
                    continue
                for m in ID_RE.finditer(line):
                    pre, num, var = m.group(1), m.group(2), m.group(3)
                    if len(num) >= 2 or pre == "R-AB":
                        continue
                    if num == "0" and var == "x":
                        continue
                    bad.add(f"{pre}-{num}{var}")
            if bad:
                content.append((rel, sorted(bad)[:8]))

    # ---------- 汇总 ----------
    errs = [f for f in findings if f["level"] == "ERROR"]
    warns = [f for f in findings if f["level"] == "WARN"]
    infos = [f for f in findings if f["level"] == "INFO"]

    out = []
    P = out.append
    P("=" * 74)
    P("ADEN 命名与标识规范 · 工作区合规校验")
    P("=" * 74)
    P("依据: references/12-aden-naming-and-identifier-standard.md v1.4")
    P("规则移植自: scripts/naming-lint.js（未重写条款）")
    P(f"根目录: {root}")
    P(f"作用域: {a.profile}")
    P(f"生效日: {a.effective}（{a.exempt_basis} 早于此日者按 §1.3 存量豁免）")
    P(f"受管辖对象: {scanned} 项；豁免 {len(skipped)} 项（§1.2-6 代码与脚手架）")
    P("")
    P("--- 规则命中统计 ---")
    from collections import Counter
    c = Counter(("[豁免]" if f["exempt"] else "") + f["rule"] for f in findings)
    for k, v in c.most_common():
        P(f"  {v:>4}  {k}")
    if not c:
        P("  (无命中)")
    P("")
    P("--- 须整改（新产物，§1.3 不豁免）---")
    if not errs:
        P("  (无)")
    else:
        for f in (errs if a.all else errs[:50]):
            P(f"  [ERROR] {f['path']}")
            P(f"          违反 {f['clause']}（{f['rule']}）：{f['frag']}")
            P(f"          建议 → {f['suggest']}")
        if len(errs) > 50 and not a.all:
            P(f"  … 另有 {len(errs)-50} 处（--all 全量 / --csv 导出）")
    P("")
    P("--- 内容层标识未补零（§7.1 · §7.2-1）---")
    if not content:
        P("  (无)")
    else:
        for rel, ids in content:
            P(f"  [WARN] {rel}")
            P(f"         序号未补零：{' '.join(ids)}")
            P(f"         建议 → 补零至 2 位（如 OP-1 → OP-01）")
    P("")
    P("--- 存量备案（§1.3 豁免，不判违规）---")
    if not infos:
        P("  (无)")
    else:
        for f in (infos if a.all else infos[:30]):
            P(f"  [豁免] {f['path']}  ← {f['clause']}（{f['rule']}）")
        if len(infos) > 30 and not a.all:
            P(f"  … 另有 {len(infos)-30} 处")
    P("")
    P(f"合计: {len(errs)} ERROR / {len(warns)} WARN / {len(infos)} INFO（存量豁免）")
    verdict = ("FAIL —— 新产物存在不合规命名，须整改。" if errs
               else ("PASS（有 WARN：形式问题，须核实整改）" if warns
                     else "PASS —— 命名的形式可校验项全部合规。"))
    P(f"结论: {verdict}")

    text = "\n".join(out)
    print(text)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8-sig") as fh:
            w = _csv.writer(fh)
            w.writerow(["level", "path", "clause", "rule", "fragment", "suggest", "exempt"])
            for f in findings:
                w.writerow([f["level"], f["path"], f["clause"], f["rule"], f["frag"],
                            f["suggest"], "存量豁免" if f["exempt"] else "新产物"])
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
