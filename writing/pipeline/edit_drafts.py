# -*- coding: utf-8 -*-
"""apply(reps, tag): each (old, new) must occur exactly once across all draft files; backs up once per tag."""
import io, re, os, glob, sys
sys.path.insert(0, r"C:\Users\niko\AppData\Local\Temp")
import sm_quality as Q

D = u"C:\\Users\\niko\\storymoss_case\\full_rewrite\\draft\\"
R = re.compile(u'[\u201c"]([^\u201d"]*)[\u201d"]')


def files():
    return sorted(glob.glob(D + u"卷*.txt"))


def apply(reps, tag):
    texts = {f: io.open(f, encoding="utf-8").read() for f in files()}
    orig = dict(texts)
    for a, b in reps:
        hits = [f for f, t in texts.items() if a in t]
        tot = sum(texts[f].count(a) for f in hits)
        if tot != 1:
            print("SKIP(%d)" % tot, a[:24].replace("\n", " "))
            continue
        texts[hits[0]] = texts[hits[0]].replace(a, b)
    for f, t in texts.items():
        if t == orig[f]:
            continue
        name = os.path.basename(f)
        bk = D + u"_quarantine_drift\\" + name.replace(".txt", ".pre_%s.txt" % tag)
        if not os.path.exists(bk):
            io.open(bk, "w", encoding="utf-8").write(orig[f])
        t = re.sub(u"\n{3,}", u"\n\n", t)
        io.open(f, "w", encoding="utf-8").write(t)
        n = len(re.sub(r"\s", "", t)); s = Q.score(t)
        print(name[:8], n, round(sum(len(x) for x in R.findall(t)) / n, 3), s["score"],
              round(s["m"]["avg_sent"], 2), s.get("issues"))


def total():
    return sum(len(re.sub(r"\s", "", io.open(f, encoding="utf-8").read())) for f in files())
