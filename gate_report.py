# -*- coding: utf-8 -*-
u"""全书质量门体检。

用法：
    python gate_report.py                    # 体检 manuscript/
    python gate_report.py manuscript/        # 指定目录
    python gate_report.py . --md report.md   # 同时输出 Markdown 报告
    python gate_report.py --strict           # 有不达标章则退出码 1（默认始终 0）

门禁（与 build_v3.py 一致）：
    字数 2,800–3,300（非空白字符）
    对白占比 0.20–0.30（中文双引号内字数 / 全章字数）
    sm_quality >= 95
    首行形如「第N章 标题」，且 N 与文件名前三位一致

只依赖标准库与同目录的 sm_quality.py。
"""
import sys
import io
import os
import re
import glob
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.join(_HERE, "writing")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import sm_quality as Q

QUOTE = re.compile(u'[\u201c"]([^\u201d"]*)[\u201d"]')
HEAD = re.compile(u'^第\\s*(\\d+)\\s*章\\s*\\S')

CHARS_MIN, CHARS_MAX = 2800, 3300
DLG_MIN, DLG_MAX = 0.20, 0.30
SM_MIN = 95


def measure(path):
    t = io.open(path, encoding="utf-8").read()
    n = len(re.sub(r"\s", "", t))
    dl = sum(len(x) for x in QUOTE.findall(t)) / float(max(n, 1))
    s = Q.score(t)
    first = t.strip().split("\n", 1)[0].strip()
    m = HEAD.match(first)
    head_no = int(m.group(1)) if m else None
    return {
        "chars": n,
        "dialogue": round(dl, 3),
        "sm": s["score"],
        "issues": s.get("issues") or [],
        "first": first,
        "head_no": head_no,
    }


def judge_file(path):
    base = os.path.basename(path)
    m = re.match(r"^(\d{1,4})_", base)
    no = int(m.group(1)) if m else None
    r = measure(path)
    reasons = []
    if not (CHARS_MIN <= r["chars"] <= CHARS_MAX):
        reasons.append(u"字数 %d" % r["chars"])
    if not (DLG_MIN <= r["dialogue"] <= DLG_MAX):
        reasons.append(u"对白 %.3f" % r["dialogue"])
    if r["sm"] < SM_MIN:
        reasons.append(u"质检 %d" % r["sm"])
    if r["head_no"] is None:
        reasons.append(u"缺标题行")
    elif no is not None and r["head_no"] != no:
        reasons.append(u"章号不符(%d)" % r["head_no"])
    return {
        "no": no,
        "file": base,
        "chars": r["chars"],
        "dialogue": r["dialogue"],
        "sm": r["sm"],
        "ok": not reasons,
        "reasons": reasons,
        "first": r["first"],
        "issues": r["issues"],
    }


def parse_args(argv):
    u"""拆出位置参数与 --md 的值，其余视为开关。"""
    pos, flags, md_path = [], [], None
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--md":
            if i + 1 < len(argv):
                md_path = argv[i + 1]
                i += 2
                continue
        elif a.startswith("--md="):
            md_path = a.split("=", 1)[1]
            i += 1
            continue
        elif a.startswith("--"):
            flags.append(a)
            i += 1
            continue
        pos.append(a)
        i += 1
    return pos, flags, md_path


def main(argv):
    args, flags, md_path = parse_args(argv)
    target = args[0] if args else "manuscript"
    if not os.path.isabs(target):
        target = os.path.join(os.path.dirname(os.path.abspath(__file__)), target)

    files = sorted(glob.glob(os.path.join(target, "*.txt")))
    if not files:
        print(u"目录中没有 .txt：%s" % target)
        return 0

    rows = [judge_file(f) for f in files]
    bad = [r for r in rows if not r["ok"]]

    # 控制台表格
    print(u"章   字数  对白   质检  结果  原因")
    print(u"-" * 72)
    for r in rows:
        print(u"%-4s %5d %.3f  %4d  %-4s %s" % (
            ("%03d" % r["no"]) if r["no"] is not None else "??",
            r["chars"], r["dialogue"], r["sm"],
            u"通过" if r["ok"] else u"不通过",
            u"; ".join(r["reasons"])))
    print(u"-" * 72)

    # 统计
    # 质检分是字数/对白/句长的合成结果，单独列出会重复计数，故只在它是唯一原因时统计
    reasons = {}
    sm_only = 0
    for r in bad:
        others = [x for x in r["reasons"] if not x.startswith(u"质检")]
        if not others:
            sm_only += 1
            continue
        for x in others:
            key = re.sub(r"[0-9.]+$", "", x).strip()
            reasons[key] = reasons.get(key, 0) + 1
    if sm_only:
        reasons[u"仅质检分不足"] = sm_only
    total_chars = sum(r["chars"] for r in rows)
    print(u"合计 %d 章 | 通过 %d | 不通过 %d | 总字数 %d | 均 %.0f" % (
        len(rows), len(rows) - len(bad), len(bad), total_chars,
        total_chars / float(len(rows))))
    if reasons:
        print(u"不达标项：" + u"，".join(u"%s %d 章" % (k, v) for k, v in sorted(reasons.items(), key=lambda x: -x[1])))

    # Markdown 报告
    if md_path:
        lines = [u"## 质量门体检", u"",
                 u"| 章 | 字数 | 对白 | 质检 | 结果 | 原因 |", u"|---:|---:|---:|---:|:--:|---|"]
        for r in rows:
            lines.append(u"| %s | %d | %.3f | %d | %s | %s |" % (
                r["no"] if r["no"] is not None else "?", r["chars"], r["dialogue"], r["sm"],
                u"✅" if r["ok"] else u"❌", u"; ".join(r["reasons"])))
        lines += [u"", u"**合计 %d 章 | 通过 %d | 不通过 %d | 总字数 %d**" % (
            len(rows), len(rows) - len(bad), len(bad), total_chars), u""]
        if reasons:
            lines.append(u"不达标项：" + u"，".join(u"%s %d 章" % (k, v) for k, v in sorted(reasons.items(), key=lambda x: -x[1])))
        io.open(md_path, "w", encoding="utf-8", newline="\n").write(u"\n".join(lines) + u"\n")
        print(u"Markdown 报告已写入 %s" % md_path)

    if "--strict" in flags and bad:
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main(sys.argv))
