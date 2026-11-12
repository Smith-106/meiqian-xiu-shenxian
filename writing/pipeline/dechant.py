import io, re, glob, os, sys, json
sys.path.insert(0, r"C:\Users\niko\AppData\Local\Temp")
import sm_quality as Q
D = u"C:\\Users\\niko\\storymoss_case\\full_rewrite\\draft\\"
APPLY = len(sys.argv) > 1
RQ = re.compile(u'[\u201c"]([^\u201d"]*)[\u201d"]')
part = re.compile(u'[的了吗呢么吧你我他她谁什怎哪这那是不没有要会能就也还都别]')
def chant(q):
    segs = [s for s in re.split(u'[，。、；！]', q) if s]
    return len(segs) >= 2 and all(len(s) <= 7 for s in segs) and not any(part.search(s) for s in segs)
para = re.compile(u'^(?:([\u4e00-\u9fff]{1,4}(?:道|唱|说|应|接|念)[，：]?))?\u201c([^\u201d]*)\u201d(?:([\u4e00-\u9fff]{1,6}(?:道|唱|说|应|接|念))[。，]?)?$')
def st(t):
    n = len(re.sub(r"\s","",t)); d = sum(len(x) for x in RQ.findall(t))/n
    return n, d
tot = 0; log = []
for f in sorted(glob.glob(D + u"卷*.txt")):
    t = io.open(f, encoding="utf-8").read()
    n0, d0 = st(t)
    ps = t.split("\n\n"); keep = []; seen = set(); removed = []
    for i, p in enumerate(ps):
        s = p.strip(); m = para.match(s)
        if m and chant(m.group(2)):
            nxt = ps[i+1].strip() if i+1 < len(ps) else ""
            first = m.group(2) not in seen; seen.add(m.group(2))
            asks = nxt.startswith(u"\u201c") and (u"？" in nxt[:30])
            if not first and not asks or (len(removed) < 99 and not asks and i > 0 and i < len(ps)-1 and not first) :
                trial = "\n\n".join(keep + ps[i+1:])
                n1, d1 = st(trial)
                if d1 >= 0.21 and n1 >= n0*0.93:
                    removed.append(s); continue
            elif not asks and i > 0 and i < len(ps)-1:
                trial = "\n\n".join(keep + ps[i+1:])
                n1, d1 = st(trial)
                if d1 >= 0.21 and n1 >= n0*0.93 and len([1 for r in removed]) < 8:
                    removed.append(s); continue
        keep.append(p)
    if removed:
        nt = "\n\n".join(keep); n1, d1 = st(nt); sc = Q.score(nt)["score"]
        tot += len(removed)
        log.append("%s %d->%d d%.3f->%.3f sm%s rm%d: %s" % (os.path.basename(f)[:9], n0, n1, d0, d1, sc, len(removed), " | ".join(r[:22] for r in removed)))
        if APPLY and sc >= 95: io.open(f, "w", encoding="utf-8").write(nt)
print("\n".join(log)); print("total", tot)
