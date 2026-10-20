# Skills

> **我的 Agent Skill 集合** — 跨客户端复用（WorkBuddy / Claude Code / Cursor 等）
> **My collection of Agent Skills** — reusable across Agent Skills clients

📖 [中文文档](#中文文档) · [English Documentation](#english-documentation)

**解决什么问题** — 用 AI 干真正要落地的活，缺三样东西：**可核查**、**不像机器写的**，和**经得起追问**。`spp-source-principle` 管第一样：承重结论必须带出处、必须区分「已确认 / 待验证」、遇到不可逆操作必须停下来等人批准。`de-ai-flavor` 管第二样：中英双语去掉 LLM 文本里的「AI 味儿」。`devils-advocate` 管第三样：给已经成形的方案做对抗性审查，只报跨过「承重线」的风险，并在挑刺没被采纳时自动降档——它不是靠嘴毒，是靠按程序凿证据。另有一块底座：`context-persistence` 管**上下文不丢**——跨模型切换、隔天复用同一任务时，按 KV Cache 友好布局注入静态前缀与状态栏，开场即恢复，不必从零复述背景。

**谁该用** — 把 AI 用在架构选型、合规审计、研究结论、方案评审这类「错了要付代价」场景的人；要把中文或英文文本对外发出去、不希望被读成 AI 生成的人；手里已经攥着一个方案、想在被别人挑刺之前先自己过一遍的人；以及经常换模型、或同一个任务要跨好几天断续接着做，受不了每次开场从零复述背景的人。

**最小上手路径** — `git clone` 本仓库 → 把 `skills/<name>/` 整个目录拷进你的客户端 skills 目录 → 对话里说一句「启动 SPP」、「去掉 AI 味儿」、「毒舌陪练」或「恢复上下文」。除 `context-persistence` 需把随附引擎部署进项目才可用完整命令（见下注）外，零第三方依赖、无 API key、无需配置。

**What it solves** — Pointing AI at work that actually ships leaves three gaps: **verifiability**, **not sounding machine-written**, and **surviving challenge**. `spp-source-principle` covers the first — load-bearing conclusions must carry provenance, must be tagged confirmed vs. unverified, and irreversible operations must stop for human sign-off. `de-ai-flavor` covers the second — stripping "AI flavor" from LLM output, in Chinese and English. `devils-advocate` covers the third — adversarial review of an already-formed plan, reporting only the risks that cross a load-bearing threshold and backing off automatically once its critiques go unused; it earns its keep through procedure, not harshness. One more foundation layer: `context-persistence` keeps context from being lost — when switching models or resuming the same task days later, it injects a KV-cache-friendly static prefix plus status bar, so a session resumes instead of restarting from a fresh briefing.

**Who it's for** — Anyone using AI on architecture choices, compliance, research findings, or design reviews, where being wrong costs real money; anyone publishing Chinese or English text that must not read as AI-generated; anyone holding a finished plan who wants to red-team it before somebody else does; and anyone who keeps switching models or spreads one task across days and is tired of re-explaining the background from scratch at the start of every session.

**How to start** — `git clone` this repo → copy the whole `skills/<name>/` directory into your client's skills directory → say "启动 SPP", "去掉 AI 味儿", "毒舌陪练" or "恢复上下文" in chat. Zero third-party dependencies, no API key, no configuration — except `context-persistence`, whose bundled engine must be deployed into a project for its full command set (see note below).

---

## 中文文档

### 这是什么

这是我的**自建 Agent Skill 集合仓库**。每个 skill 是一个独立目录，遵循 Agent Skills 规范（`SKILL.md` 为薄入口，重型内容按需加载自 `references/` 与 `assets/`），可被任意支持该规范的 AI 客户端加载。

**收录边界**：只收录**本人自建**的 skill。市场安装或他人版权的 skill 一律不入库。

### 收录的 Skill

| Skill | 说明 | 版本 | 状态 | 文件数 |
|---|---|---|---|---|
| [`spp-source-principle`](skills/spp-source-principle/) | 源头原则协议（SPP v4.0 R4.4）执行引擎——承重结论判定、课题共构、证据链与三态治理、G/A/S 三轴、不可逆操作门禁、契约优先级裁决、协作姿态与反迎合、会话人格档位 | R4.4 | stable | 27 |
| [`de-ai-flavor`](skills/de-ai-flavor/) | 去除 LLM 输出的「AI 味儿」（中英双语）——双语禁词表 + 中英**各自**的篇章/句法层规则 + **各自的**「不许改」保护清单 + 格式与残留标记清扫 + 常驻人设片段 + 保真护栏 + **评估层**（AI-Check 取证打分 + 确定性 Python linter，只诊断不改写） + **判定边界**（上下文级排除 + 样本优先） | 1.6.3 | stable | 16 |
| [`devils-advocate`](skills/devils-advocate/) | 毒舌陪练 / 反方批判者模式——给已经成形的想法做对抗性检验：零奉承但不零确认、阈值制（只报跨过「承重线」的风险且无下限）、三档强度、缺参数单列、挑刺未被采纳即自动降档、模式边界 | 1.0.0 | stable | 1 |
| [`context-persistence`](skills/context-persistence/) | 跨模型 / 跨时间上下文持久化（KV Cache 友好注入）——A 静态前缀 / B 状态栏 / C 参考层 / D 外部来源四通道契约，记忆层分层声明（〔常驻〕注入 / 〔按需〕只列名）、三个动作（开场 layout / 每回合末 capture / 结束 flush+export）、模型适配注册表、外部内容单一咽喉点统一包裹为不可信数据；**引擎三分支**（有引擎→用 / 拿得到→部署不重建 / 拿不到→按任务层契约手工兜底）与内嵌 `task_state.json` 字段契约；**引擎随技能发布**（`engine/` 子目录，纯 Python 3 标准库） | 1.3.1 | stable | 6 |

完整目录（含自动统计的描述、版本、文件数）见 [`CATALOG.md`](CATALOG.md)，由 `scripts/build-catalog.py` 从各 skill 的 frontmatter 生成。

> **注**：`context-persistence` 描述的是**协议与行为规范**；它驱动的引擎随技能发布在 [`skills/context-persistence/engine/`](skills/context-persistence/engine/)——**只读分发副本**，部署进目标项目的 `.workbuddy/context/` 即可（三步见 `engine/DEPLOY.md`）。没有引擎时，可按其 `SKILL.md` 的「任务层契约」节手工执行（字段全貌已内嵌，兜底从猜变成照抄）。

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
    ├── de-ai-flavor/
    ├── devils-advocate/
    └── context-persistence/
        ├── SKILL.md
        └── engine/            # 执行体（随技能发布的只读分发副本）
            ├── context_manager.py    #   主引擎（纯 Python 3 标准库）
            ├── k_lint.py             #   K 面一致性自检
            ├── measure_context.py    #   只读体量盘点仪
            ├── model_adapters.json   #   模型适配注册表
            └── DEPLOY.md             #   三步部署到任意项目
```

### 安装

skill 目录名必须与 `SKILL.md` 的 `name` 字段一致。安装即把 `skills/<name>/` 整目录拷入目标客户端的 skills 目录。

```bash
git clone https://github.com/mcaserhn/skills.git /tmp/skills

# WorkBuddy:
cp -r /tmp/skills/skills/spp-source-principle ~/.workbuddy/skills/
cp -r /tmp/skills/skills/de-ai-flavor        ~/.workbuddy/skills/
cp -r /tmp/skills/skills/devils-advocate     ~/.workbuddy/skills/
cp -r /tmp/skills/skills/context-persistence ~/.workbuddy/skills/

# context-persistence 的引擎（随技能一起被拷进来了；装了才能用完整命令）。
# 引擎要放进【项目】的 .workbuddy/context/ 才生效——装在 skills 目录里那一份不参与运行：
mkdir -p <你的项目>/.workbuddy/context
cp ~/.workbuddy/skills/context-persistence/engine/context_manager.py \
   ~/.workbuddy/skills/context-persistence/engine/k_lint.py \
   ~/.workbuddy/skills/context-persistence/engine/measure_context.py \
   ~/.workbuddy/skills/context-persistence/engine/model_adapters.json \
   <你的项目>/.workbuddy/context/
python <你的项目>/.workbuddy/context/context_manager.py --ws <你的项目> init

# Claude Code:
# cp -r /tmp/skills/skills/<name> ~/.claude/skills/
```

```powershell
git clone https://github.com/mcaserhn/skills.git $env:TEMP\skills
Copy-Item -Recurse -Force "$env:TEMP\skills\skills\spp-source-principle" "$env:USERPROFILE\.workbuddy\skills\"
Copy-Item -Recurse -Force "$env:TEMP\skills\skills\de-ai-flavor"        "$env:USERPROFILE\.workbuddy\skills\"
Copy-Item -Recurse -Force "$env:TEMP\skills\skills\devils-advocate"     "$env:USERPROFILE\.workbuddy\skills\"
Copy-Item -Recurse -Force "$env:TEMP\skills\skills\context-persistence" "$env:USERPROFILE\.workbuddy\skills\"

# context-persistence 的引擎（随技能一起被拷进来了；装了才能用完整命令）。
# 引擎要放进【项目】的 .workbuddy\context\ 才生效——装在 skills 目录里那一份不参与运行：
New-Item -ItemType Directory -Force "<你的项目>\.workbuddy\context"
Copy-Item "$env:USERPROFILE\.workbuddy\skills\context-persistence\engine\context_manager.py",`
          "$env:USERPROFILE\.workbuddy\skills\context-persistence\engine\k_lint.py",`
          "$env:USERPROFILE\.workbuddy\skills\context-persistence\engine\measure_context.py",`
          "$env:USERPROFILE\.workbuddy\skills\context-persistence\engine\model_adapters.json" `
          "<你的项目>\.workbuddy\context\"
python "<你的项目>\.workbuddy\context\context_manager.py" --ws "<你的项目>" init
```

### 维护约定

- **单一真源**：本地 `~/.workbuddy/skills/` 是编辑真源，本仓库是发布镜像；只按脚本白名单单向同步，不反向回写
- **发布 context-persistence 的陷阱**：`sync-from-local.py` 对白名单技能是**整目录镜像**（先删后拷）。暂存区若只放 `SKILL.md` 而漏掉 `engine/` 子目录，下一次发布会把仓库里的引擎**删掉**。发布它时暂存区必须是 `SKILL.md` + `engine/` 的完整 6 文件
- **发布流程**：本地开发 → `python scripts/sync-from-local.py` → `python scripts/validate.py` → `python scripts/build-catalog.py` → `git commit && git push`
- **新增 skill**：复制 `template/skill-template/` → 在本地开发 → 把目录名加入 `scripts/sync-from-local.py` 的白名单 → 走上述流程
- **frontmatter 基线**：`name`（须等于目录名）、`description`（非空且 ≤ 1024 字符）、`license`，以及 `version` 与 `status`（顶层字段或 `metadata.` 子字段均可，目录脚本会回退查找）
- **行尾**：由 `.gitattributes` 锁定为 LF

### 最近更新

- **2026-10-20** — `spp-source-principle` 随协议升级至 **R4.4**（**Re-Discovery 重建**，27 文件，纯追加增量挂载、未新增文件）：R4.4 本体定稿（1,613 行，修订议程 8 批次 A–H 逐批 Gate），新增条款原文全部落位——§2.3 契约优先级表、§2.5 协作姿态、§2.6 反迎合（含与 `de-ai-flavor` 的单一来源清单分工）、§8.1 过程播报 + 渐进式输出护栏、§8.2 思考外显护栏、§10.1 主动声明、§10.4.4 情感客观性、§11.7 自我模型披露、§11.8 品质词汇边界护栏、§12.5 异议后执行、§13.4 不可逆操作亮线清单、§17.5 人格档位、§17.6 主动性分级护栏；入口层 wiring（执行流程图 / 路由表 / Override 指令 / 输出前最低检查）同步。四件条件引入器件只落护栏不开器件，2–4 周观察期巡检挂运行期（触发即回退并记录）。R4.3 基线 27 文件备份留档，技能封装 → GitHub 镜像单向派生
- **2026-10-20** — `de-ai-flavor` 升版 **1.6.3**（**SPP R4.4 互引，判据与 linter 零变化**）：依 SPP R4.4 §2.6「清单分工（单一来源）」落两侧互引——原则层权威在 SPP §2.6，词汇层操作清单在本技能，修改后回查对侧；新增例外条款四条：身份声明语境下的身份事实陈述（「我是 AI 协作者」类）与品质词汇借用（诚实 / 审慎 / 尽责等）不属「助手腔客套」命中范围，范围仅限身份声明语境、禁入结论 / 证据 / 分析正文、回退触发为品质词包装无证据结论即全面禁用——该例外同时消解了「作为 AI」禁词与 SPP §11.7 身份陈述义务的表面冲突。禁词表、篇章 / 句法层规则、反向保护清单、linter 规则编号全部未动
- **2026-10-20** — `context-persistence` 修版 **1.3.1**（**文档漂移修补**，零行为变化）：一次全仓漂移审计（catalog 重生成 diff / 引擎与机制权威逐字节对账 / 命令清单 vs 引擎 `argv` 分支逐条比 / 目录树 vs `ls-tree` / Python 版本声称核对）发现两处文档问题——引擎 20 个顶层命令中文档漏了 `show` 与 `wrap-external` 两条底层命令；② 层身份路径 `~/.workbuddy/…` 未与泛化后的环境前置统一。均已补。审计结论其余各项零漂移（引擎 4 文件与机制权威字节一致、CATALOG 重生成无 diff、目录树与实际相符、`3.8+` 声称经 `from __future__ import annotations` 核实成立）。
- **2026-10-20** — `context-persistence` 升版 **1.3.0**（**修可移植性**，机制条款零变化），**引擎随技能发布**在 `skills/context-persistence/engine/`（4 引擎文件 + `DEPLOY.md`）。缘起：一次全新环境（另一用户 / 新家目录）加载本技能后，因引擎不在发布面、技能又无内建契约，只能靠猜重建状态层。本版修三处：① 「环境前置」重写为**引擎三分支**——项目里已有引擎 → 正常用；拿得到引擎 → **部署不重建**（拷 4 文件 + `init` + `k_lint` 验证）；都拿不到 → 按契约手工兜底；② 新增「**任务层契约**」节，把 `task_state.json` 字段全貌、条目结构、flush 物理动作、文件格式**内嵌进技能**，无引擎兜底从「猜结构」变「照抄」；③ 明确**严禁照说明书重写引擎**（必然产出分叉实现，分叉一旦成为事实权威，机制就收不回去）。注入契约 / 体量边界 / 记忆层规则 / 三个动作 / 外部通道等一字未动。`engine/` 是技能目录内的**只读分发副本**：修机制回机制权威处，不回写本仓库。
- **2026-10-19** — 新增 **`context-persistence`**（**1.2.0**）：把「换模型、隔天续同一任务时上下文不能丢」变成一套可执行契约。地基是 **KV Cache 友好注入**：上下文拆成 **A 静态前缀**（身份，写一次后字节级冻结）/ **B 状态栏**（每轮追加到对话末尾的 `<agent_status>`）/ **C 参考层**（跨会话事实 + 近期日志）/ **D 外部来源**（采集时原样存、注入时统一包裹为不可信数据）四条通道，并明令**禁止把 time / 状态 / 进度写进 system 前缀**——实测踩坑代价是 TTFT 0.5s→3-5s、账单近乎翻倍。配套四件事：**记忆层分层声明**（`## 标题 〔常驻〕` 整节注入 / `〔按需〕` 只列名，渲染唯一出口是 `render_memory_excerpt()`）；**三个动作**（开场 `layout` / 每回合末 `capture` / 结束 `flush` + `export` 生成可移植握手包）；**模型适配注册表**（workbuddy / claude / gpt / raw，新增模型只写一份 wrapper，不动存储层与核心代码）；**外部内容单一咽喉点**（采集与包裹解耦，但不给「忘记」留位置）。另含体量边界（`[A]/[C]` 有 cap、`[B]/[D]` 无 cap，压缩判据是「最坏每轮达窗口 80%」而非「数字看着大」）与一条硬教训：**装载位置与收尾纪律同等重要**——本技能曾在交付后 15 天零写入而失效，根因是只存在于不被会话收录的目录。已加入 `scripts/sync-from-local.py` 白名单与 `CATALOG.md`。
- **2026-10-08** — 新增 **`devils-advocate`**（通用版 **1.0.0**）：一个**反方批判者 / 毒舌陪练**模式，对**已经成形**的想法、方案或判断做对抗性审查，而不是提供安慰。三条核心纪律：**零奉承但不零确认**（事实层面成立的判断必须直说——一个从不承认对方正确的批判者，其否定会退化成背景噪声）；**阈值制输出**（只报跨过「承重线」的风险，≤ 5 条且**无下限**，一条都不过线就直说「本轮无承重级问题」）；**自动降档**（连续若干轮挑刺未被采纳，即判定未被使用并主动停供）。另含三档强度（轻 / 标准 / 全力）、缺参数单列（计入未决项总数，不另开旁路）、模式边界（断言式，不适用于想法尚在概念期）。已加入 `scripts/sync-from-local.py` 白名单与 `CATALOG.md`。
- **2026-10-08** — `de-ai-flavor` 升版 **1.6.2**（**`SKILL.md` 瘦身，功能零变化**）：入口文件由 20,957 B / 6,495 tok 压到 **13,411 B / 4,051 tok**（o200k；cl100k 4,986），**两个口径均回到自设的「SKILL.md < 5k token」上限之内**。做法全部是**搬移与去重**，不动任何触发条件、判据、规则编号或 linter：① 原「来源与许可」整章（版本沿革 + 证据引注 + 已知局限，约占入口 30%）外移 —— **证据源与逐版沿革**并入 `references/04`，**已知局限**归入 `references/10` 第 7 / 8 节（并补上 linter 的两处覆盖缺口：`05` 第 3 / 10.1 条无法正则判定、英文直引号内引文未机械排除），`SKILL.md` 只留许可 / 借鉴来源 / 证据基础 / 指针四行；② 原「三个层次」+「语言门控」+「路由表」三张各列一遍同一批文件的表**合并为一张「加载路由表」**（行 = 文件，列 = 层 / 语言 / 何时读）；③「输出前自查」由 12 条压到 7 条，与上一节重复的保真项收成一行「保真四查」指回本节。文件数不变（16）
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
| [`spp-source-principle`](skills/spp-source-principle/) | Execution engine for the Source Principle Protocol (SPP v4.0 R4.4) — load-bearing conclusions, subject co-construction, evidence chains, three-state governance, G/A/S tri-axis, irreversible-operation gating, contract-priority adjudication, collaboration posture and anti-sycophancy, session persona modes | R4.4 | stable | 27 |
| [`de-ai-flavor`](skills/de-ai-flavor/) | Removes "AI flavor" from LLM output (Chinese + English) — bilingual banned-word lists, **parallel** Chinese and English discourse/syntax rules, **per-language** do-not-change lists, format / markup-artifact cleanup, persona snippets, fidelity guardrails, an **evaluation layer** (AI-Check forensic scoring + a deterministic Python linter; diagnose only, never rewrite), and **decision boundaries** (context-level exclusions + sample-overrides-all) | 1.6.3 | stable | 16 |
| [`devils-advocate`](skills/devils-advocate/) | Devil's-advocate / adversarial-review mode — pressure-tests a plan you already hold: zero flattery but not zero acknowledgement, threshold-based output (only risks past the load-bearing line, with no floor), three intensity levels, missing parameters listed separately, automatic de-escalation once its critiques go unused, and explicit mode boundaries | 1.0.0 | stable | 1 |
| [`context-persistence`](skills/context-persistence/) | Cross-model / cross-session context persistence with KV-cache-friendly injection — a four-channel contract (A static prefix / B status bar / C reference layer / D external sources), memory-layer injection declarations ([resident] injects / [on-demand] names only), three actions (layout on open / capture each turn / flush+export on close), a model-adapter registry, a single choke point that wraps all external content as untrusted data; plus an **engine three-branch check** (engine present → use it / obtainable → deploy, never rebuild / neither → hand-run the embedded task-state contract), the embedded `task_state.json` field contract, and the **engine published with the skill** (`engine/` subdirectory, Python 3 stdlib only) | 1.3.1 | stable | 6 |

See [`CATALOG.md`](CATALOG.md) for the full listing (with generated descriptions, versions and file counts), produced by `scripts/build-catalog.py` from each skill's frontmatter.

> **Note**: `context-persistence` is a **protocol and behaviour specification**; the engine it drives ships with the skill under [`skills/context-persistence/engine/`](skills/context-persistence/engine/) — a **read-only distribution copy** you deploy into a target project's `.workbuddy/context/` (three steps in `engine/DEPLOY.md`). Without the engine, its "task-state contract" section documents every field, so the fallback path is copy-not-guess.

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
    ├── de-ai-flavor/
    ├── devils-advocate/
    └── context-persistence/
        ├── SKILL.md
        └── engine/            # Execution body (read-only distribution copy)
            ├── context_manager.py    # Main engine (Python 3 stdlib only)
            ├── k_lint.py             # K-surface consistency self-check
            ├── measure_context.py    # Read-only volume meter
            ├── model_adapters.json   # Model adapter registry
            └── DEPLOY.md             # Three-step deployment to any project
```

### Installation

The skill directory name must match the `name` field in `SKILL.md`. Installing means copying the whole `skills/<name>/` directory into your client's skills directory.

```bash
git clone https://github.com/mcaserhn/skills.git /tmp/skills
cp -r /tmp/skills/skills/spp-source-principle ~/.workbuddy/skills/   # WorkBuddy
cp -r /tmp/skills/skills/de-ai-flavor        ~/.workbuddy/skills/
cp -r /tmp/skills/skills/devils-advocate     ~/.workbuddy/skills/
cp -r /tmp/skills/skills/context-persistence ~/.workbuddy/skills/

# Engine for context-persistence (it came along with the skill above; required
# for the full command set). The engine has to live in the PROJECT's
# .workbuddy/context/ to run - the copy under skills/ does not:
mkdir -p <your-project>/.workbuddy/context
cp ~/.workbuddy/skills/context-persistence/engine/context_manager.py \
   ~/.workbuddy/skills/context-persistence/engine/k_lint.py \
   ~/.workbuddy/skills/context-persistence/engine/measure_context.py \
   ~/.workbuddy/skills/context-persistence/engine/model_adapters.json \
   <your-project>/.workbuddy/context/
python <your-project>/.workbuddy/context/context_manager.py --ws <your-project> init

# cp -r /tmp/skills/skills/<name> ~/.claude/skills/                  # Claude Code
```

### Conventions

- **Single source of truth**: authoring happens in the local `~/.workbuddy/skills/`; this repository is the published mirror. Sync is one-way and whitelisted - nothing is ever written back
- **Publishing trap for `context-persistence`**: `sync-from-local.py` mirrors each whitelisted skill as a **whole directory** (delete-then-copy). If your staging copy holds only `SKILL.md` and omits the `engine/` subdirectory, the next publish **deletes the engine from this repository**. Stage the full 6 files (`SKILL.md` + `engine/`) when publishing it
- **Publish flow**: author locally -> `python scripts/sync-from-local.py` -> `python scripts/validate.py` -> `python scripts/build-catalog.py` -> `git commit && git push`
- **Adding a skill**: copy `template/skill-template/` -> develop locally -> add the directory name to the whitelist in `scripts/sync-from-local.py` -> run the flow above
- **Frontmatter baseline**: `name` (must equal the directory name), `description` (non-empty, <= 1024 chars), `license`, plus `version` and `status` (either top-level keys or `metadata.` sub-keys - the repo scripts fall back between both)
- **Line endings**: locked to LF by `.gitattributes`

### Recent changes

- **2026-10-20** — `spp-source-principle` moves to **R4.4** (**Re-Discovery rebuild**; 27 files, append-only incremental remount, no new files). The R4.4 protocol is final (1,613 lines, revision agenda batches A-H each through its own Gate), and every new clause is now mounted verbatim: §2.3 contract-priority table, §2.5 collaboration posture, §2.6 anti-sycophancy (with the single-source list split against `de-ai-flavor`), §8.1 progress broadcast + progressive-output guardrail, §8.2 thinking-externalization guardrail, §10.1 proactive declaration, §10.4.4 emotional objectivity, §11.7 self-model disclosure, §11.8 quality-vocabulary boundary guardrail, §12.5 post-dissent execution, §13.4 bright-line list for irreversible operations, §17.5 persona modes, §17.6 proactivity-tiers guardrail; entry-layer wiring (flow diagram / routing table / Override commands / pre-output minimum checks) is synced too. The four conditional-introduction devices land as guardrails only (no devices enabled), with a 2-4 week observation window whose triggers roll back and log on firing. The R4.3 baseline (27 files) is archived; the chain runs skill package -> GitHub mirror, one way
- **2026-10-20** — `de-ai-flavor` released as **1.6.3** (**SPP R4.4 cross-reference; criteria and linter untouched**). Implements the §2.6 "list split (single source)" clause with two-way cross-references: principle authority lives in SPP §2.6, the operational word lists live here, and each side re-checks the other after changes. Four exception clauses added: identity-fact statements in an identity-declaration context ("I am an AI collaborator") and borrowed quality vocabulary (honest / prudent / diligent) do not fall inside the "assistant-tone pleasantries" hit range; the scope is limited to identity-declaration contexts, barred from conclusions / evidence / analysis bodies, with rollback defined as quality words wrapping an unevidenced conclusion (full ban and log). The exception simultaneously resolves the apparent conflict between the "as an AI" ban and SPP §11.7's self-model disclosure duty. Banned-word lists, discourse/syntax rules, do-not-change lists and linter rule IDs are all untouched
- **2026-10-20** — `context-persistence` patched to **1.3.1** (**documentation-drift repair, zero behaviour change**). A repo-wide drift audit (catalog regeneration diff / engine vs mechanism authority byte comparison / every documented command vs the engine's `argv` branches / directory tree vs `ls-tree` / the Python-version claim) found two documentation gaps: the engine's 20 top-level commands were documented as 18 (`show` and `wrap-external` were missing), and layer-2's identity path `~/.workbuddy/…` had not been aligned with the generalised environment prerequisites. Both fixed; every other audit item came back clean (the 4 engine files are byte-identical to the mechanism authority, CATALOG regenerates with zero diff, the trees match reality, and the "3.8+" claim holds thanks to `from __future__ import annotations`).
- **2026-10-20** — `context-persistence` released as **1.3.0** (**portability fix, zero mechanism change**), with the **engine published alongside the skill** at `skills/context-persistence/engine/` (4 engine files + `DEPLOY.md`). Origin: a fresh environment (different user, different home directory) loaded the skill and had to rebuild the state layer by guesswork, because the engine was not on the publish surface and the skill carried no inline contract. Three fixes: (1) "environment prerequisites" rewritten as an **engine three-branch check** — engine already in the project → use it; obtainable → **deploy, never rebuild** (copy 4 files + `init` + verify with `k_lint`); neither → hand-run the documented fallback; (2) a new "**task-state contract**" section embeds every `task_state.json` field, entry shape, flush mechanics and file format, turning the no-engine fallback from guesswork into copywork; (3) an explicit ban on **re-implementing the engine from the spec** (it necessarily forks the implementation, and once a fork becomes the de-facto authority the mechanism can never be pulled back). The injection contract, volume boundaries, memory-layer rules, three actions and external channel are untouched. `engine/` is a **read-only distribution copy** inside the skill directory: mechanism changes go back to the mechanism authority, never into this repository.
- **2026-10-19** — new skill **`context-persistence`** (**1.2.0**): turns "context must not be lost when switching models or resuming the same task days later" into an executable contract. Its foundation is **KV-cache-friendly injection**: context is split into four channels — **A static prefix** (identity, frozen byte-for-byte after the first write), **B status bar** (an `<agent_status>` block appended to the end of the dialogue each turn), **C reference layer** (cross-session facts + recent journal), and **D external sources** (stored verbatim on capture, wrapped as untrusted data on injection) — with an explicit ban on writing time / status / progress into the system prefix; the measured cost of that mistake is TTFT 0.5s -> 3-5s and a near-doubled bill. Four mechanisms come with it: **memory-layer injection declarations** (`## Heading [resident]` injects the whole section / `[on-demand]` lists the name only, with `render_memory_excerpt()` as the single rendering exit); **three actions** (`layout` on open / `capture` at the end of every turn / `flush` on close plus `export` for a portable handoff bundle); a **model-adapter registry** (workbuddy / claude / gpt / raw — adding a model is one wrapper, never a change to the storage layer or core code); and a **single choke point for external content** (decoupling capture from wrapping, leaving no room for "forgot"). It also carries volume boundaries (`[A]/[C]` capped, `[B]/[D]` uncapped, with compression gated on "worst-case turn hits 80% of the window" rather than "the number looks big") and one hard lesson: **where a skill is loaded matters as much as wrap-up discipline** — this skill once died from 15 days of zero writes because it lived only in a directory no session ever scans. Added to the `scripts/sync-from-local.py` whitelist and `CATALOG.md`.
- **2026-10-08** — new skill **`devils-advocate`** (general-purpose, **1.0.0**): an **adversarial-review / devil's-advocate** mode that pressure-tests an already-formed idea, plan or judgement instead of offering reassurance. Three disciplines carry it: **zero flattery but not zero acknowledgement** (when a point is factually sound it has to be said out loud — a critic who never concedes degrades into background noise); **threshold-based output** (only the risks that cross the load-bearing line, at most five and with **no floor** — if none qualify, it says so in a single line); and **automatic de-escalation** (after several rounds of unused critiques it declares itself unused and stops supplying more). It also carries three intensity levels (light / standard / full), a separate listing for missing parameters (folded into the open-items total instead of opening a side channel), and mode boundaries (assertion-style; not for ideas still in the concept stage). Added to the `scripts/sync-from-local.py` whitelist and `CATALOG.md`.
- **2026-10-08** — `de-ai-flavor` released as **1.6.2** (**`SKILL.md` slimmed down, zero functional change**): the entry file went from 20,957 B / 6,495 tok to **13,411 B / 4,051 tok** (o200k; cl100k 4,986), bringing **both encodings back under this skill's self-imposed "SKILL.md < 5k tokens" cap**. Every change is a move or a de-duplication — no trigger condition, criterion, rule ID or linter rule was touched: (1) the former "sources and licence" chapter (version history + evidence citations + known limitations, roughly 30% of the entry) was relocated, with **evidence sources and the version-by-version history** folded into `references/04` and **known limitations** into `references/10` sections 7 / 8 — which also picks up the linter's two remaining coverage gaps (`references/05` items 3 and 10.1 cannot be decided by regex, and quotations inside straight double quotes are not mechanically excluded) — leaving `SKILL.md` with four lines for licence, borrowed sources, evidence basis and pointers; (2) the former "three layers" + "language gate" + "routing table" sections — three tables each listing the same set of files — were **merged into a single load-routing table** (rows = files, columns = layer / language / when to read); (3) "self-check before output" dropped from 12 items to 7, with the fidelity items that duplicated the preceding section folded into one "fidelity four-check" line pointing back to it. File count unchanged (16)
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
