# -*- coding: utf-8 -*-
"""Re-judge chapters whose neutral or rule score is missing in a judge json, and merge in place.
Usage: python judge_fill.py <judge json>   (same judge.check protocol; use DSH_JUDGE / DSH_JUDGE_WORKERS / DSH_JUDGE_RETRIES)"""
import sys, io, os, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge as J

C = r"C:\Users\niko\storymoss_case\full_rewrite\chapters"
P = sys.argv[1]
d = json.load(io.open(P, encoding="utf-8"))
todo = [f for f in sorted(os.listdir(C)) if f.endswith(".txt")
        and (f not in d or not d[f].get("neutral_dims") or not isinstance(d[f].get("rule"), (int, float)))]
print("refill", len(todo), [f[:3] for f in todo], flush=True)


def one(f):
    old = d.get(f) or {}
    r = J.check(os.path.join(C, f))
    if old.get("neutral_dims") and not r.get("neutral_dims"):
        for k in ("neutral", "neutral_dims", "neutral_issues"):
            r[k] = old.get(k)
    if isinstance(old.get("rule"), (int, float)) and not isinstance(r.get("rule"), (int, float)):
        r["rule"], r["rule_issues"] = old.get("rule"), old.get("rule_issues")
    print(f[:3], r.get("neutral_dims"), r.get("rule"), flush=True)
    return f, r


with ThreadPoolExecutor(max_workers=int(os.environ.get("DSH_JUDGE_WORKERS", "2"))) as ex:
    for f, r in ex.map(one, todo):
        d[f] = r
io.open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
print("missing after:", [f[:3] for f in d if not d[f].get("neutral_dims") or not isinstance(d[f].get("rule"), (int, float))])
