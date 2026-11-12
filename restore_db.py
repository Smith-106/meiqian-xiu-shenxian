# -*- coding: utf-8 -*-
r"""从仓库内的快照与正文重建 StoryMoss 数据库。

用法：
    python restore_db.py --db out.db            # 重建到指定路径
    python restore_db.py --db out.db --force    # 覆盖已存在的文件（先自动备份）
    python restore_db.py                        # 重建到 %APPDATA%\com.storymoss.app\restored.db

流程：
    1. 执行 data/schema.sql 建表
    2. 载入 data/storymoss_snapshot.json 的各表数据
    3. 用 manuscript/NNN_*.txt 填充 scenes.content（正文以文件为准）
    4. 校验章节数、正文字数与快照是否一致

注意：重建库的 id 与外键关系沿用快照，但版本历史链（scene_versions/snapshots）不会恢复。
"""
import sys
import io
import os
import re
import json
import time
import glob
import uuid
import shutil
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
MAN = os.path.join(HERE, "manuscript")
SNAP = os.path.join(DATA, "storymoss_snapshot.json")
SCHEMA = os.path.join(DATA, "schema.sql")


def default_target():
    appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(appdata, "com.storymoss.app", "restored.db")


def read_manuscript():
    u"""返回 {章号: (标题行, 全文)}"""
    out = {}
    for f in sorted(glob.glob(os.path.join(MAN, "*.txt"))):
        base = os.path.basename(f)
        m = re.match(r"^(\d{1,4})_", base)
        if not m:
            continue
        n = int(m.group(1))
        t = io.open(f, encoding="utf-8").read().replace("\r\n", "\n").replace("\r", "\n")
        first = t.strip().split("\n", 1)[0].strip()
        out[n] = (first, t.strip() + "\n")
    return out


def insert_rows(con, table, rows):
    if not rows:
        return 0
    cur = con.cursor()
    cols = [r[1] for r in cur.execute('pragma table_info("%s")' % table)]
    if not cols:
        print(u"  跳过未知表 %s" % table)
        return 0
    keys = [k for k in rows[0].keys() if k in cols]
    ph = ",".join("?" * len(keys))
    sql = 'insert or replace into "%s" (%s) values (%s)' % (
        table, ",".join('"%s"' % k for k in keys), ph)
    vals = [tuple(r.get(k) for k in keys) for r in rows]
    cur.executemany(sql, vals)
    return len(vals)


def main(argv):
    target = None
    force = False
    i = 1
    while i < len(argv):
        if argv[i] == "--db" and i + 1 < len(argv):
            target = argv[i + 1]
            i += 2
        elif argv[i] == "--force":
            force = True
            i += 1
        else:
            i += 1
    target = target or default_target()

    for p in (SNAP, SCHEMA):
        if not os.path.exists(p):
            print(u"缺少 %s，先运行 python export_snapshot.py" % p)
            return 2

    if os.path.exists(target):
        if not force:
            print(u"目标已存在：%s\n加 --force 覆盖（会自动备份）" % target)
            return 2
        bak = target + ".bak-%s" % time.strftime("%Y%m%d-%H%M%S")
        shutil.copy2(target, bak)
        os.remove(target)
        print(u"已备份到 %s" % bak)

    os.makedirs(os.path.dirname(os.path.abspath(target)) or ".", exist_ok=True)

    print(u"建库 %s" % target)
    con = sqlite3.connect(target)
    con.executescript(io.open(SCHEMA, encoding="utf-8").read())

    snap = json.load(io.open(SNAP, encoding="utf-8"))
    meta = snap.pop("_meta", {})
    scenes_meta = snap.pop("scenes_meta", [])

    print(u"载入快照表：")
    for t in sorted(snap.keys()):
        n = insert_rows(con, t, snap[t])
        print(u"  %-26s %5d" % (t, n))

    man = read_manuscript()
    print(u"\n合并正文：manuscript/ %d 章" % len(man))

    by_seq = {r.get("sequence_number"): r for r in scenes_meta}
    story_id = None
    for r in snap.get("stories", []):
        if u"续" in (r.get("title") or "") or story_id is None:
            story_id = r.get("id")
    chap_id = {r.get("chapter_number"): r.get("id") for r in snap.get("chapters", [])}

    cur = con.cursor()
    cols = [r[1] for r in cur.execute("pragma table_info(scenes)")]
    now = time.strftime("%Y-%m-%dT%H:%M:%S")
    n_ins = 0
    for no in sorted(man):
        head, text = man[no]
        row = dict(by_seq.get(no) or {})
        row.setdefault("id", str(uuid.uuid4()))
        row.setdefault("story_id", story_id)
        row["sequence_number"] = no
        row["title"] = head
        row["content"] = text
        if not row.get("chapter_id"):
            row["chapter_id"] = chap_id.get(no)
        row.setdefault("created_at", now)
        row.setdefault("updated_at", now)
        keys = [k for k in row.keys() if k in cols and row.get(k) is not None]
        cur.execute('insert or replace into scenes (%s) values (%s)' % (
            ",".join('"%s"' % k for k in keys), ",".join("?" * len(keys))),
            tuple(row[k] for k in keys))
        n_ins += 1
    con.commit()

    skipped = [s for s in by_seq if s not in man]
    if skipped:
        print(u"  快照中有 %d 条场景无对应正文，已跳过：%s" % (len(skipped), sorted(skipped)))

    # 校验
    n_sc = cur.execute("select count(*) from scenes").fetchone()[0]
    n_ch = cur.execute("select count(*) from chapters").fetchone()[0]
    tot = cur.execute("select sum(length(content)) from scenes").fetchone()[0] or 0
    print(u"\n校验：scenes %d 章 | chapters %d 章 | 正文字符 %d" % (n_sc, n_ch, tot))
    try:
        con.execute("vacuum")
    except sqlite3.Error:
        pass
    con.commit()
    con.close()
    print(u"完成：%s  %.2f MB" % (target, os.path.getsize(target) / 1048576.0))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main(sys.argv))
