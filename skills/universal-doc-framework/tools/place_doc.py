#!/usr/bin/env python3
"""USP place_doc — 把一份「内容已结晶」的产物按规范命名并落位到六段骨架。

这是 doc-framework 与 SPP 等内容技能的交接工具：SPP 负责共构出结论/证据/规格，
本工具只负责「叫什么名、放哪个段、建一个空壳」，绝不替你写内容。

纯 Python 3 标准库，无第三方依赖。用法：

    python place_doc.py <项目根> --type InformationNote --domain Academic \
        --subject "Zoho定价调研纪要" --phase 20-Build --prefix AGI \
        --version v0.1 --status Draft --purpose "记录 Zoho 定价证据"

行为纪律：
- 受控值（type/domain/status/phase/prefix）必须来自白名单，防止即席造词（docs/04 §4）。
- 文件名严格按 docs/04 §2 统一式组装，各段用载体形，段间用 '-'。
- 只生成「元数据头 + 空章节骨架」；正文留「（待填写）」，不臆造任何内容。
- 默认状态随落位段推导（docs/04 §4.4）：00/10/20→Draft，30→Review，40→Approved。
- 幂等：目标文件已存在则跳过并报告，绝不覆盖（对齐 §1.3 存量豁免）。
- 目标段目录不存在时报错退出，不自动补建（骨架应由 scaffold.py 先建好）。
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import date

PHASES = {"00-Ingest", "10-Analyze", "20-Build", "30-Verify", "40-Deliver", "50-Sustain"}

PREFIXES = {"AGI", "ADEN", "PERS", "FAM"}

DOC_TYPES = {
    "ExploratoryStudy", "InformationNote", "PositionNote", "GroupStandard", "GroupService",
    "ResearchProposal", "LiteratureReview", "ResearchNote", "ExperimentReport",
    "CareerPlan", "SkillSpec", "RequirementSpec", "InventoryReport",
}

DOMAINS = {
    "00FrontEnd", "10Server", "20Networking", "30MonitorLog", "40SecurityCompliance",
    "50BackupRecovery", "60SharedFolder", "70Office365", "80Patch",
    "Software", "BusinessLogic", "Reverse", "AgentCraft", "Academic", "Career",
}

STATUSES = {"Draft", "Review", "Approved", "Signed", "Retired"}

PHASE_DEFAULT_STATUS = {
    "00-Ingest": "Draft", "10-Analyze": "Draft", "20-Build": "Draft",
    "30-Verify": "Review", "40-Deliver": "Approved", "50-Sustain": "Draft",
}

DOC_TITLE_ZH = {
    "ExploratoryStudy": "预研报告", "InformationNote": "信息说明", "PositionNote": "立场说明",
    "GroupStandard": "集团标准", "GroupService": "集团服务", "ResearchProposal": "课题立项书",
    "LiteratureReview": "文献综述", "ResearchNote": "科研笔记", "ExperimentReport": "实验报告",
    "CareerPlan": "发展规划", "SkillSpec": "技能规格", "RequirementSpec": "需求规格",
    "InventoryReport": "盘点报告",
}

DOC_SKELETON = """# {subject}

> 文档类型：{type}（{type_zh}） · 域：{domain} · 版本：{version} · 状态：{status}
> 用途：{purpose}
> 生成于 {today} · place_doc.py · USP v1.1
> 正文留白：内容须经 SPP 等过程共构、有证据支撑后再填写；未经共构的判断不应写成事实。

## 1. 待填写

（待填写）

---

完成判据：（待 SPP 共构后定义）。
"""


def fail(msg: str) -> int:
    print(f"error: {msg}", file=sys.stderr)
    return 2


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="按规范命名并落位一份产物（只建空壳，不写内容）")
    ap.add_argument("root", help="项目根目录（六段骨架须已由 scaffold.py 建好）")
    ap.add_argument("--type", required=True, metavar="载体形", help="文档类型载体形，如 InformationNote")
    ap.add_argument("--domain", required=True, metavar="载体形", help="域载体形，如 Academic / 10Server")
    ap.add_argument("--subject", required=True, help="主体段（自由文本，中文保持自然书写）")
    ap.add_argument("--phase", required=True, metavar="段码", help="落位段，如 20-Build")
    ap.add_argument("--prefix", default="AGI", help="组织前缀（默认 AGI）")
    ap.add_argument("--version", default="v0.1", help="版本，形如 v0.1（默认 v0.1）")
    ap.add_argument("--status", default="", help="状态五值；留空则按落位段推导")
    ap.add_argument("--ext", default="md", help="扩展名（默认 md）")
    ap.add_argument("--purpose", default="（待填写）", help="用途一句话，写入元数据头")
    args = ap.parse_args(argv)

    if args.type not in DOC_TYPES:
        return fail(f"未知文档类型 {args.type!r}；可选：{', '.join(sorted(DOC_TYPES))}")
    if args.domain not in DOMAINS:
        return fail(f"未知域 {args.domain!r}；可选：{', '.join(sorted(DOMAINS))}")
    if args.prefix not in PREFIXES:
        return fail(f"未知组织前缀 {args.prefix!r}；可选：{', '.join(sorted(PREFIXES))}")
    if args.phase not in PHASES:
        return fail(f"未知落位段 {args.phase!r}；可选：{', '.join(sorted(PHASES))}")

    status = args.status or PHASE_DEFAULT_STATUS[args.phase]
    if status not in STATUSES:
        return fail(f"未知状态 {status!r}；可选：{', '.join(sorted(STATUSES))}")

    import re
    if not re.fullmatch(r"v\d+\.\d+(\.\d+)?", args.version):
        return fail(f"版本格式应为 vX.Y，收到 {args.version!r}")
    if not re.fullmatch(r"[a-z0-9]+", args.ext):
        return fail(f"扩展名应仅含小写字母与数字，收到 {args.ext!r}")
    subject = args.subject.strip()
    if not subject or any(c in subject for c in "/\\"):
        return fail("主体段不能为空，也不能含路径分隔符")
    if "_" in subject or " " in subject:
        return fail("主体段不应含空格或下划线（上游 §5.2 / §4.3-3）；多词请写为载体形，如 CustomerPortal")

    phase_dir = os.path.join(args.root, args.phase)
    if not os.path.isdir(phase_dir):
        return fail(f"落位段目录不存在：{phase_dir}；请先用 scaffold.py 建好骨架")

    filename = "-".join([
        args.prefix, args.type, args.domain, subject, args.version, status
    ]) + "." + args.ext
    target = os.path.join(phase_dir, filename)

    if os.path.exists(target):
        print(f"place_doc skip: {os.path.relpath(target, os.getcwd())}  [已存在，跳过]")
        return 0

    body = DOC_SKELETON.format(
        subject=subject, type=args.type, type_zh=DOC_TITLE_ZH[args.type],
        domain=args.domain, version=args.version, status=status,
        purpose=args.purpose, today=date.today().isoformat(),
    )
    with open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)

    print(f"place_doc ok: {os.path.relpath(target, os.getcwd())}")
    print(f"  {args.type}/{args.domain} → {args.phase} · {status}")
    print("  正文留白：内容须经共构与证据支撑后填写")
    return 0


if __name__ == "__main__":
    sys.exit(main())
