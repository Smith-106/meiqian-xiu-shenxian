# -*- coding: utf-8 -*-
r"""从 StoryMoss 正库导出叙事元数据快照。

用法：
    python export_snapshot.py                    # 默认读 %APPDATA%\com.storymoss.app\cinema_ai.db
    python export_snapshot.py --db 路径          # 指定数据库
    python export_snapshot.py --out data         # 指定输出目录

输出：
    data/storymoss_snapshot.json   23 张叙事表的完整内容（不含 scenes 正文）
    data/schema.sql                建表语句（可直接重建空库）

正文不写入快照：`scenes.content` 已按章拆在 manuscript/，由 restore_db.py 合并。
"""
import sys
import io
import os
import json
import sqlite3

TABLES = [
    "stories",
    "story_chapter_sequences",
    "story_metadata",
    "story_outlines",
    "story_summaries",
    "story_segment_summaries",
    "story_style_configs",
    "chapters",
    "characters",
    "narrative_characters",
    "reference_characters",
    "character_relationships",
    "character_states",
    "world_rules",
    "world_buildings",
    "foreshadowing_tracker",
    "story_timeline_events",
    "chapter_reading_power",
    "chase_debt",
    "asset_nodes",
    "asset_asset_edges",
    "intention_nodes",
    "intention_asset_edges",
    "export_templates",
    "schema_migrations",
]

# scenes 只存元数据，正文另存
SCENE_COLS_SKIP = {"content"}

DEFAULT_DB = os.path.join(os.environ.get("APPDATA", ""), "com.storymoss.app", "cinema_ai.db")


def open_ro(path):
    uri = "file:%s?mode=ro" % path.replace("\\", "/")
    con = sqlite3.connect(uri, uri=True)
    con.row_factory = sqlite3.Row
    return con


def dump(db_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    con = open_ro(db_path)
    cur = con.cursor()

    snap = {}
    for t in TABLES:
        try:
            rows = [dict(r) for r in cur.execute(u'select * from "%s"' % t)]
        except sqlite3.Error as e:
            print(u"  跳过 %-26s %s" % (t, e))
            continue
        snap[t] = rows
        print(u"  %-26s %5d 行" % (t, len(rows)))

    # scenes：除正文外的全部列
    cols = [r[1] for r in cur.execute("pragma table_info(scenes)")]
    keep = [c for c in cols if c not in SCENE_COLS_SKIP]
    sel = ",".join('"%s"' % c for c in keep)
    scenes = [dict(r) for r in cur.execute(u"select %s from scenes order by sequence_number" % sel)]
    snap["scenes_meta"] = scenes
    print(u"  %-26s %5d 行（不含正文）" % ("scenes_meta", len(scenes)))

    snap["_meta"] = {
        "source_db": os.path.basename(db_path),
        "scene_columns": keep,
        "tables": {k: len(v) for k, v in snap.items() if isinstance(v, list)},
    }

    jp = os.path.join(out_dir, "storymoss_snapshot.json")
    with io.open(jp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(snap, f, ensure_ascii=False, indent=1, default=str)
    print(u"\n快照 %s  %.2f MB" % (jp, os.path.getsize(jp) / 1048576.0))

    sql = [r[0] for r in cur.execute(
        "select sql from sqlite_master where sql is not null and name not like 'sqlite_%' "
        "order by case type when 'table' then 0 when 'index' then 1 else 2 end, name")]
    sp = os.path.join(out_dir, "schema.sql")
    with io.open(sp, "w", encoding="utf-8", newline="\n") as f:
        f.write(u";\n\n".join(sql) + u";\n")
    print(u"建表语句 %s  %.1f KB（%d 条）" % (sp, os.path.getsize(sp) / 1024.0, len(sql)))
    con.close()


def main(argv):
    db = DEFAULT_DB
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    i = 1
    while i < len(argv):
        if argv[i] == "--db" and i + 1 < len(argv):
            db = argv[i + 1]
            i += 2
        elif argv[i] == "--out" and i + 1 < len(argv):
            out = argv[i + 1]
            i += 2
        else:
            i += 1
    if not os.path.exists(db):
        print(u"找不到数据库：%s" % db)
        return 2
    print(u"源库 %s（%.1f MB）" % (db, os.path.getsize(db) / 1048576.0))
    dump(db, out)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main(sys.argv))
