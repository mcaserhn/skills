# Engine deployment · 把状态层装进一个项目

`skills/context-persistence/SKILL.md` 描述**契约**（A/B/C/D 注入、三个动作、失败模式）；本目录是**执行体**。二者分开：技能负责「怎么做是对的」，引擎负责「把它做出来」。**换机器、换用户、换家目录都不影响——引擎只依赖 Python 3 标准库。**

## 清单

| 文件 | 作用 |
|---|---|
| `context_manager.py` | 主引擎：`layout` / `bootstrap` / `init` / `goal` / `decide` / `progress` / `subgoal` / `artifact` / `open_question` / `flush` / `export` / `adapter` / `external` 等全部命令 |
| `k_lint.py` | K 面一致性自检（引用 / 时效 / 体量 / 编号 / 清单条数），ERROR 时 exit 1 |
| `measure_context.py` | 只读体量盘点仪 |
| `model_adapters.json` | 模型适配注册表（`init` 会自动补一份） |

## 部署（三步，约 1 分钟）

在**本文件所在目录**执行（也就是技能目录下的 `engine/`——仓库 clone 后是 `skills/context-persistence/engine/`，已安装到客户端后是 `<宿主家目录>/skills/context-persistence/engine/`；两处文件相同，命令不变）。`<项目>` 换成你的项目路径：

```bash
# 1. 引擎就位（四个文件就在当前目录，无需再找 engine/ 子路径）
mkdir -p <项目>/.workbuddy/context
cp context_manager.py k_lint.py measure_context.py model_adapters.json \
   <项目>/.workbuddy/context/

# 2. 初始化（建 journal/、写空 task_state.json、补 model_adapters.json）
python <项目>/.workbuddy/context/context_manager.py --ws <项目> init

# 3. 验证（期望：0 ERROR / 0 WARN）
python <项目>/.workbuddy/context/k_lint.py --ws <项目>
```

Windows PowerShell 等价物（同样在本文件所在目录执行）：

```powershell
# 1. 引擎就位
New-Item -ItemType Directory -Force "<项目>\.workbuddy\context"
Copy-Item context_manager.py,k_lint.py,measure_context.py,model_adapters.json "<项目>\.workbuddy\context\"

# 2. 初始化
python "<项目>\.workbuddy\context\context_manager.py" --ws "<项目>" init

# 3. 验证
python "<项目>\.workbuddy\context\k_lint.py" --ws "<项目>"
```

`python` 用你机器上的 Python 3（3.8+ 即可，详见下方「版本」说明）。

## 之后

- 开场：`python <项目>/.workbuddy/context/context_manager.py --ws <项目> layout`
- 收尾：`... flush "今日摘要"`
- 改完文档 / SSOT / 术语表：跑一次 `k_lint.py`

命令全集与行为契约见技能入口 `../SKILL.md`（即 `skills/context-persistence/SKILL.md`）；本目录不含说明书。

## 常见问题

| 现象 | 原因 / 处置 |
|---|---|
| `layout` 的 [A] 段是空的 | 身份三件套（`<宿主家目录>/.workbuddy/{SOUL,IDENTITY,USER}.md`）不存在 → **不是故障**，L0 未配置而已，降级为空继续用 |
| 换机器 / 换用户后找不到状态 | 状态在**每项目**的 `.workbuddy/context/task_state.json` 里，不随技能走；搬项目请连同 `.workbuddy/` 一起搬，或用 `export` 生成可移植握手包 |
| 没有 Python | 按 `SKILL.md`「任务层契约」节用文件工具手工维护 SSOT；**不要照 SKILL.md 重写引擎**——那必然产出分叉实现 |
| 引擎版本不明 | 校验 `task_state.json` 的 `schema_version`（当前 `1.0`）；契约不兼容时以 SKILL.md 契约节为准升级 |
| Python 版本要求 | **3.8+**。脚本用了 `dict \| None` 这类 PEP 604 联合类型注解，但三个脚本都带 `from __future__ import annotations`，注解在运行时不求值，故 3.8 可跑；无需第三方包 |
| `cp` / `Copy-Item` 找不到文件 | 你在错误的目录执行——命令必须在**本文件所在目录**（`engine/`）运行；更早期的 DEPLOY 版本写过 `cp engine/…`（按仓库根），已废，勿照抄旧教程 |

## 边界（不要越界）

- 本目录是**只读分发副本**：修 bug / 改机制请回到机制权威处，不要把改动的引擎回写给本仓库。
- 不要把 `task_state.json` / `journal/` / `memory/` 等运行时数据提交进本目录——它们是项目态内容，不是机制。
- 每个项目一份引擎副本是刻意设计（项目自治）；但这意味着**修引擎要记得同步各项目**，校验用 `k_lint.py`。
