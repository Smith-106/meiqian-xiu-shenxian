# -*- coding: utf-8 -*-
"""全量重写抽样复测：每卷 2 章（卷十一并入末章），跑 本书铁律五维(S)、中性文学五维(N)、成对盲比(P，正反两序)。
新章对照原稿取其对应原章区间的中位章。评审器与试点 pilot_opus\\review_compare.py 相同。只读，不碰正库。
输出 full_rewrite\\review_sample.json / .txt。"""
import sys, io, os, json, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"C:\Users\niko\storymoss_case")
sys.path.insert(0, r"C:\Users\niko\storymoss_case\pilot_opus")
import review_ext as R
import rev_whole as W

B = r"C:\Users\niko\storymoss_case\full_rewrite"
PILOT = r"C:\Users\niko\storymoss_case\pilot_opus"
# 原评审 muse-spark-1.3-contributor 已下线（HTTP 400 model_not_found）；改用非写手模型，并在同一次运行里复测试点基线。
# gpt-oss-120b-medium 于 2026-10-29 晚亦下线（model_not_found）；可用 DSH_JUDGE 环境变量指定替代评审，换评审须同次复测试点基线。
JUDGE = os.environ.get("DSH_JUDGE", "gpt-oss-120b-medium")
CM = json.load(io.open(os.path.join(B, "chapter_map.json"), encoding="utf-8"))["chapters"]


def pick():
    byvol = {}
    for c in CM:
        byvol.setdefault(c["volume"], []).append(c)
    out = []
    for vol, cs in byvol.items():
        if len(cs) <= 2:
            out += cs
        else:
            out += [cs[len(cs) // 3], cs[(2 * len(cs)) // 3]]
    last = CM[-1]
    if last not in out:
        out.append(last)
    return out


def chat(prompt, max_tokens=6000):
    body = json.dumps({"model": JUDGE,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": max_tokens, "temperature": 0.0,
                       "stream": False}).encode()
    import urllib.request
    last = None
    for att in range(int(os.environ.get("DSH_JUDGE_RETRIES", "3"))):
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
        time.sleep(20 if "429" not in str(last) else 45)
    return "FAIL:" + str(last)


STRICT = None  # filled in main(): book-rule prompt from rev_whole, sent to JUDGE


def strict_prompt(n, text):
    import rev5
    return (u"你是《渡劫外包·续》复审员。" + rev5.STYLE5 + u"读下面第%d章【全文】正文，按五维打分：" % n
            + u"1文风贴合度2逻辑自洽3对白自然度4剧情节奏5角色一致性。"
            + u"（不评画面感：公文体以器物手续承载情绪，画面感免考。）"
            + u"每维0-100百分制，先逐维打出五个分数，再算总分=五维均值（保留一位小数）。"
            + u"输出严格JSON，格式：{\"ch\":%d,\"dims\":[d1,d2,d3,d4,d5],\"scores\":[a,b],\"median\":m,\"crit\":0,\"issues\":[]}" % n
            + u"。scores为两位评审独立总分（五维均值），median取中位数，crit只计high。"
            + u"issues必填五条，每维一条，写明维度和一句话判词。只输出JSON。全文正文：%s" % text)


def strict(n, text):
    return chat(strict_prompt(n, text), 8000)


NEUTRAL = (u"你是资深中文网络文学编辑，用通用的高水准小说标准（不预设任何本书特有文风）评下面这一章。"
           u"五维各0-100：1可读性与语言质量 2人物与情感张力 3情节推进与信息量 4重复/注水程度（越少越高） 5与上下文连贯可信。"
           u"输出严格JSON：{\"dims\":[d1,d2,d3,d4,d5],\"total\":均值,\"issues\":[每维一句判词]}。只输出JSON。正文：%s")
PAIR = (u"你是资深中文小说编辑。下面是同一章节的两个版本 A 和 B（同一情节位置、同一人物）。"
        u"请从文学质量、人物塑造、情节推进、重复注水、与书中设定一致性五方面比较，"
        u"输出严格JSON：{\"winner\":\"A\"或\"B\"或\"tie\",\"margin\":1-5,\"dims\":{\"文学质量\":\"A/B/tie\",\"人物\":\"A/B/tie\",\"推进\":\"A/B/tie\",\"注水\":\"A/B/tie\",\"一致性\":\"A/B/tie\"},\"reason\":\"一句话\"}。只输出JSON。"
        u"\n【版本A】\n%s\n【版本B】\n%s")


def safe_parse(txt):
    try:
        return R.parse(txt)
    except Exception as e:
        return {"_raw": (txt or "")[:600], "_err": str(e)[:100]}


def num(d, *keys):
    for k in keys:
        v = d.get(k) if isinstance(d, dict) else None
        if isinstance(v, (int, float)):
            return float(v)
    return None


def main():
    sample = pick()
    jobs = []
    for c in sample:
        new = io.open(os.path.join(B, "chapters", c["file"]), encoding="utf-8").read()
        o0, o1 = c["orig_range"]
        on = (o0 + o1) // 2
        orig = io.open(os.path.join(B, "orig", "ch%03d.txt" % on), encoding="utf-8").read()
        k = str(c["new_no"])
        jobs.append(("S", k, "new", lambda n=c["new_no"], t=new: strict(n, t)))
        jobs.append(("S", k, "orig", lambda n=on, t=orig: strict(n, t)))
        jobs.append(("N", k, "new", lambda t=new: chat(NEUTRAL % t)))
        jobs.append(("N", k, "orig", lambda t=orig: chat(NEUTRAL % t)))
        jobs.append(("P", k, "AorigBnew", lambda o=orig, w=new: chat(PAIR % (o, w))))
        jobs.append(("P", k, "AnewBorig", lambda o=orig, w=new: chat(PAIR % (w, o))))

    for n in (256, 257, 300, 450, 631):  # pilot v2 calibration under the same judge
        for side in ("orig", "new"):
            t = io.open(os.path.join(PILOT, side, "ch%03d.txt" % n), encoding="utf-8").read()
            jobs.append(("CS", str(n), side, lambda n=n, t=t: strict(n, t)))
            jobs.append(("CN", str(n), side, lambda t=t: chat(NEUTRAL % t)))

    def run(j):
        kind, k, tag, fn = j
        t0 = time.time()
        txt = fn()
        print("%s new%s %s %.0fs %s" % (kind, k, tag, time.time() - t0, "FAIL" if txt.startswith("FAIL") else "ok"), flush=True)
        return kind, k, tag, txt

    with ThreadPoolExecutor(max_workers=3) as ex:
        results = list(ex.map(run, jobs))
    out = {"judge": JUDGE, "S": {}, "N": {}, "P": {}, "CS": {}, "CN": {}, "sample": [(c["new_no"], c["volume"], c["orig_range"]) for c in sample]}
    for kind, k, tag, txt in results:
        out[kind].setdefault(k, {})[tag] = safe_parse(txt) if not txt.startswith("FAIL") else {"_fail": txt}

    lines, tally = [], {"orig": 0, "new": 0, "tie": 0}
    agg = {"S": {"orig": [], "new": []}, "N": {"orig": [], "new": []}}
    byvol = {}
    for c in sample:
        k = str(c["new_no"])
        s_o, s_n = num(out["S"][k].get("orig", {}), "median"), num(out["S"][k].get("new", {}), "median")
        n_o, n_n = num(out["N"][k].get("orig", {}), "total"), num(out["N"][k].get("new", {}), "total")
        for kind, a, b in (("S", s_o, s_n), ("N", n_o, n_n)):
            if a is not None: agg[kind]["orig"].append(a)
            if b is not None: agg[kind]["new"].append(b)
        byvol.setdefault(c["volume"], []).append((s_n, n_n))
        p1 = out["P"][k].get("AorigBnew", {}).get("winner")
        p2 = out["P"][k].get("AnewBorig", {}).get("winner")
        m1 = {"A": "orig", "B": "new"}.get(p1, "tie" if p1 == "tie" else None)
        m2 = {"A": "new", "B": "orig"}.get(p2, "tie" if p2 == "tie" else None)
        for m in (m1, m2):
            if m in tally: tally[m] += 1
        lines.append(u"new%s(%s 原%d-%d) 铁律五维 orig=%s new=%s | 中性五维 orig=%s new=%s | 成对 正序=%s 反序=%s" % (
            k, c["volume"], c["orig_range"][0], c["orig_range"][1], s_o, s_n, n_o, n_n, m1, m2))

    def avg(v):
        v = [x for x in v if x is not None]
        return round(sum(v) / len(v), 1) if v else None
    lines.append(u"AVG 铁律五维 orig=%s new=%s | 中性五维 orig=%s new=%s | 成对票数 %s" % (
        avg(agg["S"]["orig"]), avg(agg["S"]["new"]), avg(agg["N"]["orig"]), avg(agg["N"]["new"]), tally))
    cal = {"S": {"orig": [], "new": []}, "N": {"orig": [], "new": []}}
    for n in ("256", "257", "300", "450", "631"):
        for side in ("orig", "new"):
            cal["S"][side].append(num(out["CS"].get(n, {}).get(side, {}), "median"))
            cal["N"][side].append(num(out["CN"].get(n, {}).get(side, {}), "total"))
    lines.append(u"PILOT(同评审复测) 铁律五维 orig=%s v2=%s | 中性五维 orig=%s v2=%s" % (
        avg(cal["S"]["orig"]), avg(cal["S"]["new"]), avg(cal["N"]["orig"]), avg(cal["N"]["new"])))
    for vol, v in byvol.items():
        lines.append(u"VOL %s 铁律=%s 中性=%s" % (vol, avg([a for a, b in v]), avg([b for a, b in v])))
    out["summary"] = lines
    io.open(os.path.join(B, "review_sample.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
    io.open(os.path.join(B, "review_sample.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
