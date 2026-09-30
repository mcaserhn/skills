#!/usr/bin/env python3
"""扫描输出中的排他性关键词，提示检查非目标集合（SPP §12.1）。

用法：
    python scan-exclusivity.py < output.md
    echo "仅 A 可行" | python scan-exclusivity.py

注意：本脚本只做提示，不替代 §12 的反证义务。
"""
import re
import sys

EXCLUSIVE = ["仅", "全部", "唯一", "不存在", "不会影响",
             "完全替代", "严格等价", "必然"]


def scan(text: str):
    hits = []
    for kw in EXCLUSIVE:
        for m in re.finditer(re.escape(kw), text):
            start = max(0, m.start() - 30)
            end = min(len(text), m.end() + 30)
            hits.append((kw, m.start(), text[start:end].replace("\n", " ")))
    return hits


def main():
    text = sys.stdin.read()
    hits = scan(text)
    if not hits:
        print("[OK] 未发现排他性关键词。")
        return 0
    print("[!] 发现 %d 处排他性表述，请检查非目标集合（SPP §12.3）：\n" % len(hits))
    for kw, pos, ctx in hits:
        print("  [%s] (offset %d)" % (kw, pos))
        print("      ...%s..." % ctx)
        print()
    print("提醒：每处都需回答——'非目标集合是否不存在或不影响当前结论？'")
    return 1


if __name__ == "__main__":
    sys.exit(main())
