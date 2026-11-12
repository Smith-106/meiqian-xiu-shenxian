# -*- coding: utf-8 -*-
"""Claude Code subagent judge adapter (HANDOFF section 6 plan C: claude-opus-5.5 is gone from the cpa endpoint).
prep  writes, verbatim, the user message that judge.check / review_sample.main would send to chat(),
      one <id>.prompt.txt per job, plus manifest.json (chars / dialogue / sm frozen at prep time).
      A subagent reads one prompt file and writes its raw answer to <id>.out.txt.
todo  lists job ids whose answer is missing or unparseable.
collect parses the answers into judge_chapters_cc_<round>.json (same format as judge_chapters.json).
Usage:
  python judge_cc.py prep <round> [--baseline] [--only 273,274]
  python judge_cc.py todo <round>
  python judge_cc.py collect <round>
"""
import sys, io, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge as J
import review_sample as RS

B = r"C:\Users\niko\storymoss_case\full_rewrite"
C = os.path.join(B, "chapters")
OPUS_ORIG_RULE = 78.9  # claude-opus-5.5 baseline on the same 20 originals (review_sample_opus.txt)


def rdir(rnd):
    return os.path.join(B, "judge_cc", "r%s" % rnd)


def load_manifest(rnd):
    return json.load(io.open(os.path.join(rdir(rnd), "manifest.json"), encoding="utf-8"))


def answer(rnd, jid):
    p = os.path.join(rdir(rnd), jid + ".out.txt")
    if not os.path.exists(p):
        return None
    return RS.safe_parse(io.open(p, encoding="utf-8").read())


def prep(rnd, baseline, only):
    d = rdir(rnd)
    os.makedirs(d, exist_ok=True)
    man = {}
    for f in sorted(x for x in os.listdir(C) if x.endswith(".txt")):
        if only and f[:3] not in only:
            continue
        path = os.path.join(C, f)
        t = io.open(path, encoding="utf-8").read()
        stat = J.check(path, llm=False)
        for kind, prompt in (("N", RS.NEUTRAL % t), ("S", RS.strict_prompt(0, t))):
            jid = "%s_%s" % (kind, f[:3])
            io.open(os.path.join(d, jid + ".prompt.txt"), "w", encoding="utf-8", newline="\n").write(prompt)
            man[jid] = {"kind": kind, "file": f, "stat": stat}
    if baseline:
        # same 20 originals as the claude-opus-5.5 baseline run (review_sample.main: mid chapter of each orig range)
        sample = json.load(io.open(os.path.join(B, "review_sample_opus.json"), encoding="utf-8"))["sample"]
        for new_no, vol, (o0, o1) in sample:
            on = (o0 + o1) // 2
            t = io.open(os.path.join(B, "orig", "ch%03d.txt" % on), encoding="utf-8").read()
            jid = "B_%d" % on
            io.open(os.path.join(d, jid + ".prompt.txt"), "w", encoding="utf-8", newline="\n").write(RS.strict_prompt(on, t))
            man[jid] = {"kind": "B", "file": "orig/ch%03d.txt" % on, "new_no": new_no}
    io.open(os.path.join(d, "manifest.json"), "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1))
    print("prepped %d jobs in %s" % (len(man), d))


def todo(rnd):
    left = []
    for jid in load_manifest(rnd):
        a = answer(rnd, jid)
        if a is None or "_err" in a:
            left.append(jid)
    print("todo %d: %s" % (len(left), " ".join(left)))


def num(v):
    return v if isinstance(v, (int, float)) else None


def collect(rnd):
    man = load_manifest(rnd)
    out = {}
    for jid, m in sorted(man.items()):
        if m["kind"] != "N":
            continue
        f = m["file"]
        r = dict(m["stat"])
        nt = answer(rnd, jid) or {}
        st = answer(rnd, "S_" + f[:3]) or {}
        r["neutral"] = nt.get("total"); r["neutral_dims"] = nt.get("dims"); r["neutral_issues"] = nt.get("issues")
        r["rule"] = st.get("median"); r["rule_issues"] = st.get("issues")
        out[f] = r
    io.open(os.path.join(B, "judge_chapters_cc_%s.json" % rnd), "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, indent=1))

    full = {f: r["neutral_dims"] for f, r in out.items()
            if isinstance(r.get("neutral_dims"), list) and len(r["neutral_dims"]) == 5}
    for f, r in sorted(out.items()):
        print("%s | %d | %.3f | sm=%s | N=%s %s | R=%s" % (
            f[:3], r["chars"], r["dialogue"], r["sm"], r.get("neutral"), r.get("neutral_dims"), r.get("rule")))
    if full:
        dims = [round(sum(v[i] for v in full.values()) / float(len(full)), 1) for i in range(5)]
        ns = [num(out[f].get("neutral")) for f in full]
        ns = [x for x in ns if x is not None]
        print("neutral %d/%d chapters | avg %.1f | dims %s | all dims >80: %d %s" % (
            len(full), len(out), sum(ns) / max(len(ns), 1), dims,
            sum(1 for v in full.values() if min(v) > 80), [f[:3] for f, v in sorted(full.items()) if min(v) > 80]))
    rs = [num(r.get("rule")) for r in out.values()]
    rs = [x for x in rs if x is not None]
    if rs:
        print("rule %d/%d chapters | avg %.2f | min %.1f" % (len(rs), len(out), sum(rs) / len(rs), min(rs)))
    base = {jid: num((answer(rnd, jid) or {}).get("median")) for jid, m in man.items() if m["kind"] == "B"}
    if base:
        got = [v for v in base.values() if v is not None]
        avg = round(sum(got) / len(got), 1) if got else None
        io.open(os.path.join(B, "review_baseline_cc_%s.json" % rnd), "w", encoding="utf-8").write(
            json.dumps({"orig_rule": base, "avg": avg, "opus_api_avg": OPUS_ORIG_RULE}, ensure_ascii=False, indent=1))
        print("baseline orig rule %d/%d | avg %s (claude-opus-5.5 API run: %.1f)" % (len(got), len(base), avg, OPUS_ORIG_RULE))
    missing = [jid for jid in man if (answer(rnd, jid) or {"_err": 1}).get("_err")]
    print("missing/unparsed:", missing)


if __name__ == "__main__":
    cmd, rnd = sys.argv[1], sys.argv[2]
    if cmd == "prep":
        only = set()
        if "--only" in sys.argv:
            only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
        prep(rnd, "--baseline" in sys.argv, only)
    elif cmd == "todo":
        todo(rnd)
    elif cmd == "collect":
        collect(rnd)
