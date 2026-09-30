# Skills

> **我的 Agent Skill 集合** — 跨客户端复用（WorkBuddy / Claude Code / Cursor 等）
> **My collection of Agent Skills** — reusable across Agent Skills clients

📖 [中文文档](#中文文档) · [English Documentation](#english-documentation)

---

## 中文文档

### 这是什么

这是我的**自建 Agent Skill 集合仓库**。每个 skill 是一个独立目录，遵循 Agent Skills 规范（`SKILL.md` 为薄入口，重型内容按需加载自 `references/` 与 `assets/`），可被任意支持该规范的 AI 客户端加载。

**收录边界**：只收录**本人自建**的 skill。市场安装或他人版权的 skill 一律不入库。

### 收录的 Skill

| Skill | 说明 | 版本 | 状态 | 文件数 |
|---|---|---|---|---|
| [`spp-source-principle`](skills/spp-source-principle/) | 源头原则协议（SPP v4.0 R4.3）执行引擎——承重结论判定、课题共构、证据链与三态治理、G/A/S 三轴、不可逆操作门禁 | R4.3 | stable | 27 |
| [`de-ai-flavor`](skills/de-ai-flavor/) | 去除 LLM 输出的「AI 味儿」（中英双语）——双语禁词表 + 中英**各自**的篇章/句法层规则 + **各自的**「不许改」保护清单 + 格式与残留标记清扫 + 常驻人设片段 + 保真护栏 | 1.5.1 | stable | 14 |

完整目录（含自动统计的描述、版本、文件数）见 [`CATALOG.md`](CATALOG.md)，由 `scripts/build-catalog.py` 从各 skill 的 frontmatter 生成。

### 目录结构

```
.
├── README.md                  # 本文件（中英双语）
├── CATALOG.md                 # 全部 skill 目录（自动生成，勿手改）
├── LICENSE                    # MIT
├── .gitattributes             # 行尾锁 LF
├── .gitignore
├── template/
│   └── skill-template/        # 新 skill 脚手架，复制即用
├── scripts/                   # 仓库维护工具（构建期，非 skill 运行依赖）
│   ├── validate.py            # 结构与内容自检
│   ├── sync-from-local.py     # 本地 skills/ → 仓库（发布方向，白名单控制）
│   └── build-catalog.py       # 生成 CATALOG.md
└── skills/                    # 全部 skill 平铺于此，一目录一 skill
    ├── spp-source-principle/
    └── de-ai-flavor/
```

### 安装

skill 目录名必须与 `SKILL.md` 的 `name` 字段一致。安装即把 `skills/<name>/` 整目录拷入目标客户端的 skills 目录。

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

- **单一真源**：本地 `~/.workbuddy/skills/` 是编辑真源，本仓库是发布镜像；只按脚本白名单单向同步，不反向回写
- **发布流程**：本地开发 → `python scripts/sync-from-local.py` → `python scripts/validate.py` → `python scripts/build-catalog.py` → `git commit && git push`
- **新增 skill**：复制 `template/skill-template/` → 在本地开发 → 把目录名加入 `scripts/sync-from-local.py` 的白名单 → 走上述流程
- **frontmatter 基线**：`name`（须等于目录名）、`description`（非空且 ≤ 1024 字符）、`license`，以及 `version` 与 `status`（顶层字段或 `metadata.` 子字段均可，目录脚本会回退查找）
- **行尾**：由 `.gitattributes` 锁定为 LF

### 最近更新

- **2026-09-30** — `de-ai-flavor` 升版 **1.5.1**：英文侧完成**本地独立复算**（P2 / D-7）——取用论文公开的 Biber 特征计数，以 `chunk-2` 为人类基准、配对 n=8,290，**复现论文五个关键倍数（误差 <1%，d 值一致）**；并以数据确认「AI 味来自指令微调」（instruct/base = 1.71× / 1.80×，基座模型最接近人类）。据此把 `references/07` 第 5 条、`references/08` 第 4 条升级为 🟢，为第 2、6、8 条补上模型依赖边界；**未改动任何规则的触发条件或改法方向**
- **2026-09-30** — `de-ai-flavor` 升版 **1.5.0**：**补齐英文侧**，与中文侧对称——新增英文篇章/句法层规则（`references/07`，10 项按 HAP-E 倍数排序）、英文反向保护清单（`references/08`，12 项）、格式与残留标记清扫（`references/09`，中英共用）；依 PNAS 2025 的 33.5M 词平行语料实测，**修正三处旧规则**——被动语态摘出并移入保护清单、hedge 降级为「仅提示」、判据改为「密度 + 触发标记」并明令禁止同义词机械替换；`SKILL.md` 新增**语言门控**（中英专用规则不交叉加载）
- **2026-09-30** — `de-ai-flavor` 升版 **1.4.0**：新增中文篇章/句法层规则（`references/05`，11 项按证据强度排序）与反向保护清单（`references/06`，10 项「不许改」）；对照 283 万字语料统计修订禁词表——虚词移出必删清单、三段式改判为「序数词当小标题」；重写保真护栏为白名单默认 + 实词溯源
- **2026-09-30** — `de-ai-flavor` 分层拆分：单文件 → 薄入口 `SKILL.md` + `references/` ×6 + `assets/` ×4
- **2026-09-30** — 仓库初始化，收纳 `spp-source-principle`（27 文件）与 `de-ai-flavor`

### 许可

MIT License（见 [`LICENSE`](LICENSE)）。

---

## English Documentation

### What this is

My **personal collection of Agent Skills**. Each skill is a self-contained directory following the Agent Skills specification (`SKILL.md` as a thin entry point, with heavier material loaded on demand from `references/` and `assets/`), loadable by any client that supports the spec.

**Inclusion policy**: only skills **I authored** live here. Marketplace-installed or third-party-copyrighted skills are never committed.

### Included skills

| Skill | What it does | Version | Status | Files |
|---|---|---|---|---|
| [`spp-source-principle`](skills/spp-source-principle/) | Execution engine for the Source Principle Protocol (SPP v4.0 R4.3) — load-bearing conclusions, subject co-construction, evidence chains, three-state governance, G/A/S tri-axis, irreversible-operation gating | R4.3 | stable | 27 |
| [`de-ai-flavor`](skills/de-ai-flavor/) | Removes "AI flavor" from LLM output (Chinese + English) — bilingual banned-word lists, **parallel** Chinese and English discourse/syntax rules, **per-language** do-not-change lists, format / markup-artifact cleanup, persona snippets, fidelity guardrails | 1.5.1 | stable | 14 |

See [`CATALOG.md`](CATALOG.md) for the full listing (with generated descriptions, versions and file counts), produced by `scripts/build-catalog.py` from each skill's frontmatter.

### Repository layout

```
.
├── README.md                  # This file (bilingual)
├── CATALOG.md                 # Full skill catalog (auto-generated - do not edit)
├── LICENSE                    # MIT
├── .gitattributes             # LF line endings locked
├── .gitignore
├── template/
│   └── skill-template/        # New-skill scaffold, copy and go
├── scripts/                   # Repository maintenance tools (build-time only)
│   ├── validate.py            # Structure and content checks
│   ├── sync-from-local.py     # Local skills/ -> repo (publish direction, whitelisted)
│   └── build-catalog.py       # Generates CATALOG.md
└── skills/                    # All skills, flat - one directory per skill
    ├── spp-source-principle/
    └── de-ai-flavor/
```

### Installation

The skill directory name must match the `name` field in `SKILL.md`. Installing means copying the whole `skills/<name>/` directory into your client's skills directory.

```bash
git clone https://github.com/mcaserhn/skills.git /tmp/skills
cp -r /tmp/skills/skills/spp-source-principle ~/.workbuddy/skills/   # WorkBuddy
cp -r /tmp/skills/skills/de-ai-flavor        ~/.workbuddy/skills/
# cp -r /tmp/skills/skills/<name> ~/.claude/skills/                  # Claude Code
```

### Conventions

- **Single source of truth**: authoring happens in the local `~/.workbuddy/skills/`; this repository is the published mirror. Sync is one-way and whitelisted - nothing is ever written back
- **Publish flow**: author locally -> `python scripts/sync-from-local.py` -> `python scripts/validate.py` -> `python scripts/build-catalog.py` -> `git commit && git push`
- **Adding a skill**: copy `template/skill-template/` -> develop locally -> add the directory name to the whitelist in `scripts/sync-from-local.py` -> run the flow above
- **Frontmatter baseline**: `name` (must equal the directory name), `description` (non-empty, <= 1024 chars), `license`, plus `version` and `status` (either top-level keys or `metadata.` sub-keys - the repo scripts fall back between both)
- **Line endings**: locked to LF by `.gitattributes`

### Recent changes

- **2026-09-30** — `de-ai-flavor` released as **1.5.1**: the English side is now **independently recomputed** (P2 / D-7) from the paper's published Biber feature counts — human baseline = `chunk-2`, n = 8,290 pairs — **reproducing all five headline multipliers (<1% error, matching Cohen's d)** and confirming from data that AI flavor comes from instruction tuning (instruct/base = 1.71x / 1.80x; base models sit closest to human). `references/07` item 5 and `references/08` item 4 are upgraded to verified, and items 2/6/8 gain model-dependence caveats; no trigger condition or rewrite direction was changed
- **2026-09-30** — `de-ai-flavor` released as **1.5.0**: **English side filled in**, now symmetric with Chinese — added English discourse/syntax rules (`references/07`, 10 items ordered by HAP-E multipliers), an English do-not-change list (`references/08`, 12 items), and format / markup-artifact cleanup (`references/09`, shared); **corrected three legacy English rules** against the PNAS 2025 parallel corpus (33.5M words) — passive voice moved out to the protection list, hedging demoted to a hint, criterion switched to "density + trigger markers" with synonym-swapping explicitly forbidden; added a **language gate** to `SKILL.md` (Chinese-only and English-only rules never load together)
- **2026-09-30** — `de-ai-flavor` released as **1.4.0**: added Chinese discourse/syntax rules (`references/05`, 11 items ordered by evidence strength) and a do-not-change protection list (`references/06`, 10 items); revised the banned-word lists against a 2.83M-character corpus (function words moved out of the must-delete list, tricolon narrowed to "ordinal as heading"); rewrote fidelity guardrails as whitelist-first with word-level provenance
- **2026-09-30** — `de-ai-flavor` split: monolithic file -> thin `SKILL.md` + `references/` x6 + `assets/` x4
- **2026-09-30** — repository initialised with `spp-source-principle` (27 files) and `de-ai-flavor`

### License

MIT License — see [`LICENSE`](LICENSE).
