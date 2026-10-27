# 11 · ADEN 内部命名与标识存量盘点 + 个人规范设计（草案）

> **文档定位**：`docs/10` 回答的是"**外面有没有通用表**"（第一层方法标准 / 第二层领域注册表 / 第三层组织受控词表）。
> 本文回答的是另一个问题：**"我们自己已经有什么表？"** ——把 ADEN 两个大库（Enterprise_Solutions、Global_Infrastructure）以及此前 6 个目录的存量命名/编号/标识**全量盘点**，找出规律，并据此设计一套**第一层采标 / 第二层注册表 / 第三层自建词表**的个人规范草案。
> **定位变更（2026-10-12 收口 · 重要）**：**本文自此为「研究底稿」**——只保留盘点、证据、规律、缺陷与裁决记录；**不再承担规范职责**。
> **规范正文已独立成文 → `docs/12-aden-naming-and-identifier-standard.md`**（纯净产物：只含条款，无检索过程、无缺陷清单、无 AI 判断标记）。两者冲突时**以 `docs/12` 为准**；本文 §5 降格为「设计推导记录」。
> **状态**：v0.5（2026-10-12）· 研究底稿（**冻结**）· 检索 + 归纳 + 设计稿 + Q1–Q6 裁决回写 + §2.10 / §3.4 / §4 缺陷-12~缺陷-15 / §5.6 / §5.7 · **未修改任何既有文件、配置或产物**。
> **编号变更（2026-10-12 · 按 `docs/12` §8.1 R-AB-3 收口）**：本文的「命名缺陷族」原用 `D-1…D-15`，与 `context/07-decisions.md` 的**决策族** `D-01…D-12`、`docs/07` 的**分发三式** `D1/D2/D3` 同字母三套并存（`D-01` 与 `D-1` **仅差一个补零**，人工扫读必混）。现**缺陷族迁出 `D`，改为全称式 `缺陷-1…缺陷-15`**（不缩写、不占拉丁字母轴）；决策族维持 `D-01…`（权威处 `context/07`）。
> **裁决日期**：2026-10-12（Stanley）。裁决要点见 §7。
> **证据分级**：✅ 有原始文件名/原文正文可核 · ⚠️ 推断（证据不完整） · 🔶 本报告判断。

---

## 0. 检索范围与规模（✅）

| # | 位置 | 文件数 | 目录数 | 体积 |
|---|---|---|---|---|
| 1 | `Aden Group\Enterprise_Solutions - Documents` | 1,433 | 170 | 6.9 GB |
| 2 | `Aden Group\Global_Infrastructure - Documents` | 17,204 | 3,835 | 62.2 GB |
| **2 库小计** | | **18,637** | **4,005** | **69.1 GB** |
| 3 | 此前已检索的 6 个目录 | — | — | — |
| **合计** | | **≈ 19k** | **≈ 4.1k** | **≈ 69 GB+** |

**扩展名分布（前 8）**：Enterprise_Solutions = `.pptx 426 / .xlsx 299 / .potx 183 / .pdf 147 / .docx 102 / .sql 79`；Global_Infrastructure = `.xlsx 2465 / .docx 2271 / .html 1843 / .jpg 1537 / .pptx 1352 / .pdf 1036 / .doc 652 / .txt 642`。

> **口径说明**：本盘点以**文件名与目录名**为主证据（这是命名规范的直接载体）。对其中 2 份**规范文档本体**做了正文提取（`AGI-Group Standard-Front End Naming Convention v0.3.docx`、ISMS 索引图探测）。

---

## 1. 最大的发现：ADEN 早已有成文的命名体系（✅）

`Global_Infrastructure` 里存在一份**由 Elliott Jiao 起草、2018-10-31 创建、2022-01-17 更新至 v0.3 的集团标准**：

```
AGI-Group Standard-Front End Naming Convention v0.3.docx
（副本共 5 处：backup\006_Standard、2_ServiceSupport\08_Documentation\006_Standard、
  6_General\10_AGI Document MGMT\00_Group Standard\00_FrontEnd、066_One Voice Project\Docs\SD、
  1_ServiceDelivery\39. capex_Vietnam IT Standard\...\6. Project Summary）
```

**这意味着**：本项目此前"从零设计命名规范"的前提是错的——**底座已经存在，且是集团标准级（Group Standard）**。个人规范的定位应改为：**继承 + 收口 + 补缺**，而不是另起一套。

---

## 2. 存量清单（按资产类型）

### 2.1 文档分类体系 —— 5 类（✅）

`Front End Naming Convention v0.3` 正文的 `DOCUMENT CLASSIFICATION` 勾选框，与 `6_General\10_AGI Document MGMT` 的目录结构**互相印证**：

| 序号 | 文档类型（英文原文） | 中文对应 | 目录位置 |
|---|---|---|---|
| 1 | **Exploratory Study** | 预研报告 | `40_Exploratory Study` |
| 2 | **Information Note** | 信息说明 / 操作指引 | `10_Information Note` |
| 3 | **Position Note** | 立场说明 | `30_Position Note` |
| 4 | **Group Standard** | 集团标准（正式发布级） | `00_Group Standard` |
| 5 | **Group Service** | 集团服务（政策类） | `20_Group Service` |

**文档头字段（模板固化）**：`FROM / TO / COPY / SUBJECT / ISSUE DATE / VERSION / STATUS / APPROVALS / DOCUMENT CLASSIFICATION`。
**文档历史表结构**：`Version | Revision | Who | date (mm/dd/yyyy)`。

> 这是全世界通行的**文档种类代码（DCC）**思路，与 `docs/10` §3.2 的 **IEC 81355-1** 同源——ADEN 的做法是"**类型名 + 主题 + 版本**"，而非 IEC 的"三字母码"。

### 2.2 ISMS 四级文件体系（✅，第二层注册表）

ISO 27001 文档层级，ADEN 已用**四个类型码 + 三位流水号**落地：

| 级别 | 类型码 | 中文语义 | 实例 |
|---|---|---|---|
| 一级 | **MAN** | 管理手册 | `Aden-ISMS-MAN001 信息安全管理手册 V1.0.docx`、`MAN002 适用性声明（SOA）V2.0` |
| 二级 | **SOP** | 程序文件 | `ADEN-ISMS-SOP001 文件管理程序` … `SOP030 Defender安全操作指导文档` |
| 三级 | **INS** | 规范 / 制度 / 工作指南 | `ADEN-ISMS-INS001 备份管理流程`、`INS002 变更管理流程`、`INS003 机房管理规定` |
| 四级 | **FOR** | 记录 / 表单 | `Aden-ISMS-FOR001 四级文件结构索引图` … `FOR032 相关方及其需求分析评审表` |

**编号式（✅）**：`<组织>-<域>-<子域>-<类型码><三位序号> <中文名>[ 版本]`
- 域示例：`ISMS`（信息安全管理）、`SUM`（供应商管理）
- 子域示例：`IMP`（实施）
- 完整例：`Aden-SUM-IMP-SOP001 供应商选择管理条例.pdf`、`Aden-SUM-IMP-INS006 供应商选择管理工作指南.pdf`
- 记录表格另有变体：`Aden SUM IMP FOR 01-09 采购申请单 Purchase Request Form_2022.01.xlsx`（**无连字符、序号含范围 `01-09`**）

> `Aden-ISMS-FOR001 四级文件结构索引图.xls` 本身就是**这套体系的索引图**（OLE2/BIFF8 格式，47 KB，需 Excel 打开）。

### 2.3 业务域编号轴（✅，第二层注册表）

**主域（Global_Infrastructure 顶层）**：`N_名称`
```
0_Achitect   1_ServiceDelivery   2_ServiceSupport   [3 缺]
4_Technical_Doc   5_Security&Compliance   6_General
```
**子域示例**：`00_AGI / 1_Infrastructure_HLD / 2_Compliance / 99_old_doc`（0_Achitect）；
`01_MajorIncedents … 10_opex_DataCleanup`（2_ServiceSupport，**06 缺**）；
`00. China Cybersecurity Law Compliance … 12. Cybercurity training / 90. Financing / 99. Reporting / 100.ToSLB`（5_Security&Compliance）。

**文档类型 × 域 的九宫格（✅，`10_AGI Document MGMT` 实际结构）**：
```
00_Group Standard   → 00_FrontEnd | 10_Server | 20_Networking | 30_Monitor&Log |
                      40_Security&Compliance | 50_Backup&Recovery | 60_Shared Folder |
                      70_Office365 | 80_Patch
10_Information Note → （同上 9 个域，编号完全一致）
20_Group Service    → Policy_Change Mgmt
30_Position Note
40_Exploratory Study
```
> **这就是第一层与第二层的接口**：**文档类型（纵轴 5 类）× 技术域（横轴 9 域）**。横轴 9 个域是一个**可直接复用的受控代码表**。

### 2.4 项目组合（Portfolio）编号 —— 五条并行编号线（✅，含冲突）

`1_ServiceDelivery` 下并存 **5 套**编号：

| 线 | 形态 | 范围 | 实例 |
|---|---|---|---|
| **S1** | `N_名称`（下划线） | 1–14 | `1_capex_MDM`、`2_capex_PC_standard`、`14_opex_ASEAN_ITenvorinment_Imporvement - 2017.9.19 ~ 11.12` |
| **S2** | `N. <capex\|opex>_名称 - 日期区间` | 1, 16–48 | `1. capex_FollowMe Print - 2017.1.10 ~ 4.10`、`16. capex_McAfee Deployment  - 2017.11.15 ~ 2018.1.19` |
| **S3** | 同 S2 | 51–60, 81–87 | `51.capex_Network Security_IPS`（**点后无空格**）、`81. opex_O365_LicRenewal` |
| **S4** | `NNNN. 名称`（四位文件柜） | 1000–1004 | `1000. MasterPlan`、`1001. SvrInf`、`1002. NetInf`、`1003. IT Infra Hosting Checklist`、`1004. ITIL Report` |
| **S5** | `NNN_名称`（三位文档登记） | 001–102 | `001_SOP`、`024_M365 SecureScore`、`102_365_MSFTTraCourse` |

**冲突证据（✅，均可核）**：
- **编号 1 被两条线占用**：`1_capex_MDM`（S1）与 `1. capex_FollowMe Print`（S2）。
- **分隔符三态并存**：S1 用 `_`、S2/S3 用 `. `、S3 中 `51.`/`59.`/`85.` 无空格 → **`.` 后空格不统一**。
- **S5 内部重号**：`068_Microsoft Purview` 与 `068_StructureOfTech-data-app`；`010_PhoneMeeting` 与 `010_RapidLife`；`99_new ITSM` 与 `099_new ITSM`、`99_new ITSM-old` 三者并存。
- **两处 S5 登记表已漂移**：`2_ServiceSupport\08_Documentation` 缺 `024`，而 `backup` 下存在 `024_M365 SecureScore`；`backup` 无 `007_Scripts/011…`，`08_Documentation` 有。
- **拼写错**：`46. opexx_SD-WAN`（opexx）；`2_ServiceSupport\01_MajorIncedents`（Incidents）；`12.Cybercurity training`（Cybersecurity）；`1_Ent._Solutions_PMO`（多一个点）。
- **成本标记缺失**：S1/S2/S3 共约 60 项中，约 1/4（如 `3_WAN_WLAN Restructure`、`27. SkypeforBusiness rollout`、`35. O365 MOVE`、`44. Kunshan F4.0 Office setup`）**没有 capex/opex 标记**。

> **⚠️ 裁决更新（2026-10-12）**：上述"重号"类冲突**不再一律视为缺陷**——按裁决，**跨「类型 × 域」的重号允许共存**（唯一性范围 = 类型 × 域，见 §5.4）。**同一 (类型, 域) 内**的线内重号仍需处理。**S1–S5 五线不并轨、既有命名一律不改动**。

### 2.5 位置 / 站点码（✅，第二层注册表）

**A. 列名注册表**（`0_Achitect\99_old_doc\20. MA Information\...`）：
```
中国：BCHD  BJG  CCR  CHS  CHZ  DAL  FY  HGZ  HQ  KUN  NAJ  NAT
      NCRR  NIB  QD  SCR  SHA1  SHA2_ECR_GSA  SHA3  SHA4  SHY  SUZ  TJN  WUX  XIA
SEA ：Indonesia  Laos  Vietnam(HANOI / HCM)
非洲：Guinea  Ivory Coast  Somalia
```
**状态后缀（✅）**：`<站点> - not connected`（如 `BCHD - not connected`、`XIA - not connected`）——**这是既存的"状态"后缀用法**。

**B. 官方附录**：`Front End Naming Convention` 正文含 **Appendix 1 – IATA country codes**（全文 200+ 条，✅）与 **Appendix 2 – Location Code**（标题存在，表体为嵌入对象，本次未提取 ⚠️）。
**C. 业务单元码**（合同命名中）：`GSA / GSHA / GSUZ / GWUX / GS / HQ / IFM`，如 `ADEN-GSA-洗衣服务-上海荣泰-2024.1.1-2026.12.31.pdf`。

### 2.6 对象命名式（✅，来自规范正文原文）

| 对象 | 命名式 | 备注 |
|---|---|---|
| 计算机名 | `C<Code1><LT/DT><Code2>-<Name1><Name2>` | `Code1`=IATA 国家码(2)；`LT`=Laptop/`DT`=Desktop；`Code2`=Office 码(3)；`Name1`=部门(3)；`Name2`=名字前 3 字母 |
| 员工账号 | `Firstname.Lastname<Digits>@<Domain>` | `Digits` 1–9 仅重名时用；`Domain`∈{`adenservices.com`,`axingservices.com`} |
| 通讯组·团队 | `<HQ/Region>-<Dept./Function>-<Scope/Sub-function>` | 例 `CN-GSA-SAL`、`HQ-IFM-SIGNIFY`、`ASEAN-SAL-ALL`、`RSM-BD-ALL` |
| 通讯组·项目 | `<HQ/Region>-<Dept./Function>-<Project>` | |
| M365 组·团队/项目 | **同 DL，但分隔符改为 `.`** | `<HQ/Region>.<Dept./Function>.<Scope>` |
| 共享邮箱·职能(团队) | `<Region/Dept.>.<function>@<Domain>` | 例 `HQ.LEG@`、`CN.FIN@`、`BJG.SAL@` |
| 共享邮箱·职能(项目) | `<Region+Function>.<Project>@<Domain>` | |
| 共享邮箱·系统 | `<Name1>.noreply@<Domain>` | |
| 非用户邮箱 | `<Name1>@<Domain>` | 例 `jobs@` |
| IT 支持单一入口 | `888it@adenservices.com` | |

**通用字符纪律（✅ 原文四条）**：
1. 禁用国别字符（重音、波浪号等），每个字符必须能在任意键盘/任意语言下输入。
2. **复合名每部分仅首字母大写，其余小写；大小写变化本身就用于区分各部分；不需要连字符**。
3. 连字符/破折号**仅**用于分隔"已定义名称"作为更大名称的一部分（如 Site Link name）。
4. 未特别说明时允许字符：`a–z`、`A–Z`、`0–9`、`-`。

### 2.7 版本号、日期、语言、状态后缀（✅，全库实测）

**版本号写法实测词频（前 12）**：
```
-V1.0 (128)  V1.0 (110)  -v0.1 (93)  v0.1 (61)  _v1.0 (46)  v1.1 (44)
_v0.2 (35)   v0.2 (29)   -V1.1 (29)  v2.0 (20)   -v0.2 (18)  _v0.1 (18)
```
→ 三个自由度：**分隔符** {`-`, `_`, 空格, 无} × **大小写** {`V`, `v`} × **段数** {2, 3, 4}（存在 `V1.5.1`、`v0.3.1`）。
→ 规范文档内部另有**纯数字**写法（`0.1 / 0.2 / 0.3`，文档历史表）与中文写法（`V2.0`、`V3.0`）。

**日期写法实测**：
```
YYYYMMDD     20190520(x120) 20240522 20180915   ← 主用（无分隔）
YYYY.M.D     2017.1.10  2024.1.1              ← 契约/项目目录
YYYY-MM-DD   2017-7-10                        ← 少数
YYYYMM       202603   202601                  ← 日志目录
YYYYHn/H1    2026H1 ;  YYYYQn/Q1  2026Q1 ;  YYYYWn/W10  2026W10
YTD 口径     2023 YTD 6 GSR ; YTD10 ; CPI_YTD11
mm/dd/yyyy   10/31/2018                       ← 仅文档历史表（美国制）
```

**语言 / 语向后缀**：`-cn`、`-en`、`-中文`、`CN`、`EN`、`_EN`、`_ENG`（并存）。
**状态/生命周期后缀（✅ 实测）**：`Final`、`final`、` - final`、`-s`、`-signed`、`Sample`、`_sample`、`previous`、`Archive`、`bkup`、`99_old_doc`、`-old`、`_old`、`backup`、`Copy`、`(1)(2)`、`-updated`、`UPD`、`；`中文`最终版`/`修改版`/`发布版`/`备份`、`- not connected`、`-Ongoing`、`-Done`。

### 2.8 在线保存失败产生的重复副本后缀（✅，2026-10-12 人工确认）

大量文件名尾部带 `-CCNLT<3字母>-<字母串>`，实测 16 种：

| 出现次数 | 后缀 | | 出现次数 | 后缀 |
|---|---|---|---|---|
| 15 | `CCNLTCHO-MISDEA` | | 2 | `CCNLTCHO-ITNIHU` |
| 12 | `CCNLTCHO-ITDEXU` | | 2 | `CCNLTCHO-ITSTHA` |
| 12 | `CCNLTCHO-ITKAH` | | 2 | `CCNLTSUZ-ITAARN` |
| 6 | `CCNLTCHO-SHTEST` | | 2 | `CCNLTSUZ-ITPARK` |
| 3 | `CCNLTSUZ-ITADOR` | | 1 | `CCNLTCHO-ITDEAN` / `ITWIW` / `ITELL`；`CCNLTINF-ECRKYO`；`CCNLTSUZ-ITAARON` / `ITSUN` / `MISELL` |

**定性（✅ 2026-10-12 Stanley 裁决，对应 Q1 / Q4）**：这**不是敏感度标签**——此前判断为 Microsoft Purview / AIP 自动标签，**已作废更正**。真实成因是：

> **文件在"在线保存"（OneDrive / SharePoint）时保存失败，系统自动另存了一份带 `-CCNLT…` 后缀的副本。** 属**偶发的系统异常产物**，**绝大多数正常文件中不存在**。

（后缀内 `CHO`=上海总部 / `SUZ`=苏州 / `INF`=基础设施，`MIS` / `IT` 为部门码——这些段由系统在另存时取自保存上下文，**不代表人工命名意图**。）

**规范处置**：声明为「**系统异常产物**」——① **不纳入**命名规则；② **不得人工模仿**；③ 在清理动作中列为**候选（须人工比对确认后方可删除）**。

### 2.9 其他组织前缀与文档码（✅）

`AGI-`（ADEN Group Infrastructure）、`ADEN-` / `Aden-`（大小写并存）、`AGTS-`（另一组织线）、`ES`（Enterprise_Solutions）。
文档码实例：`AGTS-Exploratory Study-AD Design-AD0-1 Aden AD Logical Design - Naming Convention v0.3.1_sample.docx`
→ 出现**第 4 级文档码 `AD0-1`** 与 **3 段版本 `v0.3.1`**、**`_sample` 后缀**。

### 2.10 内容内技术标识编码（✅，以 Satellite FDD v1.8 为实证）

命名不止"文件名 / 目录名"一层；**文档内部的标识码**是第二层，同样需要受控。以下取自
`Aden_Webtool_FDD_SatelliteSystem-D365FnO-MiddlewareObservability_Ch0-13_v1.8_Final.docx`（正文提取，✅ 3,433 行 / 14.3 万字符）：

| 标识族 | 形态 | 值域 | 实例 | 备注 |
|---|---|---|---|---|
| **接口码** | `INT-NN` | 01–13 | `INT-01` … `INT-13` | **两位补零**；文档明文声明为"单一权威编号"（§4.16.2） |
| 接口子项 | `INT-NN<字母>` | a– | `INT-01a`、`INT-03a` | **小写字母后缀**，表派生 / 部分实现（NSS 仓库常量） |
| **集成开放点码** | `INT-OP<n>` | 1–14 | `INT-OP1` … `INT-OP14` | **不补零**；"域前缀 + OP + 序号" |
| **文档级开放点码** | `OP-<n>` | 1–10 | `OP-1` … `OP-10` | 全文档 TBD 寄存器（§13）。**引用原样** —— 该 FDD 的实际写法，按 `docs/12` §7.2-8 不受规范约束、**不应**改造 |
| EOD 开放点码 | `EOD-Q<n>` | 1–6 | `EOD-Q1` … `EOD-Q6` | 章节局部命名空间 |
| 主数据开放点 | `MD-OP<n>` | 1–4 | `MD-OP1–4` | **范围写法**（en-dash） |
| 假设码 | `A<n>` | 7, 8 | `A7`、`A8` | 假设登记 |
| **延迟类别码** | `S / C / N / B` | 4 值 | `class N` | S=同步 / C=关键异步(<5min) / N=准实时异步 / B=批处理（§6.3 定义） |
| 需求码 | `FR-NN` | 09 | `FR-09` | |
| 章节号 | `Ch<n>–<n>` ／ `N.N[.N]` | 0–13 | `Ch0-13`、`4.16.2`、`6.5.13` | 多级十进制（ISO 2145 式） |
| 业务单据号 | `<业务前缀>+YYYYMMDD+<站点码>+<N 位序号>` | — | 期初库存号（`OI…`） | 由 `opening_number_seq` 生成 |

> **与 StreamLens 同族**：本项目的 `FR-01` / `NFR-0x` / `BASE-2026-00x` / `FO-YYMM-xxx` 就是同一范式——"**类型前缀 + 补零序号**"。它与 §2.6 的对象命名式（计算机名 / 账号 / 组）属于**不同命名层**（载体层 vs 内容层）。

**该实证同时暴露 4 处不一致** → 见 §4 的 缺陷-12～缺陷-15 与 §5.7 的统一规则。

---

## 3. 规律（归纳）

### 3.1 四条元规律（🔶）

| # | 元规律 | 证据 |
|---|---|---|
| **M1** | **"类型码 + 域码 + 流水号"三元组**贯穿全部体系 | ISMS `MAN/SOP/INS/FOR`＋三位号；文档 5 类；域 `00_–80_`；项目 `NN.` |
| **M2** | **同一体系里存在两条编号线（下划线线 vs 点号线）**，且互相不知道 | `1_capex_MDM` vs `1. capex_FollowMe Print`；`0_Achitect` vs `00. Policy_Standard`；`08_Documentation\006_Standard` vs `backup\006_Standard` |
| **M3** | **信息密度靠"段数"承载，不靠分隔符**——这与规范正文第 2 条"大小写变化即分隔"一致；但实际执行为省事而**退化为分隔符混用** | `-V1.0 / V1.0 / _v1.0 / v1.0` 四种写法表达同一件事 |
| **M4** | **状态靠后缀，且后缀是中英混杂的散词**（无受控词表） | `Final / final / -s / 最终版 / 发布版 / _sample / -signed / -Ongoing / -Done` |

### 3.2 三个"轴"（🔶，可直接作为规范的骨架）

```
轴 1｜是什么    ：对象类型（文档类型 5 类 / 文件类型 / 记录）
轴 2｜属于谁    ：域（技术域 9 域 / 业务域 / 组织）
轴 3｜第几版    ：时间（版本号 / 日期 / 周期口径）
```
ADEN 现有命名**全部可以分解到这三轴**——缺的只是"**轴内取值的受控词表**"与"**轴的书写顺序**"。

### 3.3 与原设计目标的映射（🔶）

| 会话中提出的概念 | 在存量里的对应物 | 状态 |
|---|---|---|
| 第一层：方法标准 | `Front End Naming Convention`（集团标准）+ ISO/IEC 11179-5 六原则 | ✅ 已存在，仅是"前端对象"域 |
| 第二层：领域注册表 | ISMS 四级码、技术域 9 域、位置码、IATA 附录 | ✅ 已存在，**分散在多处** |
| 第三层：自建受控词表 | 无（散在文件名里） | ❌ 缺 |

### 3.4 第五个观察：命名分两层，内容标识码另有四轴（🔶，2026-10-12 补）

| # | 元规律 | 证据 |
|---|---|---|
| **M5** | **命名有两层**：① **载体层**（文件名 / 目录名 / 对象名，§2.1–2.9）② **内容层**（文档内标识码，§2.10）。两层共用同一套"轴"逻辑，但**取值与唯一性范围各自独立**。 | FDD 的接口码 `INT-01` 与文件名末尾 `_Ch0-13_v1.8_Final` 是**两套**编号，互不冲突 |

**内容标识码的轴**（与 §3.2 三轴同构，值域另定）：

```
轴 1｜是什么   ：类型码 —— INT 接口 / OP 开放点 / A 假设 / FR 需求 / MD 主数据 / EOD 批次
轴 2｜属于谁   ：域前缀 —— 无前缀 = 文档级 / INT- = 集成域 / EOD- = 批次域 / MD- = 主数据域
轴 3｜第几号   ：序号 —— 补零位数（§5.7 统一为 2 位）
轴 4｜哪种变体 ：字母后缀 —— a/b/c（派生 / 部分实现，如 INT-01a）
```

---

## 4. 缺陷 / 漂移清单（✅，可核）

| # | 缺陷 | 证据 | 风险 |
|---|---|---|---|
| 缺陷-1 | **编号重号**（跨线 + 线内）—— **跨「类型 × 域」者按裁决允许共存** | `1_capex_MDM` ∥ `1. capex_FollowMe Print`；`068_Microsoft Purview` ∥ `068_StructureOfTech-data-app` | 仅**同 (类型, 域) 内**重号构成检索歧义（§5.4） |
| 缺陷-2 | **登记表双份且漂移**（裁决：**不合并**，见 §5.4） | `08_Documentation` 缺 `024`；`backup` 有 `024_M365 SecureScore` | 需指定主表；既有不改动 |
| 缺陷-3 | **分隔符三态** | `_` / `. ` / `.`（无空格）；`-` / `_` / 空格 / 无（版本号） | 机器排序失效 |
| 缺陷-4 | **版本号 6 种写法** | 见 §2.7 词频 | 无法自动比对版本先后 |
| 缺陷-5 | **状态后缀散词** | `Final/final/-s/最终版/发布版/_sample` | 无法判定"哪份是现行版" |
| 缺陷-6 | **组织前缀大小写不一** | `AGI-` / `ADEN-` / `Aden-` / `AGTS-` | 前缀分组统计错漏 |
| 缺陷-7 | **拼写错进入正式目录** | `opexx_`、`MajorIncedents`、`Cybercurity`、`Convent…` → 另有 `AGI-Group Standard-Naming Convetion-v0.1.docx`（Convention 拼错） | 影响检索命中 |
| 缺陷-8 | **日期 6 种写法** | `YYYYMMDD` / `YYYY.M.D` / `YYYY-MM-DD` / `YYYYMM` / `mm/dd/yyyy` / `YTDn` | 跨库时间排序不可比 |
| 缺陷-9 | **成本标记缺失约 1/4** | 项目目录缺 `capex_`/`opex_` | 财务口径归类不全 |
| 缺陷-10 | **中英混杂且无统一** | `中文文件名` 与 `EN` 混排；`-cn/-en/CN/EN/中文` 四种语言标记 | 双语版本管理混乱 |
| 缺陷-11 | **系统异常副本混入命名区** | `-CCNLTCHO-ITKAH`（§2.8，在线保存失败自动另存） | 若被当成命名法模仿会污染命名空间；清理时须人工比对 |
| 缺陷-12 | **标识码零填充不一致**（同文档内） | `INT-01`（2 位补零）∥ `INT-OP1`（不补零）∥ `OP-1`（连字符式）；`MD-OP1–4`（范围式） —— **引用原样，勿改** | 机器排序与自动引用失效 |
| 缺陷-13 | **范围写法混用** | `MD-OP1–4`（en-dash 范围）∥ 逐条 `INT-OP1`…`INT-OP14` —— **引用原样，勿改** | 检索 / 校验规则无法统一 |
| 缺陷-14 | **单字母类别码未登记** | `S / C / N / B`（延迟类别）仅在 FDD §6.3 定义、正文裸用（`class N`） | 跨文档裸引用会**重演 `W/A/P/L` 事故**（见 §5.6） |
| 缺陷-15 | **文件名状态段位置漂移 + 同版多状态** | `_Ch0-13_Complete_v1.0`（状态在 `v` 前）∥ `_Ch0-13_v1.2_CommentsDelphine`、`_Ch0-13_v1.8_Final`（状态在 `v` 后）；`_v1.7.docx` 与 `_v1.7_Final.docx` **并存** | 无法判定现行版；与本规范 §5.3.6 状态受控 5 值冲突 |

---

## 5. 规范设计（草案）

> **设计原则**：① **不推翻、不改动既有**（`Front End Naming Convention` 与 ISMS 体系直接继承，只做"轴化"与"受控化"；**2026-10-12 裁决进一步收紧：既有命名一律不动、五线不并轨、规范只约束新产物**）；② **一轴一符号**；③ **先定义后使用**；④ **默认不缩写**（与 `docs/00-glossary.md` 纪律一致）；⑤ 新增词表**必须落在唯一登记处**。

### 5.1 第一层｜方法标准（采标，不发明）

| 用于管什么 | 采标 | 落地动作 |
|---|---|---|
| 建表与命名的**总方法** | **ISO/IEC 11179-5**（Scope / Authority / Semantic / Syntactic / Lexical / **Uniqueness**）· 中国等同 **GB/T 18391.5-2009** | 每条注册项必须声明"域 + 授权方 + 唯一性范围" |
| 术语的**全称/缩写形式** | **ISO 704:2022** · ISO 1087:2019 | 登记表列"首选全称 / 缩写形式 / 弃用形式" |
| **符号与缩略语章节**写法 | **GB/T 1.1—2020 §3.2.8**（按字母序：大写→小写→…） | 登记表按此排序 |
| **章条编号法** | **ISO 2145:1978**（阿拉伯数字、点分层、末层无点） | 文档章节号；`docs/` 文件名沿用 `NN-` |
| **日期时间** | **ISO 8601** | 统一 `YYYYMMDD`（文件名）/ `YYYY-MM-DD`（正文） |
| **文档种类代码** | **IEC 81355-1**（前 IEC 61355-1） | 与 ADEN 的"文档类型 5 类"建立**映射表**，不替换 |
| **国家/货币/语言码** | ISO 3166 / 4217 / 639 | 直接引用；**ADEN 已用 IATA**（附录 1）→ 二者建映射，**不并轨** |

### 5.2 第二层｜领域注册表（继承 + 收口为一处）

> **核心动作**：把散落的 5 套注册表**收口成一张索引**，每张表指定唯一权威位置。**表体不改写，只登记指针。**

| 注册表 | 取值样例 | 现有权威位置 | 建议唯一权威位置 |
|---|---|---|---|
| **文档类型（5 类）** | Exploratory Study / Information Note / Position Note / Group Standard / Group Service | `6_General\10_AGI Document MGMT` | ✅ 沿用 |
| **技术域（9 域）** | `00_FrontEnd` `10_Server` `20_Networking` `30_Monitor&Log` `40_Security&Compliance` `50_Backup&Recovery` `60_Shared Folder` `70_Office365` `80_Patch` | 同上（Group Standard / Information Note 下各一份） | ✅ 沿用（**建议抽为独立受控表**） |
| **ISMS 文件层级（4 级）** | `MAN` → `SOP` → `INS` → `FOR` | `5_Security&Compliance` + `Aden-ISMS-FOR001 索引图` | ✅ 沿用，索引图为准 |
| **业务域码** | `ISMS` `SUM` … | 散在文件名 | 需**新建**登记 |
| **位置 / 站点码** | `BJG CHS CHZ SUZ WUX HQ KUN …` + IATA 附录 | `0_Achitect\99_old_doc\20. MA Information` + 规范附录 2 | **不并轨**（裁决 Q3）：IATA=国家码 / 列名=站点·办公点，语义不同 → **保留为两张独立注册表**，仅按需建映射（附录 2 表体待提取 ⚠️） |
| **业务单元码** | `GSA GSHA GSUZ GWUX GS HQ IFM` | 合同文件名 | 需**新建**登记 |
| **项目组合编号** | S1–S5 五条线（§2.4） | `1_ServiceDelivery` / `08_Documentation` / `backup` | 需**并轨 + 冻结**（见 5.4） |

### 5.3 命名式（模板，草案）

```
[组织前缀]-[文档类型]-[域]-[主体]-[版本][.扩展名]
    AGI|ADEN|AGTS     5 类之一   9 域之一   自由    vX.Y
```
**规则**：
1. **分隔符只允许** `-`（段间）与 `.`（扩展名前）；**禁用** `_`、空格、全角符号、国别字符。
2. **大小写**：段内每词首字母大写，其余小写；**不靠大小写区分段**（与规范正文第 2 条兼容但更严格，避免 `-V1.0`/`-v1.0` 分裂）。
3. **组织前缀**统一为 `AGI-`（文档）/ `ADEN-`（合同与记录），大小写固定。
4. **版本号**统一 `-vX.Y`（小写 v，两段起，第三段仅用于不兼容修订 `vX.Y.Z`）。
5. **日期**统一 `YYYYMMDD`（文件）、`YYYY-MM-DD`（正文）；周期口径统一 `YYYYQn` / `YYYYHn` / `YYYYWnn`（**周号补零**）。
   > ⚠️ **本条已被 `docs/12` §5.5 取代**：`docs/12` 另收「**期间标识段** `YYYY-MM`」（可读式，仅用于期间）。以 `docs/12` 为准。
6. **状态后缀**改为**受控 5 值**：`-Draft` / `-Review` / `-Approved` / `-Signed` / `-Retired`（替换 `Final/最终版/发布版/_sample`）。
7. **语言段**受控 2 值：`-zh` / `-en`（替换 `-cn/-中文/CN/EN/_ENG`）。
8. **系统异常副本后缀**（§2.8，`-CCNLT…`，在线保存失败时自动另存）**不得人工模仿**；规范中声明为"**系统异常产物、不参与命名规则、属清理候选**"。

### 5.4 编号分配与冲突解决（2026-10-12 裁决后）

> **裁决要点（Q2）**：**不执行并轨**；**既有命名一律不改动**；规范**只约束新产物**；**跨「类型 × 域」的重号允许共存**；**并轨方案仍须明确备案**（备查 ≠ 执行）。

**（1）唯一性范围（Uniqueness Scope）** —— 对齐 ISO/IEC 11179-5 的 *Uniqueness* 原则：

```
唯一性范围 = （对象 / 文档类型）× （域）
规则：同一 (类型, 域) 内序号唯一；跨 (类型, 域) 允许重号。
```

**（2）五条编号线的定位（不并轨，各自明确语义）**：

| 线 | 形态 | 定位（语义） | 范围 | 新产物去向 |
|---|---|---|---|---|
| S1 | `N_名称` | 早期 capex/opex 项目（下划线线） | 1–14 | 冻结（历史） |
| S2 | `N. <capex\|opex>_名称 - 日期区间` | 项目组合（点号线） | 1, 16–48 | 冻结（历史） |
| S3 | 同 S2 | 项目组合（点号线续） | 51–60, 81–87 | **新项目组合项入此线** |
| S4 | `NNNN. 名称` | 知识域柜（四位，非流水） | 1000–1004 | 按语义扩展 |
| S5 | `NNN_名称` | 文档登记（三位流水） | 001–102 | **新文档登记入此线** |

> **"不并轨"的含义**：S1/S2/S3 **物理上不合并、不重编号**；`1_capex_MDM` 与 `1. capex_FollowMe Print` **继续共存**。未来新产物只需**每线各取各的空号**。

**（3）并轨方案（仅备案，本次不执行）**：

```
若将来需要并轨（须另立决策）：
  合并 S1/S2/S3 → 一线：NNN. <capex|opex>_<项目名> - <YYYY.M.D> ~ <YYYY.M.D>
  S4（四位）保留为知识域柜 〔语义不同，不参与并轨〕
  S5（三位）保留为文档登记 〔语义不同，不参与并轨〕
  历史重号（如编号 1）→ 双方保留，加注"历史冲突"标记，不再新发
```

记录于此**备查**；**除另行决议外不予执行**。

**（4）文档登记表（`NNN_`）**：`2_ServiceSupport\08_Documentation` 与 `backup\` 两份登记**不合并**（既有不改动）。🔶 建议以 `2_ServiceSupport\08_Documentation` 为**在用主表**（新产物入此），`backup\` 视为**历史快照**；具体以人工确认为准。

**（5）其他编号**：

| 编号对象 | 分配规则 | 冲突处理 |
|---|---|---|
| ISMS `<类型码><NNN>` | 每类型独立三位流水 | 类型码固定 4 值，不得新增（新增须走 §5.5 流程） |
| 域码（主域/子域） | 两位十进制 `NN_` | `3` 空缺**保留不占用**（历史断层留白） |

### 5.5 登记与生命周期（草案，对齐 `docs/10` §4.2）

```
提交 → 域评审 → 批准 → 发布 → 弃用 → 退役
状态值：Draft → Under Review → Approved → Deprecated → Retired
```
- **唯一登记处**：新建一张 `naming-registry`（建议落 SharePoint 列表，与 `docs/09` 的 T3 载体一致）。
- **RACI**：域负责人（`elliott`=基础设施/前端；`jade`=D365；`stanley`=治理与裁决）。
- **审计**：每季度用脚本反向扫描文件名，输出**不合规清单**（对齐 `docs/10` §4.2 的"脚本反向审计"实践）。
- **变更影响**：注册项变更必须记录"影响到的既有路径数"。
- **分线声明（Q6）**：**明文凭据治理与命名规范分线**——本文只管命名与标识，凭据泄露另行独立处置。

### 5.6 缩写与代号纪律（含 AI 生成约束）

> **补此节的动因（✅ 本对话实证）**：AI 曾在正文里**即席造出**「托管四选 `W/A/P/L`」「分发三式 `D1/D2/D3`」——无定义处、跨会话无规律。`docs/00-glossary.md` §3/§4 已登记并给出整改，但**本文（命名规范草案）此前未收编该纪律**。现补入，使其成为命名规范的一部分。

**规则 R-AB-1 … R-AB-6**：

| # | 规则 | 说明 |
|---|---|---|
| **R-AB-1** | **先定义，后使用** | 任何字母 / 缩写首次出现，必须**同句或同表**给出全称；禁止以"见上文 / 见前表"代替 |
| **R-AB-2** | **必须登记** | 唯一登记处 = `docs/00-glossary.md` §2；**未登记即使用 = 缺陷**，审计须报出 |
| **R-AB-3** | **一轴一套符号，字母不复用** | 已被占用的字母不得再开新轴（占用情况**应**查登记表 —— `H/M/L`=风险、`FR`/`NFR`/`BASE`=需求与基线） |
| **R-AB-4** | **默认不缩写** | 仅当同时满足「跨 ≥3 处引用」且「已在本表登记」才引入字母 |
| **R-AB-5** | **枚举选项一律全称** | 3–4 项的一次性枚举，字母**零信息增益**（`W/A/P/L` 即反例）；确需编号时**首引必须带全称**（如「推送（D2）」） |
| **R-AB-6** | **AI 生成内容的额外约束** ⚠️ | 人机协作产物中，**AI 不得自造代号**；确需压缩时**只能复用已登记符号**，或**在正文内先给全称定义再使用**。发现未登记代号 → 视为缺陷 |

**同族陷阱（须警惕）**：`T1/T2/T3`（回流载体，`docs/09`）撞个人档案维护触发器 `T1–T5`，亦撞 🌐 SKU `Anonymous T1`；`P0–P3` 存在"源优先级 / 待办优先级 / 整改优先级"三套并存。
**对策**：跨域同名符号加**域限定前缀**（`源-P0` / `待办-P0`）——即 **ISO/IEC 11179-5 的 Scope 原则**。

### 5.7 内容内标识编码规范（草案，2026-10-12 新增）

> **本节的规范职责已移交 `docs/12` §7**（2026-10-12 收口）。以下保留**设计推导记录**；与 `docs/12` 冲突时**以 `docs/12` 为准**。
> 说明：本节示例一律取 `docs/12` v1.3 之后的口径（文档级标识码**补零**）；**引用既有文档的实际编码**（如 FDD 的 `OP-1` / `INT-OP1`）不受本规范约束，见 `docs/12` §7.2-8。

> 适用于**文档 / 规格 / 看板内部**的标识码（**非**文件名）。模板取自 §2.10 的 FDD 实证 + 本项目 `FR-/NFR-/BASE-` 实践。

**（1）标识式**

```
<域前缀>-<类型码>-<序号>[<变体字母>]
```

| 组成 | 取值 | 说明 |
|---|---|---|
| **域前缀**（可选） | `INT-` / `EOD-` / `MD-` … | 标识所属域；**省略 = 文档级**（如 `OP-01`、`FR-01`） |
| **类型码** | 2–4 字母，**须登记** | `INT` 接口 / `OP` 开放点 / `A` 假设 / `FR` 需求 / `NFR` / `BASE` / `MD` / `EOD` … |
| **序号** | **≥2 位、补零** | `INT-01`；超过 99 自然扩 3 位，**不重编号** |
| **变体字母**（可选） | 小写 `a/b/c` | 表派生 / 部分实现（`INT-01a`） |

**（2）规则**

1. **零填充统一 2 位**（修 缺陷-12）。
2. **类型码必须登记**于 `docs/00-glossary.md` §2 或域内注册表，**不得即席新造**。
3. **域前缀决定唯一性范围**：`INT-OP01` 与 `OP-01` 属**不同命名空间**，允许同号（对齐 §5.4「唯一性范围 = 类型 × 域」）。
4. **范围引用**统一写 `起–止`（en-dash）或"起 … 止"，**二者不混用**（修 缺陷-13）。
5. **单字母类别码**（如 `S/C/N/B`）**必须先登记**才可正文使用；裸用视为缺陷（修 缺陷-14，对齐 §5.6 R-AB-2）。
6. **章节号**沿用 **ISO 2145** 多级十进制（`4.16.2`）；**章节范围**统一 `Ch<n>–<n>`（如 `Ch0–13`），**不写** `Ch0-13`（连字符与减号歧义）。
7. **业务单据号**推荐 `<业务前缀>+YYYYMMDD+<站点码>+<N 位序号>`（对齐 FDD 期初库存号 `OI…`）；日期段一律 **ISO 8601 基本式**。

**（3）与载体层的边界**

| 层 | 对象 | 实例 | 唯一性范围 |
|---|---|---|---|
| **载体层**（§2.1–2.9） | 文件 / 目录 / 对象 | `..._Ch0-13_v1.8_Final.docx` | 路径内 |
| **内容层**（本节） | 文档内标识码 | `INT-01`、`FR-09`、`BASE-2026-001` | (类型 × 域) × 文档 |

---

## 6. 与 StreamLens 本项目的衔接

| 本项目既有物 | 落在哪一层 | 需对齐什么 |
|---|---|---|
| `docs/00-glossary.md` 5 条纪律 | 第三层 | 补"标准依据"（`docs/10` U1）；补生命周期状态（U2） |
| `docs/` 的 `NN-名称.md` | 第一层｜ISO 2145 应用 | 已经是 `NN-` 三位序，**符合** |
| `output/{dashboards,review,digest,data}/YYYY-MM-*.ext` | 第三层 | 已统一 `YYYY-MM`；建议在登记表登记为"产物命名定式" |
| 条目 id / `FR-` / `NFR-` / `BASE-` | 第三层｜**内容标识编码**（§5.7） | 已是"类型前缀 + 补零序号"范式，**符合**；唯一登记处 = `docs/00` §2 |
| 缩写 / 代号（`H/M/L`、`D1–D3`、`T1–T3`） | 第三层｜**缩写纪律**（§5.6） | 遵守 `docs/00` §1 五条纪律；**AI 不得自造代号**（R-AB-6） |
| `scope` 派生（d365/m365/shared） | 第三层｜受控取值 | 应登记进受控词表（目前只在代码里） |

> **一句话**：StreamLens 自己的命名其实是**本项目内最干净的一块**；真正的欠账在**公司存量库**，而那块已有集团标准可依——**个人规范的价值 = 把集团标准"轴化 + 受控化"，让 StreamLens 成为它的第一个合规样板**。

---

## 7. 人工裁决结果（2026-10-12）

> 由 Stanley 裁决；此前"须人工决定、AI 不得自决"的 6 项已全部落定。**裁决后仍未改动任何既有文件**。

| # | 原问题 | 裁决（2026-10-12） | 已回写处 |
|---|---|---|---|
| **Q1** | §2.8 的 `-CCNLT…` 后缀是否为敏感度标签？纳入还是例外？ | **不是敏感度标签**（此前"Purview/AIP"判断**作废**）。成因：**文件在线保存失败时系统自动另存了一份带 `-CCNLT…` 后缀的副本**。→ 声明为**系统异常产物**：不纳入命名规则、不得人工模仿、属清理候选。 | §2.8、§4 缺陷-11、§5.3.8 |
| **Q2** | 项目组合五线是否并轨？重号如何裁决？ | **不并轨**；**既有命名一律不改动**；**只规范新产物**；**跨「类型 × 域」的重号允许**；**并轨方案须明确备案**（备而不执行）。 | §2.4、§5.4 |
| **Q3** | IATA 附录 与 列名注册表 是否并轨？ | **不并轨**。二者语义不同（国家码 vs 站点/办公点），各保留独立注册表，仅按需建映射。 | §5.2 |
| **Q4** | 机器后缀与手工后缀的边界？ | 与 Q1 同源：`-CCNLT…` 系**在线保存失败自动副本**，**正常情况不存在**。边界即：**系统异常产物 ⟂ 人工命名**。 | §2.8 |
| **Q5** | 是否升级为集团标准（Group Standard）正式发布？ | **暂不发布**——"尚未形成一份纯净的产物"。本文**维持 Draft**；**不加入 `README` 目录表**。 | 文档头、§8 |
| **Q6** | 明文凭据治理是否与命名规范分线？ | **分线独立处理**。命名规范不承担凭据治理职责，另行处置。 | §5.5、§8 |

---

## 8. 本次检索的边界与未做

- **裁决后仍未改动（Q1–Q6，2026-10-12）**：裁决**已回写本文**，但**未触发任何既有文件、目录、配置的改动**；本文也**未发布**（Q5：维持 Draft，不进 `README` 目录表）。
- **未做**：任何文件的移动 / 重命名 / 删除 / 修改；任何配置与既有文档的改动。
- **未逐字读取**：Office/PDF 二进制正文（18k+ 个），仅 2 份规范文档提取正文；`ADEN-ISMS-FOR001 四级文件结构索引图.xls` 仅探测格式（OLE2/BIFF8），**未解析内容** ⚠️。
- **未覆盖**：`Global_Infrastructure` 中 `.jpg/.mp4/.ttf` 等非文档资产；`_gsdata_`、`__pycache__`、`.git` 等系统目录。
- **提取受限**：`Front End Naming Convention` 的 **Appendix 2 – Location Code** 表体为嵌入对象，未取到值 ⚠️。

---

## 9. 参考（本次可核对的原始证据）

- `Aden Group\Global_Infrastructure - Documents\backup\006_Standard\AGI-Group Standard-Front End Naming Convention v0.3.docx` ← **第一层原始依据**
- `Aden Group\Global_Infrastructure - Documents\6_General\10_AGI Document MGMT\` ← **类型 × 域 九宫格**
- `Aden Group\Global_Infrastructure - Documents\5_Security&Compliance\07. ISO27001 project\00.ISO27001-2013\02. Stage 1 Audit\ADEN-ISMS-FOR001 四级文件结构索引图.xls`
- `Aden Group\Global_Infrastructure - Documents\1_ServiceDelivery\` ← 项目组合五条编号线
- `Aden Group\Global_Infrastructure - Documents\0_Achitect\99_old_doc\20. MA Information\` ← 位置码 + `not connected` 状态后缀
- `Aden Group\Enterprise_Solutions - Documents\D365_ERP\` ← `ADEN-ERP-<Title> (FDD)-V1.0 - Item N` 记录式命名
- `OneDrive - Aden Group\00. Working\Y2026\Project_WEBTOOL_CRM_F&O_Project\00.todevelopnewwebtoolinternally\Aden_Webtool_FDD_SatelliteSystem-D365FnO-MiddlewareObservability_Ch0-13_v1.8_Final.docx` ← **内容内标识编码**实证（§2.10：INT / OP / A / FR / 类别码 / 章节号 / 单据号）
- `docs/10-abbreviation-and-numbering-standards.md` ← 第一/二/三层的国际依据
- `docs/00-glossary.md` ← 本项目第三层登记表 + 缩写登记处（§5.6 的登记处）
