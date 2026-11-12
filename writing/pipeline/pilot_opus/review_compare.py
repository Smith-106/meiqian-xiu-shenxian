# -*- coding: utf-8 -*-
"""试点盲比·模型评审：同一评审模型（muse-spark-1.3，即原稿写手）对原稿/新稿打分。
三组：S=本书铁律五维(rev_whole 原尺)；N=中性文学五维；P=两稿成对盲比(正反两序抵消位置偏差)。
结果写 pilot_opus\\review_compare.json / .txt（UTF-8），不碰正库。"""
import sys, io, os, json, random, time, statistics, urllib.request
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "C:\\Users\\niko\\storymoss_case")
import review_ext as R
import rev_whole as W

BASE = "C:\\Users\\niko\\storymoss_case\\pilot_opus"
PILOT = [256, 257, 300, 450, 631]

def chat(prompt, max_tokens=6000):
    body = json.dumps({"model": "muse-spark-1.3-contributor",
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": max_tokens, "temperature": 0.0,
                       "reasoning_effort": "low", "stream": False}).encode()
    last = None
    for att in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(
                R.URL, data=body, headers={"Content-Type": "application/json",
                                           "Authorization": "Bearer " + R.KEY}), timeout=240)
            d = json.loads(r.read().decode())
            txt = ((d["choices"][0]["message"] or {}).get("content") or "").strip()
            if txt:
                return txt
            last = "EMPTY"
        except Exception as e:
            last = "%s %s" % (type(e).__name__, str(e)[:100])
        time.sleep(8)
    return "FAIL:" + str(last)

NEUTRAL = (u"你是资深中文网络文学编辑，用通用的高水准小说标准（不预设任何本书特有文风）评下面这一章。"
           u"五维各0-100：1可读性与语言质量 2人物与情感张力 3情节推进与信息量 4重复/注水程度（越少越高） 5与上下文连贯可信。"
           u"输出严格JSON：{\"dims\":[d1,d2,d3,d4,d5],\"total\":均值,\"issues\":[每维一句判词]}。只输出JSON。正文：%s")

PAIR = (u"你是资深中文小说编辑。下面是同一章节的两个版本 A 和 B（同一情节位置、同一人物）。"
        u"请从文学质量、人物塑造、情节推进、重复注水、与书中设定一致性五方面比较，"
        u"输出严格JSON：{\"winner\":\"A\"或\"B\"或\"tie\",\"margin\":1-5,\"dims\":{\"文学质量\":\"A/B/tie\",\"人物\":\"A/B/tie\",\"推进\":\"A/B/tie\",\"注水\":\"A/B/tie\",\"一致性\":\"A/B/tie\"},\"reason\":\"一句话\"}。只输出JSON。"
        u"\n【版本A】\n%s\n【版本B】\n%s")

def load(side, n):
    return io.open(os.path.join(BASE, side, "ch%03d.txt" % n), encoding="utf-8").read()

def safe_parse(txt):
    try:
        return R.parse(txt)
    except Exception as e:
        return {"_raw": (txt or "")[:600], "_err": str(e)[:100]}

jobs = []
for n in PILOT:
    o, w = load("orig", n), load("new", n)
    for side, t in (("orig", o), ("new", w)):
        jobs.append(("S", n, side, lambda n=n, t=t: W.call_full_single(n, t)))
        jobs.append(("N", n, side, lambda t=t: chat(NEUTRAL % t)))
    # 成对盲比：正序 A=orig,B=new；反序 A=new,B=orig
    jobs.append(("P", n, "AorigBnew", lambda o=o, w=w: chat(PAIR % (o, w))))
    jobs.append(("P", n, "AnewBorig", lambda o=o, w=w: chat(PAIR % (w, o))))

def run(j):
    kind, n, tag, fn = j
    t0 = time.time()
    txt = fn()
    print("%s ch%d %s %.0fs %s" % (kind, n, tag, time.time() - t0, "FAIL" if txt.startswith("FAIL") else "ok"), flush=True)
    return kind, n, tag, txt

with ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(run, jobs))

out = {"S": {}, "N": {}, "P": {}}
for kind, n, tag, txt in results:
    out[kind].setdefault(str(n), {})[tag] = safe_parse(txt) if not txt.startswith("FAIL") else {"_fail": txt}

def num(d, *keys):
    for k in keys:
        v = d.get(k) if isinstance(d, dict) else None
        if isinstance(v, (int, float)):
            return float(v)
    return None

lines, tally = [], {"orig": 0, "new": 0, "tie": 0}
agg = {"S": {"orig": [], "new": []}, "N": {"orig": [], "new": []}}
for n in PILOT:
    k = str(n)
    s_o, s_n = num(out["S"][k].get("orig", {}), "median"), num(out["S"][k].get("new", {}), "median")
    n_o, n_n = num(out["N"][k].get("orig", {}), "total"), num(out["N"][k].get("new", {}), "total")
    for kind, a, b in (("S", s_o, s_n), ("N", n_o, n_n)):
        if a is not None: agg[kind]["orig"].append(a)
        if b is not None: agg[kind]["new"].append(b)
    p1 = out["P"][k].get("AorigBnew", {}).get("winner")
    p2 = out["P"][k].get("AnewBorig", {}).get("winner")
    m1 = {"A": "orig", "B": "new"}.get(p1, "tie" if p1 == "tie" else None)
    m2 = {"A": "new", "B": "orig"}.get(p2, "tie" if p2 == "tie" else None)
    for m in (m1, m2):
        if m in tally: tally[m] += 1
    lines.append("ch%d 铁律五维 orig=%s new=%s | 中性五维 orig=%s new=%s | 成对 正序胜=%s 反序胜=%s" % (n, s_o, s_n, n_o, n_n, m1, m2))
def avg(v): return round(sum(v) / len(v), 1) if v else None
lines.append("AVG 铁律五维 orig=%s new=%s | 中性五维 orig=%s new=%s | 成对票数 %s" % (
    avg(agg["S"]["orig"]), avg(agg["S"]["new"]), avg(agg["N"]["orig"]), avg(agg["N"]["new"]), tally))
out["summary"] = lines
io.open(os.path.join(BASE, "review_compare.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
io.open(os.path.join(BASE, "review_compare.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
