# 在新机器上搭起这套环境

两种搭法，按需要选：

| 目标 | 需要什么 | 耗时 |
|---|---|---|
| **A. 写作 + 质量门** | Python 3.8+ | 5 分钟 |
| **B. 连 StoryMoss 一起复刻** | Python + StoryMoss 应用 | 20 分钟 |

---

## A. 写作 + 质量门（推荐先做这个）

```bash
git clone https://github.com/Smith-106/meiqian-xiu-shenxian
cd meiqian-xiu-shenxian

python gate_report.py manuscript          # 全书体检
python gate_report.py manuscript --md 报告.md   # 导出 Markdown 报告
cd writing && python build_v3.py          # 42 章门禁
```

零依赖，全部标准库。Windows / macOS / Linux 都一样。

改稿流程：

```bash
# 改 manuscript/256_空两字.txt
python gate_report.py manuscript          # 看有没有过门
git commit -am "改 256 章对白"
git push                                  # CI 自动再跑一遍
```

### 单章检查

```bash
python gate_report.py manuscript | grep "^256"
```

### 重跑压缩流水线（可选）

`writing/pipeline/` 里是当时把 374 章压成 42 章的脚本，路径写死，先修正：

```bash
cd writing/pipeline
python patch_paths.py --apply
python assemble.py            # draft/ → chapters/，42 章
```

从 `draft/` 往后的每一步都能重跑；`draft/` 本身的生成没有脚本（见 `writing/pipeline/README.md`）。

### 评审（可选，需要 API Key）

```bash
cp writing/review_ext.example.py writing/review_ext.py
# 编辑：填 KEY 与 URL
cd writing && python judge.py ../manuscript/256_空两字.txt
```

`review_ext.py` 已被 `.gitignore` 排除，不会误传。

---

## B. 连 StoryMoss 一起复刻

### 1. 装应用

StoryMoss 装在 `C:\Program Files\storymoss`（Windows）。新机器需要单独安装，
应用本体不在本仓库。

### 2. 重建数据库

```bash
python restore_db.py --db "%APPDATA%\com.storymoss.app\cinema_ai.db" --force
```

会自动备份原库为 `.bak-时间戳`。

重建内容：

| 项目 | 数量 |
|---|---:|
| 章节 | 297 |
| 正文 | 297 章（取自 `manuscript/`） |
| 人物 | 83 |
| 人物关系 | 29 |
| 人物状态 | 125 |
| 世界规则 | 9 |
| 伏笔追踪 | 36 |
| 时间线事件 | 255 |
| 记忆图谱节点 | 195 + 26 |
| 章节大纲 | 255（第 1–255 章） |

### 3. 打开应用

数据库就位后启动 StoryMoss，图书、人物、伏笔、时间线应该都在。

**重建不回来的部分：**

- 版本历史链（`scene_versions`、`story_checkpoints` 本来就为空）
- 番茄发布相关的登录态与任务记录
- 第 256–297 章的 `chapters.outline`（原库中即为空，大纲在 `writing/plan_v3.md`）

---

## 目录说明

```
manuscript/    297 章正文，一章一文件，正文以此为准
novel/         631 章原版（历史存档）
data/
  storymoss_snapshot.json   叙事元数据快照（4.7 MB）
  schema.sql                建表语句（374 条）
writing/       规约、台账、门禁、评审脚本、42 章源文件
```

## 重新生成快照

元数据有变动时（新写了人物、加了伏笔）：

```bash
python export_snapshot.py                 # 读 %APPDATA%\com.storymoss.app\cinema_ai.db
python export_snapshot.py --db 其他路径 --out data
git commit -am "更新元数据快照"
```

---

## 常见问题

**Q：`gate_report.py` 报 `ModuleNotFoundError: sm_quality`**
脚本会自动把 `writing/` 加进 `sys.path`。如果仍报错，确认 `writing/sm_quality.py` 存在。

**Q：Windows 控制台中文乱码**
脚本已强制 UTF-8 输出。若仍乱码，先执行 `chcp 65001`。

**Q：CI 红了**
`.github/workflows/gate.yml` 里 42 章门禁是硬性检查，`FAILING` 非空即失败。
全书体检只是报告，不阻断。

**Q：能完全复刻原来的工作状态吗**
不能。正文、门禁、元数据能复原；应用本体、番茄账号、评审网关的密钥和已下线的模型不能。
本会话积累的判断（红线、锁定谜题、八轮评审诊断）部分在
`writing/PROGRESS.md`、`writing/plan_v3.md`、`writing/HANDOFF.md`、`writing/judge_rounds.md`。
