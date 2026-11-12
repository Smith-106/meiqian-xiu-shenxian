# -*- coding: utf-8 -*-
"""Judge selected assembled chapters N times each (neutral + rule) and print mean scores.
Usage: python judge_one.py <chapter numbers comma-separated> [runs=2]
"""
import sys, io, os, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge as J

C = r"C:\Users\niko\storymoss_case\full_rewrite\chapters"
nums = [x.strip() for x in sys.argv[1].split(",") if x.strip()]
runs = int(sys.argv[2]) if len(sys.argv) > 2 else 2
files = [f for f in sorted(os.listdir(C)) if f.endswith(".txt") and f[:3] in nums]
jobs = [(f, i) for f in files for i in range(runs)]
with ThreadPoolExecutor(max_workers=6) as ex:
    res = list(ex.map(lambda x: (x[0], J.check(os.path.join(C, x[0]))), jobs))
agg = {}
for f, r in res:
    agg.setdefault(f, []).append(r)
for f in files:
    rs = agg[f]
    ns = [r["neutral"] for r in rs if isinstance(r.get("neutral"), (int, float))]
    rr = [r["rule"] for r in rs if isinstance(r.get("rule"), (int, float))]
    print("%s | %d | %.3f | sm=%s | N=%s mean=%.1f | R mean=%.1f" % (
        f, rs[0]["chars"], rs[0]["dialogue"], rs[0]["sm"], ns, sum(ns) / max(len(ns), 1), sum(rr) / max(len(rr), 1)))
    for r in rs[:1]:
        for x in (r.get("neutral_issues") or [])[:5]:
            print("    -", str(x)[:120])
