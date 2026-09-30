# Skills

> **我的 Agent Skill 集合** — 跨客户端复用（WorkBuddy / Claude Code / Cursor 等）
> **My collection of Agent Skills** — reusable across Agent Skills clients

📖 [中文文档](#中文文档) · [English Documentation](#english-documentation)

---

## 中文文档

### 这是什么

这是我的**自建 Agent Skill 集合仓库**。每个 skill 是一个独立目录，遵循 Agent Skills 规范（`SKILL.md` + 按需加载的 `references/` 与 `assets/`），可被任意支持该规范的 AI 客户端加载。

**收录边界**：只收录**本人自建**的 skill。市场安装或他人版权的 skill 一律不入库。

### 收录的 Skill

| Skill | 说明 | 版本 | 状态 |
|---|---|---|---|
| [`spp-source-principle`](skills/spp-source-principle/) | 源头原则协议（SPP v4.0 R4.3）执行引擎——承重结论、课题共构、证据链与三态治理 | — | stable |
| [`de-ai-flavor`](skills/de-ai-flavor/) | 去除 LLM 输出的「AI 味儿」（中英双语）：禁词约束 + 人设片段 + 保真护栏 | 1.2.0 | stable |

完整目录见 [`CATALOG.md`](CATALOG.md)（由脚本生成）。

### 目录结构

```
.
├── README.md                  # 本文件（中英双语）
├── CATALOG.md                 # 全部 skill 目录（自动生成）
├── LICENSE                    # MIT
├── .gitattributes             # 行尾锁 LF
├── .gitignore
├── template/
│   └── skill-template/        # 新 skill 脚手架，复制即用
├── scripts/                   # 仓库维护工具（构建期，非 skill 运行依赖）
│   ├── validate.py            # 结构与内容自检
│   ├── sync-from-local.py     # 本地 skills/ → 仓库（发布方向）
│   └── build-catalog.py       # 生成 CATALOG.md
└── skills/                    # 全部 skill 平铺于此，一目录一 skill
    ├── spp-source-principle/
    └── de-ai-flavor/
```

### 安装

skill 目录名必须与 `SKILL.md` 的 `name` 字段一致。安装即把 `skills/<name>/` 拷入目标客户端的 skills 目录。

```bash
git clone https://github.com/mcaserhn/skills.git /tmp/skills

# WorkBuddy:
cp -r /tmp/skills/skills/spp-source-principle ~/.workbuddy/skills/
cp -r /tmp/skills/skills/de-ai-flavor        ~/.workbuddy/skills/

# Claude Code:
# cp -r /tmp/skills/skills/<name> ~/.claude/skills/
```

```powershell
git clone https://github.com/mcaserhn/skills.git $env:TEMP\skills
Copy-Item -Recurse -Force "$env:TEMP\skills\skills\spp-source-principle" "$env:USERPROFILE\.workbuddy\skills\"
Copy-Item -Recurse -Force "$env:TEMP\skills\skills\de-ai-flavor"        "$env:USERPROFILE\.workbuddy\skills\"
```

### 维护约定

- **单一真源**：本地 `~/.workbuddy/skills/` 是编辑真源，本仓库是发布镜像
- **发布流程**：本地开发 → `python scripts/sync-from-local.py` → `python scripts/validate.py` → `python scripts/build-catalog.py` → `git commit && git push`
- **新增 skill**：复制 `template/skill-template/` → 在本地开发 → 加入 `sync-from-local.py` 白名单 → 走上述流程
- **frontmatter 基线**：`name`（须等于目录名）、`description`（≤ 1024 字符）、`license`、`metadata.version` / `metadata.status`
- **行尾**：由 `.gitattributes` 锁定为 LF

### 许可

MIT License（见 [`LICENSE`](LICENSE)）。

---

## English Documentation

### What this is

This is my **personal collection of Agent Skills**. Each skill is a self-contained directory following the Agent Skills specification (`SKILL.md` plus on-demand `references/` and `assets/`), loadable by any client that supports the spec.

**Inclusion policy**: only skills **I authored** live here. Marketplace-installed or third-party-copyrighted skills are never committed.

### Included skills

| Skill | What it does | Version | Status |
|---|---|---|---|
| [`spp-source-principle`](skills/spp-source-principle/) | Execution engine for the Source Principle Protocol (SPP v4.0 R4.3) — load-bearing conclusions, subject co-construction, evidence chains, three-state governance | — | stable |
| [`de-ai-flavor`](skills/de-ai-flavor/) | Removes "AI flavor" from LLM output (Chinese + English): banned-word constraints, persona snippets, fidelity guardrails | 1.2.0 | stable |

See [`CATALOG.md`](CATALOG.md) for the full listing (script-generated).

### Repository layout

```
.
├── README.md                  # This file (bilingual)
├── CATALOG.md                 # Full skill catalog (auto-generated)
├── LICENSE                    # MIT
├── .gitattributes             # LF line endings locked
├── .gitignore
├── template/
│   └── skill-template/        # New-skill scaffold, copy and go
├── scripts/                   # Repository maintenance tools (build-time only)
│   ├── validate.py            # Structure and content checks
│   ├── sync-from-local.py     # Local skills/ -> repo (publish direction)
│   └── build-catalog.py       # Generates CATALOG.md
└── skills/                    # All skills, flat — one directory per skill
    ├── spp-source-principle/
    └── de-ai-flavor/
```

### Installation

The skill directory name must match the `name` field in `SKILL.md`. Installing means copying `skills/<name>/` into your client's skills directory.

```bash
git clone https://github.com/mcaserhn/skills.git /tmp/skills
cp -r /tmp/skills/skills/spp-source-principle ~/.workbuddy/skills/   # WorkBuddy
# cp -r /tmp/skills/skills/<name> ~/.claude/skills/                  # Claude Code
```

### Conventions

- **Single source of truth**: the local `~/.workbuddy/skills/` is where authoring happens; this repository is the published mirror
- **Publish flow**: author locally -> `python scripts/sync-from-local.py` -> `python scripts/validate.py` -> `python scripts/build-catalog.py` -> `git commit && git push`
- **Adding a skill**: copy `template/skill-template/` -> develop locally -> add the name to the `sync-from-local.py` whitelist -> run the flow above
- **Frontmatter baseline**: `name` (must equal the directory name), `description` (<= 1024 chars), `license`, `metadata.version` / `metadata.status`
- **Line endings**: locked to LF by `.gitattributes`

### License

MIT License — see [`LICENSE`](LICENSE).
