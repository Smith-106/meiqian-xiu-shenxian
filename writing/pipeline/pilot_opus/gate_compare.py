# -*- coding: utf-8 -*-
"""试点盲比·本地门禁：同一把尺子 sm_quality.score 给原稿/新稿打分，结果写 UTF-8 文件。"""
import sys, io, os, json, random
sys.path.insert(0, r"C:\Users\niko\AppData\Local\Temp")
import sm_quality as Q
BASE = r"C:\Users\niko\storymoss_case\pilot_opus"
PILOT = [256, 257, 300, 450, 631]
random.seed(20261028)
out = {"chapters": {}, "blind_map": {}}
for n in PILOT:
    name = "ch%03d.txt" % n
    texts = {}
    for side in ("orig", "new"):
        p = os.path.join(BASE, side, name)
        if os.path.exists(p):
            texts[side] = io.open(p, encoding="utf-8").read()
    # 去章号盲标：随机分配 X/Y，评分时不带来源
    sides = list(texts)
    random.shuffle(sides)
    labels = dict(zip(sides, ["X", "Y"]))
    out["blind_map"][str(n)] = labels
    row = {}
    for side, t in texts.items():
        r = Q.score(t)
        row[side] = {"label": labels[side], "chars": len(t), "score": r["score"],
                     "issues": r["issues"], "m": r["m"]}
    out["chapters"][str(n)] = row
def avg(side):
    v = [out["chapters"][str(n)][side]["score"] for n in PILOT if side in out["chapters"][str(n)]]
    return round(sum(v) / len(v), 2) if v else None
out["avg"] = {"orig": avg("orig"), "new": avg("new")}
io.open(os.path.join(BASE, "gate_compare.json"), "w", encoding="utf-8").write(
    json.dumps(out, ensure_ascii=False, indent=1, default=str))
lines = []
for n in PILOT:
    c = out["chapters"][str(n)]
    lines.append("ch%d orig score=%s chars=%s issues=%d | new score=%s chars=%s issues=%d" % (
        n, c["orig"]["score"], c["orig"]["chars"], len(c["orig"]["issues"]),
        c["new"]["score"], c["new"]["chars"], len(c["new"]["issues"])))
lines.append("AVG orig=%s new=%s" % (out["avg"]["orig"], out["avg"]["new"]))
io.open(os.path.join(BASE, "gate_compare.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
