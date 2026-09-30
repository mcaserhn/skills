#!/usr/bin/env python3
"""Validate every skill under ./skills against the repository conventions.

Checks per skill:
  1. SKILL.md exists
  2. YAML frontmatter is present and its `name` / `description` are readable
  3. `name` equals the directory name
  4. `description` is non-empty and <= 1024 characters
  5. backticked relative paths (references/... assets/... scripts/...) resolve

Checks per repository:
  6. secret-like patterns (private keys, cloud keys, hard-coded credentials)
  7. absolute user paths (warning only - may leak environment details)

Exit code 0 if no FAIL, 1 otherwise. Warnings never fail the run.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
MAX_DESC = 1024

SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"\bghp_[A-Za-z0-9]{36}\b"), "GitHub personal access token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), "GitHub fine-grained PAT"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"), "OpenAI-style API key"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "Slack token"),
    (re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)\b\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{12,}"),
     "possible hard-coded credential"),
]

ABS_PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9_.\-]+"),
    re.compile(r"[A-Za-z]:/Users/[A-Za-z0-9_.\-]+"),
    re.compile(r"/home/[A-Za-z0-9_.\-]+"),
]

REL_REF = re.compile(r"`((?:references|assets|scripts)/[^`\s]+)`")

TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".txt"}


def split_frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None, text


def get_field(fm, key):
    lines = fm.split("\n")
    for i, ln in enumerate(lines):
        m = re.match(r"^([A-Za-z_][\w\-]*):\s*(.*)$", ln)
        if m and m.group(1) == key:
            val = m.group(2).strip()
            if val in (">", "|", ">-", "|-", ">+", "|+"):
                buf = []
                for j in range(i + 1, len(lines)):
                    nxt = lines[j]
                    if nxt.strip() == "":
                        buf.append("")
                        continue
                    if nxt[:1].isspace():
                        buf.append(nxt.strip())
                    else:
                        break
                return " ".join(x for x in buf if x).strip()
            return val.strip("\"'")
    return None


def nested_field(fm, key):
    for ln in fm.split("\n"):
        m = re.match(r"^\s+([A-Za-z_][\w\-]*):\s*(.*)$", ln)
        if m and m.group(1) == key:
            return m.group(2).strip().strip("\"'")
    return None


def iter_text_files(path):
    for p in sorted(path.iterdir()):
        if p.is_dir():
            yield from iter_text_files(p)
        elif p.suffix.lower() in TEXT_SUFFIXES:
            yield p


def main():
    fails = []
    warns = []

    if not SKILLS_DIR.is_dir():
        print("FAIL  skills/ directory not found at %s" % SKILLS_DIR)
        return 1

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        print("WARN  skills/ is empty")

    print("Validating %d skill(s) under %s\n" % (len(skill_dirs), SKILLS_DIR))

    for d in skill_dirs:
        problems = []
        skill_md = d / "SKILL.md"

        if not skill_md.is_file():
            fails.append("%s: SKILL.md missing" % d.name)
            print("FAIL  %-28s SKILL.md missing" % d.name)
            continue

        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fm, _ = split_frontmatter(text)
        if fm is None:
            problems.append("no YAML frontmatter")
        else:
            name = get_field(fm, "name")
            desc = get_field(fm, "description")
            if not name:
                problems.append("frontmatter `name` missing")
            elif name != d.name:
                problems.append("name '%s' != directory '%s'" % (name, d.name))
            if not desc:
                problems.append("frontmatter `description` missing or empty")
            elif len(desc) > MAX_DESC:
                problems.append("description %d chars > %d" % (len(desc), MAX_DESC))

        for rel in sorted(set(REL_REF.findall(text))):
            target = rel.split("#")[0].rstrip("/")
            if not (d / target).exists():
                problems.append("referenced path not found: %s" % rel)

        n_files = sum(1 for p in d.rglob("*") if p.is_file())
        if problems:
            fails.extend("%s: %s" % (d.name, p) for p in problems)
            print("FAIL  %-28s %d file(s)" % (d.name, n_files))
            for p in problems:
                print("        - %s" % p)
        else:
            dlen = len(get_field(fm, "description")) if fm else 0
            ver = nested_field(fm, "version") or "-"
            print("PASS  %-28s %d file(s), description %d/%d chars, version %s"
                  % (d.name, n_files, dlen, MAX_DESC, ver))

    print("\nScanning for secrets and absolute paths ...")
    for d in skill_dirs:
        for f in iter_text_files(d):
            rel = f.relative_to(ROOT)
            content = f.read_text(encoding="utf-8", errors="replace")
            for pat, label in SECRET_PATTERNS:
                if pat.search(content):
                    fails.append("%s: possible %s" % (rel, label))
                    print("FAIL  %s -> %s" % (rel, label))
            for pat in ABS_PATH_PATTERNS:
                m = pat.search(content)
                if m:
                    warns.append("%s: absolute path %s" % (rel, m.group(0)))
                    print("WARN  %s -> %s" % (rel, m.group(0)))
                    break

    print("\n%s" % ("-" * 60))
    for w in warns:
        print("WARN  %s" % w)
    if fails:
        print("\nRESULT: FAIL (%d problem(s))" % len(fails))
        return 1
    print("RESULT: PASS (%d warning(s))" % len(warns))
    return 0


if __name__ == "__main__":
    sys.exit(main())
