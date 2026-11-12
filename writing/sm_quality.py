# -*- coding: utf-8 -*-
u"""离线门禁打分模块（2026-11-01 重建版）。

原文件位于 %TEMP%\\sm_quality.py，被系统清理后丢失。本文件按以下依据重建：
  * build_v3.py / judge.py 的调用契约：score(t) -> {"score":int, "issues":[...], "m":measure(t)}
  * 其他脚本用到的字段：measure(t) -> chars / dialogue / avg_sent / avg_para / mild / aphorism
  * 项目文档记载的门禁：2800-3300 字、对白 0.20-0.30、均句 11-24、均段 <=58、
    感叹 <=1.0‰、head <=0.22、禁感叹号、禁格言式章尾、禁词（这一刻/这一刻钟/他觉得）

校准：42 章现有正文在 measure() 下分别为 chars 2801-3297、dialogue 0.205-0.295、
avg_sent 17.2-21.1、avg_para 36.5-56.1、emotion 0.000‰、head 0.013-0.071，
与历史记录的 sm=100 完全一致，故各阈值沿用原值。

用法：
    import sm_quality as Q
    s = Q.score(text)
    s["score"]          # 0-100
    s["issues"]         # [{"dim": str, "msg": str}, ...]
    s["m"]["dialogue"]  # 各指标
"""

import re

QUOTE = re.compile(u'[\u201c"]([^\u201d"]*)[\u201d"]')
EXCL = re.compile(u'[！!]')
SENT_SPLIT = re.compile(u'[。！？…]+')

# 硬禁词：出现即扣分
FORBIDDEN = [u"这一刻", u"这一刻钟", u"他觉得"]

# 章尾格言化：结尾若是短促的、不带对白的判断句，且命中以下标记，判为格言收尾
APHORISM_MARKERS = [u"才算是", u"不过如此", u"从来如此", u"本就如此", u"就是道理",
                    u"便是规矩", u"这才是", u"说到底", u"终究是"]

CHARS_MIN, CHARS_MAX = 2800, 3300
DLG_MIN, DLG_MAX = 0.20, 0.30
SENT_MIN, SENT_MAX = 11.0, 24.0
PARA_MAX = 58.0
EMO_MAX = 1.0          # 千分比
HEAD_MAX = 0.22


def _nows(s):
    return len(re.sub(r"\s", "", s))


def measure(t):
    u"""返回客观指标字典。"""
    t = t or u""
    n = _nows(t)
    paras = [p.strip() for p in t.split("\n") if p.strip()]
    quotes = QUOTE.findall(t)
    dlg_chars = sum(_nows(x) for x in quotes)
    dialogue = dlg_chars / float(max(n, 1))

    frags = [s for s in SENT_SPLIT.split(t) if _nows(s)]
    n_sent = max(len(frags), 1)
    n_para = max(len(paras), 1)

    avg_sent = n / float(n_sent)
    avg_para = n / float(n_para)

    excl = len(EXCL.findall(t))
    emotion = excl / float(max(n, 1)) * 1000.0

    head_chars = sum(_nows(p) for p in paras[:3])
    head = head_chars / float(max(n, 1))

    # 单字词/短句密度（“mild”沿用原字段名：轻度冗余提示，仅作参考不作门禁）
    mild = 0.0
    if n_para:
        short = sum(1 for p in paras if _nows(p) <= 8)
        mild = short / float(n_para)

    aphorism = 0
    if paras:
        last = paras[-1]
        if not QUOTE.search(last) and _nows(last) <= 22:
            if any(m in last for m in APHORISM_MARKERS):
                aphorism = 1

    return {
        "chars": n,
        "dialogue": round(dialogue, 3),
        "avg_sent": round(avg_sent, 1),
        "avg_para": round(avg_para, 1),
        "emotion": round(emotion, 2),
        "head": round(head, 3),
        "mild": round(mild, 3),
        "aphorism": aphorism,
        "n_para": len(paras),
        "n_sent": len(frags),
        "excl": excl,
    }


def score(t):
    u"""返回 {"score": int, "issues": [...], "m": measure(t)}。"""
    m = measure(t)
    issues = []

    def bad(dim, msg, pen):
        issues.append({"dim": dim, "msg": msg, "penalty": pen})

    if m["chars"] < CHARS_MIN:
        bad(u"字数", u"不足 %d 字（现 %d）" % (CHARS_MIN, m["chars"]), 10)
    elif m["chars"] > CHARS_MAX:
        bad(u"字数", u"超出 %d 字（现 %d）" % (CHARS_MAX, m["chars"]), 10)

    if m["dialogue"] < DLG_MIN:
        bad(u"对白", u"对白占比过低 %.3f" % m["dialogue"], 8)
    elif m["dialogue"] > DLG_MAX:
        bad(u"对白", u"对白占比过高 %.3f" % m["dialogue"], 8)

    if m["avg_sent"] < SENT_MIN:
        bad(u"句长", u"均句过短 %.1f" % m["avg_sent"], 5)
    elif m["avg_sent"] > SENT_MAX:
        bad(u"句长", u"均句过长 %.1f" % m["avg_sent"], 5)

    if m["avg_para"] > PARA_MAX:
        bad(u"段长", u"均段过长 %.1f" % m["avg_para"], 5)

    if m["emotion"] > EMO_MAX:
        bad(u"情绪", u"感叹过密 %.2f‰" % m["emotion"], 6)

    if m["head"] > HEAD_MAX:
        bad(u"开头", u"开头占比过大 %.3f" % m["head"], 4)

    if m["aphorism"]:
        bad(u"格言", u"章尾疑似格言化", 6)

    for w in FORBIDDEN:
        if w in t:
            bad(u"禁词", u"出现禁词「%s」" % w, 5)

    total = 100 - sum(i["penalty"] for i in issues)
    return {"score": max(0, min(100, total)), "issues": issues, "m": m}


if __name__ == "__main__":
    import sys, io, glob, os
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "chapters_v3")
    for f in sorted(glob.glob(os.path.join(d, "*.txt"))):
        s = score(io.open(f, encoding="utf-8").read())
        print("%s %d %s" % (os.path.basename(f)[:3], s["score"],
                            "; ".join(i["msg"] for i in s["issues"])))
