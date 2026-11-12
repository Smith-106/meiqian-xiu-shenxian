# -*- coding: utf-8 -*-
"""全量重写准备：备份正库，导出原 256-631 正文/标题与续书大纲，统计字数与对白占比。只读正库。"""
import sqlite3, os, io, json, datetime, re
SRC = r'C:\Users\niko\AppData\Roaming\com.storymoss.app\cinema_ai.db'
CASE = r'C:\Users\niko\storymoss_case'
BASE = os.path.join(CASE, 'full_rewrite')
os.makedirs(os.path.join(BASE, 'orig'), exist_ok=True)
os.makedirs(os.path.join(BASE, 'draft'), exist_ok=True)
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
bak = os.path.join(CASE, 'backup_cinema_ai_%s_before_full_rewrite.db' % stamp)
src = sqlite3.connect(SRC)
dst = sqlite3.connect(bak)
src.backup(dst)
dst.close()
sid = io.open(os.path.join(CASE, 'story_id.txt'), encoding='utf-8').read().strip()
rows = src.execute('SELECT sequence_number, title, content, chapter_id FROM scenes WHERE story_id=? AND sequence_number>=255 ORDER BY sequence_number', (sid,)).fetchall()
Q = re.compile(u'[\u201c\"]([^\u201d\"]*)[\u201d\"]')
idx = []
for seq, title, content, chap in rows:
    t = content or ''
    io.open(os.path.join(BASE, 'orig', 'ch%03d.txt' % seq), 'w', encoding='utf-8').write(t)
    dl = sum(len(x) for x in Q.findall(t))
    idx.append({'seq': seq, 'title': title, 'chars': len(t), 'dialogue': round(dl / max(len(t), 1), 3), 'chapter_id': chap})
outs = src.execute("SELECT content FROM story_summaries WHERE story_id=? AND summary_type='outline_continuation'", (sid,)).fetchone()
io.open(os.path.join(BASE, 'outline_continuation.txt'), 'w', encoding='utf-8').write(outs[0] if outs else 'MISSING')
chap_cnt = src.execute('SELECT COUNT(*) FROM scenes WHERE story_id=?', (sid,)).fetchone()[0]
src.close()
json.dump({'backup': bak, 'total_scenes': chap_cnt, 'exported': len(idx), 'index': idx}, io.open(os.path.join(BASE, 'orig_index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
lines = ['%d\t%s\t%d\t%.3f' % (r['seq'], r['title'], r['chars'], r['dialogue']) for r in idx]
io.open(os.path.join(BASE, 'orig_index.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
tot = sum(r['chars'] for r in idx if r['seq'] >= 256)
print('backup', bak, os.path.getsize(bak))
print('total_scenes', chap_cnt, 'exported', len(idx), 'chars_256_631', tot)
