# -*- coding: utf-8 -*-
"""全量重写准备：从原 256-631 正文抽逐章情节要点（标题/字数/对白/在场人物/开头/结尾/关键唱词），写 beats.json 与 beats_digest.txt。只读 orig。"""
import io, os, re, json
BASE = r"C:\Users\niko\storymoss_case\full_rewrite"
ORIG = os.path.join(BASE, "orig")
idx = {r["seq"]: r for r in json.load(io.open(os.path.join(BASE, "orig_index.json"), encoding="utf-8"))["index"]}
NAMES = [u"白曦", u"小满", u"裴琬", u"晏吏", u"库役", u"沈确", u"接更吏", u"新俟编", u"俟编", u"新俟", u"新值", u"卯十九", u"廿一", u"廿二", u"阙"]
Q = re.compile(u"\u201c([^\u201d]*)\u201d")
VOL = [(256, 270, u"一"), (271, 310, u"二"), (311, 350, u"三"), (351, 390, u"四"), (391, 430, u"五"), (431, 470, u"六"),
       (471, 510, u"七"), (511, 550, u"八"), (551, 590, u"九"), (591, 630, u"十"), (631, 631, u"十一")]
def vol(s):
    for a, b, v in VOL:
        if a <= s <= b:
            return v
    return u"?"
def clean(t):
    return re.sub(u"\\s+", u"", t)
out, lines = [], []
for seq in range(256, 632):
    p = os.path.join(ORIG, "ch%03d.txt" % seq)
    t = io.open(p, encoding="utf-8").read() if os.path.exists(p) else u""
    r = idx.get(seq, {})
    cast = [n for n in NAMES if n in t]
    quotes = [q for q in Q.findall(t) if len(q) >= 4]
    seen, keyq = set(), []
    for q in quotes:
        if q not in seen:
            seen.add(q); keyq.append(q)
    c = clean(t)
    b = {"seq": seq, "vol": vol(seq), "title": r.get("title", u""), "chars": len(t), "dialogue": r.get("dialogue"),
         "cast": cast, "head": c[:120], "tail": c[-160:], "key_lines": keyq[:8]}
    out.append(b)
    lines.append(u"%d|卷%s|%s|%d字|%s|在场:%s|唱:%s|尾:%s" % (seq, b["vol"], b["title"], b["chars"], b["dialogue"],
                 u",".join(cast), u" / ".join(keyq[:4]), c[-80:]))
json.dump(out, io.open(os.path.join(BASE, "beats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(BASE, "beats_digest.txt"), "w", encoding="utf-8").write(u"\n".join(lines) + u"\n")
miss = [b["seq"] for b in out if b["chars"] == 0]
print("beats", len(out), "missing", miss)
print("digest", os.path.getsize(os.path.join(BASE, "beats_digest.txt")))
