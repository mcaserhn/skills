#!/usr/bin/env python3
"""de-ai-flavor 确定性 AI 味儿 linter（deterministic AI-flavor linter）。

只覆盖 de-ai-flavor 规则里「机械可判定」的子集：正则能认、不依赖语感。
规则编号直接对应本 skill 的 references/，不引用任何外部检测器的私有编号：

  02-*  词汇层禁词表           references/02-banned-words-and-patterns.md
  05-*  中文篇章 / 句法层       references/05-zh-syntax-and-structure.md
  07-*  英文篇章 / 句法层       references/07-en-syntax-and-structure.md
  09-*  格式与残留标记         references/09-format-and-artifacts.md

反向保护清单（references/06-do-not-change.md 中文 / references/08-en-do-not-change.md
英文）一律列为 PROTECTED，本脚本永不判为命中。这是与通用 AI 检测器最大的差别：
被动语态、hedge、问句、比喻、单组三项、词汇多样性等在本 skill 里是**人类特征**，
报出来只会诱导「越改越不像人」。用 --show-protected 可以列出这份排除清单。

设计铁律
  * 不提供任何自动改写 / 同义词替换功能。references/02 明令禁止机械换词——
    本脚本只报位置 + 规则编号 + 原文片段，改与不改由人判断。
  * 判据是「触发标记 + 密度」，不是「出现即命中」。预算类检查按阈值触发，
    预算内出现一律不报。
  * 不读网络、不写文件、无第三方依赖，仅 Python 标准库。

用法
  python3 scripts/ai_pattern_lint.py FILE [FILE ...]
  cat draft.md | python3 scripts/ai_pattern_lint.py
  python3 scripts/ai_pattern_lint.py --lang zh --json --threshold 8 draft.md
  python3 scripts/ai_pattern_lint.py --list-rules
  python3 scripts/ai_pattern_lint.py --show-protected

密度口径
  units = 英文词数 + 中日韩字符数（中文按字计，不折词）
  density = 命中数 / units * 1000
  中英混排时这个数字只在同语言、同体裁之间比，不要跨语言比。

退出码
  0 = 通过
  1 = 密度超阈值，或命中 09-A 零假阳性残留标记
  2 = 使用错误（如文件不存在）

Python 3.8+，仅标准库。
"""

import argparse
import json
import re
import sys

# --------------------------------------------------------------------------
# 预算与阈值
# --------------------------------------------------------------------------

DEFAULT_THRESHOLD = 5.0      # 命中数 / 1000 units
ZH_DASH_BUDGET_CHARS = 300   # 中文：每 N 字允许 1 个「——」（05 第 4 条）
CONNECTIVE_BUDGET = 2        # 句首连接词全文允许次数（02 密度判据 / 05 第 10.4 条）
BOLD_BUDGET_PER_1000 = 12    # 行内粗体：每 1000 units 允许的个数（09-B2）
HR_BUDGET = 2                # 全文允许的 `---` 分隔线数量（09-B7）
ZH_ENUM_ORDINAL_MIN = 3      # 「一、二、三」小标题连续多少个才算命中（05 第 6 条）
TRICOLON_BUDGET = 3          # 英文三连 A, B, and C 全文允许次数（07 第 10 条）
THAT_REL_BUDGET = 2          # 英文 that 关系从句允许次数（07 第 3 条）

# --------------------------------------------------------------------------
# 规则登记表：id -> (所属层, 中文名, 来源文件, 默认严重度)
# 严重度只用于报告排序与提示语气，不改变「命中即计入密度」这一事实。
# --------------------------------------------------------------------------

RULES = {
    # ---- 02 词汇层 ----
    "02-zh-cliche":      ("02 词汇层", "中文套话开场 / 收尾", "02-banned-words-and-patterns.md", "strong"),
    "02-zh-certainty":   ("02 词汇层", "中文确定语气空转词", "02-banned-words-and-patterns.md", "strong"),
    "02-zh-abstract":    ("02 词汇层", "中文抽象大词", "02-banned-words-and-patterns.md", "weak"),
    "02-zh-assistant":   ("02 词汇层", "中文助手腔客套", "02-banned-words-and-patterns.md", "strong"),
    "02-en-buzzword":    ("02 词汇层", "英文 buzzword", "02-banned-words-and-patterns.md", "moderate"),
    "02-en-cliche":      ("02 词汇层", "英文套话开场 / 收尾", "02-banned-words-and-patterns.md", "strong"),
    "02-en-certainty":   ("02 词汇层", "英文以确定语气说空话", "02-banned-words-and-patterns.md", "strong"),
    "02-en-assistant":   ("02 词汇层", "英文助手腔客套", "02-banned-words-and-patterns.md", "strong"),
    "02-en-connective":  ("02 词汇层", "英文句首连接词堆积", "02-banned-words-and-patterns.md", "moderate"),
    # ---- 05 中文篇章 / 句法层 ----
    "05-1":              ("05 中文篇章层", "翻案腔（不是 A 而是 B）", "05-zh-syntax-and-structure.md", "strong"),
    "05-2":              ("05 中文篇章层", "顿号并列过密", "05-zh-syntax-and-structure.md", "notice"),
    "05-4":              ("05 中文篇章层", "破折号滥用", "05-zh-syntax-and-structure.md", "moderate"),
    "05-5a":             ("05 中文篇章层", "冒号：提示语引出", "05-zh-syntax-and-structure.md", "moderate"),
    "05-5b":             ("05 中文篇章层", "冒号：空转句引列表", "05-zh-syntax-and-structure.md", "moderate"),
    "05-6":              ("05 中文篇章层", "序数词当小标题", "05-zh-syntax-and-structure.md", "moderate"),
    "05-7":              ("05 中文篇章层", "拟人化喻体", "05-zh-syntax-and-structure.md", "moderate"),
    "05-8":              ("05 中文篇章层", "概括词盖掉已有具体值", "05-zh-syntax-and-structure.md", "moderate"),
    "05-9":              ("05 中文篇章层", "禁用起手式", "05-zh-syntax-and-structure.md", "moderate"),
    "05-10.2":           ("05 中文篇章层", "「当……时」前置时间从句", "05-zh-syntax-and-structure.md", "weak"),
    "05-10.3":           ("05 中文篇章层", "前置话题壳", "05-zh-syntax-and-structure.md", "weak"),
    "05-10.4":           ("05 中文篇章层", "句首连接词当路标", "05-zh-syntax-and-structure.md", "weak"),
    "05-10.5":           ("05 中文篇章层", "「这意味着」式复述句", "05-zh-syntax-and-structure.md", "moderate"),
    "05-11":             ("05 中文篇章层", "段首零回指评论", "05-zh-syntax-and-structure.md", "moderate"),
    # ---- 07 英文篇章 / 句法层 ----
    "07-1":              ("07 英文句法层", "现在分词状语从句", "07-en-syntax-and-structure.md", "strong"),
    "07-2":              ("07 英文句法层", "名词化堆叠", "07-en-syntax-and-structure.md", "moderate"),
    "07-3":              ("07 英文句法层", "that 关系从句密度", "07-en-syntax-and-structure.md", "moderate"),
    "07-5":              ("07 英文句法层", "回避系词", "07-en-syntax-and-structure.md", "moderate"),
    "07-6":              ("07 英文句法层", "空转意义强调", "07-en-syntax-and-structure.md", "strong"),
    "07-7":              ("07 英文句法层", "否定平行", "07-en-syntax-and-structure.md", "moderate"),
    "07-8":              ("07 英文句法层", "提纲式结尾", "07-en-syntax-and-structure.md", "moderate"),
    "07-9":              ("07 英文句法层", "模糊归属（只标不改）", "07-en-syntax-and-structure.md", "notice"),
    "07-10":             ("07 英文句法层", "三段式密度", "07-en-syntax-and-structure.md", "moderate"),
    # ---- 09 格式与残留标记 ----
    "09-A":              ("09 格式层", "机器残留标记（零假阳性）", "09-format-and-artifacts.md", "strong"),
    "09-B1":             ("09 格式层", "行内粗体小标题列表", "09-format-and-artifacts.md", "moderate"),
    "09-B2":             ("09 格式层", "粗体滥用", "09-format-and-artifacts.md", "weak"),
    "09-B3":             ("09 格式层", "标题式大写（英文）", "09-format-and-artifacts.md", "weak"),
    "09-B5":             ("09 格式层", "只含子标题的空标题", "09-format-and-artifacts.md", "weak"),
    "09-B6":             ("09 格式层", "跳过标题层级 / 多个一级标题", "09-format-and-artifacts.md", "weak"),
    "09-B7":             ("09 格式层", "段落间分隔线过密", "09-format-and-artifacts.md", "weak"),
    "09-B8":             ("09 格式层", "emoji 当格式符", "09-format-and-artifacts.md", "weak"),
    "09-B10":            ("09 格式层", "弯直引号混用（弱信号）", "09-format-and-artifacts.md", "weak"),
}

# 反向保护清单：永不判为命中。列出只为可解释、可为 --show-protected 输出。
PROTECTED = [
    ("06-1", "句长、段长不够参差（中文）", "06-do-not-change.md", "R≈0.87/0.94，与人类无差别"),
    ("06-2", "单字虚词偏少（中文）", "06-do-not-change.md", "方向是补不是删"),
    ("06-3", "反复写全称、少用代词（中文）", "06-do-not-change.md", "人类比 AI 更常重复名词"),
    ("06-4", "被动句（中文）", "06-do-not-change.md", "正常汉语书写"),
    ("06-5", "名词化、长句本身（中文）", "06-do-not-change.md", "现代汉语书面语常态"),
    ("06-6", "正文里的「首先……其次」（中文）", "06-do-not-change.md", "与人类无差别"),
    ("06-7", "句内同构排比（中文）", "06-do-not-change.md", "人类用得不比 AI 少"),
    ("06-8", "问句 / 设问 / 问句小标题（中文）", "06-do-not-change.md", "人类远多于 AI（17 倍）"),
    ("06-9", "比喻本身、比喻独立成段（中文）", "06-do-not-change.md", "人类多用 2.4 倍 / 8 倍"),
    ("06-10", "抽象名词配具体动词（中文）", "06-do-not-change.md", "两边都几乎不写"),
    ("08-1", "简单的 is / has 短语（英文）", "08-en-do-not-change.md", "人类更常用"),
    ("08-2", "普通动词而非「高级」同义词（英文）", "08-en-do-not-change.md", "改 used→utilized 是制造 AI 味"),
    ("08-3", "最高级与确定性陈述（英文）", "08-en-do-not-change.md", "人类更常用"),
    ("08-4", "Hedging qualifiers 与 intensifiers（英文）", "08-en-do-not-change.md", "6 个模型上均 <1"),
    ("08-5", "孤立的冗词结构（英文）", "08-en-do-not-change.md", "as a result of / in order to"),
    ("08-6", "无施事被动语态（英文）", "08-en-do-not-change.md", "AI ≈0.5×，人类多用 2 倍"),
    ("08-7", "脏话与粗俗语（英文）", "08-en-do-not-change.md", "AI 低 100 倍以上"),
    ("08-8", "词汇多样性 / elegant variation（英文）", "08-en-do-not-change.md", "维基列为非 AI 信号"),
    ("08-9", "语感类的「像 AI」印象（英文）", "08-en-do-not-change.md", "完美语法 / bland / fancy 均无效"),
    ("08-10", "孤立出现的转折词（英文）", "08-en-do-not-change.md", "判据是密度不是出现"),
    ("08-11", "无来源陈述（英文）", "08-en-do-not-change.md", "走 01 第 6 条，不属去味"),
    ("08-12", "弯引号本身（英文）", "08-en-do-not-change.md", "只在同文档混用时才算弱信号"),
]

# --------------------------------------------------------------------------
# 词表
# --------------------------------------------------------------------------

ZH_CLICHE = [
    r"在当今[^，。；\n]{0,12}(?:时代|社会|环境|世界)",
    r"在[^，。；\n]{0,14}背景下",
    r"随着[^，。；\n]{0,18}的发展",
    r"众所周知", r"不容忽视", r"值得一提", r"总而言之", r"总的来说",
    r"综上所述", r"归根结底",
]

ZH_CERTAINTY = [r"毋庸置疑", r"不可否认", r"不言而喻", r"毫无疑问", r"无须赘言"]

ZH_ABSTRACT = [
    r"赋能", r"打造", r"闭环", r"抓手", r"打通", r"全生命周期", r"一站式",
    r"生态化?布局", r"沉淀", r"裂变", r"组合拳", r"保驾护航", r"颗粒度",
    r"可视化呈现", r"全方位", r"立体化",
]

ZH_ASSISTANT = [
    r"很高兴为您提供帮助", r"作为\s*AI\b", r"作为一个人工智能",
    r"如果您还有其他问题", r"随时告诉我", r"请问还有什么可以帮您",
    r"希望这个回答对您有帮助", r"希望对您有所帮助",
]

ZH_BANNED_OPENER = [r"说白了", r"说穿了", r"先说结论"]

ZH_COMMENT_OPENER = [
    r"听起来", r"看起来", r"说白了", r"值得注意的是", r"更重要的是",
    r"关键在于", r"问题在于", r"意味着", r"不难看出",
]

ZH_ANAPHORA = [r"这", r"那", r"其", r"此", r"上面", r"上述", r"上面提到"]

# 翻案腔：顿号 / 逗号都允许出现在中间，但不得跨句（遇 。！？；\n 即边界）。
ZH_NEGATION_FLIP = [
    r"不是[^。；！？\n]{0,30}?而是", r"并非[^。；！？\n]{0,30}?而是",
    r"不在于[^。；！？\n]{0,30}?而在于", r"与其说[^。；！？\n]{0,30}?不如说",
    r"表面[^。；！？\n]{0,30}?实际", r"看似[^。；！？\n]{0,30}?实则",
    r"你以为[^。；！？\n]{0,30}?其实", r"回头才发现", r"说到底",
    r"答案恰恰相反", r"不只是[^。；！？\n]{0,26}?更是",
]

# 05-8 的配套判据：同一行或相邻行必须已有具体值（阿拉伯数字或中文数字+量词）。
HAS_CONCRETE_RE = re.compile(
    r"\d|[零一二三四五六七八九十百千万]{1,4}(?:小时|分钟|天|年|月|日|周|倍|成|个|项|条|次|家|人|万|亿)")


def split_sentences_zh(text):
    return [s for s in re.split(r"[。！？；\n]", text) if s.strip()]

ZH_COLON_HINT = [
    r"一句话总结", r"核心是", r"关键在于", r"原因如下", r"结论是",
    r"本质上", r"换句话说", r"简单说",
]

ZH_FRONT_TOPIC = [
    r"^(?:对于|对)[^，。；：\n]{0,20}(?:来说|而言|来讲)",
    r"^就[^，。；：\n]{0,16}而言",
    r"^关于[^，。；：\n]{0,16}[，,、]",
    r"^在[^，。；：\n]{0,16}方面",
]

ZH_SENTENCE_CONNECTIVE = [r"然而", r"因此", r"此外", r"与此同时", r"换言之", r"总而言之", r"综上"]

ZH_RESTATE = [r"这意味着", r"这表明", r"这说明", r"换句话说", r"也就是说"]

ZH_ABSTRACT_SUMMARY = [r"显著提升", r"大幅增长", r"明显改善", r"效率的提升", r"大幅提升", r"显著的提升"]

ZH_PERSONA_ROLE = r"导师|秘书|助手|顾问|管家|审查员|实习生|老师傅|专家|向导|伙伴|朋友|领航员|守护者"

EN_BUZZWORDS = [
    r"leverage", r"seamless(?:ly)?", r"robust", r"delve", r"navigat(?:e|ing)",
    r"empower", r"unlock", r"game[- ]chang(?:er|ing)", r"synerg(?:y|ies)",
    r"ecosystem", r"streamlin(?:e|ing)", r"holistic", r"cutting[- ]edge",
    r"best[- ]in[- ]class", r"move the needle", r"circle back", r"deep dive",
    r"low[- ]hanging fruit", r"utiliz(?:e|ing)", r"paradigm", r"transformative",
    r"unparalleled", r"state[- ]of[- ]the[- ]art",
]

EN_CLICHE = [
    r"in today'?s fast[- ]paced world", r"in the ever[- ]evolving landscape of",
    r"it is important to note that", r"it is worth (?:noting|mentioning)",
    r"in conclusion", r"to summari[sz]e", r"at the end of the day",
    r"in this (?:post|article|section),? (?:I|we) will",
]

EN_CERTAINTY = [
    r"it goes without saying", r"needless to say", r"it is undeniable that",
    r"cannot be overstated", r"there is no doubt that", r"it is clear that",
]

EN_ASSISTANT = [
    r"I'?d be happy to help", r"great question", r"as an AI\b",
    r"as a language model", r"let me know if you have any questions",
    r"hope this helps", r"feel free to (?:ask|reach out)",
]

EN_CONNECTIVE = r"(?:^|[.!?]\s+)(Additionally|Furthermore|Moreover|Notably|Consequently|In addition),"

EN_PARTICIPLE = (
    r"(?:highlighting|underscoring|emphasi[sz]ing|reflecting|demonstrating|showcasing|"
    r"ensuring|allowing for|paving the way for|solidifying|reinforcing|cementing|"
    r"signal(?:l)?ing|marking|positioning|illustrating|facilitating|enabling|driving|"
    r"shaping|fostering|bolstering|enhancing|contributing to|symboli[sz]ing|embodying)"
)

EN_COPULA_AVOID = (
    r"\b(?:serves?|served|stands?|stood|functions?|functioned|operates?|operated|"
    r"constitutes?|constituted)\s+as\s+(?:a|an|the)\b"
)

EN_SIG_EMPHASIS = [
    r"is a testament to", r"underscores? the importance of", r"reflects? a broader",
    r"in an evolving landscape", r"marks? a key turning point",
    r"leaves? an indelible mark", r"speaks? to the",
]

EN_OUTLINE_CLOSER = [
    r"despite these challenges", r"the path forward is",
    r"^\s{0,3}#{1,6}\s*(?:conclusion|future outlook|challenges and legacy|final thoughts)\b",
]

EN_VAGUE_ATTR = [
    r"experts?\s+(?:say|agree|argue|believe|note)", r"studies?\s+(?:show|suggest|have shown|indicate)",
    r"research\s+(?:shows|suggests|indicates)", r"industry (?:reports?|publications?)",
    r"observers? have\s+\w+", r"many (?:believe|argue|say)",
    r"it is widely (?:believed|regarded|considered)",
]

# 07 第 2 条：后缀口径以 v1.5.2 核对结果为准——tion / ment / ness / ity，
# 不含 -ance（原写法已按 pseudobibeR 源码更正）。
EN_NOMINALIZATION = (
    r"\bthe\s+\w+(?:tions?|ments?|ness(?:es)?|it(?:y|ies))\s+of\b"
)

EN_NEG_PARALLEL = [
    r"\b(?:it|this|that)(?:'s| is| was)?\s*n[o']?t\s+(?:just|only|merely|simply|about)\b",
    r"\bisn'?t\s+(?:just|only|merely|about)\b",
    r"\bnot\s+only\b[^.!?\n]{0,80}\bbut\s+(?:also\s+)?",
]

# 09-A 零假阳性残留标记：命中即硬失败，不参与密度平均。
ARTIFACT_PATTERNS = [
    ("ChatGPT", r"contentReference|oaicite|oai_citation|turn\d+search\d+|attributableIndex"),
    ("Gemini", r"\[cite:\s*\d+\]|\[span_\d+\]\(start_span\)"),
    ("Grok", r"grok_card|grok_render_citation_card_json"),
    ("Perplexity", r"attached_file|ppl-ai-file-upload"),
    ("未分类", r":::writing"),
]

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F000-\U0001F02F"
    "\U00002600-\U000026FF\U0001F900-\U0001F9FF\u2b00-\u2bff\ufe0f]"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
BOLD_TERM_BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+\*\*[^*\n]{1,40}?\*\*\s*[：:]")
BOLD_RE = re.compile(r"\*\*[^*\n]+\*\*")
HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
LIST_START_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+\S")
ZH_ORDINAL_HEADING_RE = re.compile(
    r"^(?:#{1,6}\s*)?(?:\*\*)?\s*(?:[一二三四五六七八九十]+[、,，]|第[一二三四五六七八九十]+[、,，])"
)
EN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z']*")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]")
CURLY_QUOTES = "\u201c\u201d"
STRAIGHT_DOUBLE = '"'
QUOTED_SPAN_RE = re.compile(r"[\u300c\u300e\u201c\u201d][^\u300d\u300f\u201c\u201d\n]{0,300}[\u300d\u300f\u201c\u201d]")
URL_RE = re.compile(r"https?://\S+")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
# 连续 ≥5 个拉丁词视为「真英文子句」——用于中英混排判定（见 detect_lang）
EN_CLAUSE_RE = re.compile(r"(?:[A-Za-z][A-Za-z'\-]*[ \t]+){4,}[A-Za-z][A-Za-z'\-]*")

# 英文标题式大写的停用词
TITLE_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "for", "nor", "of", "to", "in", "on",
    "at", "by", "with", "from", "as", "is", "are", "was", "were", "be", "it",
}


# --------------------------------------------------------------------------
# 文本处理工具
# --------------------------------------------------------------------------

def visible_lines(raw_lines):
    """返回 [(lineno, line)]，跳过围栏代码块，去掉行内代码与 URL。"""
    out = []
    in_fence = False
    for i, line in enumerate(raw_lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        cleaned = INLINE_CODE_RE.sub(" ", line)
        cleaned = URL_RE.sub(" ", cleaned)
        out.append((i, cleaned))
    return out


def strip_quoted_spans(line):
    """去掉「」『』“” 包裹的内容——06/08 明确：对话与引语不在射程内。"""
    return QUOTED_SPAN_RE.sub(" ", line)


def count_units(text):
    """(英文词数, 中日韩字符数)。"""
    return len(EN_WORD_RE.findall(text)), len(CJK_RE.findall(text))


def detect_lang(text):
    """判定 zh / en / mixed。

    关键：不能只按「中日韩字符数 vs 拉丁词数」比——中文技术文档里满是
    Microsoft 365 / Azure DevOps 一类专名，会让比例误判为混排；反过来，
    中文文档里插一整句英文，又会被误判为纯中文而漏检。
    故先认「连续 ≥5 个拉丁词的英文子句」，认到就是混排。
    """
    en, cjk = count_units(text)
    if cjk == 0 and en == 0:
        return "zh"
    if cjk == 0:
        return "en"
    if en == 0:
        return "zh"
    if has_en_clause(text):
        return "mixed"
    ratio = cjk / (cjk + en)
    if ratio >= 0.95:
        return "zh"
    if ratio <= 0.05:
        return "en"
    return "mixed"


def has_en_clause(text):
    """是否存在连续 ≥5 个拉丁词的真英文子句。"""
    return bool(EN_CLAUSE_RE.search(text))


def is_title_case(heading_text):
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", heading_text)]
    if len(words) < 3:
        return False
    content = [w for w in words if w.lower() not in TITLE_STOPWORDS]
    if not content:
        return False
    caps = sum(1 for w in content if w[0].isupper())
    return caps / len(content) >= 0.8


# --------------------------------------------------------------------------
# 检查器
# --------------------------------------------------------------------------

class Collector:
    def __init__(self, name):
        self.name = name
        self.hits = []

    def add(self, lineno, rule, excerpt, severity=None):
        layer, rname, source, default_sev = RULES[rule]
        self.hits.append({
            "file": self.name,
            "line": lineno,
            "rule": rule,
            "name": rname,
            "layer": layer,
            "source": source,
            "severity": severity or default_sev,
            "excerpt": (excerpt or "").strip()[:100],
            "counted": default_sev != "notice",
        })


def check_zh_lines(vis, col, prose):
    """逐行中文检查。vis = [(lineno, line)]"""
    for idx, (lineno, raw) in enumerate(vis):
        line = strip_quoted_spans(raw)

        for rx in ZH_CLICHE:
            for m in re.finditer(rx, line):
                col.add(lineno, "02-zh-cliche", m.group(0))
        for rx in ZH_CERTAINTY:
            for m in re.finditer(rx, line):
                col.add(lineno, "02-zh-certainty", m.group(0))
        for rx in ZH_ABSTRACT:
            for m in re.finditer(rx, line):
                col.add(lineno, "02-zh-abstract", m.group(0))
        for rx in ZH_ASSISTANT:
            for m in re.finditer(rx, line, re.I):
                col.add(lineno, "02-zh-assistant", m.group(0))
        for rx in ZH_NEGATION_FLIP:
            for m in re.finditer(rx, line):
                col.add(lineno, "05-1", m.group(0))
        for rx in ZH_COLON_HINT:
            for m in re.finditer(rx + r"\s*[：:]", line):
                col.add(lineno, "05-5a", m.group(0))
        for rx in ZH_RESTATE:
            for m in re.finditer(r"^\s*" + rx, line):
                col.add(lineno, "05-10.5", m.group(0))
        for rx in ZH_FRONT_TOPIC:
            for m in re.finditer(rx, line):
                col.add(lineno, "05-10.3", m.group(0))
        for m in re.finditer(r"当[^，。；：\n]{2,40}?时[，,]", line):
            col.add(lineno, "05-10.2", m.group(0))
        for m in re.finditer(r"(?:像|相当于)\s*(?:一个|一位|一名)\s*[^，。！？\n]{0,4}(?:" + ZH_PERSONA_ROLE + r")", line):
            col.add(lineno, "05-7", m.group(0))

        # 05-9 禁用起手式（段首 / 句首）
        for rx in ZH_BANNED_OPENER:
            m = re.match(r"^\s*(?:[-*+]|\d+\.)?\s*" + rx, line)
            if m:
                col.add(lineno, "05-9", m.group(0))

        # 05-11 段首零回指评论（非首段，且整句无回指成分）
        if idx > 0:
            for rx in ZH_COMMENT_OPENER:
                m = re.match(r"^\s*(?:[-*+]|\d+\.)?\s*" + rx, line)
                if m:
                    sentence = re.split(r"[。！？\n]", line)[0]
                    if not any(re.search(a, sentence) for a in ZH_ANAPHORA):
                        col.add(lineno, "05-11", sentence)
                    break

        # 05-10.4 段首连接词当路标
        m = re.match(r"^\s*(" + "|".join(ZH_SENTENCE_CONNECTIVE) + r")[，,]", line)
        if m:
            col.add(lineno, "05-10.4", m.group(1))

        # 05-8 概括词盖掉已有具体值：同行或相邻行确已有数字 / 中文数字+量词才报
        window = " ".join(
            vis[k][1] for k in range(max(0, idx - 1), min(len(vis), idx + 2))
        )
        if HAS_CONCRETE_RE.search(window):
            for rx in ZH_ABSTRACT_SUMMARY:
                for m in re.finditer(rx, line):
                    col.add(lineno, "05-8", m.group(0))

        # 05-2 顿号并列过密（notices：06 第 7 条保护句内同构排比，只提示）
        segs = re.split(r"[。！？\n]", line)
        for seg in segs:
            if seg.count("、") >= 3:
                col.add(lineno, "05-2", seg.strip()[:60])

    # ---- 整篇级 ----
    joined = "\n".join(l for _, l in vis)

    # 05-4 破折号密度
    units = sum(count_units(l)[1] for _, l in vis)
    allowed = max(1, units // ZH_DASH_BUDGET_CHARS)
    dash_lines = [(ln, l) for ln, l in vis if "\u2014\u2014" in l]
    for ln, l in dash_lines[allowed:]:
        col.add(ln, "05-4", "破折号超预算（允许 %d 个 / %d 字）" % (allowed, units))

    # 05-6 序数词当小标题
    ordinal_heads = []
    for ln, l in vis:
        stripped = l.strip()
        if not stripped:
            continue
        is_heading = HEADING_RE.match(stripped) or (
            stripped.startswith("**") and stripped.endswith("**") and len(stripped) < 60
        )
        if is_heading and ZH_ORDINAL_HEADING_RE.match(stripped):
            ordinal_heads.append((ln, stripped))
    if len(ordinal_heads) >= ZH_ENUM_ORDINAL_MIN:
        for ln, text in ordinal_heads:
            col.add(ln, "05-6", text)

    # 05-5b 冒号空转句引列表：行尾冒号 + 下一非空行是列表项
    for i, (ln, l) in enumerate(vis):
        s = strip_quoted_spans(l).rstrip()
        if not s.endswith("：") and not s.endswith(":"):
            continue
        for j in range(i + 1, min(i + 4, len(vis))):
            nxt = vis[j][1].strip()
            if not nxt:
                continue
            if LIST_START_RE.match(nxt):
                body = s.rstrip("：: ").strip()
                tail = split_sentences_zh(body)[-1:] or [body]
                tail = tail[0].strip()
                if len(tail) <= 30:
                    col.add(ln, "05-5b", tail + "：")
            break


def check_en_lines(vis, col, prose):
    for lineno, raw in vis:
        line = raw
        for rx in EN_BUZZWORDS:
            for m in re.finditer(r"\b" + rx + r"\b", line, re.I):
                col.add(lineno, "02-en-buzzword", m.group(0))
        for rx in EN_CLICHE:
            for m in re.finditer(rx, line, re.I):
                col.add(lineno, "02-en-cliche", m.group(0))
        for rx in EN_CERTAINTY:
            for m in re.finditer(rx, line, re.I):
                col.add(lineno, "02-en-certainty", m.group(0))
        for rx in EN_ASSISTANT:
            for m in re.finditer(rx, line, re.I):
                col.add(lineno, "02-en-assistant", m.group(0))
        for rx in EN_NEG_PARALLEL:
            for m in re.finditer(rx, line, re.I):
                col.add(lineno, "07-7", m.group(0))
        for rx in EN_SIG_EMPHASIS:
            for m in re.finditer(rx, line, re.I):
                col.add(lineno, "07-6", m.group(0))
        for rx in EN_OUTLINE_CLOSER:
            for m in re.finditer(rx, line, re.I):
                col.add(lineno, "07-8", m.group(0))
        for rx in EN_VAGUE_ATTR:
            for m in re.finditer(rx, line, re.I):
                col.add(lineno, "07-9", m.group(0))
        for m in re.finditer(EN_COPULA_AVOID, line, re.I):
            col.add(lineno, "07-5", m.group(0))
        for m in re.finditer(EN_NOMINALIZATION, line, re.I):
            col.add(lineno, "07-2", m.group(0))
        # 07-1 现在分词状语（句尾 / 句首 / 句中，紧随标点）
        for m in re.finditer(r"(?:,\s*|\A\s*)" + EN_PARTICIPLE + r"\b", line, re.I):
            col.add(lineno, "07-1", m.group(0).strip(" ,"))

    # 整篇级
    prose_lines = [(ln, l) for ln, l in vis]

    connectives = []
    for ln, l in prose_lines:
        for m in re.finditer(EN_CONNECTIVE, l):
            connectives.append((ln, m.group(1)))
    for ln, word in connectives[CONNECTIVE_BUDGET:]:
        col.add(ln, "02-en-connective",
                "%s 句首第 %d+ 次" % (word, CONNECTIVE_BUDGET + 1))

    tricolons = []
    for ln, l in prose_lines:
        for m in re.finditer(r"\b([A-Za-z]+),\s+([A-Za-z]+),\s+and\s+([A-Za-z]+)\b", l):
            tricolons.append((ln, m.group(0)))
    for ln, text in tricolons[TRICOLON_BUDGET:]:
        col.add(ln, "07-10", text)

    that_rel = []
    for ln, l in prose_lines:
        for m in re.finditer(r"\bthe\s+\w+\s+that\s+(?:\w+\s+){0,3}?(?:is|are|was|were|\w+s|\w+ed)\b", l, re.I):
            that_rel.append((ln, m.group(0)))
    for ln, text in that_rel[THAT_REL_BUDGET:]:
        col.add(ln, "07-3", text)


def check_format(vis, col, lang, units, doc_name):
    heads = []
    for i, (ln, l) in enumerate(vis):
        m = HEADING_RE.match(l.strip())
        if m:
            heads.append((i, ln, len(m.group(1)), m.group(2).strip()))

    # 09-B1 行内粗体小标题列表
    for ln, l in vis:
        if BOLD_TERM_BULLET_RE.match(l):
            col.add(ln, "09-B1", l.strip())

    # 09-B2 粗体滥用
    bold_count = sum(len(BOLD_RE.findall(l)) for _, l in vis)
    bold_allowed = max(3, units * BOLD_BUDGET_PER_1000 // 1000)
    if bold_count > bold_allowed:
        col.add(1, "09-B2", "全文行内粗体 %d 处，预算 %d" % (bold_count, bold_allowed))

    # 09-B5 只含子标题的空标题 / 09-B6 跳过层级、多个一级标题
    h1_count = sum(1 for _, _, lvl, _ in heads if lvl == 1)
    if h1_count > 1:
        col.add(heads[0][1], "09-B6", "本文档有 %d 个一级标题" % h1_count)
    prev_lvl = None
    for i, ln, lvl, text in heads:
        if prev_lvl is not None and lvl > prev_lvl + 1:
            col.add(ln, "09-B6", "标题层级 %d -> %d 跳级：%s" % (prev_lvl, lvl, text[:40]))
        # 空标题：下一个可见行仍是标题
        nxt = None
        for j in range(i + 1, len(vis)):
            if vis[j][1].strip():
                nxt = vis[j][1].strip()
                break
        if nxt is None or HEADING_RE.match(nxt):
            col.add(ln, "09-B5", text[:40])
        prev_lvl = lvl

    # 09-B3 标题式大写（英文）
    if lang in ("en", "mixed"):
        for _, ln, _, text in heads:
            if is_title_case(text):
                col.add(ln, "09-B3", text[:60])

    # 09-B7 分隔线过密
    hr_lines = [ln for ln, l in vis if HR_RE.match(l)]
    for ln in hr_lines[HR_BUDGET:]:
        col.add(ln, "09-B7", "本文档第 %d 条分隔线（预算 %d）" % (len(hr_lines), HR_BUDGET))

    # 09-B8 emoji 当格式符（标题或列表项）
    for ln, l in vis:
        if EMOJI_RE.search(l) and (HEADING_RE.match(l.strip()) or LIST_START_RE.match(l)):
            col.add(ln, "09-B8", l.strip()[:60])

    # 09-B10 弯直引号混用（弱信号）
    has_curly = any(q in l for _, l in vis for q in CURLY_QUOTES)
    has_straight = any(STRAIGHT_DOUBLE in l for _, l in vis)
    if has_curly and has_straight:
        ln = next(ln for ln, l in vis if any(q in l for q in CURLY_QUOTES))
        col.add(ln, "09-B10", "同一文档混用弯引号与直引号")


def check_artifacts(raw_lines, col):
    for lineno, line in enumerate(raw_lines, start=1):
        for source, rx in ARTIFACT_PATTERNS:
            for m in re.finditer(rx, line):
                col.add(lineno, "09-A", "%s: %s" % (source, m.group(0)))


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------

def lint_text(text, name="<stdin>", lang=None):
    raw_lines = text.splitlines()
    vis = visible_lines(raw_lines)
    prose = "\n".join(l for _, l in vis)
    resolved = lang if lang in ("zh", "en", "mixed") else detect_lang(prose)
    en_units, cjk_units = count_units(prose)
    units = en_units + cjk_units

    col = Collector(name)
    if resolved in ("zh", "mixed"):
        check_zh_lines(vis, col, prose)
    if resolved in ("en", "mixed"):
        check_en_lines(vis, col, prose)
    check_format(vis, col, resolved, units, name)
    check_artifacts(raw_lines, col)   # 09-A 对任何语言、含代码块都要扫

    col.hits.sort(key=lambda h: (h["file"], h["line"], h["rule"]))
    meta = {
        "lang": resolved,
        "units": units,
        "en_words": en_units,
        "cjk_chars": cjk_units,
    }
    return col.hits, meta


def format_report(all_hits, total_units, threshold, as_json):
    counted = [h for h in all_hits if h["counted"]]
    density = (len(counted) / total_units * 1000) if total_units else 0.0
    artifacts = [h for h in all_hits if h["rule"] == "09-A"]
    passed = (density < threshold) and not artifacts

    if as_json:
        print(json.dumps({
            "units": total_units,
            "hit_count": len(counted),
            "notice_count": len(all_hits) - len(counted),
            "density_per_1000_units": round(density, 2),
            "threshold": threshold,
            "artifact_hits": len(artifacts),
            "pass": passed,
            "hits": all_hits,
        }, ensure_ascii=False, indent=2))
        return passed

    for h in all_hits:
        tag = "!! " if h["rule"] == "09-A" else ("~  " if not h["counted"] else "   ")
        print("%s%s:%d  [%s] %s (%s): %s" % (
            tag, h["file"], h["line"], h["rule"], h["name"], h["severity"], h["excerpt"]))

    print()
    if artifacts:
        print("!! 命中 09-A 机器残留标记 %d 处——零假阳性，生成过程泄漏，必删"
              "（删前确认来源不丢失，见 references/09 第 A 节）。" % len(artifacts))
    verdict = "PASS" if passed else "FAIL"
    print("%d units, %d hits (%d notices), density %.1f/1000 (threshold %g) -> %s" % (
        total_units, len(counted), len(all_hits) - len(counted),
        density, threshold, verdict))
    if not passed and not artifacts:
        print("提示：密度超阈值只说明「值得按对应规则逐条看」，不等于每处都该改；"
              "拿不准就保留原文（references/01 第 1 条）。")
    return passed


def list_rules():
    print("de-ai-flavor 确定性 linter 规则表\n")
    print("%-16s %-14s %-30s %s" % ("RULE", "LAYER", "NAME", "SOURCE"))
    for rid, (layer, rname, source, sev) in RULES.items():
        print("%-16s %-14s %-30s %s [%s]" % (rid, layer, rname, source, sev))
    print("\nnotice 级只提示、不计入密度：%s" % ", ".join(
        rid for rid, v in RULES.items() if v[3] == "notice"))


def show_protected():
    print("反向保护清单——本 linter 永不判为命中（references/06、references/08）\n")
    print("%-8s %-40s %s" % ("ID", "PROTECTED FEATURE", "WHY"))
    for pid, name, source, why in PROTECTED:
        print("%-8s %-40s %s" % (pid, name, why))
    print("\n结论：被动语态、hedge、问句、比喻、单组三项、词汇多样性、"
          "简单 is/has、普通动词等在此一律不报；报出来只会诱导越改越糟。")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="de-ai-flavor 确定性 AI 味儿 linter（只报不改）")
    ap.add_argument("files", nargs="*", help="待检查的文本文件（缺省读 stdin）")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help="每 1000 units 允许的命中数（默认 %(default)s）")
    ap.add_argument("--lang", choices=["auto", "zh", "en", "mixed"], default="auto",
                    help="语言判定（默认自动）")
    ap.add_argument("--json", action="store_true", dest="as_json",
                    help="输出 JSON 报告")
    ap.add_argument("--list-rules", action="store_true",
                    help="打印规则编号表后退出")
    ap.add_argument("--show-protected", action="store_true",
                    help="打印反向保护清单后退出")
    args = ap.parse_args(argv)

    if args.list_rules:
        list_rules()
        return 0
    if args.show_protected:
        show_protected()
        return 0

    lang = None if args.lang == "auto" else args.lang
    texts = []
    if args.files:
        for path in args.files:
            try:
                with open(path, encoding="utf-8") as fh:
                    texts.append((path, fh.read()))
            except (OSError, UnicodeDecodeError) as exc:
                sys.stderr.write("无法读取 %s：%s\n" % (path, exc))
                return 2
    else:
        data = sys.stdin.buffer.read().decode("utf-8", "replace")
        texts.append(("<stdin>", data))

    all_hits, total_units = [], 0
    for name, text in texts:
        hits, meta = lint_text(text, name=name, lang=lang)
        all_hits.extend(hits)
        total_units += meta["units"]

    passed = format_report(all_hits, total_units, args.threshold, args.as_json)
    return 0 if passed else 1


def _configure_stdout():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


_configure_stdout()

if __name__ == "__main__":
    sys.exit(main())
