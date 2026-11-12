# -*- coding: utf-8 -*-
r"""v3 pipeline: chapters_v3\NNN_标题.txt are the source of truth (one file per chapter, 256..297).
python build_v3.py            -> gate report only
python build_v3.py --publish  -> if all 42 pass, back up chapters\ once, copy v3 into chapters\, write chapter_map.json
Gates: 2800-3300 chars (non-whitespace), dialogue 0.20-0.30, sm_quality >= 95, title line '第N章 标题'.
"""
import sys, io, os, re, json, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sm_quality as Q

R = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.join(R, "chapters_v3")
CH = os.path.join(R, "chapters")
QUOTE = re.compile(u'[\u201c"]([^\u201d"]*)[\u201d"]')


def stats(path):
    t = io.open(path, encoding="utf-8").read()
    n = len(re.sub(r"\s", "", t))
    dl = sum(len(x) for x in QUOTE.findall(t)) / float(max(n, 1))
    s = Q.score(t)
    first = t.strip().split("\n", 1)[0]
    return t, n, round(dl, 3), s["score"], s.get("issues"), first


def main():
    files = sorted(glob.glob(os.path.join(V3, "*.txt")))
    rows, bad = [], []
    for f in files:
        t, n, dl, sm, iss, first = stats(f)
        no = int(os.path.basename(f)[:3])
        ok = 2800 <= n <= 3300 and 0.20 <= dl <= 0.30 and sm >= 95 and first.startswith(u"第%d章 " % no)
        rows.append((no, os.path.basename(f), n, dl, sm, iss, ok))
        print("%s %4d %.3f %3d %s %s" % (os.path.basename(f), n, dl, sm, "" if ok else "FAIL", iss or ""))
        if not ok:
            bad.append(no)
    nos = [r[0] for r in rows]
    print("count", len(rows), "missing", sorted(set(range(256, 298)) - set(nos)), "FAILING", bad)
    if "--publish" in sys.argv:
        if bad or nos != list(range(256, 298)):
            raise SystemExit("not publishing: gates not met")
        bk = os.path.join(R, "chapters_pre_v3")
        if not os.path.isdir(bk):
            shutil.copytree(CH, bk)
        for f in glob.glob(os.path.join(CH, "*.txt")):
            os.remove(f)
        cmap = []
        for no, name, n, dl, sm, iss, ok in rows:
            shutil.copy(os.path.join(V3, name), os.path.join(CH, name))
            cmap.append({"new_no": no, "title": name[4:-4], "chars": n, "dialogue": dl, "sm_score": sm, "issues": iss})
        json.dump({"chapters": cmap}, io.open(os.path.join(R, "chapter_map.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("published", len(cmap))


if __name__ == "__main__":
    main()
