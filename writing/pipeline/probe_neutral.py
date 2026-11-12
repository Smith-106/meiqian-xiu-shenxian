# -*- coding: utf-8 -*-
"""Neutral-only repeated judging of one or more files (sequential, to stay under 429).
Usage: python probe_neutral.py N [--rule] file1 [file2 ...]
--rule also runs the strict book-rule judge once per file.
"""
import sys, io, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_sample as RS

args = sys.argv[1:]
n = int(args.pop(0))
rule = "--rule" in args
args = [a for a in args if a != "--rule"]
for f in args:
    t = io.open(f, encoding="utf-8").read()
    for i in range(n):
        r = RS.safe_parse(RS.chat(RS.NEUTRAL % t))
        print(os.path.basename(f), i, r.get("dims"), r.get("total"), flush=True)
        for k, s in enumerate(r.get("issues") or []):
            print("   ", k + 1, s, flush=True)
        time.sleep(5)
    if rule:
        st = RS.safe_parse(RS.strict(0, t))
        print(os.path.basename(f), "RULE", st.get("median"), flush=True)
        for s in (st.get("issues") or [])[:5]:
            print("    R", s, flush=True)
