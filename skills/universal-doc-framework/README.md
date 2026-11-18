# universal-doc-framework

**通用文档骨架与规范** —— 一套自包含的 AI Agent 技能：通用文件夹结构 + 命名规范 + 文档命名。

安装后即可离线使用：规则正文、脚手架、校验器和示例都在技能包内，不依赖作者的本机工作区。

## 它能做什么

- 为课题调研、需求调研、软件开发、系统盘点逆向复刻、Agent 打磨、专业与科研规划六类场景生成同一套六段骨架；
- 按对象类型路由到正确命名式，为文档 / ISMS 文件 / 业务域 / 项目组合 / 站点 / 账号 / 内容层标识 / 数据对象自动选名；
- 生成 `AGENTS.md` 静态识别契约，支持与 `context-persistence` 的动态状态层接缝；
- 脚手架只建**空骨架**，内容文档经 SPP 等技能共构结晶后，用 `place_doc.py` 按规范命名落位（空壳不写内容）；
- 校验骨架结构与命名形式，校验跑不通时只报「校验未完成」，不凭手感判合规。

## 安装

技能目录名必须与技能 ID 一致：`universal-doc-framework`。

```bash
# macOS / Linux：本技能位于集合仓库的 skills/ 子目录
git clone https://github.com/mcaserhn/skills.git /tmp/skills
cp -r /tmp/skills/skills/universal-doc-framework \
  "$HOME/.workbuddy-ai/skills/universal-doc-framework"
```

```powershell
# Windows PowerShell
git clone https://github.com/mcaserhn/skills.git "$env:TEMP\skills"
Copy-Item -Recurse -Force "$env:TEMP\skills\skills\universal-doc-framework" `
  "$env:USERPROFILE\.workbuddy-ai\skills\universal-doc-framework"
```

在 WorkBuddy 中，用户级技能从 `~/.workbuddy-ai/skills/` 发现；安装后若技能列表未刷新，重开会话即可。触发词包括：项目结构、文件夹结构、目录规范、文档命名、命名规范、骨架、新建项目、scaffold、六段骨架、USP。

升级：

```bash
git -C /tmp/skills pull
cp -r /tmp/skills/skills/universal-doc-framework/. \
  "$HOME/.workbuddy-ai/skills/universal-doc-framework/"
```

## 目录结构

```
universal-doc-framework/
├── SKILL.md                      技能入口（Agent 读取）
├── README.md                     本文件
├── CHANGELOG.md                  版本记录
├── LICENSE                       MIT
├── docs/                         规范正文（01–05）
├── tools/
│   ├── scaffold.py               项目骨架生成器（只建空骨架）
│   ├── place_doc.py              产物落位器（规范命名 + 空文档壳，不写内容）
│   ├── structure_lint.py         结构 + 命名校验入口
│   └── sync_from_workspace.py    维护者用：同步与漂移检查
└── examples/
    ├── naming-samples.md         合规/不合规命名对照
    └── sample-project/           脚手架生成的示例项目
```

## 快速使用

```bash
SKILL_DIR="$HOME/.workbuddy-ai/skills/universal-doc-framework"

# 生成项目骨架
python "$SKILL_DIR/tools/scaffold.py" ./my-project \
  --scenario Software --name "客户门户" --mix single

# 内容结晶后再落位（只建空壳，不写内容）
python "$SKILL_DIR/tools/place_doc.py" ./my-project \
  --type InformationNote --domain Academic --subject "定价调研纪要" \
  --phase 20-Build --prefix PERS --purpose "记录定价证据"

# 校验（设置 ADEN_NAMING_LINT 指向上游 naming-lint.js 可同时校验命名）
python "$SKILL_DIR/tools/structure_lint.py" ./my-project

# 混合场景：一次生成根级共享六段 + 两个实例各自的六段
python "$SKILL_DIR/tools/scaffold.py" ./duo --scenario Software --name "客户门户" \
  --mix parallel \
  --instance W01-CustomerPortal:Software \
  --instance W02-BusinessRules:BusinessLogic
```

更完整的场景判定、命名路由与失败分支见 `SKILL.md` 与 `docs/03-scenario-profiles.md`。

## 依赖与边界

- **必需**：Python 3（仅标准库）。
- **可选**：Node.js；上游技能 `aden-naming-standard` v1.4（提供权威命名 lint）。
- 本包**不复制**上游命名规范的条款原文；命名细目以 `aden-naming-standard` 为准。未安装上游技能时，命名校验只报「未完成」，不输出合规判定。
- 本地扩展取值（组织前缀、文档类型、域码等）全部是**本地 Draft**，不是集团受控值，升级须走上游 §9.3 流程。
- 存量对象一律豁免；生成器只建新对象，不覆盖已有文件。

## 维护者：与开发样板工作区同步

`docs/` 与两个工具是从开发样板工作区同步过来的分发副本。维护者可用同步脚本检查或更新：

```bash
export UDF_WORKSPACE=/path/to/设计一套通用的文件夹结构
python tools/sync_from_workspace.py --check   # 只检查漂移，有差异退出 1
python tools/sync_from_workspace.py           # 按源文件覆盖副本
```

同步脚本不会改动 `SKILL.md`、`README.md` 等包内自有文件，也不会删除多余文件。

## 许可

MIT，见 `LICENSE`。
