# -*- coding: utf-8 -*-
"""Write full_rewrite\\chapters\\NNN_标题.txt back into StoryMoss (scenes + chapters, seq 256..N).

Usage:
  python writeback.py --db <path> [--commit]
Without --commit the whole transaction is rolled back after verification (dry run).
Steps (single transaction):
  1. scenes seq 256..N: title / content / draft_content / updated_at; delete seq N+1..old last.
  2. chapters 256..N: title / word_count / updated_at; delete N+1..old last.
  3. chain: 255 <-> 256 <-> ... <-> N, last next = NULL.
  4. story_metadata chapter_count / last_chapter / total_words.
Then: integrity_check, foreign_key_check, contiguity, non-empty, chain, file==DB.
"""
import sys, io, os, re, json, sqlite3, datetime

STORY = "0fd0b287-a134-4a8c-9874-a1b0b98880a4"
CH = r"C:\Users\niko\storymoss_case\full_rewrite\chapters"
FIRST, MAX_SEQ = 256, 100000


def load_chapters():
    out = []
    for f in sorted(os.listdir(CH)):
        m = re.match(u"^(\\d{3})_(.+)\\.txt$", f)
        if not m:
            continue
        n, title = int(m.group(1)), m.group(2)
        body = io.open(os.path.join(CH, f), encoding="utf-8").read().strip() + "\n"
        out.append((n, title, body))
    nums = [x[0] for x in out]
    assert nums == list(range(FIRST, FIRST + len(out))), "chapter files not contiguous from 256"
    assert all(len(b.strip()) > 1000 for _, _, b in out), "empty/short chapter body"
    return out


def run(db, commit):
    chs = load_chapters()
    last = chs[-1][0]
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    con = sqlite3.connect(db, isolation_level=None)
    con.execute("PRAGMA foreign_keys=OFF")
    cur = con.cursor()
    fk_before = set(tuple(r) for r in con.execute("PRAGMA foreign_key_check").fetchall())
    cur.execute("BEGIN IMMEDIATE")
    try:
        sc = {r[1]: r[0] for r in cur.execute(
            "select id, sequence_number from scenes where story_id=? and sequence_number between ? and ?",
            (STORY, FIRST, MAX_SEQ))}
        cp = {r[1]: r[0] for r in cur.execute(
            "select id, chapter_number from chapters where story_id=? and chapter_number between ? and ?",
            (STORY, FIRST, MAX_SEQ))}
        OLD_LAST = max(sc)
        assert sorted(sc) == list(range(FIRST, OLD_LAST + 1)), "unexpected scene seq set"
        assert sorted(cp) == list(range(FIRST, OLD_LAST + 1)), "unexpected chapter number set"
        assert last <= OLD_LAST, "new chapter count exceeds existing rows; insert path not implemented"
        s255 = cur.execute("select id from scenes where story_id=? and sequence_number=255", (STORY,)).fetchone()[0]

        for n, title, body in chs:
            full = u"第%d章 %s" % (n, title)
            cur.execute("update scenes set title=?, content=?, draft_content=?, updated_at=? where id=?",
                        (full, body, body, now, sc[n]))
            cur.execute("update chapters set title=?, word_count=?, updated_at=? where id=?",
                        (full, len(body), now, cp[n]))
        dels = [sc[n] for n in range(last + 1, OLD_LAST + 1)]
        cdels = [cp[n] for n in range(last + 1, OLD_LAST + 1)]
        cur.executemany("delete from scenes where id=?", [(x,) for x in dels])
        cur.executemany("delete from chapters where id=?", [(x,) for x in cdels])

        order = [s255] + [sc[n] for n in range(FIRST, last + 1)]
        for i, sid in enumerate(order):
            prev = order[i - 1] if i > 0 else None
            nxt = order[i + 1] if i + 1 < len(order) else None
            if i == 0:
                cur.execute("update scenes set next_scene_id=? where id=?", (nxt, sid))
            else:
                cur.execute("update scenes set previous_scene_id=?, next_scene_id=? where id=?", (prev, nxt, sid))

        total = cur.execute("select coalesce(sum(length(content)),0) from scenes where story_id=?", (STORY,)).fetchone()[0]
        for k, v in (("chapter_count", str(last)), ("last_chapter", str(last)), ("total_words", str(total))):
            cur.execute("update story_metadata set value=?, updated_at=? where story_id=? and key=?", (v, now, STORY, k))

        # ---- verification inside the transaction ----
        rep = {}
        seqs = [r[0] for r in cur.execute("select sequence_number from scenes where story_id=? order by sequence_number", (STORY,))]
        rep["scene_seq_contiguous"] = seqs == list(range(1, last + 1))
        cn = [r[0] for r in cur.execute("select chapter_number from chapters where story_id=? order by chapter_number", (STORY,))]
        rep["chapter_num_contiguous"] = cn == list(range(1, last + 1))
        rep["empty_content"] = cur.execute(
            "select count(*) from scenes where story_id=? and (content is null or length(trim(content))=0)", (STORY,)).fetchone()[0]
        rows = {r[0]: r[1:] for r in cur.execute(
            "select id, sequence_number, previous_scene_id, next_scene_id from scenes where story_id=?", (STORY,))}
        byseq = {v[0]: k for k, v in rows.items()}
        bad = 0
        for s in range(1, last + 1):
            sid = byseq[s]
            _, pv, nx = rows[sid]
            if s > 1 and pv != byseq[s - 1]:
                bad += 1
            if s < last and nx != byseq[s + 1]:
                bad += 1
            if s == last and nx is not None:
                bad += 1
        rep["chain_errors"] = bad
        mism = 0
        for n, title, body in chs:
            r = cur.execute("select title, content from scenes where story_id=? and sequence_number=?", (STORY, n)).fetchone()
            if r[0] != u"第%d章 %s" % (n, title) or r[1] != body:
                mism += 1
        rep["file_db_mismatch"] = mism
        fk_after = set(tuple(r) for r in cur.execute("PRAGMA foreign_key_check").fetchall())
        rep["fk_preexisting"] = len(fk_before)
        rep["fk_check"] = sorted(fk_after - fk_before)[:5]  # only violations introduced by this write
        rep["integrity"] = cur.execute("PRAGMA integrity_check").fetchone()[0]
        rep["last"] = last
        rep["deleted_scenes"] = len(dels)
        rep["total_words"] = total
        ok = (rep["scene_seq_contiguous"] and rep["chapter_num_contiguous"] and rep["empty_content"] == 0
              and bad == 0 and mism == 0 and not rep["fk_check"] and rep["integrity"] == "ok")
        rep["ok"] = ok
        if commit and ok:
            cur.execute("COMMIT")
            rep["committed"] = True
        else:
            cur.execute("ROLLBACK")
            rep["committed"] = False
        return rep
    except Exception:
        cur.execute("ROLLBACK")
        raise
    finally:
        con.close()


if __name__ == "__main__":
    a = sys.argv[1:]
    db = a[a.index("--db") + 1]
    print(json.dumps(run(db, "--commit" in a), ensure_ascii=False, indent=1))
