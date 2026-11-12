# -*- coding: utf-8 -*-
"""Fold runs of consecutive chant paragraphs into one narration line.

A chant paragraph is a paragraph that is (optionally attributed) a single quote whose text
starts with a two-character ritual verb followed by ，or 。 and contains no question mark.
In a run of >= MINRUN consecutive chant paragraphs (blank lines between them allowed),
the first chant is kept verbatim and the rest are folded into one narration sentence:
    "其后X、Y、Z，一句接一句，唱声没有停。"
where X/Y/Z are the leading two-character verbs.
Usage: python fold_chants.py <regex> [--write]
Backups: draft\\_quarantine_drift\\<name>.pre_fold_v1.txt
"""
import sys, io, os, re, shutil
sys.path.insert(0, r"C:\Users\niko\AppData\Local\Temp")
import sm_quality as Q

D = r"C:\Users\niko\storymoss_case\full_rewrite\draft"
MINRUN = 3
CH = re.compile(u"^(?:[\u4e00-\u9fff]{1,4}道：)?\u201c([\u4e00-\u9fff]{2})[，。][^\u201d？]*\u201d(?:[\u4e00-\u9fff]{1,6}(?:道|应声|应)[。，]?)?(?:\u201c[^\u201d？]*\u201d)?$")
R = re.compile(u'[\u201c"]([^\u201d"]*)[\u201d"]')
TAILS = [u"一句接一句，唱声没有停。", u"一样一样唱过去，没有差。", u"唱声一句压着一句，平的。",
         u"都唱过了，字字和上一回一样。"]


def fold(t):
    paras = [p for p in t.split(u"\n")]
    blocks = []  # list of non-empty paragraphs
    for p in paras:
        if p.strip():
            blocks.append(p.strip())
    out = []
    i = 0
    k = 0
    while i < len(blocks):
        m = CH.match(blocks[i])
        if not m:
            out.append(blocks[i]); i += 1; continue
        j = i
        verbs = []
        while j < len(blocks):
            mj = CH.match(blocks[j])
            if not mj:
                break
            verbs.append(mj.group(1)); j += 1
        if j - i >= MINRUN:
            out.append(blocks[i])
            rest = []
            for v in verbs[1:]:
                if v not in rest:
                    rest.append(v)
            out.append(u"其后" + u"、".join(rest) + u"，" + TAILS[k % len(TAILS)])
            k += 1
        else:
            out.extend(blocks[i:j])
        i = j
    return u"\n\n".join(out) + u"\n"


if __name__ == "__main__":
    pat = re.compile(sys.argv[1]); write = "--write" in sys.argv
    for f in sorted(os.listdir(D)):
        if not f.endswith(".txt") or f.startswith("_") or not pat.search(f):
            continue
        p = os.path.join(D, f); t = io.open(p, encoding="utf-8").read(); t2 = fold(t)
        n0 = len(re.sub(r"\s", "", t)); n1 = len(re.sub(r"\s", "", t2))
        dl = sum(len(x) for x in R.findall(t2)) / float(n1); s = Q.score(t2)
        print("%s chars %d->%d dl %.3f sm %s %s" % (f, n0, n1, dl, s["score"], s.get("issues") or ""))
        if write and s["score"] >= 95 and t2 != t:
            bk = os.path.join(D, "_quarantine_drift", f[:-4] + ".pre_fold_v1.txt")
            if not os.path.exists(bk):
                shutil.copyfile(p, bk)
            io.open(p, "w", encoding="utf-8").write(t2)
