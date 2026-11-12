# -*- coding: utf-8 -*-
"""Trim repeated ritual micro-action clauses from NARRATION only (quotes untouched).

A narration sentence is split into comma clauses. A clause is dropped when
  * it is short (<= MAXC chars) and contains a ritual word, and
  * the same ritual word already appeared earlier in this segment more than KEEP times, and
  * the sentence keeps at least one clause.
Usage: python trim_ritual.py <regex for segment names> [--write]
Backups go to draft\\_quarantine_drift\\<name>.pre_trim_v1.txt (only with --write).
"""
import sys, io, os, re, shutil
sys.path.insert(0, r"C:\Users\niko\AppData\Local\Temp")
import sm_quality as Q

D = r"C:\Users\niko\storymoss_case\full_rewrite\draft"
W = [u"半步", u"鞋尖", u"足跟", u"砖缝", u"贴线", u"踏定", u"不挡", u"线外", u"不动", u"不翘",
     u"灯影", u"尘伏", u"压线", u"踏实", u"立定", u"不移", u"不散"]
KEEP = 3
MAXC = 12
QUOTE = re.compile(u"(\u201c[^\u201d]*\u201d)")
R = re.compile(u'[\u201c"]([^\u201d"]*)[\u201d"]')


def trim_narr(s, seen):
    # s: a narration chunk (no quotes). split into sentences keeping terminators
    out = []
    for sent in re.findall(u"[^。？]*[。？]|[^。？]+$", s):
        if not sent:
            continue
        end = sent[-1] if sent[-1] in u"。？" else u""
        body = sent[:-1] if end else sent
        cl = body.split(u"，")
        keep = []
        for i, c in enumerate(cl):
            ws = [w for w in W if w in c]
            drop = False
            # never drop the first clause (it carries the subject); never drop locative clauses
            # that a following clause may depend on.
            if (i > 0 and ws and len(c) <= MAXC and all(seen.get(w, 0) >= KEEP for w in ws)
                    and not c.endswith((u"上", u"里", u"前", u"外", u"侧"))):
                drop = True
            for w in ws:
                seen[w] = seen.get(w, 0) + 1
            if not drop:
                keep.append(c)
        if not keep:
            continue
        out.append(u"，".join(keep) + end)
    return u"".join(out)


def process(t):
    seen = {}
    paras = t.split(u"\n")
    res = []
    for p in paras:
        if not p.strip():
            res.append(p)
            continue
        parts = QUOTE.split(p)
        np = []
        for x in parts:
            if x.startswith(u"\u201c"):
                np.append(x)
                for w in W:
                    if w in x:
                        seen[w] = seen.get(w, 0) + 1
            else:
                np.append(trim_narr(x, seen))
        q = u"".join(np)
        if q.strip():
            res.append(q)
        else:
            res.append(u"")
    out = u"\n".join(res)
    out = re.sub(u"\n{3,}", u"\n\n", out)
    return out


def dens(t):
    L = len(re.sub(r"\s", "", t))
    return sum(t.count(w) for w in W) * 1000.0 / max(L, 1)


if __name__ == "__main__":
    pat = re.compile(sys.argv[1])
    write = "--write" in sys.argv
    for f in sorted(os.listdir(D)):
        if not f.endswith(".txt") or f.startswith("_") or not pat.search(f):
            continue
        p = os.path.join(D, f)
        t = io.open(p, encoding="utf-8").read()
        t2 = process(t)
        n0 = len(re.sub(r"\s", "", t)); n1 = len(re.sub(r"\s", "", t2))
        dl = sum(len(x) for x in R.findall(t2)) / float(n1)
        s = Q.score(t2)
        print("%s chars %d->%d dens %.1f->%.1f dl %.3f sm %s %s" % (f, n0, n1, dens(t), dens(t2), dl, s["score"], s.get("issues") or ""))
        if write and s["score"] >= 95:
            bk = os.path.join(D, "_quarantine_drift", f[:-4] + ".pre_trim_v1.txt")
            if not os.path.exists(bk):
                shutil.copyfile(p, bk)
            io.open(p, "w", encoding="utf-8").write(t2)
