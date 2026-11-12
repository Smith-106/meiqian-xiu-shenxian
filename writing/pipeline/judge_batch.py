# -*- coding: utf-8 -*-
"""Batch judge draft segments matching a regex (default 卷06–卷11). Writes judge_batch.json."""
import sys, io, os, re, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge as J

D = r"C:\Users\niko\storymoss_case\full_rewrite\draft"
pat = re.compile(sys.argv[1] if len(sys.argv) > 1 else u"^卷(06|07|08|09|10|11)_p\\d+_orig[\\d-]+\\.txt$")
files = sorted(f for f in os.listdir(D) if pat.match(f))

with ThreadPoolExecutor(max_workers=4) as ex:
    res = list(ex.map(lambda f: (f, J.check(os.path.join(D, f))), files))
out = {f: r for f, r in res}
io.open(os.path.join(os.path.dirname(D), "judge_batch.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
for f, r in res:
    print("%s | %d | %.3f | %s | N=%s %s | R=%s" % (f, r["chars"], r["dialogue"], r["sm"], r.get("neutral"), r.get("neutral_dims"), r.get("rule")))
