# -*- coding: utf-8 -*-
"""Assemble draft segments (258-631) into chapters of 2800-3300 chars with hook endings.
Outputs: chapters/NNN_标题.txt, chapter_map.json, chapter_table.md
"""
import io, os, re, sys, json

B = r"C:\Users\niko\storymoss_case\full_rewrite"
D = os.path.join(B, "draft")
OUT = os.path.join(B, "chapters")
sys.path.insert(0, r"C:\Users\niko\AppData\Local\Temp")
import sm_quality as Q

LO, HI, TARGET = 2800, 3300, 2810
FIRST_NEW_NO = 258  # new chapters continue after pilot 256, 257
FIXED = {256: u"卷01_p00_orig256.txt", 257: u"卷01_p00_orig257.txt"}  # pilot v2 openings, dialogue raised to 20%+
SEG_RE = re.compile(u"^(卷(\\d\\d))_p(\\d+)_orig(\\d+)(?:-(\\d+))?\\.txt$")
QUOTE = re.compile(u'[\u201c"]([^\u201d"]*)[\u201d"]')
DAY_RE = re.compile(u"^第[一二三四五六七八九十]+日")
VOL_CN = {1: u"卷一", 2: u"卷二", 3: u"卷三", 4: u"卷四", 5: u"卷五", 6: u"卷六",
          7: u"卷七", 8: u"卷八", 9: u"卷九", 10: u"卷十", 11: u"卷十一"}


def clen(s):
    return len(re.sub(r"\s", "", s))


def load_segments():
    segs = []
    for f in os.listdir(D):
        m = SEG_RE.match(f)
        if not m:
            continue
        a = int(m.group(4)); b = int(m.group(5) or a)
        if a in FIXED:
            continue  # pilot openings are kept as whole chapters
        segs.append((a, b, int(m.group(2)), f))
    segs.sort()
    return segs


def load_titles():
    titles = {}
    for line in io.open(os.path.join(B, "beats_digest.txt"), encoding="utf-8"):
        f = line.rstrip("\n").split("|")
        if len(f) > 2 and f[0].isdigit():
            titles[int(f[0])] = re.sub(u"^第\\d+章\\s*", "", f[2]).strip()
    for line in io.open(os.path.join(B, "orig_index.txt"), encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) > 1 and f[0].isdigit() and int(f[0]) not in titles:
            titles[int(f[0])] = re.sub(u"^第\\d+章\\s*", "", f[1]).strip()
    return titles


def paragraphs():
    """Yield paragraph dicts with volume and estimated original chapter."""
    paras = []
    for a, b, vol, f in load_segments():
        t = io.open(os.path.join(D, f), encoding="utf-8").read().replace("\r\n", "\n")
        ps = [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip()]
        total = sum(clen(p) for p in ps) or 1
        acc = 0
        for i, p in enumerate(ps):
            mid = acc + clen(p) / 2.0
            est = a + int((b - a + 1) * mid / total)
            est = min(max(est, a), b)
            paras.append({"text": p, "n": clen(p), "vol": vol, "orig": est,
                          "seg": f, "seg_first": i == 0})
            acc += clen(p)
    return paras


def hook_cost(paras, j):
    """Cost of ending a chapter after paragraph index j (lower is better)."""
    p = paras[j]["text"]
    nxt = paras[j + 1]["text"] if j + 1 < len(paras) else ""
    c = 6.0
    tail = p[-12:]
    if u"？" in tail or u"?" in tail:
        c -= 4.0                      # unanswered question
    if re.search(u"没有答|没答|没有回答|没有再问|没有动|候着|候令|未落|未至|还空着|还没|不知道", p[-40:]):
        c -= 3.0                      # pending / unresolved state
    if j + 1 < len(paras) and (DAY_RE.match(nxt) or paras[j + 1]["seg_first"]):
        c -= 2.0                      # next chapter opens on a fresh beat
    if p.startswith(u"\u201c") and p.endswith(u"\u201d") and len(p) < 20 and u"？" not in p:
        c += 3.0                      # bare chant is a weak ending
    if p.endswith(u"："):
        c += 2.0                      # cut right before a quotation
    return c


def split(paras, K=42):
    n = len(paras)
    pre = [0]
    for p in paras:
        pre.append(pre[-1] + p["n"])
    INF = float("inf")
    best = [[INF] * (n + 1) for _ in range(K + 1)]
    back = [[-1] * (n + 1) for _ in range(K + 1)]
    best[0][0] = 0.0
    for k in range(1, K + 1):
        bp, bk, bb = best[k - 1], best[k], back[k]
        for j in range(1, n + 1):
            hc = hook_cost(paras, j - 1) if j < n else 0.0
            for i in range(j - 1, -1, -1):
                L = pre[j] - pre[i]
                if L > HI:
                    break
                if L < LO or bp[i] == INF:
                    continue
                cost = bp[i] + abs(L - TARGET) / 150.0 + hc
                if cost < bk[j]:
                    bk[j] = cost; bb[j] = i
    if best[K][n] == INF:
        raise SystemExit("no feasible split")
    cuts = []
    j, k = n, K
    while j > 0:
        i = back[k][j]; cuts.append((i, j)); j = i; k -= 1
    return cuts[::-1]


def main():
    titles = load_titles()
    paras = paragraphs()
    cuts = split(paras, 42 - len(FIXED))
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".txt"):
            os.remove(os.path.join(OUT, f))
    cmap, rows, used = [], [], set()
    for no, fn in sorted(FIXED.items()):
        text = io.open(os.path.join(D, fn), encoding="utf-8").read().replace("\r\n", "\n").strip() + "\n"
        title = titles[no]; used.add(title)
        n = clen(text)
        dl = sum(len(x) for x in QUOTE.findall(text)) / float(n)
        s = Q.score(text)
        fname = u"%03d_%s.txt" % (no, title)
        io.open(os.path.join(OUT, fname), "w", encoding="utf-8").write(u"第%d章 %s\n\n%s" % (no, title, text))
        cmap.append({"new_no": no, "title": title, "volume": VOL_CN[1], "chars": n,
                     "dialogue": round(dl, 3), "sm_score": s["score"], "issues": s.get("issues"),
                     "orig_range": [no, no], "file": fname, "ending": text.strip()[-40:]})
        rows.append(u"| %d | %s | %s | %d | %.3f | %s | %d |" % (no, title, VOL_CN[1], n, dl, s["score"], no))
    for k, (i, j) in enumerate(cuts):
        no = FIRST_NEW_NO + k
        chunk = paras[i:j]
        text = "\n\n".join(p["text"] for p in chunk) + "\n"
        o0, o1 = chunk[0]["orig"], chunk[-1]["orig"]
        vol = chunk[0]["vol"]
        mid = (o0 + o1) // 2
        cand = [mid] + [c for c in range(o0, o1 + 1) if c != mid]
        if k == len(cuts) - 1 and o1 in titles:
            cand = [o1] + cand  # final chapter carries the closing original title
        title = next((titles[c] for c in cand if c in titles and titles[c] not in used), titles.get(mid, u"无题"))
        used.add(title)
        n = clen(text)
        dl = sum(len(x) for x in QUOTE.findall(text)) / float(n)
        s = Q.score(text)
        fname = u"%03d_%s.txt" % (no, title)
        io.open(os.path.join(OUT, fname), "w", encoding="utf-8").write(
            u"第%d章 %s\n\n%s" % (no, title, text))
        cmap.append({"new_no": no, "title": title, "volume": VOL_CN[vol], "chars": n,
                     "dialogue": round(dl, 3), "sm_score": s["score"], "issues": s.get("issues"),
                     "orig_range": [o0, o1], "file": fname,
                     "ending": chunk[-1]["text"][-40:]})
        rows.append(u"| %d | %s | %s | %d | %.3f | %s | %d–%d |" % (no, title, VOL_CN[vol], n, dl, s["score"], o0, o1))
    json.dump({"note": u"orig_range 为按段内位置估算的原章区间；新章号续接试点 256、257。",
               "chapters": cmap}, io.open(os.path.join(B, "chapter_map.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    hdr = u"| 新章号 | 标题 | 卷 | 字数 | 对白比 | sm | 对应原章 |\n| --: | :-- | :-- | --: | --: | --: | :-- |\n"
    io.open(os.path.join(B, "chapter_table.md"), "w", encoding="utf-8").write(hdr + "\n".join(rows) + "\n")
    bad = [c for c in cmap if not (LO <= c["chars"] <= HI) or not (0.20 <= c["dialogue"] <= 0.30) or c["sm_score"] < 95]
    print("chapters:", len(cmap), "range", cmap[0]["new_no"], "-", cmap[-1]["new_no"])
    print("chars min/max:", min(c["chars"] for c in cmap), max(c["chars"] for c in cmap))
    print("dialogue min/max:", min(c["dialogue"] for c in cmap), max(c["dialogue"] for c in cmap))
    print("sm min:", min(c["sm_score"] for c in cmap))
    print("FAILING:", [(c["new_no"], c["chars"], c["dialogue"], c["sm_score"], c["issues"]) for c in bad])


if __name__ == "__main__":
    main()
