# 全量重写进度与缺口追踪

> 目标：以试点 v2 的 256、257 为起点，从原第 258 章重写到原第 631 章。
> 门禁：`C:\Users\niko\AppData\Local\Temp\sm_quality.py`，每分部须 100 分（≥95 为达标线）。
> 分段规范：每分部约 1,800–3,500 字，对白 0.20–0.30，禁感叹号，禁 SEVERE/MILD 词表。
> 情节红线以 `spec.md` 第二节为准：不新增具名人物与设定；卯十九只作账目点名；J 组悬丝不回收；最上格空栏两字到原 567 才随来名落墨（此前不落），保人户栏始终空；裴琬始终在位；带钩贴白曦腕。

## 一、已完成的卷分部

| 卷 | 分部数 | 覆盖原章 | 状态 |
| :-- | --: | :-- | :-- |
| 卷01 | 3 | 258–270 | 100 |
| 卷02 | 7 | 271–274, 279–310 | 100（缺口待核 275–278） |
| 卷03 | 7 | 311–333, 337–350 | 100（缺口待核 334–336） |
| 卷04 | 7 | 351–361, 363–367, 371–390 | 100（缺口待核 362, 368–370） |
| 卷05 | 6 | 391–394, 400–414, 420–430 | 100（缺口待核 395–399, 415–419） |
| 卷06 | 6 | 431–433, 439–442, 448–470 | 100（p05 已按原拍重写；缺口待核 434–438, 443–447） |
| 卷07 | 6 | 471–510 | 100（按原拍重写完成） |
| 卷08 | 4 | 511–550 | 100（按原拍重写完成） |
| 卷09 | 4 | 551–590 | 100（按原拍重写完成） |

## 二、漂移隔离（2026-10-29）

审计发现以下分部偏离原情节，违反 spec.md 红线（新增“师兄/堂尊/张阿六/寒水瓮/错核/断梓/断头签/南岭义庄/仵作命案”等原稿不存在的人物与设定，展开并回收卯十九旧账，填写空栏，带钩嵌入总版）。已整体移入 `draft\_quarantine_drift\`，不参与总装，可随时查阅：

- 卷06_p05（455–462，已用原拍重写替换）
- 卷07_p01 至 p06（471–510）
- 卷08_p01 至 p04（511–530）

同时修订：卷06_p04 结尾删去“判你的是我”这条虚构旧案；卷06_p06 删去“师兄暗手”、改正“卯十九已销账”为“底联存、转记保人户下、对销堂候核”。

## 三、待核缺口（共 31 章）

需逐一核对：若为重复仪式且已被相邻分部压缩覆盖，则标记“已并入”；若含推进性事件，则补写。

- [ ] 275–278（4 章）
- [ ] 334–336（3 章）
- [ ] 362（1 章）
- [ ] 368–370（3 章）
- [ ] 395–399（5 章）
- [ ] 415–419（5 章）
- [ ] 434–438（5 章）
- [ ] 443–447（5 章）

补写命名：`draft\补_pNN_orig<起>-<止>.txt`

## 四、后续待写正章

- 卷07：471–510（重写）
- 卷08：511–550（重写）
- 卷09：551–590
- 卷10：591–630
- 卷11：631

## 五、收尾工序（全部正文完成后）

1. 统一断章：每章约 3,000 字，章尾留钩子。
2. 二次质检：全稿逐章过 sm_quality，须 ≥95；对白 20%–30%。
3. 写回正库前**重新备份**原稿，保留可回滚。
4. 写回正库。

## 六、更新日志

- 2026-10-29：查明 31 章覆盖缺口并建档。
- 2026-10-29：审计发现 卷06_p05 起情节漂移，隔离 11 个分部；按原拍重写 卷06_p05（2,607 字，对白 0.214，100 分）；修订 卷06_p04、p06 衔接句。
- 2026-10-29：按原拍重写 卷07_p01（471–475，2,096 字，对白 0.231，100 分）、卷07_p02（476–480，2,178 字，对白 0.236，100 分）。
- 2026-10-29：按原拍重写 卷07_p03（481–485，2,083 字，对白 0.221，100 分）、卷07_p04（486–490，1,952 字，对白 0.234，100 分）。
- 2026-10-29：按原拍重写 卷07_p05（491–500，2,260 字，对白 0.267，100 分）、卷07_p06（501–510，2,121 字，对白 0.228，100 分）。卷07 完成；下一步 卷08（511–550）。
- 2026-10-29：按原拍重写 卷08_p01（511–520，2,350 字，对白 0.236，100 分）、卷08_p02（521–530，1,857 字，对白 0.246，100 分）。删去 卷07_p02、p03、卷08_p02 中原稿没有的具体牒数（三十七等），改为“数合”。
- 2026-10-29：按原拍重写 卷08_p03（531–540，2,110 字，对白 0.242，100 分）、卷08_p04（541–550，2,054 字，对白 0.260，100 分）。卷08 完成；下一步 卷09（551–590）。
- 2026-10-29：卷09_p01（551–560，1,923 字，对白 0.215，100 分）、卷09_p02（561–570，2,352 字，对白 0.226，100 分）。核原 567：最上格两字随来名落墨，裴琬择日之手不伸；草稿中虚构的“裴琬点指择日”“白曦朱线旧名”已删。
- 2026-10-29：卷09_p03（571–580，2,133 字，对白 0.273，100 分）、卷09_p04（581–590，2,216 字，对白 0.239，100 分）。原 572 唱俟编正名；578/581 廿一为课次，白曦讲；585–587 新值门侧候代交接；589–590“俟编未至，格空两字”按新旬候下一任处理。卷09 完成。
- 2026-10-29：卷10_p01–p04（591–630，1,775/1,863/2,091/1,764 字，对白 0.242/0.247/0.287/0.230，均 100 分）、卷11_p01（631，1,536 字，对白 0.216，100 分）。按原文：593 司核档壹员随牌到（无名），597–598 交牌后“新值”改称老值、随牌者记新值；606 老值出栈；615 裴琬后撤让位、621 压栏外新线；616 廿二为课次；630 俟编入格；631 俟编落廿二首笔，五验。
- 虚构词清查：通政司见 spec 口吻示例，保留；卷01_p02“几十年”改为不计年；卷06_p05“朱线”改为原 326 的“随审除名，墨痕不留边”。
- 正文 258–631 已覆盖，仅余缺口 275–278、334–336、362、368–370、395–399、415–419、434–438、443–447（共 31 章）。
- 2026-10-29：缺口已全部按分部改名并入（覆盖检查 258–631：缺 0、重 0）。修正：卷05_p04 裴琬代词改“她”、删新值交接；卷08_p02 删俟编（原 521–535 无俟编，536 才入场）、“十几旬”改“很久”；卷08_p04 首句“第十一日”改为不计日；卷03_p05 白曦独白改为与库役问答（对白补足）。
- 2026-10-29：试点 v2 的 256、257 对白补到 0.204 / 0.210（2,945 / 2,840 字，均 100 分），存为 `draft\卷01_p00_orig256.txt`、`卷01_p00_orig257.txt`。
- 2026-10-29：统一断章脚本 `assemble.py`（段落级动态规划，2,800–3,300 字，章尾优先落在问句/未决状态/下一章换日处）。输出 `chapters\`（新 256–301 共 46 章）、`chapter_map.json`、`chapter_table.md`。46 章全部字数 2,821–3,295、对白 0.201–0.272、sm 100。原 374 章因压缩重复仪式合为 44 章（spec 一-13 允许）。
- 2026-10-29：抽样复测 `review_sample.py`（每卷 2 章 + 末章）。原评审模型 muse-spark-1.3-contributor 已下线（HTTP 400 model_not_found），改用 gpt-oss-120b-medium，并在同一次运行复测试点基线：试点 v2 中性 65.6、铁律 85.1（原稿 24.0 / 87.2）。新稿抽样中性均分 51.8、铁律 84.2，成对盲比 40:0 新稿胜；卷六至卷十中性 31.5–54，低于试点底线，进入返修（`judge.py` 分部自检）。写回正库暂缓。
- 2026-10-29：返修第二轮（子代理全部启动即失败，改为手工）。重写 卷08_p02、卷09_p03、卷06_p06：唱词只保留每拍关键句，余者改叙述；去掉"第N日"流水；补问答和白曦的内心。分部中性（同一评审）：卷09_p03 35→53，卷06_p06 30→47，卷08_p02 59/64/54（评审噪声约 ±5–10）。旧稿存 `_quarantine_drift\*.pre_expand_v1.txt`。
- 忠实度清查：卷10_p01–p04、卷11_p01 删去人物替规矩讲道理的句子（"门砖不算栈里""两字是名，三栏是课""卷合了他跟着卷走""验够了才算"等），改为不答或候令；按原 627/630/631 校唱词归属（只有裴琬两句"迎旬已候""栈口已让"和"影定"有明署，其余唱句不署人）；卷11_p01 原稿"行款三栏待填已毕"，改为三栏落满；章末去掉"五毕可指"流水，以保人户栏仍空作钩。卷07/卷09 各分部"第N日"改为变化的时间衔接（备份 `*.pre_deledger_v1.txt`）。
- 章级全量评审 `judge_chapters.py`（46 章，gpt-oss）：返修前中性均分 59.4、铁律 85.3；256–281 中性 54–76，282–301 中性 30–70（301 最低 30、297 为 34）。

- 2026-10-30：去仪式/去讲规矩第三轮（手工）。卷07_p03/p04、卷08_p02/p03/p04、卷09_p01–p04、卷10_p02、卷11_p01、卷01/02/03/05 若干处：删去人物或旁白替规矩下定义的句子（"才算""意思是""后来才知道"等），改为不答、候令或短问答；卷09_p01/p02/p04 合并逐日流水；卷06_p05–卷11 叙述中重复的鞋尖/足跟/砖缝短分句按 KEEP=1 再删一轮（误删成残句的 7 处已手工补回）。卷01_p03、卷02_p01/p03/p04 原稿不在场的"库役"送牒改为在场的裴琬。备份 `*.pre_dechant_v1 / pre_derule_v1 / pre_trim2_v1 / pre_skip_v1.txt`。
- 终检（gemini-3.8-flash-high）：46 章 2,804–3,295 字，对白 0.201–0.269，sm 全 100，覆盖原 258–631 无缺无重。章级中性均分 80.2、铁律 97.6（铁律最低 94.7，章 273）；中性最低 300 62.2、297/298 65.6、295 66.6、292 67.4。抽样复测：新稿中性 78.4 / 铁律 97.6，原稿 25.8 / 97.7，成对盲比 40:0；同评审试点 v2 中性 85.0。分卷中性：卷一 88.6、卷二 87.0、卷三 82.0、卷四 84.3、卷五 80.6、卷六 76.1、卷七 65.8、卷八 74.9、卷九 65.1、卷十 79.2。卷七、卷九过 spec 底线（61.0）未到 70 目标。
- 写回：StoryMoss 未运行。先在 `Temp\wb_test.db` 副本试写通过；正库写回前备份 `storymoss_case\backup_cinema_ai_20261030_015112_before_full_rewrite.db`（integrity ok，631 场景）。`writeback.py --commit`：替换 256–301，删除 302–631 共 330 场景/章节，255↔256…301 链接，301.next=NULL；integrity ok，外键违例 338（与写前相同，无新增），场景与章节均 1–301 连续，文件与库逐章一致，story_metadata chapter_count/last_chapter=301、total_words=951083（按 content 字符长度计）。回滚：用上述备份覆盖 cinema_ai.db，或 `full_rewrite\orig\` 原文。

- 2026-10-30：每章中性 >80 返修（r80 第 13–21 轮，gemini-3.8-flash-high，评审协议不变）。各分部删去唱词套式（“核目/压据/守尘/让缝/送止/讫束”等两段唱）、寸/半步度量和悬腕/退步微动作，流程段压成一句；每处删减补一个只用既有线索、不揭底的新信息拍（涂墨年份“秋分前三天”、镇石石粉“有人挪过它”、门槛青砂、首格页脚“候”字、匣缝月牙指甲印、第三道红格纸边、名纸收笔一挑、保结栏新贴纸条、候对格背面反向凸点、栈板印泥碎屑等）。`assemble.py` 改为固定 42 章的分段 DP（K = 42 − 固定章数），TARGET 2810。
- 终检 r80_21：42 章（256–297）2802–2902 字，对白 0.206–0.284，sm 全 100，`FAILING: []`；章级中性均分 86.5，最低 81.8（每章 >80），铁律 97.7（原稿 97.7，未降）。各轮均分：13 86.2、14 85.5、15 85.4、16 85.7、17 85.3、18 85.3、19 85.9、20 86.1、21 86.5。
- 写回：StoryMoss 未运行。备份 `storymoss_case\backup_cinema_ai_20261030_161719_before_r80_writeback.db`（哈希一致）。`Temp\wb_test.db` 试写通过后 `writeback.py --commit` 正库：替换 256–297，删除 298–301 共 4 场景/章节；integrity ok，外键违例 338（与写前同），章节 1–297 连续，255↔256 链接，297.next=NULL，文件与库逐章一致。回滚：用该备份覆盖 cinema_ai.db。
- 2026-10-30 r80_22（每维 >80 返修，未评分）：返修 257、286、289、294、265、271、274、276、270、273、279、288、293、296、291、261、282 等的来源分部（tag `dim3_v1` / `dim4_v1`，改前备份在 `draft\_quarantine_drift\*.pre_*.txt`）。删去重复问答与“卯十九，贰毫，连滞纳，转记保人户下”在 264/266/272/276–278/282/284/287 的复述，并删去 286/288/289/291/293/294/296 中重开卯十九转记/户下的段落（红线 5）。新增的拍都只用既有线索、不揭底：白曦页边自具去处、外档房“不认也不刮”、存疑册墨点、外档房收件戳断口与“戳已报换”、梓库收件簿压据栏的小圈、晕边同向（“疑同垫”）、守夜录被裁半页、腰牌绳右收结、白垩粉扫痕与新值自记、裴琬“我认得”、俟编自写“请启”、朱笔“候”字夹条、小满补具单押到字、沈确在侧册上自写“到”。assemble：42 章，2805–2884 字，对白 0.207–0.296，sm 全 100，`FAILING: []`。正库未动，仍是 r80_21 的文本。
- r80_22 评审失败：gemini-3.8-flash-high 返回 503（`auth_unavailable`，上游 403，供应商账号因违反服务条款被停用）。`judge_chapters_r80_22.json` 全部为 None，本轮无分数。换评审属评审协议变更，须同次复测基线，待用户决定。
- 2026-10-30 换评审：用户指示 gemini 停用后改用 opus 5.5。评审模型取 `claude-opus-5.5`（不取 `kiro-opus-5.5`，后者是写作模型，避免自评），经 `DSH_JUDGE` 指定，评审提示词不变。opus 并发 7 时大量 429，`review_sample.chat()` 重试次数改由 `DSH_JUDGE_RETRIES` 控制、429 退避 45 秒，`judge_chapters.py` 并发改由 `DSH_JUDGE_WORKERS` 控制；新增 `judge_fill.py` 只补评缺分章并合并。
- opus 同评审基线（`review_sample_opus.txt`，部分样本 429 缺分）：铁律 原稿 78.9 / 新稿 89.2；中性 原稿 16.4 / 新稿 66.8；成对盲比 30:0 新稿胜；试点复测 铁律 原 73.5 / v2 91.1，中性 原 19.5 / v2 63.4。opus 比 gemini 严得多：r22 文本章级（`judge_chapters_opus_22.json`，42 章补全）中性均分 68.0，五维均分 76.9 / 72.9 / 62.5 / 62.2 / 65.4，铁律 91.35（最低 82.5），没有一章五维都 >80。opus 主要指出：时间线错位、她/他代词错、同一事件两稿拼接、同一问答复现、“看了很久/没有答”高频。
- r23 返修（tag `c262/coh_v1/c295/c288/c297/c271/c281/c294/c290/c289/c287/c291/c293`）：修 262 栈道木/石、裴琬去向、布袋未入库（补库役收袋与晏吏落押）；281 裴琬代词、唱和对句删减并补接更吏在缴检单按印；286/287 新值越线后重复“判在验后”、牌与腰牌混淆、俟编称谓、裴琬出栈写两遍、新值午前未回（补外档房留一夜与库役代押）；289 删验尘/照孔复写，补裴琬要页号与丙字抄手牌；290 删重复“口外问起来”，补白曦具单付新值；291 时间线与说话人；293 库役“名到了”改“封到了”，补白垩扫痕右缺与新值见袖带白；294 小满揭角跨三日改为当场复合并自记；295/297 删重复的空格候名与壬字棚两问，修“末一日/新旬”跳接与老值新值称谓。assemble：42 章，`FAILING: []`。
- r23 opus 章级全量（`judge_chapters_opus_23.json`，42 章补全）：中性均分 68.6（r22 68.0），五维均分 76.8 / 72.4 / 63.6 / 64.0 / 66.2，铁律 91.61（最低 86.8，高于原稿基线 78.9）。返修章：286 [80,74,70,72,68]（原 [76,72,62,58,48]）、288 ③52→62 ④50→64、289 ③55→62 ④52→66、295 ⑤54→60、271 ④55→66 ⑤55→68、262 ⑤50→55。未改的 256 同一文本两次评分 ③60→55、⑤78→70，评审噪声约 ±5–8。各章第③维最高 70，没有一章五维都 >80。
- 其后 `coh_v2` 小修：“号”字五笔；“晏吏没去开锁”重复；273/280 说话人；“那一夜白曦没有答”重复；“四十个早上”复述；287 对白降回 0.296。assemble：42 章，2800–2884 字，对白 0.208–0.296，sm 全 100，`FAILING: []`。这次小修后还没评分。正库仍是 r80_21。
- r24（`p286` 拆匣罚则落定、二纸俱无入存疑册；`tic_v1/v2` 机械去口癖：“看了很久” 27→0，“没有答/没答” 66→52，“通政司只认结果” 5→3；改前备份 `*.pre_tic_v1/v2.txt`）。assemble 42 章 `FAILING: []`。opus 章级全量（`judge_chapters_opus_24.json`，42 章补全）：中性 69.0，五维均分 77.0 / 73.0 / 64.0 / 64.2 / 66.9，铁律 91.62（最低 87.4）。各维最高 84 / 80 / 72 / 74 / 80，没有一章五维都 >80。286 单章 opus 中性复评两次，第③维 67、72。
- 阻塞结论：opus 连续三轮全量（r22、r23、r24，共 126 个章分）第③维没有一次超过 72，未改动的章与用户认可的试点 v2 也一样（55–60）。评审的判词每次都指向同一点：在这种以规程与器物为主的中性文风下，篇幅大半写流程，主谜按红线不能揭开，所以“实质推进不足”。在不改文风、不破红线的前提下，“每章每维 >80”在 opus 下达不到。待用户决定：改达标线（例如同评审下不低于试点 v2，或每维 ≥60），或允许改动文风/红线。正库仍是 r80_21，没有写回。

- 2026-10-30 用户决定：放宽文风、放宽部分红线。具体：每章流程或清点只写 1–2 句；每章写一件真事件，并在本章内了结；次要谜团可以揭开，主谜（保结人、被遮的名、九月守者、裴琬去留、小满实授、“上头的手”、断纹押纸条作者、带钩归属）和设定集红线 1–6 不动；达标线仍是每章每维 >80。
- v3 重写（`chapters_v3\`，大纲与逐章事件见 `plan_v3.md`）：42 章（256–297）逐章重写，不再从分部拼章。每章用 `build_v3.py` 把关：2800–3300 字，对白 0.20–0.30，sm ≥95。opus 单章探测（`probe_neutral.py`）的中性分在 72–84 之间，同一文本两次评分相差 ±4–8。291–297 收束廿二堂对：
  - 收件戳落在竹签上，不压押边。
  - 呈词第四行裁为不回避，因为外档房按日轮差送件。
  - 翘角经验浆，裁为雾泡，没有揭过。
  - 小满、白曦“猜过，不说”，九月一事另立一条，候另对。
  - 丙五当堂认下缺口小圈和报失不实。合口小圈出自另一只手，没有对上。
  - 外架四十八号由名主收回原格，新签照实写“首页缺”。总版印落在框外。
  - 铜钥还给泊台，放进存照匣。栈口新锁挂着不合，值守立线。
  - 日计分两行写：讫写讫，候写候。

  续写前修了 287：白曦因 269 拓纸上有他的押，同小满一起站阶下，并押了“知”。286 补了第五夜由裴琬守。为去掉口癖，“没有答/过了一会儿/没有再问/没有回头”等改成轮换说法。
- `build_v3.py --publish`：42 章全部通过，旧 `chapters\` 备份到 `chapters_pre_v3\`，v3 已复制进 `chapters\`。opus 全量评审 r25 已启动（`judge_full_opus_25.log`）。

- 2026-10-31 opus 全量评审结果。达标线是每章每维都 >80。
  - r26：均分 78.7，1/42 章达标（261）。
  - r27：均分 78.3，0/42 章达标。
  - r28：均分 79.0，0/42 章达标。五维平均为 ① 83.7，② 78.7，③ 78.3，④ 76.0，⑤ 78.2。④ 一直最低，判词多指流程反复和动作复现。
  - 同一文本两次评分相差 ±4–8，有 6 章单维只差 1–3 分（256、270、280、286、288、297）。
- r27/r28 之后的返修，全部过门禁：
  - 返修内容：按判词修⑤里的硬伤，包括人物走位、时间先后、对象指代、计数和规则依据。压缩重复的流程句。凡是判词说“只记不动”的章，都加了一件次要谜团的揭开。
  - 涉及章节：259、262–265、268、271、272、274–276、279、281–284、287、290–292、294、295。
  - 新收束的次要线：
    - 274：行走录里回条栏三年都写“不要”，是白曦写的。
    - 279：缴牌簿上值守牌二十年前由晏吏缴库，前天按对销堂单子复设。
    - 290：替条留在第七夜那只匣子的青布底下，是来人来不及取走；浆是隔了几天的米浆。
    - 294：白粉是丙字头抄案扑纸用的白垩。沈确追问初五的换差条，丙五说条子压在他的抄案上。
    - 295：管架人的收条上画的是合口圈。
  - 283：去掉了“库役替她记”，改成小满自己记，避开红线 3。这一处是在 r29 发布之后才改进 v3 的，r29 读到的 283 仍是旧文，要等下一次发布。
- 已发布，opus 全量评审 r29 已启动（`judge_full_opus_29.log`）。正库仍是 r80_21，没有写回。
- r29（`judge_chapters_opus_29.json`）：均分 79.1，1/42 章达标（297）。五维平均为 ① 83.4，② 79.0，③ 78.3，④ 76.4，⑤ 78.6。
  - 返修针对的单维多数上去了：271 ⑤ 70→82，292 ⑤ 68→82，262 ③ 72→80，263 ③ 72→80，281 ④ 71→80。
  - 没改的章受评分波动，有升有降。
  - r26–r29 四轮均分都停在 78.3–79.1。照 ±4 的波动算，要在一次全量里 42 章每维都 >80，每章每维的期望分得在 86 左右。现在差 6–7 分，主要差在 ④ 和 ②。
- 下一步：发布 283 的修订。逐章压 ④，删重复的动作和流程句。补 ②，加人物之间的正面分歧，用对话和动作写出来。
- 第 7 轮返修，以下各章改完都过了门禁：
  - 268：外架号改成按册续号、不分旬，修正四十七号与四十九号之间的时间矛盾；补了帚痕的来路，是丙字头抄手扫的，没有登簿。
  - 276：压缩印蜕流程，删掉“押了就是他肯 / 问了他就写”这类对句；加了老吏在门里质疑小满送单的一场。
  - 294：删去“是”字问答和录事的复述；加了丙五对沈确说“我的名没有人替我落”的正面交锋。结尾改成落在器物上。
  - 295：第二次揭示改成瘦老头不待人问、自己说出来。
  - 266：删掉卯十九户栏折痕那段，避开红线 5；改成去年秋冬七页刮浆同墨。修正唱核时说话人不清和“退腕”一句。
  - 257：修正“三栏/三格”的矛盾，交代裴琬在场，白粉线有了回应。
  - 296：压缩旧册批注和排钥仪式；加了沈确追问守线的差记，晏吏补差簿。
  - 261、274、281：去掉重复的动作句。
- r30（`judge_chapters_opus_30.json`）：均分 79.9，1/42 章达标（258）。五维平均为 ① 84.3，② 79.3，③ 79.2，④ 77.1，⑤ 79.5。四轮均分依次是 78.3 → 79.0 → 79.1 → 79.9。
- r30 发布之后又改了以下各章，还没评审：
  - 275：交代站位，加了领物底簿“多领一块”的推断，压缩交更一段。
  - 278：删去重复的解释，加了管钥人指出去年秋分那一月借钥簿尾押的是晏吏的断纹押。
  - 283：修正晏吏的位置，拆开末段。
- r31（`judge_chapters_opus_31.json`）：均分 79.9，1/42 章达标（270）。五维平均为 ① 84.1，② 79.5，③ 79.7，④ 77.0，⑤ 79.0。
- r32（`judge_chapters_opus_32.json`，评的是 267 等章改动之前的发布稿）：均分 79.5，0/42 章达标。五维平均为 ① 83.9，② 78.9，③ 78.6，④ 77.4，⑤ 78.9。最低一维是 266 ⑤ 66（散堂后沈确仍坐案心写录）。
- r32 之后的返修，全部过门禁，已发布，opus 全量评审 r33 已启动（`judge_full_opus_33.log`）：
  - 257：问询改成正面交锋，抄手以“越栏添字”记过相逼，白曦认下；删去否定句和“收笔压着起笔半分”；裴琬看见袖口的距离改成一步之内，并让她亲口说出。
  - 260：走法写明八个字；跑腿送纸改在当天未时；补白曦看见代押线被勾、听到押归新俟时的反应。
  - 263：交代“新俟”是代称；裴琬懂外档房用笔，因为她对了多年抄底；“摹谁的字”接上 264。
  - 264、268、282、294：理顺指代、时间和押的归属（294 中“那人”多改为丙五，六个圈写明是一张加五张）。
  - 266：结尾改成沈确站着叫库役开匣补记，消除前后矛盾；加晏吏对“自具去处”的正面反对。
  - 269：炭灰拓印的原理改正；点明牌上是裴琬的名，交代她是总版印主；补白曦被除名时的动作。
  - 274：消除白曦“从没要过 / 问过一回”的矛盾；删去重复的“门缝合上了”；压缩落号流程；裴琬先行出场。
  - 277：名纸改为夹进存疑册，不再重开梓库；送名人的灯改成“灭了”；删去一大一小、一软一硬和库役的说明腔；加晏吏解释他为什么担这一张。
  - 279、283、287：删去复述和回声对白；283 库役改为抄近路候着脚夫。
  - 280：删去姿态复现和横牌仪式；加沈确提议“重抄不呈”、被晏吏驳回的一场。
  - 292：压缩点件和站位；加堂官追问换差条没有正戳、老吏“我认戳，不认圈”的交锋。
  - 296：替条横纹由小满确认（接 290）；加裴琬追问自己那几夜站线没有入簿，晏吏补记。
  - 281、284、296：“锁鼻”统一为“铁环”。另清掉了全书剩余的“好几息 / 好一会儿 / 没有再问”等句式。
- r33（`judge_chapters_opus_33.json`，评的是上一条所列返修的发布稿）：均分 79.8，0/42 章达标。五维平均为 ① 83.5，② 79.7，③ 79.0，④ 77.6，⑤ 79.2。266 ⑤ 66→75；改过的章多数升 2–8，没改的章（273、287、261、294）降 4–7，都在评分波动范围内。r28–r33 六轮均分停在 79.0–79.9。
- r33 发布之后又改了以下各章，已发布，还没评审：
  - 272：交代两把锁同一匠人打、一把铁钥配两把；拓钥人先试栈口锁是为了校准锉钥；库役取匣改到对话结束以后；小满“照缝”的时序理顺。
  - 275：删去“声音发紧 / 册上没有”的复现和晏吏翻押样录的内心交代；库役记得“手很白”，改成登簿时那只手一直按在单上；加晏吏与沈确的一来一回。
  - 256：晏吏补报以前先反对（“三年前收旧拓的是我”），删“替他担了一半”。262：抄手先顶回“歪刀也是一房的人都用”，再认；“昨天”改成“昨天午后对保结栏”。265：删去“号不续”的三次复述，加库役“借刀不是头一回”。
  - 272、278：三角戳的位置统一为“锁身”（接 277、281）。278、295：去掉“没有马上 / 一指空白”的复现。
- r34 (`judge_chapters_opus_34.json`, judging the post-r33 edit list above): avg 80.5, 2/42 pass (267, 270), dims 84.4/80.4/79.7/78.7/79.5. Highest so far.
- Edits after r34 started (now published, not yet judged): 287 (库役 attending the hearing explained); 282 (沈确/裴琬 clash over not amending the 版, 印 gap changed to "缴回总版两年无人领", fits 279); 273 (narrator guess cut, wrist item described without naming it, 晏吏 pushback on the 押); 296 (守线 repeats and the 土样 duplicate trimmed, 裴琬 排进轮 logic fixed); 283 (new-ledger recaps merged, 白粉 tied to the 外档房 抄手 栏柱, 白曦/裴琬 exchange on "站住"); 292 (老吏 tics cut, a fold on the 借钥簿 copy page found on opening the box) + 293 (小满 admits she folded it before sealing; the 堂官 records it); 261 (corridor setting trimmed, a 登簿房 clerk's pushback, 白曦 points out the 销名/改期 order could have been arranged); 269 (炭盆 replaced by 砚边干墨粉, 沈确's position); 276 (inventory list cut, 楷字押 repeats trimmed); 264 (半寸/一息/锋合 repeats); 280 (半页 repeats, the opening wind scene, 小满 refuses to let 沈确 smooth it over); 286 (parallel argument phrasing trimmed); 294 (白粉 repeats); 267 (门闩); 291 (收件 procedure trimmed, 白曦 recalls the 候名 days).
- r35 (`judge_chapters_opus_35.json`): avg 80.4, 2/42 pass (290, 297), dims 83.9/80.4/80.0/78.2/79.5. Unedited 259 dropped 82/76/84/80/77 → 78/75/76/72/69, which is noise.
- Edits after r35 started (published before r36): 266 (三年 vs 候对 timing; 晏吏/沈确 clash over who carries the 去处 entry; ending moved to the 存疑册 with a 晏吏 半押); 262 (面浆 vs 米浆 吸潮; the 抄手 has been waiting since last evening and could not wash); 281 (三更 timing; 二十年 repeats; 不合锁 logic); 263 (dust on the 凸起 proves the mark predates the 抽格; 白曦/晏吏 clash over taking the blame); 259 (position); 268 (晓灯 reason; 棕丝 planted earlier; basis for 小满's thickness call); 271 (ending order of 退锁外 / 封匣 / 落锁 made explicit; 裴琬 "站到堂期"); 258 (刻 vs 落 for 墨); 272/274/277/284/288 (repeats); 257 (抄手 reads a prepared slip before conceding).
- r36 (`judge_chapters_opus_36.json`): avg 80.3, 2/42 pass (290, 295), dims 83.8/80.4/79.3/78.3/79.8. 276 (same text as r35) dropped 84/77/80/73/79 → 78/72/76/68/70; 273 (unedited since r34) ④ 85 → 80. Run-to-run noise is about ±5–10 per dim, while the average has stayed flat at 80.3–80.5 for three rounds.
- Edits after r36 started (published before r37): 259 (who drew the circle; the chant line; the reason for 白曦's position; trimmed repeated explanation; 白曦's 三年 浅坑 and 裴琬's reason for marking the point added); 260 (白曦 "看出来的人没有记在簿上"; 库役's motive; the 封存押 goes to whoever bagged it; procedure trimmed); 264 (晏吏 no longer states the 指节 茧 inference as fact; 白曦/晏吏 clash over "不问"; 两个字 made consistent); 276 (记着/背面 duplication; 沈确 "我这张牒算什么"); 289 (守夜录 repeats; 卯正打捆 → 早案 lead).
- r37 (`judge_chapters_opus_37.json`): avg 80.2, 1/42 pass (297), dims 83.7/80.0/79.5/78.5/79.1. Four rounds flat: 80.5 → 80.4 → 80.3 → 80.2. 3-run means (r34–36): only 4/42 chapters have every dim >80; single-run swing is ±5–10 per dim (260 and 282 dropped 6–8 with no meaningful edit).
- Edits after r37 started (published, not yet judged): 263 (晏吏 sets a 卯初 deadline: if the outside-margin mark is unclaimed by then, merge it with the 九月 驳行 and report to the 堂; sets up 裴琬's admission in 264); 294 (six-circle list compressed; 丙五 counters 沈确 with "你那张名牒上也有我一个圈"); 281 (logic of leaving the lock hanging open clarified; risk of the open 栈口 added); 287 (镇尺/知 repeats).
- Next: run r38. If it is still flat, the remaining lever is larger structural rewrites of the bottom ~12 chapters (263/276/257/259/260/265/279/264/282/281/266/271), which still need a mean min-dim of ~85.
- r38 (`judge_chapters_opus_38.json`): avg 80.8 (best so far), 1/42 pass (256), dims 84.3/80.7/80.1/79.0/79.8. 263, with the 卯初 deadline event, rose 80/76/72/74/75 → 82/79/80/83/75. Adding an event resolved inside the chapter works better than sentence-level patching.
- Edits after r38 started (published before r39): 265 (新俟 → 沈确 naming made explicit; logic of the 浆 smear on the 照牌簿 plus half a 浅黄指印 on the 簿边, not attributed; 白曦's 匣签 line clarified; 刀鞘 simile cut); 260 (押 contradiction fixed: 晏吏 holds the 押 and 白曦 holds the 袋口; 白曦 named as subject; 跑腿 redundancy cut); 282 (笔悬 → 搁笔 continuity; floor dust vs 匣盖 dust distinguished; 印簿 is locked in the 印槽); 273 (白曦 infers 圈有两手, recorded by 晏吏); 279 (交牌 direction clarified; the 领牌单 says only 栏外守线者); 258 (白曦 links 上头催转户 to the 版首刮半分; 细线 repeats cut).
- r39 (`judge_chapters_opus_39.json`): avg 80.7, 1/42 pass (270), dims 84.3/80.9/79.7/79.3/79.3. Unedited 256 dropped from passing (88/84/86/85/84) to 82/78/76/80/80; unedited 280 ① 88 → 80. That confirms a single-run swing of up to about 10 points per dim.
- Edits after r39 started (published before r40): 288 (echo dialogue removed; 沈确 names 存疑册 only appeared in a 回文 he read aloud, with 白曦 adding "念得出口的字就有人听得去"; 库役 "二十多年前那一夜规上轮的也是我"); 284 (晏吏/裴琬 inferences turned into hypotheses awaiting checks; 前夜沈确 lamp checks the oil-line burn rate; the double motive of taking the 回条 and blocking the 漏 stated); 296 (沈确 wants to send the 蜡/土 overnight and 晏吏 refuses because it is 候另对; 值守 procedure compressed); 266 (先例/日记 repeats cut); 264 (白曦 confronts 裴琬 over the 收锋; the 摹字 ending compressed).
- r40 (`judge_chapters_opus_40.json`): avg 80.6, 0/42 pass, dims 84.2/80.7/79.9/79.1/79.5. My lamp-timing insert in 284 created a contradiction (半指半更 vs 一更半指), dropping ⑤ to 68; fixed in the next item.
- Edits after r39/r40 (published before r41): 268 (explains why 外架 stopped issuing numbers after 去年秋分; red-ink 架号 is a single horizontal stroke across the 书口; 沈确 now writes in his own rounded hand); 274 (echo "现在他画了" cut; 门槛 position clarified); 269 (order of the 押; "谢这册日计"; 挤实 logic merged into one statement); 284 (lamp math made consistent: one finger per 更, half a finger per half 更); 259 (narrator no longer spells out 裴琬's motive); 256 (押样/押样录 merged into one prop; 晏吏's turn gets a line "新拓也缺，我那个准字就站得住"; 尺格/镇石 cut); 273 (铜色扁物 named as the 带钩 and its purpose stated; 齐边 inference explained).
- r41 (`judge_chapters_opus_41.json`): avg 80.8 (ties best), 0/42 pass, dims 84.9/81.1/79.8/78.9/79.5. Unedited 263 fell from 84/80/83/85/78 to 82/76/74/80/72; unedited 279 fell from 82/79/81/77/80 to 82/76/74/72/70. Across r38–r41 the overall average sits at 80.6–80.8, and each round 0–1 chapters pass. Same-text single-chapter swings reach 8–13 points.
- Next round: rewrite the chapters that are low in at least 2 of r39–r41 (263/273/274/259/260/276/279), building each around one confrontation resolved within the chapter; then r42.
- Edits after r41 (published before r42): 279 (新值 is 后半夜接值, so no contradiction; three repeats of the 缴牌 story merged into one 晏吏 line; the 锈圈 detail moved to 白曦; 白曦 asks 裴琬 "留到几时" and she answers "留到要照它办的那一夜"); 263 (名 vs 手 made concrete: the 版 is in 白曦's hand, the 牌 is the 匠人's, and he has not written a stroke himself; the 摹格 target named as 白曦's 堂期 row; the 新俟 entry explained as staying until the 正名牒 arrives; 裴琬's long line turned into narration); 276 (门缝/楷字押 repeats cut); 260 (跑腿 calls 新俟 to the 栈口, fixing the "到栏侧/回到栏侧" contradiction).
- r42 (`judge_chapters_opus_42.json`): avg 80.2, 1/42 pass (261), dims 83.9/80.3/79.5/78.5/79.0. 273 ⑤ fell to 71; the judge called 白曦's "圈有两手" inference thin. Changed to 晏吏 "记两式，不记两手". 292: the duplicated "背对看不见脸" line was merged.
- r43 (`judge_chapters_opus_43.json`): avg 80.7, 2/42 pass (290, 291), dims 84.3/80.5/80.0/78.9/79.6. 264 ④ swung from 83 to 70 between r42 and r43 with no edit. Across r38–r43 the average stays at 80.2–80.8 with 0–2 chapters passing per round.
- Edits after r43 (published before r44): 296 (removed the "没有再说" / "沈确道" contradiction; 沈确 adds the motive "锁梁开着还来按蜡，是等泊台合上"; 晏吏's reply changed to "我睡得着，是信那把锁"); 264 (膝头 changed to 衣襟; the 指背茧 and 断纹 imprint now explained physically); 273 (the 正联/副联 overlap and 洇号 mechanism stated clearly).
- r44 (`judge_chapters_opus_44.json`): avg 80.6, 1/42 pass (269), dims 84.0/80.8/79.9/78.5/79.6. The plateau holds: across r38–r44 the average is 80.2–80.8 with 0–2 chapters passing per round.
- Edits after r44 (published before r45): 279 (小满's two lines merged under one speaker; the 牌 issue date unified as "前天发下、挂了两天"; 库役's "十几年空着" now lines up with 晏吏's twenty years; the duplicate 牌锁一家 narration cut); 294 (circle count is now "抄底五处+当堂所画一"; the 竹纸 traced to 库役 scraping it off the 窄廊活砖; the 堂官 question turned into direct speech); 288 (匣面/半步/揣袖 motifs cut; 晏吏 decides to ask the 对销堂差 the next morning whether anyone was sent); 289 (opening adds: the 差 says 堂上昨夜没有派人).
- r45 (`judge_chapters_opus_45.json`): avg 80.4, 1/42 pass (289), dims 84.1/80.4/79.1/79.4/79.2.
- Edits after r45 (published before r46): 284 (circle gap unified as "右上"; 小满 passes the 守夜录 over without leaving the 匣侧; 库役 explains the motive for stuffing the 漏: soaked overnight, the ink would dissolve); 273 (白曦 is explicitly "在线边站着"; added the 存照 rule that 洇号 copies may not be destroyed); 256 (opening says 白曦 goes up onto the 泊台 and stands at the 案前; 裴琬's line adds that she was the one at the foot of the steps receiving 对销堂 items that season); 266 (旧阶 sealed "你来坐案的前一年", timeline made explicit).
- r46: void. Only 10/42 chapters came back (gateway 502), and `claude-opus-5.5` was then removed from the cpa endpoint (HTTP 400 model_not_found).
- Judge switch (HANDOFF §6 plan C, 2026-11-05): new `judge_cc.py` (prep/todo/collect). `prep` writes the exact user message that `judge.check` / `review_sample` would send (`NEUTRAL`, and `strict_prompt()` extracted from `strict()` with unchanged behaviour), one prompt file per job. Each job is answered by a Claude Code subagent (model opus). `collect` writes `judge_chapters_cc_<round>.json` and, when baseline jobs exist, `review_baseline_cc_<round>.json`. The baseline uses the same 20 originals as `review_sample_opus.json`.
- r47 (`judge_chapters_cc_47.json`, cc route, the r45-edit texts): avg 81.7, 9/42 pass (257, 260, 261, 266, 267, 285, 286, 295, 297), dims 83.0/81.6/81.0/82.5/80.1. Rule avg 95.92, min 94.1. Same-run original baseline 81.9 (`review_baseline_cc_47.json`); on the 13 originals scored by both judges it is 85.4 vs 78.9 for the old API run, so the rule gate is now ≥ 81.9 and every chapter clears it. Against the r38–r45 mean on the 38 unedited chapters, the cc judge shifts ① −1.4, ② +0.7, ③ +1.3, ④ +3.5, ⑤ +0.7. ⑤ is now the bottleneck, and many chapters fail only on one dim at exactly 80. The cc ⑤ notes name concrete continuity slips (object positions, who holds what, timing), which are fixable one by one.
- Edits after r47 (published before r48): 273 rewritten around one resolved confrontation. 晏吏 refuses to 押 a suspicion on one 齐边 alone. 白曦 then confesses that in his first year an 外档房 courier's 方垫 caused one of his 洇号, which he never reported. The two 存照 copies carry his first-year 押. 晏吏 writes the 存疑册 line, 白曦 writes "垫系外物，坐案者未报" himself and signs, then 晏吏 signs. 白曦 does the 补压 across the line, matching 274. The 合口圈, the "记两式" line and the 存照 coincidence were removed. Backup: `chapters_v3_bak/273_压据验纸.pre_r47.txt`.
- More edits after r47 (published before r48; backups `chapters_v3_bak/*.pre_r48.txt`), each aimed at a concrete r47 cc note: 256 (removed the premature 去年秋天磕角; the previous holder's 销名 dated 去年秋分前后; the three-year gap stated; 白曦's motive for asking: he used to refuse 牒 at this 案); 258 (石纹/落墨 order; 副联 stacking; 转户→版首 causality; the cost of 经手连坐 stated; fewer 半寸/半步); 259 (画圈平了半分石 / 报版首平之 rewritten plainly; 小满 takes responsibility for the 摹圈; 新俟's arrival timeline fixed; 外档房 forwarded the 印损报 but never logged it; closing fingerprint beat); 262 (cut the 进/退线 aphorism exchange and the restated 不按指印 paragraph; 白曦's stake; the 外档房 抄手's 拇指甲抹边 habit; confession motive); 263 (the dent is dated by uncracked dust lying over it, not by equal thickness; 晏吏 records the confession because it was spoken; 裴琬 speaks because 白曦 is taking the blame; 名牒/正名牒 disambiguated; repeats cut); 264 (blocking fixed; 裴琬's motive; 茧 mechanism; 晏吏 corrects his own morning line); 268 (dust is thinner where the 首页 was pulled; the 书口 朱号 stays intact, so 首页一 matches 295/297; closing aphorisms replaced by 晏吏's first-year 押); 269 (晏吏 goes along; 副联匣 hand-off; 拓痕 physics; 随审牌 rule in one sentence; the 九月 Q&A cut); 270 (守夜录 replaces 行走录; the stub is the cut-off half, format matching 293; an in-chapter 四更 旧阶栅 check); 271 (the stamp inference no longer jumps to 同一只手; 封匣 blocking reordered); 272 (裴琬's step over the line is the first since she stood 线内; the 屑 lands one palm outside; 晏吏's motive is now shielding the 梓库 管钥人, whom 278 later shows did lend the key once; the tester used the 栈口 lock because the 栅门 lock is rusted; 一更 timing; the 发匣 牒 is checked and 收讫); 275 (the hook is lent, "比完还我"; the 三团晕 are named; the hook is taken out again for the 押样录 check; one 册上没有的地方 removed; 沈确's reaction no longer mirrors 小满's); 276 (the door no longer closes before the second note; one 押 per 印蜕; the 老吏 writes the note to cover his own 押; the 匣 is picked up from the 槛; 库役 will watch the 劈戳); 277 (wax handled with a 竹签 only; the 墨晕's straight edge, corner to corner, measures 一寸一分; 角号/骑缝/存根 and 四十天 repeats cut; 裴琬 moves her lamp over the 板沿 print; 沈确 logs and signs the 日计); 280 (行走录 → 前录封皮夹层 half-page, matching 270/289); 282 (old 封条 on the 案角; 小满 beat; pronoun fix; one 锁门; 晏吏's twenty years of 揭封; 沈确's worry about his own page); 284 (every 泊台 lamp carries 小满's 刻痕 and she lit 沈确's the night before; the plotter misjudged how fast the paper would swell; the narrator's "one trip, two things" summary cut); 289 (秋报失/春领绳 reasoning stated once; the "record belongs to that day" theme kept in one place; 库役's knot knowledge is his twenty years of untying; added 库役's own 证有添 record, 沈确's palm mark, 小满's 先看); 291 (白曦 knows the 收件吏 from the 登簿房 window; the 凡例 he copied himself; the 纸帽 exposure answered, matching 292); 296 (why not just replace the lock: a new one would be waxed again; the 蜡包 is handed to 晏吏; the 土 packets go into the 存照匣; the 印簿 line is the 堂上 stamp from 295; the 铜钥 opens nothing because the 栅门 lock was changed in 278). All 42 still pass build_v3 (FAILING []).
- At-80 batch after r47 (published before r48; backups `chapters_v3_bak/*.pre_r48.txt`), aimed at the r47 dims that sat at exactly 80: 265 (白曦 walks to the 线边 before he sees the 竹屑; 晏吏 checks the 收件簿, then the 对销堂/外档房 号底 page by page, before ruling the number is in no book; 库役 tenure 二十多年); 260 (库役 tenure 二十多年, matching the HANDOFF lock and 287/288); 274 (an in-chapter 补压 done by 沈确 himself; 沈确 asks why 白曦 wrote 不要 and writes 收 himself, not 晏吏, so there is no 代填; the 粉 under the 外档房 door is left for the 堂); 279 (the 锈圈 shows when the 牌 comes down; 库役 never saw the 牌 hung or turned; 栏外守线者 can only be 裴琬); 280 (second pass: the 抄页 is cut wide, its back carries several lines, the last being 旧阶栅门钥一，外档房丙字头借); 283 (沈确 decides to 落押 on the 回条 as 俟编 and signs at the 匣侧; 库役 watches the brick till 辰初; new ending); 288 (接更吏's 我担 exchange; the 牌 lands at his toes; the dry-sole inference; record compressed); 294 (那人 → 丙五; why there is no 对质 that night; the four 合口圈 wait for 丙四's return, consistent with 297); 287 (白曦 volunteers for the 拓纸 line; 裴琬 says why the 单 was scraped; four 知); 290 (peak: 白曦 stops 沈确 pressing the lifted seal corner; 小签 wording); 292 (sleeve-rustle beat; the 堂 is postponed because the 俟编 seat is empty; repeats cut); 278 (白曦 compares the shoe prints; 沈确 writes the 借钥 line into the 日计 and signs, knowing 外档房 reads it first; 管钥人 works out 摘了环，钥才放得平 himself); 281 (铜碰铁; 库役 asleep on a 草垫; the 匠人 no longer knows the 三角戳 or 卡一齿 unprompted; 晏吏 asks which lock he repaired; a 晏吏/裴琬 exchange on who answers to the 堂 before the lock comes off; the open-hung lock is now just a fresh keyhole as telltale). Cross-chapter fix in 285: 裴琬 had wiped three lines (279), the 新值 wipes the first of the lower-right lines (外人亮牌…, quoted in 288), so 牌背 line 2 stays 栈口无锁，值守立线 (281/296); 285's 库役 aside now reads 这块牌在梓库二十年 (279: he never saw it hung). All 42 pass build_v3 (FAILING []).
- r48 (`judge_chapters_cc_48.json`, cc route, N jobs only; the S jobs from the same prep were not dispatched because N had already failed): avg 82.2, 13/42 pass (256, 258, 261, 272, 273, 278, 280, 283, 285, 290, 292, 295, 297), dims 83.3/81.3/81.0/83.3/81.9 (r47 83.0/81.6/81.0/82.5/80.1). Passed r47 but not r48: 257, 260, 266, 267, 286. Passed r48 only: 256, 258, 272, 273, 278, 280, 283, 290, 292. Judge noise, measured on the 8 chapters unchanged since r47 (257, 261, 266, 267, 286, 293, 295, 297): per-dim r48−r47 mean −0.07, sd 2.07, max |6|, i.e. about 1.5 per single judgement. That is much tighter than the 5–12 swings of the old API judge, so a dim at 78–80 in both rounds is a real weakness, not luck; to pass reliably in one round every dim needs to sit near 84+. Lowest r48 dims: 262 ⑤76 ②77, 263 ⑤76, 276 ②76 ③77, 287 ③76, 259 ③77, 291 ⑤77, 296 ②77. Recurring notes: ② low emotional temperature, no open confrontation, voices alike, 裴琬/小满/沈确 functional; ③ procedural progress, small stakes; ⑤ chapter-specific logic and count slips. Fixed after r48 (backup `chapters_v3_bak/*.pre_r49.txt`, not yet published): 266 (白曦 now steps out over the 栏线 after 沈确 is seated; 沈确 no longer "keeps holding the pen" before he picks it up).
- Post-r48 revision pass (r49 prep; backups `chapters_v3_bak/*.pre_r49.txt`; all 42 pass build_v3 with sm 100; not yet published or judged): 30 more chapters edited against the r48 notes: 257, 259, 260, 262, 263, 264, 265, 267, 268, 269, 270, 271, 274, 275, 276, 277, 278, 279, 281, 282, 284, 286, 287, 288, 289, 290, 291, 293, 294, 296 (plus 266 above). Cross-chapter fixes: 269 is now where 裴琬 receives the 牌 and becomes 栈口值守兼总版印主 (259 no longer calls her 印主; fits 279/282/287); 282 秋分 dating; 263/264 痕 timing and 264 pen location; 270 lock-hole dust baseline → 277 wax; 289 rope break tied to 288's night; 288 rope is thin/new (matches 289), 新值 never saw the 丙三 number (matches 284), 晏吏 placed in the 耳房; 296 end hook → 297 丙四 visit; 287 差/窗口 resolved to an unnamed 丙字头抄手; 260 代押 timing 三年→两年 (小满 has been at 泊台 two years), 卷七/卷八 label swap now actually performed; 263 "亲手写的名"; 267 库 sealed by 库役 at nightfall (matches 268), 旧阶 door has no handle from outside (bolt only seen from inside); 268 日计 only gets its 外架 number and goes back to 泊台 (入格 next morning in 269); 274 "头一旬问过一回" vs "头一个问的" contradiction fixed; 286 "每行二十字" removed, 送牒 memory aligned with 265, recusal cost made explicit (matches 292:33); 290 swap plan made explicit, 裴琬 stays on the line at dawn; 293 老吏 position and the three same-day records clarified; 294 "地上那一张" fixed, 合口圈 count now includes the 换差条 (not 丙五's hand), 丙五 pressed with the 丙字头 rope before admitting "没有丢". Stakes/voice (273-style): 260 库役/白曦 exchange; 267 白曦 vs 晏吏 on nailing the 栅; 274 晏吏 owns three years of 不要; 278 管钥人 admits concealment, night visitor linked to calling the 管钥人; 281 晏吏 deliberately seeks the 三角戳 locksmith, 裴琬 refuses a handover to keep names off the record; 288 end hook on the rope; 290 裴琬 challenges the sound in the fog; 293 小满's refusal risks a 线 under her name, ruling "不记不答". Flagged for user decision, not edited: 260 代押 vs red line 3; 277 柒行末格 name never revealed; 270 missing half-page never recovered.
- r49a (31 chapters judged via judge_cc subagents, `judge_chapters_cc_49a.json`): 14/31 with all five dims > 80; failing: 259, 260, 262, 265, 266, 268, 269, 270, 271, 274, 276, 277, 279, 282, 287, 289, 293. Post-r49a revision pass (r50 prep; backups `chapters_v3_bak/*.pre_r50.txt`; all 42 pass build_v3 with sm 100; not yet published or judged): 38 chapters edited against the r48/r49a notes (all except 261, 272, 273, 285). Systemic fixes: 白曦 hedges or concedes instead of explaining; inferences moved to 小满/库役/沈确/晏吏; interior beats and stakes added; terms glossed at first use; repeated procedures and recaps trimmed; coincidences turned into procedure-driven causality; end hooks tied to the next chapter. Continuity fixes: 265/286 名牒 folded 三叠; 294 缺口圈 stroke order and the 丙字头 courier headcount (丙四 and 丙五) vs 287/297; 294 白曦 testifies 不似 but not certain; 258 空匣 vs 259 状纸; 291 dates the 7th night 二十 (not 十九) and the 小签 to before dawn on 廿二 (not 昨日); 291 registration lists the 替条 and 292 点件单 adds 替条一; 291 库役 ties the 收件签 (守匣的人不碰匣); 296 opens from 梓库 per 295 and the 差 returns with the 回文; 守缝 count unified to 八夜 (280/296/297 said 九夜, but the 283/290 dates and 284/291 imply eight). Next: publish, then a full 42-chapter r50 judge round.
- r50 (full 42-chapter neutral round via judge_cc subagents, `judge_chapters_cc_50.json`; S jobs not dispatched): avg 82.5, 16/42 pass all five dims > 80 (256, 261, 266, 267, 269, 270, 273, 278, 280, 283, 284, 288, 289, 293, 294, 295); dims 83.2/82.0/81.8/83.7/81.7. Failing minima: 75 285; 76 276, 286; 78 257, 258, 282, 291, 297; 79 259, 262, 263, 265, 268, 271, 275, 281, 287, 290; 80 260, 264, 272, 274, 277, 279, 292, 296. Noise finding: the chapter mean is flat across r48/r49a/r50 (82.2/82.5/82.5) while unedited chapters swing several points per dim between rounds (285 r48 [87,84,83,86,85] -> r50 [82,79,75,76,83]; 261 and 272 each lost 8 in one dim). The r48->r50 per-dim change has SD 2.7 over 210 dims (single-run noise about 1.9-2.7), so a >=50% chance of all 210 dims > 80 in a single run needs a true mean near 86-88. Averaged over r48/r49a/r50, only 11 chapters have every dim >= 81 and 30 have at least one dim below 81 (lowest: 276 dim2 76.7, 262 dim5 77.3, 262 and 282 dim2 78.3); light-touch edits reshuffle which chapters fail rather than lifting the mean.
- Post-r50 objective-error pass (r51 prep; backups `chapters_v3_bak/*.pre_r51.txt`; all 42 pass build_v3 with sm 100; not yet published or judged): 25 chapters, each fixing a concrete dim-5 continuity/logic note rather than taste: 286 (speaker misattribution introduced in r50 fixed; 沈确 knows 丙字头 from 265's 照牌簿; he had never studied the back stamp), 291 (天刚亮; the 接更吏 ran the 小签 down and back; 收件吏 interiority removed; 页脚例 copied into the 添记), 271 (例牒 comes from 对销堂, not 泊台; 晏吏 answers the 小圈 line; dangling 小满应了 removed), 263 (claim limited to the 候对格; 小满's 架笔 only roughly fits), 265 (库役's 浆盒 lid left open as evidence; 照牌 takes longer), 290 (裴琬 stands behind 新值; no certainty that a new 替条 needs days), 297 (单子 carried between 案心 and line; 抄手 steps up to the line; 白曦 at 案边), 258 (朱笔 paper glued flat and the same color as the 匣板), 257 (空页 laid on the 录 instead of 翻到那一页), 259 (竹笔筒 with ink-soaked silk instead of a wet brush in the sleeve), 260 (who fetched the 卷: 外档房丙字头抄手, face not remembered; 梓库格 placed behind the 案; trimmed to 3286), 264 (纸包, not 架上), 268 (middle slot label blank; 隔一格是四十七), 272 (钥 copied from his, not his), 274 (no 一排灰字), 275 (借你压一回), 276 (印蜕 断口 half a stroke wider from this morning's knock; 小满 handles the 老吏 note), 277 (册 pushed to the line; prints in the dust, not in the plank gaps), 279 (the 差 starts when the 牒 stops at 栈心; 腰牌认人，值守牌认差), 281 (梓库 copy of the new key sealed and 押'd), 282 (only a grey shadow of the 原字 survives under the seal; 原版不出库 kept consistent), 285 (线前; 右下头一行; one less dust description; 隔着线抄), 287 (晏吏/沈确 answer at their 位次, 库役 follows the 匣, the rest stand at 阶下; 晏吏 also writes 知, so 五个知; the 透光 note claims only what is legible), 292 (sound-only cues while 沈确 has his back turned), 296 (裴琬's 近铁环 entry vs her 纸帽 assumption made explicit).
- r51 (`judge_chapters_cc_51.json`, full 42, the post-r50 texts): avg 80.6, 0/42 pass, dims 84.6/80.6/79.1/78.9/79.7. r51b (`judge_chapters_cc_51b.json`, 25-chapter re-judge of the same texts for the user's decision (b) "judge twice and average"): avg 80.0, dims 83.9/80.0/78.3/78.2/79.5. Finding: from r51 on the judge subagents stopped using extended thinking (answers came back in a fraction of the r47–r50 time with flatter, lower dims), so r51+ scores are not comparable with r47–r50.
- Post-r51 edits (backups `chapters_v3_bak/*.pre_r52.txt`): 13 chapters (257, 260, 262, 263, 264, 265, 268, 271, 274, 275, 276, 279, 296). r52/r52b were judged under the collapsed-thinking judge and are void. Calibration r53cal (261, 267, 270 re-judged with subagent effort=high) did not restore the r47–r50 behaviour. User decision: accept the current judge and switch to an in-round relative standard — a chapter fails if any dim is more than 2 points below that round's per-dim mean (the absolute >80 target is kept as a reference figure only).
- r53 (`judge_chapters_cc_53.json`, full 42): avg 81.5, dims 84.0/81.3/80.5/81.3/80.3, absolute all-dims >80: 258, 270, 278, 296. Relative failures 20 (`judge_cc/r53_rel_fail.json`): 257, 259, 260, 262, 263, 264, 265, 266, 268, 269, 271, 275, 276, 279, 282, 283, 284, 289, 290, 297.
- Post-r53 edits (r54 prep; backups `chapters_v3_bak/*.pre_r54.txt`; pairs in `r54_pairs/<ch>.json`; all 42 pass build_v3, published): 257 (duplicate exchange and 抄手 debate cut; 新俟 牒 passed, 白曦 keeps his signed handwritten page), 259 (新俟 arrival no longer caused by the 泊台 单; 进了栏), 260 (新俟 asks whether the 泊台 押 holder ever changed — "二十年没换过"; tell-y line replaced), 264 (inline glosses removed; why the pen hides in the 柱脚砖缝), 265 (栏的正中; 两年/三年 clarified; 裴琬 half-turns), 266 (沈确's motive; 缴检单 back-writing; 晏吏 summons 裴琬 for the 抄本), 268 (绕着灰走 moved to the opening; 库役's reaction), 269 (裴琬 at the 栈口; 刀尖 transition; rubbing physics), 271 (repeated 牒/号/骑缝 checks cut), 275 (hook unhooked from the wrist; 白手 memory as narration), 276 (白曦 interiority; 沈确's stake on his 牒), 279 (沈确 at 案后; 栏位 not 人名), 282 (裴琬's 我担 with stakes), 283 (reactions to 记我名下 and 再退一回), 284 (lamp/刻痕 description trimmed), 289 (a 调簿单 event: the 堂 refuses to call the 外档房 值簿), 290 (明天 → 天亮以后/今日; 纸帽 carried to the 堂 as-is, matching 291), 297 (落押/守夜录 repeats trimmed).
- r54 (`judge_chapters_cc_54.json`, full 42): avg 81.4, dims 84.0/81.3/80.3/80.8/80.6 (flat vs r53), absolute all-dims >80: 259, 270, 280, 284, 293. Relative failures 18: 257, 258, 263, 264, 265, 268, 269, 275, 276, 277, 279, 281, 283, 289, 290, 292, 294, 296. Fixed vs r53: 259, 260, 262, 266, 271, 282, 284, 297. Unedited chapters swung hard (258 passed absolutely in r53 → 77.4 in r54; 263 → 76.4), so per-round judge noise still dominates; the edits reshuffle failures rather than lifting the round mean.
- Post-r54 objective fixes (r55 prep; backups `chapters_v3_bak/*.pre_r55.txt`; pairs `r55_pairs/`; published): 290 (last 明天 → 今日), 289 (after the 午正 reply, "日头升起来，雾退" → 午后日头偏过栈顶; the fog already lifted at dawn), 294 (缺口圈 = 抄底五处 + 当堂一画; 合口圈 = 存疑册四处 + 换差条一处), 277 (the prints come from the 栈道, not from 泊台; 小满 checks them from inside the line), 264 (摹纸 stays under the 镇尺 at the 案角). Noise measured on the 24 chapters unedited between r53 and r54: per-dim difference sd 2.73, i.e. single-judgement sd about 1.9, against a cross-chapter sd per dim of 2.3–3.5 in r54. With one judgement per chapter the "more than 2 below the round mean" rule flags about 15% of dims by noise alone, so 42/42 in one round is not reachable without reducing judge noise.
- r55a/b/c (full 42, three N judgements per chapter, dims averaged; user decision "每章評 3 次取平均"): round mean 83.6/81.1/80.5/80.4/80.4, absolute all-dims >80: 10. Relative failures 16: 257[3], 259[3], 260[1,5], 261[2], 263[1,2,5], 265[1,2,4,5], 266[3,5], 271[3], 272[5], 276[2,5], 278[5], 279[1,4,5], 281[4,5], 284[4], 290[3,4], 291[2].
- Post-r55 edits (backups `chapters_v3_bak/*.pre_r56.txt`, pairs `r56_pairs/`): 257, 259, 260, 261, 263, 265, 266, 271, 272, 276, 278, 279, 281, 284, 290, 291. r56a/b/c re-judged those 16 (3×). Merge r55 base + r56 overrides (`$TEMP/avgm.py`): mean 83.8/81.3/80.9/80.7/80.9, relative failures 14: 257[3], 259[2], 261[2], 263[5], 265[1,2,5], 266[1-5], 269[5], 272[5], 274[4], 276[4], 277[5], 285[4], 288[3], 290[4]; absolute all>80: 11.
- Post-r56 edits (backups `*.pre_r57.txt`, pairs `r57_pairs/`, 45 edits in 14 chapters): 266 (晏吏 owns the 扣; 小满 admits the 缴检单 back; duplicate 刮浆 line cut), 257 (裴琬 saw the 合口 circle on the 抄手's 小条), 259 (open 晏吏/白曦 confrontation), 261 (白曦 interiority at the window), 263 (why the 名主 reads before the 牌), 265 (念名 timing; 白曦 "是我先疑了你"), 269 (reason for 不铲; the 牌 arrives with the returning 库役, no coincidence), 272 (三角戳 knowledge moved to 库役; 白曦's inferences as questions), 274, 276, 285, 290 (recaps and filler trimmed), 277 (朱笔 colour fixed; 荒地 inside the line), 288 (沈确 records that he read 存疑册 aloud). r57a/b/c re-judged the 14 (3×). Three-layer merge r55 → r56 → r57: mean 83.7/81.1/80.8/80.3/80.8, relative failures 11: 257[1-5], 261[2,4], 263[1,4], 265[1,2,4,5], 266[3,4], 269[1,2,5], 274[4,5], 276[2,3,4], 277[2,3,4], 285[3], 290[4]; absolute all>80: 13. Fixed: 259, 272, 288; newly failing after edit: 261[4], 263[1,4], 269[1,2], 274[5], 276[2,3], 277[2,3,4], 285[3]. Judge sd in r57 2.4 per judgement (r55 1.96).
- Noise floor of the current criterion (simulation from the r55 residuals, 42 chapters of identical true quality, 2000 rounds): 3 judgements + "2 below mean" → 6.5 failing chapters per round on average, P(0 failing) = 0.0; 6 judgements + 2 → 1.5, P(0) 0.20; 3 judgements + 3 → 1.1, P(0) 0.32; 6 judgements + 3 → 0.06, P(0) 0.94. So r57's 11 failures are only ~4–5 above pure noise, and 42/42 under "3×, mean−2" is unreachable by editing.
- Post-r57 objective fix (backup `*.pre_r58.txt`, pairs `r58_pairs/`): 257 — the 抄手 no longer takes the 缴检单 (it stays in the 录尾 where later lines put it); 晏吏 立在案侧 throughout. build_v3 FAILING [] (not yet published).
- User decision after the noise simulation: 6 judgements per chapter, averaged; a chapter fails if any dim is more than 3 below that round's per-dim mean ("6× / mean−3"). Before r58 the r57 edits that had lowered scores were reverted to their `pre_r57` texts, and the 277 fix (朱笔 colour, 荒地 inside the line) was re-applied on its own.
- r58 (6×, full 42, `judge_chapters_cc_58*.json`): thresholds (mean−3) 81.85/78.33/76.73/76.71/77.83. Failing: 257, 263, 266, 268, 269.
- Post-r58 edits (r59; backups `*.pre_r59.txt`): 268 (the missing-48 explanation turned into dialogue), 269 (晏吏 had earlier reported the 栈口 unguarded), 263 (侧册 gloss; 裴琬's motive), 266 (出入册 wording; one repeated sentence cut), 257 (跑腿 paragraph shortened). r59 (6× on those 5): 269 passes; 257 [85.7, 82.0, 76.3, 79.7, 81.3] misses ③ by 0.4.
- Post-r59 edits (r60; backups `*.pre_r60.txt`): 263 (the 送架栏 circle is the same as the 问单's — starts lower left, closed; the 名主不近案 rule added), 266 (小满 is present when 沈确 finds the note), 268 (the 移册单 was also delivered by a 丙字头 clerk). 257's r60 edit lowered ③ and was reverted to its r59 text. r60 (6×): 266 and 268 pass; 263 [83.3, 80.0, 78.0, 80.0, 77.0] misses ⑤ by 0.8.
- User decision: 257 and 263 count as passing. Each misses one dim by under 1 point, which is inside judge noise (about ±4), and two rounds of small edits did not converge. Final state: 42/42 pass build_v3 (FAILING []), and all 42 are accepted on N.
- r61 (S + baseline, `judge_chapters_cc_61.json` / `review_baseline_cc_61.json`): S rule 42/42, avg 95.06, min 94.1 (266, 272), against a same-round original-text baseline of 82.9 (20 chapters). Every chapter has S ≥ baseline.
- Writeback after r61: StoryMoss was not running. Backed up the main DB to `storymoss_case\backup_cinema_ai_20261107_173350_before_r61_writeback.db` (sha256 matches). Test-wrote `Temp\wb_test.db` first, then ran `writeback.py --commit` on the main DB. It replaced 256–297 and deleted no scenes. Checks: integrity ok; FK violations 338, the same as before the write; scenes and chapters contiguous; 255↔256 chain intact; file and DB identical chapter by chapter; total_words 934428. Rollback: overwrite cinema_ai.db with that backup.

## r62（260/269 紅線修正 + 263 微調）重評與寫回 — 2026-11-07
- 修改：260 代押→候押（小满不替押、拉候押线，白曦隔天自补）；269「今晨起领」→「今晨起暂领，候堂期定」（保留裴琬去留）；263 一句台词。
- 6× N 平均：260 通过；263 维度五 76.7、269 维度五 77.5，低于门槛 77.83，用户裁定视为通过。S（r62a）：95.1/93.0/93.6 ≥ 82.9。
- 备份 backup_cinema_ai_20261107_182433_before_r62_writeback.db → 试写 OK → 主 DB 写回 committed，dry-run 复核 ok。

## r63 卷七/卷九中性重测（opus，6×）— 2026-11-07
- 卷七（287–290）：81.6 / 82.7 / 82.7 / 82.1，卷均 82.3（单次最低 80.8）。卷九（294–295）：83.1 / 82.6，卷均 82.9（单次最低 80.8）。
- 均过 70 目标。注：旧值 65.8/65.1 为 gemini 评审，评审不同，仅作参考，不宜直接比较差值。
