# 10 · 缩写与编号的标准依据（全球检索报告）

> **文档定位**：回答一个被提出的问题——**"是否存在一套通用的、跨行业的缩写／编号定义表？"**
> 本文是 `docs/00-glossary.md`（本项目符号登记表）的**外部依据**：它说明我们那 5 条纪律不是凭经验拍的，而是有国际标准与方法论可援引。
> **状态**：v1.0（2026-10-10）· 研究稿。
> **检索范围**：ISO / IEC / ISO-IEC JTC 1 / ITU、UNECE（UN/CEFACT）、EU（IATE）、中国国家标准化管理委员会（GB/T）、ISACA / The Open Group / AXELOS、DAMA International，以及 Google / Microsoft / IBM / Chicago 等头部组织的写作与治理规范。
> **证据分级**：✅已确认（标准现行版本 / 官方页面） · ⚠️部分确认 · 🔶判断（本报告结论）。

---

## 1. 结论先行

### 1.1 一句话回答

**不存在一张跨域通用的"缩写／编号定义表"。** 标准界的答案不是"给你一张表"，而是"**给你一套建表与管表的方法**"。

### 1.2 但存在**三层**已被标准化的工作

| 层 | 是什么 | 代表标准 | 你能拿它做什么 |
|---|---|---|---|
| **第一层｜方法标准** | 教你**怎么建、怎么管**一张符号表 | ISO 704、ISO 1087、ISO 10241-1、**ISO/IEC 11179-5**、GB/T 1.1、GB/T 20001.1 | 制定本项目符号登记表**本身的规则** |
| **第二层｜领域权威注册表** | 某个域内**全球唯一**的代码／符号清单 | ISO 3166、ISO 4217、ISO 639、ISO 8601、ISO 80000、ISO 2145、IEC 81355、ISO 20022、UN/CEFACT、IATE、术语在线 | **直接引用**，不要自己另造 |
| **第三层｜组织内受控词表** | **你自己的**术语／缩写表（必须自己建） | DAMA-DMBOK（业务词汇表）、Google／Microsoft 写作规范、Entra 命名标准 | 本项目**真正要做的**那一层 |

> **关键判断**：前两层是"别人已经做好的"，第三层"没人能替你做"。
> **本项目已有的 `docs/00-glossary.md` 属于第三层，其规则依据来自第一层**——方向是对的，只是此前没有把依据写出来。

### 1.3 真正"通用"的例外（数量极少）

只有**域内封闭**的对象才可能做到全球唯一：

- **单位与量**：SI ／ ISO 80000、IEC 80000（科学工程界通用）
- **日期时间格式**：ISO 8601
- **国家／货币／语言代码**：ISO 3166 ／ ISO 4217 ／ ISO 639
- **文档章节编号法**：ISO 2145

这些之所以能通用，是因为**对象是有限闭集**。而"缩写"面对的是**无限开放的自然语言**，先天无法穷举，故不存在通用表。

---

## 2. 第一层：方法标准 —— "怎么建一张符号表"

这是与我们的问题**最直接相关**的一层。核心是 ISO/TC 37（语言与术语）系列，外加 ISO/IEC JTC 1 的元数据注册标准。

| 标准 | 名称 | 与"缩写表"的关系 |
|---|---|---|
| **ISO 704:2022** | Terminology work — Principles and methods | 术语工作的**总方法**（第 4 版，取代 2009 版）。**明确区分 full form（全称）与 abbreviated form（缩写形式）**，规定称谓（designation）如何生成与选择——正是"先定义后使用"的依据 |
| **ISO 1087:2019** | Terminology work and terminology science — Vocabulary | 术语学的**概念框架**（概念／客体／称谓／定义）。ISO 704 的规范性引用 |
| **ISO 10241-1:2011** | Terminological entries in standards — Part 1 | 规定**标准文档里术语条目怎么写**（条目编号、首选术语、缩写形式、符号、弃用术语、排序、索引）。`docs/00` 表格结构的国际对标 |
| **ISO 860:2007** | Terminology work — Harmonization of concepts and terms | **多套术语体系如何协调合并**——正是本项目"两套并行编号线"遇到的场景 |
| **ISO 24156-1:2014** | Graphic notations for concept modelling (UML) | 概念关系的图形化表达 |
| **ISO/IEC 11179-5:2015** | Metadata registries (MDR) — **Part 5: Naming and identification principles** | **最贴近"定义表"的权威母标准**。规定命名约定的**六原则**：Scope（范围）· Authority（机构）· Semantic（语义）· Syntactic（句法）· Lexical（词法）· **Uniqueness（唯一性）**。中国等同采用为 **GB/T 18391.5-2009** |
| **ISO/IEC Directives, Part 2**<br>（第 9 版，2021） | Principles and rules for the structure and drafting of ISO/IEC documents | ISO/IEC **自家文件的编辑规则**：§8.4 **Abbreviated terms**、§9 量与单位、Annex B/C（标准项目标识）。这是"标准是怎么写标准"的原始规则 |
| **GB/T 1.1—2020** | 标准化工作导则 第1部分：标准化文件的结构和起草规则 | 中国"标准的标准"。**§3.2.8 规定「符号和缩略语」应作为文件第 4 章**，由"引导语 + 清单"构成，**严格按字母顺序排列**（大写→小写→无角标→字母角标→数字角标→希腊字母→特殊符号） |
| **GB/T 20001.1—2024** | 标准编写规则 第1部分：术语 | 术语条目与数据类别的**编排与起草要求** |
| ISO 1951 / ISO 25964 | 词典条目的表示 ／ 叙词表 | 词表的结构化表示（进阶参考） |

> **可直接挪用的一条**：GB/T 1.1 的排序规则（§3.2.8）是一个**开箱即用的登记表排序法**，比"想到哪写到哪"强。

---

## 3. 第二层：领域权威注册表 —— "某域内全球唯一"

**不要自己另造**，直接引用下表（涉及代码／编号时）。

### 3.1 通用基础代码（跨行业，最接近"通用表"）

| 标准 | 对象 | 权威维护方 | 备注 |
|---|---|---|---|
| **ISO 3166** | 国家／地区代码 | ISO 3166/MA | 字母二位／三位 + 数字码。**允许免费使用** |
| **ISO 4217** | 货币代码 | SIX Financial Information AG（代表瑞士 SNV） | 三位字母+三位数字；前两位源自 ISO 3166。**免费使用** |
| **ISO 639** | 语言代码 | ISO 639/RA | 免费使用 |
| **ISO 8601** | 日期／时间表示 | ISO/TC 154 | 项目看板、CSV 时间戳应对齐 |
| **ISO/IEC 80000**（含 IEC 80000 各部分） | 量与单位（ISQ/SI） | ISO+IPO 联合 | **符号用斜体、单字母、不得用多字母缩写当量符号** |
| **ISO 2145:1978** | 书面文件章／条**编号法** | ISO/TC 46 | 只许阿拉伯数字、层级用点号、末层不加点、引言可用 0。LaTeX 原生符合；**Word 默认样式不符合** |

### 3.2 工程 / 文档 / IT 域代码

| 标准 | 对象 | 要点 |
|---|---|---|
| **IEC 61355-1:2008 → IEC 81355-1** | 成套装置／系统的**文档种类代码（DCC）** | 三字母码 `&A1A2A3`：A1 技术领域（A/B/C/E/M/P）、A2 主类（A–W）、A3 子类。**61355 已废止，替代为 81355**——引用时注意版本 |
| **IEC Electropedia (IEV)** | 国际电工词汇 | 2 万+ 术语，英法双解，官方在线词库 |
| **ISO OBP**（Online Browsing Platform） | ISO 术语与图形符号在线库 | 查 ISO 标准用语的第一入口 |
| **ISO 20022** | 金融报文**数据字典 + 代码集** | "开放全球标准"，报文元素级定义——企业财务系统常见 |
| **UN/CEFACT Web Vocabulary + UNCL** | 贸易／运输／金融代码表 | 含 UN/LOCODE（地点码）、货币、单位等；以 SKOS 概念体系发布 |
| **Dublin Core / ISO 15836** | 元数据元素集 | 跨域最简元数据集 |

### 3.3 术语库（"已有权威表"的实例）

| 术语库 | 主管 | 规模 |
|---|---|---|
| **IATE**（Interactive Terminology for Europe） | 欧盟各机构联合 | 约 60 万条记录 / 600 万+ 术语 / 24 种欧盟语言；域分类基于 **EuroVoc** |
| **术语在线 termonline.cn** | **全国科学技术名词审定委员会** | 已审定公布 **180 种**规范名词、**60 余万条**；**国务院 1987 年批示其公布名词具权威性与约束力**，科研／教学／出版应遵照使用 |
| **ISO OBP ／ IEC Electropedia** | ISO ／ IEC | 见上 |

> **实操建议**：写中文技术文档时，**"术语在线"是中文侧最接近"权威通用表"的东西**；写英文／跨语言时用 IATE + ISO OBP。

---

## 4. 第三层：组织内受控词表 —— "你自己必须建的那张表"

这一层没有国际标准能替你完成，但**有成熟的实践模式可以照搬**。分三类：

### 4.1 写作规范（限制"用不用缩写"）

| 来源 | 核心规则（与本次问题直接相关） |
|---|---|
| **Google developer documentation style guide**（Abbreviations） | ① 首次出现写全称 + 括注缩写；② **能写全就不缩写**；③ 禁用 `i.e./e.g.`；④ 不把缩写当动词（`Use SSH to log in`，不写 `ssh into`）；⑤ 缩写不加句点 |
| **Microsoft Writing Style Guide**（Acronyms） | ① **不从产品／功能名造缩写**；② 只用受众熟悉的缩写；③ **只出现一次的词就不引入缩写**；④ 标题／小标题里避免首次引入缩写；⑤ 全称小写（专名除外）；⑥ 避免所有格 |
| **Chicago Manual of Style ／ IBM Style** | 与上述同源，强调"一致性优先于机械合规" |

> 一句话：**两大厂的规范都主张"少用缩写"**，这与我们 `docs/00` 纪律 4「默认不用缩写」完全一致。

### 4.2 数据治理（怎么把表管起来）

| 来源 | 关键内容 |
|---|---|
| **DAMA-DMBOK**（Data Management Body of Knowledge） | 定义 **11 个知识域**，其中 **"参考数据与主数据管理"** 与 **"元数据管理"** 正是"术语／代码表"的归属。治理被定位为**统御层** |
| **业务词汇表（Business Glossary）治理模型**（OvalEdge 等厂商实践总结） | **角色**：域负责人 / 术语管理员（steward）/ 治理委员会，用 RACI 划清；**流程**：提交 → 域评审 → 治理批准 → 发布；**生命周期**：`Draft → Under Review → Approved → Deprecated → Retired`；**元数据字段**：定义、负责人、域、关联术语、同义词、关联数据资产；**质量控制**：查重、查残缺、查冲突 |
| **企业命名规范实践**（Entra ID / Intune） | 前缀体系（`CFG-` `GRP-` `LIC-` `GPO-`）；**"一个概念一个缩写，并写下来"**；**"只存在于某个人脑子里的标准不算标准"**；用脚本（Graph API）反向审计不合规对象 |

### 4.3 本项目的对照（StreamLens 已经做了什么）

| 本项目的做法 | 对应的标准／实践 | 差距 |
|---|---|---|
| `docs/00-glossary.md` §1 五条使用纪律 | ISO 704「先定义后使用」+ Google/Microsoft「少用缩写」 | **未写明标准依据**（本文补上） |
| §2 已登记符号表（唯一定义处） | ISO/IEC 11179-5「Uniqueness / Authority」原则 | 未使用 11179-5 的**域限定（namespace）** 概念 |
| §3 冲突清单 + §4 整改建议 | 业务词汇表的**冲突检测与治理流程** | 未做**生命周期状态**（每个符号只区分"登记/冲突"，没有 Approved/Deprecated） |
| §5 维护（先登记后使用） | ISO 10241-1 的条目维护 | 未定义**变更影响与版本** |

---

## 5. 为什么"通用表"不可能存在（根因分析）

不搞清楚这一层，"找一张表"会变成反复踩同一个坑。

1. **域相对性**：同一个 `PM` 在项目管理域是 Project Manager、在生产域是 Preventive Maintenance、在化学里是 Particulate Matter。**没有任何机构有权限裁定谁对。**
2. **语言相对性**：**ISO 自己就是最有力的反例**——其名称在英文是 IOS、法文是 OIN，于是创始人干脆**放弃首字母缩写**，取希腊词 `isos`（平等）作跨语言短名。一个连自己名字都无法用缩写统一的组织，不可能发布通用缩写表。
3. **一词多义是系统性的**：公开词典站 `abbreviations.com` 收录 ISO 一条就有 **66 个含义**（国际标准化组织 / In Search Of / 相机感光度 / 光盘镜像…）。反过来说，**"一个字母只属于一个轴"（我们的纪律 3）之所以必须本地自建，正因为全局不可能唯一。**
4. **结论**：标准机构能做的，只是①**规定方法**（第一层）、②**在自己管的封闭域内发权威表**（第二层）。**开放域的"表"必须由使用它的组织自己建**——这就是第三层。

> **这正好解释了此前那次审计的根因**：`D2`、`W/A/P/L` 之所以是缺陷，不是因为"格式不规范"，而是因为**它们诞生在散文里、没有登记处**。现在这条判断有了标准出处（ISO 704 + ISO/IEC 11179-5）。

---

## 6. 对本项目的 3 条可选升级（建议，非必做）

保持 `docs/00` 现有 5 条纪律不动，仅在必要时增补：

| # | 建议 | 依据 | 代价 |
|---|---|---|---|
| **U1** | 在 `docs/00` §1 前增加一句"**标准依据**"，列出 ISO 704 / ISO/IEC 11179-5 / GB/T 1.1 三个编号 | 第一层 | 极低（3 行） |
| **U2** | 给 §2 登记表增加一列 **`状态`**（`Approved / Deprecated / Retired`），对齐业务词汇表生命周期 | DAMA／业务词表实践 | 低（改表头 + 现有行填 `Approved`） |
| **U3** | 引入 **`域限定`（namespace）** 概念：跨域同名符号加前缀（如 `源-P0` / `待办-P0`）——**正是 §3 最后一行已提的整改方向** | ISO/IEC 11179-5 Scope 原则 | 中（需改 `docs/02/03/07` 引用） |

> 三者都是"锦上添花"。**当前 5 条纪律本身已无缺陷**，本文的作用是让它从"凭经验"变成"**有出处**"。

---

## 7. 参考清单（可核查）

**方法标准**
- ISO/TC 37/SC 1 标准目录：https://www.iso.org/committee/48116/x/catalogue/
- ISO 704:2022（Terminology work — Principles and methods）
- ISO 1087:2019（Vocabulary）
- ISO 10241-1:2011（Terminological entries in standards）
- ISO 860:2007（Harmonization of concepts and terms）
- ISO/IEC 11179-5:2015：https://standards.iteh.ai/catalog/standards/iso/d8045933-a05f-4b62-a86f-ee002f182730/iso-iec-11179-5-2015
- GB/T 18391.5-2009（等同采用 ISO/IEC 11179-5:2005）
- ISO/IEC Directives, Part 2（第 9 版，2021）：https://www.iso.org/sites/directives/current/part2/index.xhtml
- GB/T 1.1—2020 §3.2.8（符号和缩略语）／GB/T 20001.1—2024（术语编写规则）

**领域注册表与术语库**
- ISO 4217 货币代码：https://www.iso.org/iso-4217-currency-codes.html
- ISO 2145:1978 章条编号法
- IEC 81355-1（前身 IEC 61355-1）文档种类代码：https://std.iec.ch/iec61355/
- IATE（EU 术语库）：https://iate.europa.eu/
- 术语在线（全国科学技术名词审定委员会）：https://www.termonline.cn/ ；机构：https://www.cnterm.cn/
- UN/CEFACT Web Vocabulary：https://vocab.unece.org/
- ISO OBP：https://www.iso.org/obp

**写作与治理实践**
- Google developer documentation style guide — Abbreviations：https://developers.google.com/style/abbreviations
- Microsoft Writing Style Guide — Acronyms：https://learn.microsoft.com/en-us/style-guide/acronyms
- DAMA-DMBOK（Data Management Body of Knowledge）
- Business Glossary Governance Model（角色／流程／生命周期）
- Enterprise Naming Standards（Entra ID / Intune 前缀命名）

---

## 8. 一句话留给决策

> **没有"通用缩写表"，只有"通用的建表方法"。**
> 本项目真正需要的不是去外面找一张表，而是**把 `docs/00-glossary.md` 这张自建表管好**——它现在缺的只是"依据"和"生命周期"，不缺规则本身。
