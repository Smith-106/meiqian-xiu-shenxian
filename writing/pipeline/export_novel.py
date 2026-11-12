import sqlite3, os, re
from docx import Document
from docx.shared import Pt

BASE = r'C:\Users\niko\storymoss_case'
OUT = os.path.join(BASE, 'export')
os.makedirs(OUT, exist_ok=True)

con = sqlite3.connect(r'C:\Users\niko\AppData\Roaming\com.storymoss.app\cinema_ai.db')
cur = con.cursor()
sid = open(os.path.join(BASE, 'story_id.txt'), encoding='utf-8').read().strip()
cur.execute("SELECT sequence_number, title, content FROM scenes WHERE story_id=? ORDER BY sequence_number", (sid,))
rows = cur.fetchall()
assert len(rows) == 631, len(rows)

title = '你没钱修什么仙'

VOLUMES = [
    (1, 270, '第一卷 借调归位'),
    (271, 310, '第二卷 堂期归库'),
    (311, 350, '第三卷 启晓合卷'),
    (351, 390, '第四卷 开晓落锁'),
    (391, 430, '第五卷 开栈合梓'),
    (431, 470, '第六卷 开缝合匣'),
    (471, 510, '第七卷 贴缝归雾'),
    (511, 550, '第八卷 守定迎晨'),
    (551, 590, '第九卷 核牌出栈'),
    (591, 630, '第十卷 影定合卷'),
    (631, 631, '第十一卷 廿二落墨'),
]
VOL_START = {s: (name, s, e) for s, e, name in VOLUMES}

def heading(seq, t):
    t = (t or '').strip()
    if re.match(r'^第\s*\d+\s*章', t):
        return t
    return '第 %d 章 %s' % (seq, t)

# 1) TXT
txt_path = os.path.join(OUT, title + '.txt')
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write(title + '\n\n')
    for seq, t, content in rows:
        if seq in VOL_START:
            name, s, e = VOL_START[seq]
            f.write('%s（第%d章—第%d章）\n\n' % (name, s, e))
        f.write(heading(seq, t) + '\n\n')
        f.write((content or '').strip() + '\n\n')

# 2) DOCX
doc = Document()
st = doc.styles['Normal']
st.font.size = Pt(12)
st.font.name = 'SimSun'
doc.add_heading(title, level=0)
for seq, t, content in rows:
    if seq in VOL_START:
        name, s, e = VOL_START[seq]
        doc.add_page_break()
        doc.add_heading(name, level=0)
        doc.add_paragraph('第%d章—第%d章' % (s, e))
    doc.add_heading(heading(seq, t), level=1)
    for para in (content or '').strip().split('\n'):
        para = para.strip()
        if para:
            doc.add_paragraph(para)
docx_path = os.path.join(OUT, title + '.docx')
doc.save(docx_path)

print('chapters:', len(rows))
print('txt MB:', round(os.path.getsize(txt_path) / 1e6, 2))
print('docx MB:', round(os.path.getsize(docx_path) / 1e6, 2))
