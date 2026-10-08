# Skills

> **我的 Agent Skill 集合** — 跨客户端复用（WorkBuddy / Claude Code / Cursor 等）
> **My collection of Agent Skills** — reusable across Agent Skills clients

📖 [中文文档](#中文文档) · [English Documentation](#english-documentation)

**解决什么问题** — 用 AI 干真正要落地的活，缺两样东西：**可核查**，和**不像机器写的**。`spp-source-principle` 管前者：承重结论必须带出处、必须区分「已确认 / 待验证」、遇到不可逆操作必须停下来等人批准。`de-ai-flavor` 管后者：中英双语去掉 LLM 文本里的「AI 味儿」。

**谁该用** — 把 AI 用在架构选型、合规审计、研究结论、方案评审这类「错了要付代价」场景的人；以及要把中文或英文文本对外发出去、不希望被读成 AI 生成的人。

**最小上手路径** — `git clone` 本仓库 → 把 `skills/<name>/` 整个目录拷进你的客户端 skills 目录 → 对话里说一句「启动 SPP」或「去掉 AI 味儿」。无依赖、无 API key、无需配置。

**What it solves** — Pointing AI at work that actually ships leaves two gaps: **verifiability**, and **not sounding machine-written**. `spp-source-principle` covers the first — load-bearing conclusions must carry provenance, must be tagged confirmed vs. unverified, and irreversible operations must stop for human sign-off. `de-ai-flavor` covers the second — stripping "AI flavor" from LLM output, in Chinese and English.

**Who it's for** — Anyone using AI on architecture choices, compliance, research findings, or design reviews, where being wrong costs real money; and anyone publishing Chinese or English text that must not read as AI-generated.

**How to start** — `git clone` this repo → copy the whole `skills/<name>/` directory into your client's skills directory → say "启动 SPP" or "去掉 AI 味儿" in chat. No dependencies, no API key, no configuration.

---

## 中文文档

### 这是什么

这是我的**自建 Agent Skill 集合仓库**。每个 skill 是一个独立目录，遵循 Agent Skills 规范（`SKILL.md` 为薄入口，重型内容按需加载自 `references/` 与 `assets/`），可被任意支持该规范的 AI 客户端加载。

**收录边界**：只收录**本人自建**的 skill。市场安装或他人版权的 skill 一律不入库。

### 收录的 Skill

| Skill | 说明 | 版本 | 状态 | 文件数 |
|---|---|---|---|---|
| [`spp-source-principle`](skills/spp-source-principle/) | 源头原则协议（SPP v4.0 R4.3）执行引擎——承重结论判定、课题共构、证据链与三态治理、G/A/S 三轴、不可逆操作门禁 | R4.3 | stable | 27 |
| [`de-ai-flavor`](skills/de-ai-flavor/) | 去除 LLM 输出的「AI 味儿」（中英双语）——双语禁词表 + 中英**各自**的篇章/句法层规则 + **各自的**「不许改」保护清单 + 格式与残留标记清扫 + 常驻人设片段 + 保真护栏 + **评估层**（AI-Check 取证打分 + 确定性 Python linter，只诊断不改写） + **判定边界**（上下文级排除 + 样本优先） | 1.6.1 | stable | 16 |

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

- **2026-10-08** — `de-ai-flavor` 升版 **1.6.1**：据与 `op7418/Humanizer-zh`、`blader/humanizer`、`harshaneel/humanize` 三个同类项目的逐文件对标，补三处**判定边界**（**纯增文本，未改任何触发条件、改法方向或 linter 规则**）——① **规则自带保留边界**：`references/05` 第 1（翻案腔）/ 9（禁用起手式）/ 10.1（过长前置定语）三条补上缺失的「不改」行，`references/05` 第 4 条与 `references/07` 第 5 条的保留行强化（后者**明令不得反向**把正常的 `is` / `has` 升级成 `serves as` / `represents`）；② **上下文级排除**：`references/01` 第 1 节新增「标题 / 专有名词 / 元语言指称 / 引文」四类**不构成命中**的边界（其中元语言指称同时是 linter 的已知识别边界——正则分不清「使用」与「提及」），第 4 节补「承载作者声音的细节」保护；③ **新增 `references/01` 第 9 节「样本与风格文档优先」**：把原本只写在 `references/06` / `08`「使用纪律」里的样本优先权提为**护栏级**。另 `references/10` 第 0 节补**文本年代**（2022-11-30 之前的文本不可能由 LLM 生成）与上下文边界，并修正 `references/03` / `04` 中三处指向 `01` 的**失效条款编号**。写法借鉴 `blader/humanizer` 与 `op7418/Humanizer-zh`（均 MIT）的结构，未复制文字
- **2026-10-06** — `de-ai-flavor` 升版 **1.6.0**：新增**评估层**（只诊断，不改写）——`references/10-ai-check-forensics.md`（AI-Check 取证打分：十类信号 / 30 分、0–3 严重度映射、输出格式、阈值、检测天花板）与 `scripts/ai_pattern_lint.py`（确定性 linter，仅 Python 标准库，规则编号直挂 `references/02` / `05` / `07` / `09`，支持 `--json` / `--threshold` / `--lang` / `--list-rules` / `--show-protected`，退出码 0/1/2 可进 CI，**不提供任何自动改写功能**）。骨架借鉴开源项目 `harshaneel/humanize` 的 `ai-check` 子技能与 `shir-danishyar/humanize` 的 linter（均 MIT），但**判据按本 skill 的对照语料证据逐条重新校准**——外部把 hedge、被动语态、em dash、词汇多样性判为 AI 信号，而 `references/06` / `08` 有实测证据表明这些是**人类更常用**的特征，故一律硬排除、永不判为命中（冲突处置表见 `references/10` 第 1 节）。信号数由外部 9 类 / 27 分调为 **10 类 / 30 分**（增格式层，对应 `references/09`）；`references/04` 新增「校验（三种方法，中英通用）」；`SKILL.md` 新增评估层章节，`allowed-tools` 加入 `Bash`
- **2026-09-30** — `de-ai-flavor` 升版 **1.5.2**：以 S1 作者开源的 **`pseudobibeR`**（R 包，CRAN，即 HAP-E 的 Biber 计数所用）**逐条比对源码**核对英文侧口径，**更正一处结构错配**——`references/07` 第 3 条原写「名词性 `That … is …` 从句作主句主语」，而 `f_29` 实为 **that 关系从句**（`the dog [that bit me]`）；另修正第 2 条后缀（`-ance` → 实际的 `-ness / -ity`）、第 4 条并列类别（补上动词 / 副词）、第 1 条位置说明（`f_25` 实为「紧随标点的 VBG 状语 / 从句」，含句首，非仅句尾）。同步以 Python + spaCy 复刻该口径，并在 HAP-E 全文上与官方计数**逐文档比对**（n=960，r = 0.975–1.00）确认**口径等价**，为自建语料（B 路线）铺好管线
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
| [`de-ai-flavor`](skills/de-ai-flavor/) | Removes "AI flavor" from LLM output (Chinese + English) — bilingual banned-word lists, **parallel** Chinese and English discourse/syntax rules, **per-language** do-not-change lists, format / markup-artifact cleanup, persona snippets, fidelity guardrails, an **evaluation layer** (AI-Check forensic scoring + a deterministic Python linter; diagnose only, never rewrite), and **decision boundaries** (context-level exclusions + sample-overrides-all) | 1.6.1 | stable | 16 |

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

- **2026-10-08** — `de-ai-flavor` released as **1.6.1**: three sets of **decision boundaries** added after a file-by-file comparison against `op7418/Humanizer-zh`, `blader/humanizer` and `harshaneel/humanize` (**text additions only — no trigger condition, rewrite direction or linter rule was changed**). (1) **Every rule now carries its own retention boundary**: `references/05` items 1 (not-X-but-Y), 9 (banned openers) and 10.1 (overlong pre-modifiers) gain the "do not change" lines they were missing, and the retention lines of `references/05` item 4 and `references/07` item 5 are strengthened — the latter now explicitly **forbids the reverse move** of upgrading a normal `is` / `has` into `serves as` / `represents`. (2) **Context-level exclusions**: `references/01` section 1 gains four categories that **do not count as a hit** — headings, proper nouns, metalinguistic mention (a passage *discussing* a word rather than *using* it) and quotations / dialogue; metalinguistic mention is also a documented linter limitation, since a regex engine cannot tell use from mention. Section 4 gains the "voice-carrying details" protection. (3) **New `references/01` section 9, "sample and style document take precedence"**, promoting the sample-first rule from the discipline notes in `references/06` / `08` up to guardrail level. `references/10` section 0 additionally gains the **text-age** boundary (nothing written before 2022-11-30 can be LLM-generated) and the context-level exclusion, and three broken clause cross-references into `references/01` were fixed in `references/03` / `04`. Wording follows the structure of `blader/humanizer` and `op7418/Humanizer-zh` (both MIT); no text was copied
- **2026-10-06** — `de-ai-flavor` released as **1.6.0**: added an **evaluation layer** (diagnose only, never rewrite) — `references/10-ai-check-forensics.md` (AI-Check forensic scoring: 10 signal classes / 30 points, 0-3 severity mapping, output format, thresholds, detection ceiling) and `scripts/ai_pattern_lint.py` (a deterministic linter, Python standard library only, rule IDs keyed to `references/02` / `05` / `07` / `09`, with `--json` / `--threshold` / `--lang` / `--list-rules` / `--show-protected`, exit codes 0/1/2 so it can gate CI, and **no automatic rewriting of any kind**). The skeleton follows the open-source `harshaneel/humanize` `ai-check` sub-skill and `shir-danishyar/humanize` linter (both MIT), but **every criterion was re-calibrated against this skill's own corpus evidence** — where those tools flag hedging, passive voice, em dashes and lexical diversity as AI signals, `references/06` / `08` carry measured evidence that humans use them *more*, so they are hard-excluded and never reported (see the conflict-handling table in `references/10` section 1). Signal count moved from 9 classes / 27 points to **10 classes / 30 points** (new format layer, mapped to `references/09`); `references/04` gained a "verification (three methods)" section; `SKILL.md` gained the evaluation-layer section and `Bash` in `allowed-tools`
- **2026-09-30** — `de-ai-flavor` released as **1.5.2**: English-side rules were checked against the **`pseudobibeR` source** (the R package behind HAP-E's Biber counts), definition by definition. One structural mismatch was corrected — `references/07` item 3 described a nominal `That … is …` clause as subject, while `f_29` is in fact a **that relative clause** (`the dog [that bit me]`); also fixed item 2's suffixes (`-ance` -> the actual `-ness / -ity`), item 4's coordination classes (verbs and adverbs were missing), and item 1's positional note (`f_25` is "a VBG adverbial/clausal phrase immediately after punctuation", which includes sentence-initial, not sentence-final only). The same criterion was reimplemented in Python + spaCy and cross-checked document by document against the official counts on the HAP-E full text (n = 960, r = 0.975-1.00), confirming the two are equivalent and ready for our own corpus (route B)
- **2026-09-30** — `de-ai-flavor` released as **1.5.1**: the English side is now **independently recomputed** (P2 / D-7) from the paper's published Biber feature counts — human baseline = `chunk-2`, n = 8,290 pairs — **reproducing all five headline multipliers (<1% error, matching Cohen's d)** and confirming from data that AI flavor comes from instruction tuning (instruct/base = 1.71x / 1.80x; base models sit closest to human). `references/07` item 5 and `references/08` item 4 are upgraded to verified, and items 2/6/8 gain model-dependence caveats; no trigger condition or rewrite direction was changed
- **2026-09-30** — `de-ai-flavor` released as **1.5.0**: **English side filled in**, now symmetric with Chinese — added English discourse/syntax rules (`references/07`, 10 items ordered by HAP-E multipliers), an English do-not-change list (`references/08`, 12 items), and format / markup-artifact cleanup (`references/09`, shared); **corrected three legacy English rules** against the PNAS 2025 parallel corpus (33.5M words) — passive voice moved out to the protection list, hedging demoted to a hint, criterion switched to "density + trigger markers" with synonym-swapping explicitly forbidden; added a **language gate** to `SKILL.md` (Chinese-only and English-only rules never load together)
- **2026-09-30** — `de-ai-flavor` released as **1.4.0**: added Chinese discourse/syntax rules (`references/05`, 11 items ordered by evidence strength) and a do-not-change protection list (`references/06`, 10 items); revised the banned-word lists against a 2.83M-character corpus (function words moved out of the must-delete list, tricolon narrowed to "ordinal as heading"); rewrote fidelity guardrails as whitelist-first with word-level provenance
- **2026-09-30** — `de-ai-flavor` split: monolithic file -> thin `SKILL.md` + `references/` x6 + `assets/` x4
- **2026-09-30** — repository initialised with `spp-source-principle` (27 files) and `de-ai-flavor`

### License

MIT License — see [`LICENSE`](LICENSE).
