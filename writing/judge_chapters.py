# -*- coding: utf-8 -*-
"""Judge every assembled chapter in chapters\\ (neutral + rule). Writes judge_chapters.json."""
import sys, io, os, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge as J

C = r"C:\Users\niko\storymoss_case\full_rewrite\chapters"
files = sorted(f for f in os.listdir(C) if f.endswith(".txt"))
with ThreadPoolExecutor(max_workers=int(os.environ.get("DSH_JUDGE_WORKERS", "4"))) as ex:
    res = list(ex.map(lambda f: (f, J.check(os.path.join(C, f))), files))
out = {f: r for f, r in res}
io.open(os.path.join(os.path.dirname(C), "judge_chapters.json"), "w", encoding="utf-8").write(
    json.dumps(out, ensure_ascii=False, indent=1))
ns = [r["neutral"] for _, r in res if isinstance(r.get("neutral"), (int, float))]
rs = [r["rule"] for _, r in res if isinstance(r.get("rule"), (int, float))]
for f, r in res:
    print("%s | %d | %.3f | sm=%s | N=%s | R=%s" % (f, r["chars"], r["dialogue"], r["sm"], r.get("neutral"), r.get("rule")))
print("AVG neutral %.1f over %d | AVG rule %.1f over %d" % (sum(ns) / max(len(ns), 1), len(ns), sum(rs) / max(len(rs), 1), len(rs)))
