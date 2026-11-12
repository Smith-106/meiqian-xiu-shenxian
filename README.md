# 你没钱修什么仙

> 修真 · 官署 · 公文冷硬体长篇小说（私人存档）

一个借调小吏在梓库、泊台、对销堂之间，用册、栏、押、版和规程处理"渡劫外包"的故事。

---

## 两个版本

| 目录 | 章数 | 字数 | 说明 |
|---|---:|---:|---|
| `manuscript/` | **297** | 889,274 | 新版（当前版本）。第 256 章起由原书压缩重写 |
| `novel/` | 631 | 1,981,372 | 原版完整稿（2026-10-28） |

新版把原书第 258–631 章（374 章 / 1,207,967 字）压缩成 42 章（121,827 字），
压缩比约 **9.9 : 1**。压缩的是重复的仪式流程，推进性事件按 `spec.md` 保留。

`manuscript/` 的来源：

- 第 1–255 章 ← 写作库 `scenes` 表（成文于 2026-10-18）
- 第 256–297 章 ← `writing/chapters_v3/`（2026-10-30 之后的返修稿）

标题行已统一为「第N章 标题」；第 2 章原缺标题行，按元数据补为「第2章 互撕」。

---

## 目录

```
README.md
SETUP.md                    新机器环境搭建（写作+质检 / 连 StoryMoss 一起）
LICENSE
.gitignore
gate_report.py              全书质量门体检（任意目录）
export_snapshot.py          从正库导出叙事元数据快照
restore_db.py               从快照 + 正文重建 StoryMoss 数据库
manuscript/                 新版 297 章，一章一文件
novel/                      原版 631 章（txt + docx + 封面）
data/
├─ storymoss_snapshot.json  叙事元数据（人物 83、伏笔 36、时间线 255……）
└─ schema.sql               建表语句 374 条
writing/
├─ spec.md                  重写写作规约
├─ PROGRESS.md              逐轮进度台账
├─ plan_v3.md               v3 逐章台账（每章已定事实）
├─ HANDOFF.md               交接文件
├─ judge_rounds.md          八轮评审数据汇总
├─ chapter_map.json         42 章字数/对白/评分索引
├─ build_v3.py              42 章门禁 + 发布
├─ sm_quality.py            文风质检（重建版，见下）
├─ judge.py                 单章评审
├─ judge_chapters.py        全量评审
├─ judge_fill.py            缺失章节补齐
├─ review_sample.py         评审 prompt 与调用
├─ review_ext.example.py    密钥占位模板
├─ chapters_v3/             42 章源文件（256–297）
└─ pipeline/                原始流水线脚本与中间产物（见其 README）
.github/workflows/gate.yml  推送后自动跑质量门
```

---

## 质量门

四种检查，标准一致：

| 项目 | 标准 |
|---|---|
| 字数 | 2,800 – 3,300（非空白字符） |
| 对白占比 | 0.20 – 0.30（中文双引号内字数 / 全章字数） |
| sm_quality | ≥ 95 |
| 标题行 | 「第N章 标题」，N 与文件名前三位一致 |

### 当前状态

- `writing/chapters_v3/` 42 章：**42/42 全部通过**
- `manuscript/` 297 章：**57/297 通过**
  - 不达标项：对白 216 章、字数 191 章
  - 第 1–255 章成文早于标准制定，问题是"话太少、篇幅不齐"，非文笔问题

### 评审（另一套标准）

离线门禁之外还有 LLM 评审，中性五维（可读性 / 人物 / 推进 / 重复 / 连贯）每项需 > 80。
八轮全量评审均分 80.2–80.8，未达标。详见 `writing/judge_rounds.md`。

原稿对照：原稿中性五维 16.4，新稿 66.8，成对盲比 30 胜 0 负。

---

## 在别的机器上继续

完整步骤见 [SETUP.md](SETUP.md)。零依赖，只需 Python 3.8+（全部标准库）。

```bash
git clone https://github.com/Smith-106/meiqian-xiu-shenxian
cd meiqian-xiu-shenxian

# 全书体检
python gate_report.py manuscript

# 42 章重写稿门禁
cd writing && python build_v3.py

# 改稿后在仓库根目录
python gate_report.py manuscript --md gate_report.md
git commit -am "改 256 章对白"
git push
```

推送后 GitHub Actions 会自动跑一遍，结果写在 Actions 页面的 Summary 里。
`manuscript/` 或 `writing/chapters_v3/` 有变动才会触发。

### 局部检查单章

```bash
python gate_report.py manuscript --md out.md | grep "^256"
```

### 重建 StoryMoss 数据库

```bash
python restore_db.py --db "%APPDATA%\com.storymoss.app\cinema_ai.db" --force
```

会用 `data/storymoss_snapshot.json` + `manuscript/` 重建出一个含 297 章正文、
83 个人物、29 条关系、36 条伏笔、255 条时间线的数据库。原库自动备份。

元数据有变动时重新导出：

```bash
python export_snapshot.py
```

### 评审（需要 API Key）

`judge.py` / `judge_chapters.py` 依赖 `review_ext.py` 提供接口地址与密钥，
该文件不入库。使用时：

```bash
cp writing/review_ext.example.py writing/review_ext.py
# 编辑，填入自己的 KEY 与 URL
```

---

## 关于 sm_quality.py

原文件曾置于系统临时目录，被清理后丢失。仓库中的版本是**按调用契约重建**的：
硬指标（字数、对白、均句、均段、感叹、禁词）精确复现，
原版 `SEVERE/MILD` 词表因原文件不可考未能复原，仅保留字段名。

## 关于 review_ext.example.py

`review_sample.py` 依赖同目录的 `review_ext.py` 提供接口地址与密钥。
该文件含真实 API Key，**未纳入本仓库**，仅提供占位模板。

---

## 版权

© 2026 Smith-106. 保留所有权利。

未经许可，不得复制、转载、分发或用于商业用途。详见 `LICENSE`。
