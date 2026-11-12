# 流水线存档（256–297 全量重写）

这里放的是当时把原书 **374 章压成 42 章**的实际脚本和历史产物。
脚本是一次性写就的，路径写死成 `C:\Users\niko\storymoss_case\full_rewrite`，
**克隆到新机器后先跑一次**：

```bash
cd writing/pipeline
python patch_paths.py --apply     # 把绝对路径改成当前克隆的位置，并做语法检查
```

不改也能读，只是跑不起来。

---

## 十步流程

| # | 步骤 | 脚本 | 输入 | 输出 | 状态 |
|---|---|---|---|---|:--:|
| 1 | 备份正库、导出原书 | `export_orig.py` | `cinema_ai.db` | `orig/` | ✅ |
| 2 | 抽逐章情节要点 | `beats.py` | `orig/` `orig_index.json` | `beats.json` `beats_digest.txt` | ✅ |
| 3 | **压缩改写** | **无脚本** | `beats_digest.txt` `spec.md` | `draft/` | ❌ 断点 |
| 4 | 组装成章并自检 | `assemble.py` | `draft/` `beats_digest.txt` `orig_index.txt` | `chapters/` `chapter_map.json` | ✅ |
| 5 | 折叠重复唱词 | `fold_chants.py` | `draft/` | 就地改写 | ✅ |
| 5b | 删唱词、削仪式套话 | `dechant.py` `trim_ritual.py` | `draft/` | 就地改写 | ✅ |
| 6 | 定点替换精修 | `edit_drafts.py` | `draft/` | 就地改写 | ✅ |
| 7 | 门禁 | `../build_v3.py` | `../chapters_v3/` | 报告 | ✅ |
| 8 | 评审 | `judge_batch.py` `judge_one.py` `judge_cc.py` | `chapters/` | `judge_chapters_*.json` | ⚠️ 模型已下线 |
| 9 | 回写正库 | `writeback.py --commit` | `chapters/` | `cinema_ai.db` | ✅ |
| 10 | 导出成品 | `export_novel.py` | `cinema_ai.db` | `novel/` | ⚠️ 断言 631 需改 |

### 第 3 步是唯一断点

`draft/` 那 343 个文件是逐段改写的结果，**生成过程没有脚本**——当时由模型按
`../spec.md` 直接写出。换模型、换会话，产出会不同。
所以「从原书重新压一遍」无法一键重放；但**从 `draft/` 往后的每一步都能重跑**。

---

## 已验证

在本仓库副本上执行：

```bash
python patch_paths.py --apply
python assemble.py
```

结果：

```
chars min/max: 2800 2894
dialogue min/max: 0.208 0.292
sm min: 100
FAILING: []
42 章
```

即 `draft/` → `assemble.py` → 42 章全部过门禁。

---

## 各目录

| 目录 | 文件数 | 内容 |
|---|---:|---|
| `draft/` | 343 | 压缩改写稿（`chXXX.txt` 与 `chXXX_base_v2.txt`） |
| `chapters/` | 42 | 组装后的成章（v3 之前的版本） |
| `revisions/` | 132 | 逐章返修稿 |
| `localfix/` | 75 | 局部修补稿 |
| `pilot_opus/` | 26 | 原稿/新稿盲比试点数据 |

## 数据文件

| 文件 | 说明 |
|---|---|
| `beats.json` | 374 章逐章要点（标题、字数、对白占比、在场人物、开头、结尾、关键唱词） |
| `beats_digest.txt` | 上者的可读摘要，`assemble.py` 从里面取标题 |
| `orig_index.json` / `orig_index.txt` | 原书 631 章的序号、标题、字数索引 |
| `chapter_table.md` | 42 章的字数/对白/质检/成败对照表 |
| `volume_plan_bounds.txt` | 分卷边界 |
| `outline_continuation.txt` | 续书大纲 |

## 需要手工确认的两处

`patch_paths.py` 不会改数据库路径，跑完会提示：

```
export_orig.py:4    SRC = r'C:\Users\niko\AppData\Roaming\com.storymoss.app\cinema_ai.db'
export_novel.py:9   con = sqlite3.connect(r'C:\Users\niko\AppData\Roaming\...\cinema_ai.db')
```

Windows 上默认就是 `%APPDATA%\com.storymoss.app\cinema_ai.db`，通常不用改。
