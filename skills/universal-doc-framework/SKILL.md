---
name: universal-doc-framework
description: Universal Doc Framework（通用文档骨架与规范）。自包含 skill：通用文件夹结构 + 命名规范 + 文档命名一体化，安装即可离线使用。用于各类课题调研、需求调研（软件与业务逻辑）、软件系统开发全流程（需求/设计/开发/验证/UAT/上线）、系统盘点+逆向+复刻、技能/Agent/Harness 打造打磨、专业方向与科研规划。当用户要新建项目目录、设计文件夹结构、定文档或对象命名、问"这个项目该怎么组织/分几个阶段/文件怎么命名"、或需要 AI 一进项目就自动识别场景与阶段时使用。触发词：项目结构、文件夹结构、目录规范、文档命名、命名规范、骨架、新建项目、scaffold、六段骨架、USP。
license: MIT
version: "1.1.2"
status: draft
---

# Universal Doc Framework（通用文档骨架与规范）

本 skill 是**完整自包含包**：规则正文、脚手架、校验器、示例都在本目录内，不依赖任何宿主工作区。安装后 Agent 可直接读取、直接执行。

## 1. 能力一句话

用一套六段骨架组织任意项目，用一套受控命名体系给对象起名，用 `AGENTS.md` + `task_state.json` 让 AI 零交代接手。

- **命名层**：复用上游 `aden-naming-standard` v1.4（外部 skill，本包只引用、不复制条款）。
- **结构层**：`docs/01` 定义六段通用骨架 `00-Ingest / 10-Analyze / 20-Build / 30-Verify / 40-Deliver / 50-Sustain`。
- **识别层**：静态 `AGENTS.md` + 动态 `.workbuddy/context/task_state.json` + 指向上游的命名 lint。

## 2. 包内资产

路径基准：**本 skill 根目录**。文中出现的 `docs/NN`、`tools/NN` 即包内同名文件。

| 路径 | 作用 |
| --- | --- |
| `docs/01-universal-folder-structure.md` | 结构规范正文（USP v1.1）：六段骨架、目录树规则、字符纪律、审计 |
| `docs/02-naming-extension-registry.md` | 扩展取值登记表（本地 Draft，按上游 §9.3 全字段登记） |
| `docs/03-scenario-profiles.md` | 六类场景投影、单一/混合落地步骤、`AGENTS.md` 模板、命名示例 |
| `docs/04-document-naming-scheme.md` | 文档名称方案（DocName v1.0）：双形态、13 类文档类型、AI 四步选名 |
| `docs/05-naming-system.md` | 完整命名体系（NamingSystem v1.0）：9 类对象全景 + 按对象类型选式总表 |
| `tools/scaffold.py` | 项目骨架生成器：只建空骨架，已存在一律跳过 |
| `tools/place_doc.py` | 产物落位器：按规范命名并建空文档壳，不写内容 |
| `tools/structure_lint.py` | 结构校验器：查六段目录、`AGENTS.md` 字段，命名项委托上游 lint |
| `tools/sync_from_workspace.py` | 维护者用：从开发样板工作区同步规范与工具，`--check` 可查漂移 |
| `examples/sample-project/` | 脚手架生成的示例项目（六段齐全，可直接对照） |
| `examples/naming-samples.md` | 合规/不合规命名对照，示例均经上游 lint 验证 |

> **普通用户无需关心同步脚本**。它只服务于包维护者：把开发样板工作区的 `docs/` 与两个工具同步进本包，保证分发副本不漂移。

**依赖声明**：Python 3（标准库即可）必需；Node.js 与上游 `aden-naming-standard` skill 可选。缺少上游 lint 时只报"命名校验未完成"，不输出合规判定。

## 3. 六类场景

`Academic` 课题调研 · `BusinessLogic` 业务逻辑需求 · `Software` 软件开发全流程 · `Reverse` 盘点+逆向+复刻 · `AgentCraft` 技能/Agent/Harness · `Career` 专业方向与科研规划。

完整投影表见 `docs/03` §1。混合场景判据：两条工作流是否共享同一份输入与结论 —— 共享则同一实例不同阶段，不共享则用 `W<nn>-<主体>` 并行实例（`docs/01` §4.2）。

## 4. 工作流

### 4.1 判定场景

用户没明说场景时，按 `docs/03` §1 的六段投影判断；判不了就问用户，不要默认塞进某一类。

### 4.2 命名：先判对象类型，再选式选值

**第 0 步 · 判对象类型**（查 `docs/05` §5 决策总表）：要命名的是文档 / ISMS 文件 / 业务域 / 项目组合 / 站点 / 计算机账号 / 文档内标识码 / 数据对象？各自进对应命名式。**只有"文档"才走下面的文档名称流程**；其余按 `docs/05` §4 对应卷引用上游，不自造。

**文档名称流程**（`docs/04`）：

1. 读 `AGENTS.md` 的 `scenario` 声明；
2. 查 `docs/04` §4 四步表定四段：组织前缀（§4.1）/ 文档类型（§4.2）/ 域（§4.3）/ 状态（§4.4）；
3. 文档类型与域段用**载体形**（`InformationNote`、`10Server`，段内大小写分词、去空格去下划线），不是登记表里的词典形 —— 映射见 `docs/04` §1；
4. 段间用 `-` 连接，跑 lint 校验；判不了就问用户。

工作场景优先在 ADEN 既有 5 类文档类型里找，找不到才用扩展 8 类（`docs/04` §4.2 优先级规则）。域段随**具体场景**选取，不按"ADEN 工作"这类笼统标签套用。

### 4.3 生成骨架

```bash
SKILL_DIR=<本 skill 根目录的绝对路径>   # 展开成绝对路径，不要照抄变量
python "$SKILL_DIR/tools/scaffold.py" <目标目录> --scenario <场景> \
  --name "<项目名>" [--mix single|parallel] [--phases 00,10,20] [--with-context] \
  [--instance W01-Career:Career --instance W02-AgentCraft:AgentCraft]
```

脚本只创建不存在的对象，已存在的跳过并报告，**绝不覆盖**（对齐存量豁免 §1.3）。`--with-context` 只输出部署提示，不自动初始化引擎。

**并行实例一次生成**：`--instance` 可重复，格式 `<Wnn-主体>:<场景码>`。根级建共享六段，每个实例目录内嵌完整六段（`docs/01` §4.2）。给出 `--instance` 时自动按 `parallel` 处理；`--phases` 只作用于根级，实例内始终完整六段。

**两步法兜底**：只写 `--mix parallel` 而不给 `--instance` 时，脚本只建根级骨架，并在 `AGENTS.md` 与输出里留下兜底提示。此时对每个实例目录再跑一次脚手架即可：

```bash
python "$SKILL_DIR/tools/scaffold.py" <目标目录> --scenario Career --name "画像与简历"
```

`structure_lint.py` 会检查每个 `W<nn>-<主体>` 目录内的六段与 `AGENTS.md`；若声明了 `mix_mode: parallel` 却没有实例目录，给 `§4.2` WARN（不硬判违规）。

### 4.3.1 骨架与内容的分工（硬纪律）

**脚手架只建空骨架，绝不预置内容文档。** 这是本 skill 与内容型技能（SPP 课题共构等）的边界，违反会造成「先出结论再找证据」：

- **doc-framework 管语法** —— 目录长什么样、文档叫什么名、落在哪一段。
- **SPP 等内容技能管语义** —— 写什么、凭什么成立、结论是否承重。

因此：

1. `scaffold.py` 只生成六段 + 每段 README + 根 `AGENTS.md` / `README.md`。**不应**在调研/共构开始前创建带具体内容的文档（评估维度、权重、产品清单、调研结论等）。
2. 内容**结晶之后**才落文档：某个结论/纪要/规格经 SPP 共构成型、有证据支撑，才调用 `place_doc.py` 建壳并填写。
3. 空段就留空，放 README 说明即可（`docs/01` §3.3）。骨架完整 ≠ 每段都要有文档。

### 4.3.2 按需落位（内容结晶后调用）

```bash
python "$SKILL_DIR/tools/place_doc.py" <项目根> \
  --type InformationNote --domain Academic \
  --subject "Zoho定价调研纪要" --phase 20-Build \
  --prefix PERS --purpose "记录 Zoho 定价的证据与来源"
```

- `--type` / `--domain` / `--prefix` / `--status` 是**受控值白名单**，即席造词直接报错（取值见 `docs/04` §3）；判不了就问用户，不要猜。
- `--phase` 决定落位段；`--status` 留空时按段推导（00/10/20→Draft、30→Review、40→Approved，见 `docs/04` §4.4）。
- 生成的文档**只有元数据头和空章节**，正文留白；工具**不写任何内容**，也不覆盖已存在文件。
- SPP 产物到文档类型/段位的推荐映射见 `docs/03` §7.1。

### 4.4 部署动态状态层（可选）

若用户要跨会话续接（"隔天继续""换模型""记住进度"），把 `context-persistence` 引擎部署到 `<目标目录>/.workbuddy/context/` 并 init —— 走那个 skill 的 `engine/DEPLOY.md`，不要手工重建引擎。

### 4.5 校验

```bash
python "$SKILL_DIR/tools/structure_lint.py" <目标目录>
```

命名合规另行调用上游权威 lint：

```bash
node <aden-naming-standard skill 根>/scripts/naming-lint.js --root <目标目录>
```

或把脚本路径放入环境变量 `ADEN_NAMING_LINT` 后，`structure_lint.py` 会自动调用；`.js` 脚本按扩展名选 `node` 执行。

## 5. 三条纪律

1. **规则单一权威**：命名条款以上游为准；本包 `docs/` 只做结构层、扩展取值与选名消歧，不在多处复制上游条款。
2. **不覆盖存量**：生成时遇到已存在目录/文件一律跳过；改名/移动/迁移须先拿用户确认（§1.3 + 不可逆动作检查点）。
3. **校验跑不通就报未完成**，不得凭手感下"合规/违规"结论（`docs/01` §8.2）。

## 6. 失败分支

| 现象 | 处理 |
| --- | --- |
| `docs/` 或 `tools/` 缺失 | 报"skill 包不完整"，停止生成；禁止即兴造一套规范正文 |
| scaffold.py 不存在 | 报"脚手架未部署"，按 `docs/01` 手工建六段骨架（结构在本文已列全） |
| 场景判不了 | 问用户，不要默认归类 |
| 命名 lint 跑不起来 | 报"命名校验未完成"，不输出合规判定 |
| 上游 `aden-naming-standard` 未安装 | 结构层仍可用；命名层只做本包选名表路由，不声称完成上游合规校验 |
