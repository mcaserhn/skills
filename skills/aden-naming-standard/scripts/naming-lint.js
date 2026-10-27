#!/usr/bin/env node
/**
 * naming-lint.js — 命名与标识合规校验（docs/12 的机器化落地）
 *
 * 用法：node naming-lint.js [--root <工作区>] [--out <file>] [--csv <file>]
 *                           [--since YYYY-MM-DD] [--all]
 * 退出码：0 = 无 ERROR；1 = 有 ERROR
 *
 * 装载层适配（2026-10-19 剥离入技能时唯一改动）：
 *   原文件位于工作区 `tools/` 下，ROOT 取 `__dirname/..`。移入技能后该相对路径会指向
 *   技能自身，故新增 `--root`，未指定时取**当前目录**。条款、正则、判定口径、豁免判据
 *   一字未改 —— 如需对照，`--root <StreamLens> --since 2026-10-12` 即还原原行为。
 *
 * 依据：docs/12-aden-naming-and-identifier-standard.md
 *   §1.3 存量豁免 / §1.4 系统异常产物 / §4.3 通用字符纪律 / §5.2 分隔符 / §5.4 版本号
 *   §5.5 日期 / §5.6 状态后缀 / §5.7 语言段 / §7.1 内容层标识式 / §8.1 缩写纪律
 *   §10.2 审计方式（扫新建资产，输出「路径 / 违反条款 / 建议形式」）
 *
 * 设计约束（与 ctx-lint.js 一致）：Node 零依赖；stdout 不回显时用 --out 落盘。
 *
 * 判定口径（关键，勿改）：
 *   - **存量豁免**：mtime 早于生效日（默认 2026-10-12）的对象标 [豁免]，只备案不判违规。
 *     理由 = §1.3：存量承载跨系统引用与审计留痕，批量整改的断链风险大于命名混乱本身。
 *   - **内容层标识与缩写代号不受豁免**：§8.1 R-AB-2 明确「未登记即使用 = 缺陷，审计应报出」。
 *   - **平台强制的命名不在管辖内**：`.workbuddy/memory/YYYY-MM-DD.md` 由 WorkBuddy 框架写入，
 *     不按本研究结论评判（研究只约束我们自己的产物）；`app/public/globals.css` 属资料库标准层，
 *     原样引用、禁改，其文件名不参与评判。
 */
'use strict';

const fs = require('fs');
const path = require('path');

const argv = process.argv.slice(2);
const arg = (name, dflt) => {
  const i = argv.indexOf(name);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : dflt;
};
// 目标工作区根：显式 --root 优先，否则取当前目录（见文件头「装载层适配」）
const ROOT = path.resolve(arg('--root', process.cwd()));
const OUT = arg('--out', null);
const CSV = arg('--csv', null);
// 生效日 = docs/12 制定日；早于此日期的对象按 §1.3 豁免
// 注意：必须按**本地日期**判定与显示。曾用 toISOString() 显示，
// 在东八区下 2026-10-12T00:00 被折算成 UTC 的 10-11，输出比实际早一天（负向测试实测）。
const EFFECTIVE = new Date((arg('--since', '2026-10-12') + 'T00:00:00'));
const localDate = (d) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const SHOW_ALL = argv.includes('--all');

/** 平台强制 / 标准层禁改 —— 不参与评判 */
const EXCLUDE = [
  /^node_modules\//,
  /^\.git\//,
  /^\.workbuddy\/memory\//, // WorkBuddy 框架按日写日志，文件名由平台决定
  /^app\/public\/globals\.css$/, // 资料库标准 UI 层，原样引用禁改
];

/**
 * §1.2-6 代码与脚手架：本规范**只约束目录归属，不约束文件名**。
 * 源码/脚本/配置沿用各自生态的命名约定（`package.json` / `index.html` / `ctx-lint.js`），
 * 强行套用文档命名式既表达不出、也无人遵守 —— 故整体跳过其文件名与内部标识的判定。
 * 负向测试（2026-10-12 裁决 6 落地）：不排除时，`.tmp/` `tools/` 会贡献 24 处假阳性。
 */
const CODE_SCOPE = [/^app\//, /^tools\//, /^config\//, /^\.tmp\//];
const inCodeScope = (rel) => CODE_SCOPE.some((re) => re.test(rel));

/**
 * §1.2-7 项目本地文档目录：`docs/` `context/` 与根级 `README.md` / `AGENTS.md` 沿用**项目自身**
 * 编号约定（`NN-名称.md`），不适用 §5.1 的 ADEN 载体层命名式 —— 故 §5 各条对其**均不适用**。
 * 负向测试：不排除时会把 `docs/08-webapp-prototype-design.md` 的**主体词** `prototype`
 * 误判为 §5.6 状态后缀（假阳性 —— 判状态看**段位置**，不看词本身）。
 * **仍适用**：§4.3-3（禁空格 / 全角）等**通用字符纪律**，故只豁免 §5 专属规则。
 */
const DOC_SCOPE = [/^docs\//, /^context\//, /^README\.md$/, /^AGENTS\.md$/];
const inDocScope = (rel) => DOC_SCOPE.some((re) => re.test(rel));

const findings = []; // {path, clause, rule, suggest, exempt, level}
const evidenceQuotes = []; // §7.2-8 证据引用（既有文档实际编码）—— 放行备案，不判违规
const add = (level, o) => findings.push(Object.assign({ level }, o));

// ---------- 载体层：逐条形式校验 ----------
// 每条 = {rule, clause, hit(name) → 违规片段|null, suggest(frag) → 建议写法}
const RULES = [
  {
    rule: '下划线分隔',
    scope: '§5',
    clause: '§5.2 · §5.10-4',
    hit: (n) => (/^_/.test(n) ? n.match(/^_+/)[0] : null) || (n.includes('_') ? '_' : null),
    // 前导下划线是"排序置顶"习惯，改连字符会得到裸 `-名`；正解是去掉前缀
    suggest: (f, n) => (f.startsWith('_') ? n.replace(/^_+/, '') + '（去掉前导下划线）' : n.replace(/_/g, '-')),
    why: '新产物不应引入下划线（段间用连字符、段内用大小写）',
  },
  {
    rule: '空格 / 全角',
    clause: '§4.3-3 · §5.2',
    hit: (n) => (/[ \u3000]/.test(n) ? '空格' : /[\uFF01-\uFF5E]/.test(n) ? '全角' : null),
    suggest: (f, n) => n.replace(/[ \u3000]/g, '-').replace(/[\uFF01-\uFF5E]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xfee0)),
    why: '不应使用空格与全角符号',
  },
  {
    rule: '版本号写法',
    scope: '§5',
    clause: '§5.4 · 附录 A.6',
    // 受控形式只有 -vX.Y（小写 v、连字符连接、≥2 段）
    hit: (n) => {
      const m = n.match(/([-_. ]?)([vV])(\d+(?:\.\d+)*)/);
      if (!m) return null;
      const [full, sep, letter, digits] = m;
      if (sep === '-' && letter === 'v' && digits.includes('.')) return null; // 合规
      return full;
    },
    suggest: (f, n) => n.replace(/([-_. ]?)[vV](\d+(?:\.\d+)*)/, (s, sep, d) => `-v${d.includes('.') ? d : d + '.0'}`),
    why: '受控形式 = -vX.Y（小写 v、连字符、至少两段）',
  },
  {
    rule: '日期形式',
    scope: '§5',
    clause: '§5.5 · 附录 A.7',
    // 受控形式（v1.3 起）：文件名日期段 = YYYYMMDD；**期间标识段 = YYYY-MM**（仅用于期间）；
    // 季度 = YYYYQn。故仅两式判违规：完整 ISO 日期（YYYY-MM-DD，文件名应用基本式）与 YYYY-qN（季度须大写 Q）。
    // 变更记录：v1.2 曾把 `YYYY-MM` 判违规，因当时 §5.5 未收 `YYYY-MM`、且与附录 C 自相矛盾；
    // 2026-10-12 裁决「改正文」（§5.5 增期间标识段）后，`YYYY-MM` 转为合规，故移除该判定。
    hit: (n) => {
      if (/\b20\d{2}Q[1-4]\b/.test(n) && !/\b20\d{2}-[qQ]\d/.test(n)) return null;
      const q = n.match(/20\d{2}-[qQ]\d/);
      if (q) return q[0];
      const iso = n.match(/20\d{2}-\d{2}-\d{2}/);
      if (iso) return iso[0];
      return null;
    },
    suggest: (f, n) =>
      n
        .replace(/(20\d{2})-(\d{2})-(\d{2})/g, '$1$2$3') // 文件名日期段 → 基本式
        .replace(/20(\d{2})-([qQ])(\d)/g, '20$1Q$3'), // 季度 → 大写 Q
    why: '文件名日期段用 YYYYMMDD；期间标识段可用 YYYY-MM；季度用 YYYYQn（大写 Q）',
  },
  {
    rule: '状态 / 修订散词',
    scope: '§5',
    clause: '§5.6 · §5.10-1',
    // §5.6 定义的是**后缀**（命名式 `…-版本-状态-语言.ext`），故必须是 `-` / `_` 引导的段。
    // 负向测试实测：不加前导符约束会把容器名 `output/archive/` 误判为状态词（假阳性）——
    // 目录名 `archive` 不是"状态后缀"，而 `context/03a-contracts.md` §3 恰恰要求快照进这个目录。
    hit: (n) => {
      const m = n.match(/[-_](final|sample|prototype|previous|archive|archived|bkup|old|copy|updated|upd|ongoing|done|pre|post|draft\d|r\d+)(?=$|[-_.])/i);
      if (!m) return null;
      if (/^-(Draft|Review|Approved|Signed|Retired)$/.test(m[0])) return null;
      return m[0];
    },
    suggest: () => '改用受控 5 值：-Draft / -Review / -Approved / -Signed / -Retired',
    why: '状态受控 5 值；不应另造状态词或修订标记',
  },
  {
    rule: '语言段写法',
    scope: '§5',
    clause: '§5.7 · 附录 A.5',
    hit: (n) => {
      const m = n.match(/[-_](cn|ENG?|CN|EN|zh|中文)(?=[-_.]|$)/);
      if (!m) return null;
      const v = m[1];
      if (v === 'zh' || v === 'en') return null;
      return m[0];
    },
    suggest: () => '受控 2 值：-zh / -en（小写）',
    why: '不应使用 -cn / -中文 / CN / EN / _EN / _ENG',
  },
];

/** 系统异常产物（§1.4）：非违规，列清理候选，须人工比对后方可删除 */
const SYS_ARTIFACT = /-CCNLT[A-Z]{3}-[A-Z]+/;

function walk(dir, rel = '') {
  const out = [];
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const e of entries) {
    const r = rel ? `${rel}/${e.name}` : e.name;
    if (EXCLUDE.some((re) => re.test(r))) continue;
    // 排除规则只针对内容；目录本身仍要判断（如 .workbuddy/memory 已排除整棵）
    out.push({ rel: r, name: e.name, isDir: e.isDirectory(), full: path.join(dir, e.name) });
    if (e.isDirectory()) out.push(...walk(path.join(dir, e.name), r));
  }
  return out;
}

const all = walk(ROOT);

for (const ent of all) {
  const st = (() => {
    try {
      return fs.statSync(ent.full);
    } catch {
      return null;
    }
  })();
  if (!st) continue;
  if (inCodeScope(ent.rel)) continue; // §1.2-6：代码与脚手架不适用载体层命名式
  const exempt = st.mtime < EFFECTIVE;

  if (SYS_ARTIFACT.test(ent.name)) {
    add('WARN', {
      path: ent.rel,
      clause: '§1.4',
      rule: '系统异常产物',
      suggest: '列为清理候选；删除前须人工比对确认',
      exempt: false,
    });
    continue;
  }

  for (const r of RULES) {
    // §1.2-7：`docs/` `context/` 与 README/AGENTS 不适用 §5 专属规则；§4.3-3 通用字符纪律仍适用
    if (inDocScope(ent.rel) && r.scope === '§5') continue;
    const frag = r.hit(ent.name);
    if (frag === null || frag === undefined) continue;
    add(exempt ? 'INFO' : 'ERROR', {
      path: ent.rel + (ent.isDir ? '/' : ''),
      clause: r.clause,
      rule: r.rule,
      frag,
      suggest: typeof r.suggest === 'function' ? r.suggest(frag, ent.name) : r.suggest,
      why: r.why,
      note: r.note || null,
      exempt,
    });
  }
}

// ---------- 内容层标识式（§7.1）：序号应 ≥2 位补零 ----------
// 只扫**本规范管辖的内部标识族**（docs/12 §7.1 类型码 + 本项目 docs/00 §2 登记族 +
// docs/11/12 自用族）。不泛扫 `[A-Z]+-\d+` —— 那会把外部技术编号（UTF-8 / WCAG-2 /
// GPT-4 / TLS-1.3）一并报出，属假阳性（负向测试实测：泛扫产生 21 处噪音，其中 12 处为外部码）。
const TEXT_EXT = /\.(md|js|json|csv|html|css|txt)$/;
/**
 * 审计产物自指例外：`output/audit/`（本报告的正文与清单）**必须引用**违规片段才能描述问题。
 * 扫描自己的输出是定义上的循环 —— 会把自己引用的 `OP-1` / `INT-1` 报成"未补零"。
 * 故内容层标识扫描跳过该目录；**文件名规则仍然适用**（`YYYYMMDD-*` 等照常评判）。
 */
const CONTENT_SCAN_EXCLUDE = [/^output\/audit\//];
/**
 * §7.2-8 证据引用的出处声明（与 docs-lint.js 同口径）：
 * 「规则陈述与引用不受前款约束」—— 反例 / 证据引用 / 外部编号三类均不构成违规。
 * 不实现这条豁免就会把 `docs/12`（规范正文）与 `docs/11`（设计底稿）自己报成违规：
 * 它们**必须引用**既有文档的实际编码（如 FDD 的 `OP-1`）才能描述缺陷 —— 与
 * output/audit/ 的自指循环同性质（负向测试实测：本项 4 处全为假阳性）。
 */
const EVIDENCE_CITE = /引用原样|实际编码|勿改|原文为准|照抄|FDD/;
/**
 * §7.2-8 证据引用 · **已人工裁决**的存量引用登记。
 * 裁决（Stanley，2026-10-13）原话：「这两个的来源都是 FDD 的实际编码，这个属于历史文档，
 * 不去修改。只要确保新命名规范里是正确的编码即可，新的文档需要严格遵循。」
 *
 * 为什么还要显式登记：`EVIDENCE_CITE` 是**行文关键词**启发式，措辞一改判定就翻转
 * （负向测试实测：同一处引用换个说法即从「放行」变回 WARN）。已裁决的少数几处在此**按文件 + 行特征
 * 显式登记**，使结论不再依赖偶发措辞。**新增登记须经人工裁决，不得由脚本自行追加。**
 */
const EVIDENCE_REGISTRY = [
  { file: /^context\/06-lessons\.md$/, marker: /FDD 实际编码/, note: 'Satellite FDD 实际编码 OP-1 / INT-OP1（§3-11）' },
  { file: /^context\/07-decisions\.md$/, marker: /实证到的 4 处不一致/, note: 'Satellite FDD 实际编码 INT-01 ∥ INT-OP1 ∥ OP-1（D-05）' },
];
// 只列**多字母**类型码（docs/12 §7.1 / 附录 A.9）。
// v1.3 §7.1 已明示：单一字母族（D / S / B / Q / M / U / T / A / F）**不属**「内容层标识码」——
// 它们是文档结构编号（章节号 / 附录号 / 条款号 / 编号线）或代号，不适用 §7.2-1 的补零要求。
// 负向测试实测：保留单字母会把 `B-1`（附录 B 事项号）、`D-1`（缺陷号）等结构编号全报成"未补零"（假阳性）。
const INTERNAL_FAMILY = [
  'BASE-M365', 'BASE', 'NFR', 'INT', 'EOD', 'FR', 'OP', 'MD',
].join('|');
// 前后都不许再接字母/数字/连字符，避免 `R-AB-1` 被拆成 `AB-1`、`BASE-2026-001` 被当 `BASE-202`
const ID_RE = new RegExp(String.raw`(?<![\w-])(${INTERNAL_FAMILY})-(\d{1,3})([a-z]?)(?![\wx-])`, 'g');
for (const ent of all) {
  if (ent.isDir || !TEXT_EXT.test(ent.name)) continue;
  if (inCodeScope(ent.rel)) continue; // §1.2-6：代码与脚手架不适用本节
  if (CONTENT_SCAN_EXCLUDE.some((re) => re.test(ent.rel))) continue; // 审计产物自指例外
  let text;
  try {
    text = fs.readFileSync(ent.full, 'utf8');
  } catch {
    continue;
  }
  if (text.length > 400000) continue; // 大文件跳过（原始抓取产物）
  const regFor = EVIDENCE_REGISTRY.filter((r) => r.file.test(ent.rel));
  const bad = new Set();
  const cited = new Set();
  for (const line of text.split('\n')) {
    // §7.2-8：证据引用（出处声明关键词 或 已裁决登记）—— 照抄既有文档实际编码，不判违规
    const isCite = EVIDENCE_CITE.test(line) || regFor.some((r) => r.marker.test(line));
    ID_RE.lastIndex = 0;
    let m;
    while ((m = ID_RE.exec(line))) {
      const [, prefix, num, variant] = m;
      if (num.length >= 2) continue;
      // ① 条款号不属于内容层标识码：`R-AB-n` 与 §7.2-6 的章节号同性质（ISO 2145，无补零要求）。
      //    负向测试实测：不排除会把规范自己的条款号全报一遍（假阳性）。
      if (prefix === 'R-AB') continue;
      // ② 登记表的占位写法（`NFR-0x` / `BASE-2026-00x`）不是实例，`0x` 表示"待填"，不判。
      if (num === '0' && variant === 'x') continue;
      (isCite ? cited : bad).add(`${prefix}-${num}${variant}`);
    }
  }
  if (cited.size) {
    const reg = regFor.find((r) => r.marker.test(text));
    evidenceQuotes.push({ path: ent.rel, ids: [...cited].join(' '), note: reg ? reg.note : '§7.2-8 出处声明' });
  }
  if (bad.size) {
    add('WARN', {
      path: ent.rel,
      clause: '§7.1 · §7.2-1',
      rule: '内容层序号未补零',
      frag: [...bad].slice(0, 8).join(' '),
      suggest: '序号补零至 2 位（如 OP-1 → OP-01）',
      exempt: false,
    });
  }
}

// ---------- 缩写纪律（§8.1 R-AB-2）：未登记代号裸用 ----------
// 登记处 = docs/00-glossary.md §2（项目级）；docs/12 §8.1 / 附录 A（ADEN 级）。
// 判定：命中「已登记白名单」以外的单字母+数字 或 短字母+数字 家族时报警。
const REGISTERED = [
  /^FR-\d+$/,
  /^NFR-\d+$/,
  /^BASE-(?:2026|M365)-\d+$/,
  /^[A-Z]{2,5}-\d{4}[A-Z]\d+-\d+$/, // 条目 id：FO-2026Q4-007 形态
];
// 口径（v1.3 起）：这些家族**多数已有定义处、只是尚未进登记表**。按 docs/12 §8.1「R-AB-2 过渡条款」，
// 登记表（附录 B-5）建成前，**首次出现处给出全称即视为满足 R-AB-2**；故本项报出的语义是
// 「**待登记（过渡期）**」而非「即席自造违规」——两者不可混为一谈（自造代号由 R-AB-6 另管）。
const KNOWN_UNREGISTERED = [
  { re: /\bD-0\d\b|\bD-1\d\b/, note: 'D-01…D-12 = 决策编号（context/07-decisions.md；缺陷族已于 2026-10-12 迁出为 `缺陷-n`）' },
  { re: /\bD1\b|\bD2\b|\bD3\b/, note: 'D1/D2/D3 = 分发三式（docs/00 §3 已列为已知冲突）' },
  { re: /\bS[1-5]\b/, note: 'S1…S5 = 项目组合五条编号线（docs/12 §6.2）' },
  { re: /\bB-[1-8]\b/, note: 'B-1…B-8 = 待补事项（docs/12 附录 B）' },
  { re: /\bR-AB-[1-6]\b/, note: 'R-AB-1…6 = 缩写纪律条款号（docs/12 §8.1，有定义表）' },
  { re: /\bM[1-5]\b/, note: 'M1…M5 = 元规律（docs/11）' },
  { re: /\bU[1-3]\b/, note: 'U1…U3 = 升级建议（docs/10 / docs/00 §6）' },
  { re: /\bT[1-3]\b/, note: 'T1/T2/T3 = 载体候选（docs/09 §2）' },
  { re: /\bQ[1-6]\b/, note: 'Q1…Q6 = 命名规范待裁决（docs/11）' },
  { re: /\bW\b\s*\/\s*A\b\s*\/\s*P\b\s*\/\s*L\b/, note: 'W/A/P/L = 托管四选（docs/00 §4 已列为反例）' },
];
const abbr = [];
for (const ent of all) {
  if (ent.isDir || !/\.(md)$/.test(ent.name)) continue;
  if (inCodeScope(ent.rel)) continue; // §1.2-6
  if (!/^(docs|context|README|AGENTS)/.test(ent.rel)) continue;
  let text;
  try {
    text = fs.readFileSync(ent.full, 'utf8');
  } catch {
    continue;
  }
  const hitFams = new Set();
  for (const k of KNOWN_UNREGISTERED) {
    if (k.re.test(text)) hitFams.add(k.note);
  }
  if (hitFams.size) abbr.push({ path: ent.rel, fams: [...hitFams] });
}
// 交叉核对：这些家族是否在 docs/00 §2 登记表出现
const glossary = (() => {
  try {
    return fs.readFileSync(path.join(ROOT, 'docs/00-glossary.md'), 'utf8');
  } catch {
    return '';
  }
})();
const pending = []; // 待登记代号（§8.1 R-AB-2 过渡条款）—— 非缺陷，单列
for (const a of abbr) {
  const registered = REGISTERED.some((re) => re.test(a.path));
  if (registered) continue;
  pending.push({ path: a.path, fams: a.fams });
}

// ---------- 文件名中的未登记缩写（§5.10-3 · §8.1 R-AB-2）----------
// §5.10-3「不应把内部枚举代号写进文件名」。只收录**已确认是自造、且登记处无定义**的缩写：
//   wn = what's new（whatsnew）、rn = release notes。
// 不收录外部通用词（api / js / json / html / css / md）与已登记取值（fo / pp / m365 / d365）——
// 后者若一并报出，属把技术词误判为治理缺陷（负向测试实测会引入大量假阳性）。
const UNREG_FILENAME_ABBR = new Set(['wn', 'rn']);
const SEG_SPLIT = /[-_.]+/;
for (const ent of all) {
  if (ent.isDir) continue;
  if (inCodeScope(ent.rel)) continue; // §1.2-6
  const segs = ent.name.split(SEG_SPLIT);
  const hit = segs.filter((s) => UNREG_FILENAME_ABBR.has(s.toLowerCase()));
  if (!hit.length) continue;
  const uniq = [...new Set(hit.map((s) => s.toLowerCase()))];
  add('WARN', {
    path: ent.rel,
    clause: '§5.10-3 · §8.1 R-AB-2',
    rule: '文件名含未登记缩写',
    frag: uniq.join(' '),
    suggest: `改用全称（${uniq.map((s) => (s === 'wn' ? "What's New" : 'Release Notes')).join(' / ')}）；或先登记进登记处`,
    exempt: false,
  });
}

// ---------- 汇总输出 ----------
const errs = findings.filter((f) => f.level === 'ERROR');
const warns = findings.filter((f) => f.level === 'WARN');
const infos = findings.filter((f) => f.level === 'INFO');

const byRule = new Map();
for (const f of findings) {
  const k = `${f.level === 'INFO' ? '[豁免]' : ''}${f.rule}`;
  byRule.set(k, (byRule.get(k) || 0) + 1);
}

let out = '';
out += '=== StreamLens 命名与标识合规校验 (naming-lint) ===\n';
out += `依据: docs/12-aden-naming-and-identifier-standard.md\n`;
out += `ROOT: ${ROOT}\n`;
out += `生效日: ${localDate(EFFECTIVE)}（早于此日期的对象按 §1.3 存量豁免，标 [豁免]）\n`;
out += `扫描对象: ${all.length} 项（已排除 ${EXCLUDE.length} 类平台强制/标准层路径）\n\n`;

out += '--- 规则命中统计 ---\n';
for (const [k, v] of [...byRule.entries()].sort((a, b) => b[1] - a[1])) {
  out += `  ${String(v).padStart(4)}  ${k}\n`;
}

out += '\n--- 须整改（新产物，§1.3 不豁免）---\n';
if (!errs.length) out += '  (无)\n';
else {
  const limit = SHOW_ALL ? errs.length : 40;
  const noted = new Set(); // 同一条款的冲突说明只印一次
  errs.slice(0, limit).forEach((f) => {
    out += `  [ERROR] ${f.path}\n`;
    out += `          违反 ${f.clause}（${f.rule}）：${f.frag}\n`;
    out += `          建议 → ${f.suggest}\n`;
    if (f.note && !noted.has(f.clause)) {
      noted.add(f.clause);
      out += `          ${f.note}\n`;
    }
  });
  if (errs.length > limit) out += `  … 另有 ${errs.length - limit} 处（--all 全量 / --csv 导出）\n`;
}

out += '\n--- 缩写纪律与内容层标识（不受存量豁免）---\n';
const nonExemptWarns = warns;
if (!nonExemptWarns.length) out += '  (无)\n';
else {
  nonExemptWarns.forEach((f) => {
    out += `  [WARN] ${f.path}\n`;
    out += `         违反 ${f.clause}（${f.rule}）：${f.frag}\n`;
    out += `         建议 → ${f.suggest}\n`;
    if (f.detail) f.detail.forEach((d) => (out += `         · ${d}\n`));
  });
}

out += '\n--- 待登记代号（§8.1 R-AB-2 过渡条款；非缺陷，B-5 建成后回填）---\n';
if (!pending.length) out += '  (无)\n';
else {
  pending.forEach((p) => {
    out += `  [待登记] ${p.path}\n`;
    p.fams.forEach((d) => (out += `         · ${d}\n`));
  });
}

out += '\n--- 证据引用·放行（§7.2-8；已裁决存量，不判违规）---\n';
if (!evidenceQuotes.length) out += '  (无)\n';
else {
  evidenceQuotes.forEach((q) => {
    out += `  [放行] ${q.path}\n`;
    out += `         引用既有文档实际编码：${q.ids}  —— 历史文档，不修改（${q.note}）\n`;
  });
}

out += '\n--- 存量备案（§1.3 豁免，不判违规，仅供参考）---\n';
if (!infos.length) out += '  (无)\n';
else {
  const limit = SHOW_ALL ? infos.length : 25;
  infos.slice(0, limit).forEach((f) => {
    out += `  [豁免] ${f.path}  ← ${f.clause}（${f.rule}）\n`;
  });
  if (infos.length > limit) out += `  … 另有 ${infos.length - limit} 处（--all 全量 / --csv 导出）\n`;
}

out += `\n合计: ${errs.length} ERROR / ${warns.length} WARN / ${pending.length} 待登记 / ${infos.length} INFO（存量豁免）\n`;
out += errs.length
  ? '结论: FAIL —— 新产物存在不合规命名，须整改。\n'
  : warns.length
    ? '结论: PASS（有 WARN：形式问题，须核实整改）\n'
    : pending.length
      ? '结论: PASS —— 形式可校验项全部合规；仅余登记表待建（附录 B-5）的待登记代号。\n'
      : '结论: PASS —— 命名的形式可校验项全部合规。\n';

process.stdout.write(out);
if (OUT) {
  fs.writeFileSync(OUT, out, 'utf8');
  process.stdout.write(`(已写入 ${OUT})\n`);
}
if (CSV) {
  const esc = (s) => `"${String(s == null ? '' : s).replace(/"/g, '""')}"`;
  const rows = [['level', 'path', 'clause', 'rule', 'fragment', 'suggest', 'exempt'].join(',')];
  for (const f of findings) {
    rows.push([f.level, f.path, f.clause, f.rule, f.frag, typeof f.suggest === 'string' ? f.suggest : (f.suggest || ''), f.exempt ? '存量豁免' : '新产物'].map(esc).join(','));
  }
  fs.writeFileSync(CSV, '\ufeff' + rows.join('\n'), 'utf8');
  process.stdout.write(`(CSV 已写入 ${CSV})\n`);
}
process.exit(errs.length ? 1 : 0);
