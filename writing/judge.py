# -*- coding: utf-8 -*-
"""Segment self-check: sm_quality + dialogue ratio + neutral five-dim + book-rule five-dim (judge gpt-oss-120b-medium).
Usage: python judge.py <draft file> [--no-llm]
"""
import sys, io, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sm_quality as Q
import review_sample as RS

QUOTE = re.compile(u'[\u201c"]([^\u201d"]*)[\u201d"]')


def check(path, llm=True):
    t = io.open(path, encoding="utf-8").read()
    n = len(re.sub(r"\s", "", t))
    dl = sum(len(x) for x in QUOTE.findall(t)) / float(max(n, 1))
    s = Q.score(t)
    out = {"chars": n, "dialogue": round(dl, 3), "sm": s["score"], "sm_issues": s.get("issues")}
    if llm:
        nt = RS.safe_parse(RS.chat(RS.NEUTRAL % t))
        st = RS.safe_parse(RS.strict(0, t))
        out["neutral"] = nt.get("total"); out["neutral_dims"] = nt.get("dims"); out["neutral_issues"] = nt.get("issues")
        out["rule"] = st.get("median"); out["rule_issues"] = st.get("issues")
    return out


if __name__ == "__main__":
    r = check(sys.argv[1], llm="--no-llm" not in sys.argv)
    print(json.dumps(r, ensure_ascii=False, indent=1))
