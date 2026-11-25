# 往事乐土 · 实现记录

> 记录已经写进 mod 的机制，与参考文档（刻印 / 追忆之证）配套。日期：2026-11-25 起。

## 1. 关卡（楼层）机制 — 第一版

### 1.1 规则

| 项 | 规则 |
|---|---|
| 总层数 | 17 层（不含起点与最终英桀挑战） |
| Boss 层 | 7 / 12 / 17 |
| 双倍层 | 3 / 6 / 11 / 15（第二枚刻印需再花 100 钥匙购买） |
| 固定商店层 | 16 |
| 可选商店 | 4~5 层、8~9 层、13~14 层各一次机会 |
| 推进消耗 | 每层 100 无瑕之钥 |

### 1.2 变量与标记

| 名称 | 含义 |
|---|---|
| BH3_ER_floor | 当前层数（0~17） |
| BH3_ER_double_pending | 1 = 当前在双倍层且第二枚刻印未买 |
| BH3_ER_signets | 已获得刻印数（占位计数，等刻印系统接入） |
| BH3_ER_shop_45 / _89 / _1314 | 三组可选商店是否已用过 |
| BH3_ER_boss_floor | 当前层是 Boss 层 |
| BH3_ER_shop_floor | 当前层是固定商店层（16） |
| BH3_ER_final_challenge | 已进入英桀挑战 |

### 1.3 实现文件

| 文件 | 作用 |
|---|---|
| common/scripted_effects/BH3_ER_floor_effects.txt | BH3_ER_init_run、BH3_ER_enter_floor（层类型判定 + 发刻印占位） |
| common/decisions/BH3_ER_floor_decisions.txt | 推进一层、买双倍第二枚、三组可选商店、英桀挑战 |
| common/decisions/categories/BH3_ER_categories.txt | 进度组 + 调试组 |
| common/decisions/BH3_ER_debug_decisions.txt | 解锁乐土、+500 钥匙 |
| common/scripted_localisation/BH3_ER_floor_loc.txt | 18 个楼层文本分支 |
| common/on_actions/BH3_ER_on_actions.txt | 旧存档/异常时补初始化 |
| common/special_projects/projects/BH3_ElysianRealm_projects.txt | 完成特殊项目时调用 BH3_ER_init_run |
| interface/BH3_tech.gui | ER 窗口新增“当前层数”文本与钥匙图标 |
| interface/BH3_ER_art.gfx | 无瑕之钥图标 sprite |
| gfx/interface/elysianrealm/flawless_key.png | 无瑕之钥美术（128px，来自用户提供图标） |
| gfx/interface/equipmentdesigner/graphic_db/BH3_ElysianRealm_icons.txt | 装备图标池改用新图标 |

### 1.4 无瑕之钥

- 定义：common/units/equipment/BH3_ElysianRealm_material.txt（BH3_FlawlessKey_equipment / _0）
- 解锁：特殊项目 BH3_sp_ElysianRealm_Open → enable_equipments
- 价格：250 IC，100 把 = 推进一层
- 美术：gfx/interface/elysianrealm/flawless_key.png（128×128），同时用作决议图标、装备图标与 ER 窗口装饰

### 1.5 尚未实现（下一步）

1. 刻印抽取（目前只加 BH3_ER_signets 计数，没有真正的刻印池）；
2. 商店内容（目前只记录“已进入”，没有购买项）；
3. Boss 层的战斗事件与英桀挑战；
4. 层数/刻印信息在 GUI 的完整展示（现在只有一行文本）。


---

## 2. 层数 GUI（2026-11-25 第二版）

### 2.1 窗口内容

ER 主界面（BH3_ER_menu）现在是完整面板：

| 元素 | 名称 | 说明 |
|---|---|---|
| 背景 | GFX_BH3_ER_bg | 深色紫渐变 + 无瑕之钥大图（1400×700，由 flawless_key 生成） |
| 关闭 | BH3_ER_menu_x_btn | 回主菜单 |
| 标题 | BH3_ER_menu_title | 往事乐土 |
| 层数 | BH3_ER_floor_text | scripted loc 18 分支，显示“第 N / 17 层（类型）” |
| 提示 | BH3_ER_cost_hint | 每层 100 把，双倍层第二枚再 100 |
| 推进 | BH3_ER_advance_btn | 扣 100 钥匙 + 层数 +1 |
| 双倍第二枚 | BH3_ER_double_btn | 双倍层出现，扣 100 |
| 商店 ×3 | BH3_ER_shop45/89/1314_btn | 对应层段出现，一次 |
| 英桀挑战 | BH3_ER_final_btn | 17 层后出现 |

### 2.2 Scripted GUI

- 效果：每个按钮都有 _click，内部都有 if 守卫（层数/钥匙/是否已用过），防止显隐触发器失效时误扣。
- 触发器：_visible 控制出现条件，_enabled 控制钥匙是否足够。
- 入口：主菜单 ER 按钮点击时同时置 BH3_main_menu_open，保证父窗口存在。

### 2.3 已知风险

- 若 _visible 触发器在某些版本不生效，按钮会常显但点击被守卫拦下（不会误操作）。
- 背景是 PNG sprite（本 mod 已验证可行）；如某版本不吃 PNG，可改用同名 dds。


### 2.4 右上角层数提示（2026-11-25 追加）

- 位置：ER 窗口右上角（x=960, y=18，右对齐），显示“第 N / 17 层（层类型）”
- 实现：18 个静态 instantTextBoxType（BH3_ER_badge_0..17），由 scripted_gui 的 BH3_ER_badge_N_visible 触发器按 BH3_ER_floor 精确匹配切换
- 为什么不用时间触发器：玩家可能在暂停状态下点击，日结类触发器不会执行；按钮 _click 执行后 scripted_gui 会立即重算该窗口元素状态，所以暂停时也能即时变化
- 旧的左侧 BH3_ER_floor_text（defined_text）已移除，避免两处显示不一致


---

## 3. 刻印获取机制（2026-11-25 第一版）

### 3.1 文件位置（2026-11-25 实测修正）

**HOI4 1.19 不加载 common/scripted_effects 的子目录**——已实测：放在子目录里的效果全部报 Unknown effect-type。

因此刻印文件直接放在 common/scripted_effects/ 根目录，用统一前缀区分：

- 命名约定：BH3_ER_signets_<系名或编号>.txt（将来 12 系 = 12 个文件）
- 当前：BH3_ER_signets_00_test_pool.txt（6 个测试刻印 + 抽取/放弃/授予效果）
- 子目录方案作废，不要再新建 BH3_ER_signets/ 这类目录放脚本

### 3.2 变量

| 变量 | 含义 |
|---|---|
| BH3_ER_draws | 剩余抽取次数（每推进一层 +1，双倍层购买再 +1） |
| BH3_ER_offer | 1 = 当前正在展示候选 |
| BH3_ER_c1 / c2 / c3 | 三枚候选的刻印 ID（0 = 空） |
| BH3_ER_signets | 已获得刻印数（成就/统计用） |

### 3.3 流程

1. 进入新一层 → BH3_ER_draws +1
2. 点「抽取刻印」→ BH3_ER_roll_offer：扣 1 次抽取，随机掷出 3 个不同候选（1~6），置 offer = 1
3. 6 个候选按钮按 c1/c2/c3 的取值显示（每个按钮 _visible 判断自己是否在候选中）
4. 点候选 → BH3_ER_signet_grant_N：给对应国家精神（已有则跳过）、刻印数 +1、清空候选
5. 点「放弃本次抽取」→ 退还抽取次数并清空候选

### 3.4 测试刻印（6）

| ID | 名称 | 效果 |
|---|---|---|
| BH3_ER_signet_1 | 测试刻印 1 · 救世 | army_attack_factor +3% |
| BH3_ER_signet_2 | 测试刻印 2 · 刹那 | army_speed_factor +5% |
| BH3_ER_signet_3 | 测试刻印 3 · 浮生 | army_defence_factor +3% |
| BH3_ER_signet_4 | 测试刻印 4 · 旭光 | breakthrough_factor +3% |
| BH3_ER_signet_5 | 测试刻印 5 · 黄金 | industrial_capacity_factory +2% |
| BH3_ER_signet_6 | 测试刻印 6 · 天慧 | army_org +2 |

### 3.5 已知限制

- 6 个候选按钮是硬编码的，扩到 12 系 × 14 枚（168）时需要改成“按系分池 + 动态渲染”（或每系一页）；
- 目前不做重复保护：同一刻印抽到第二次仍会给精神（已有时跳过加精神，但计数仍 +1）；
- 权重目前是均等 1/6，正式版要按稀有度/是否已持有加权。


### 2.6 传送门样式刻印按钮与重排版（2026-11-25，第二版）

参照游戏内真实传送门（竖向紫黑星尘柱体 + 顶部金冠 + 中部圆形徽记 + 底部金色扇叶）重做：

- 新增 sprite：GFX_BH3_ER_portal_tile（200x290 PNG，竖向柱体，中部留圆形徽记槽）
- 新增 6 个刻印图标 sprite：GFX_BH3_ER_signet_1..6（复用 elysianrealm/signet_*.png：救世= Savior、刹那= Setsuna、浮生= Fusheng、旭光= Kosma、黄金= Gold、天慧= Bodhi）
- 候选按钮改为 6 座“传送门”，3 列 x 2 行：
  - 列 x = 520 / 740 / 960，行 y = 55 / 368
  - 徽记槽内叠 80px 刻印图标（scale 0.62，偏移 +60/+93）
  - 每个传送门下方有名字文本（instantTextBoxType，format=center，随按钮一起显隐）
- 左列按钮：推进 150 / 双倍 205 / 商店 260·315·370 / 英桀 425 / 抽取 480 / 放弃 535
- 背景进一步压暗，无瑕之钥缩到右侧边缘、透明度 38%，避免与传送门抢视线

### 2.7 历史 bug 修复（2026-11-25）

| 文件 | 问题 | 处理 |
|---|---|---|
| common/units/equipment/BH3_ValkyrieAir.txt | module_count_limit 里嵌套 module_count_limit 导致解析错误 | 删除嵌套块 |
| common/doctrines/subdoctrines/land/BH3_valkyrie_subdoctrines.txt | has_doctrine = bh3_sd_refined，该学说不存在 | 删除该 available 块（原本就没有实际作用） |
| common/scripted_effects/BH3_createleader_scripted_effects.txt | create_corps_commander 内的 can_be_captured 不是合法字段（138 处） | 全部删除 |
| common/decisions/BH3_TheDivineKeys_decisions.txt | productivity_growth_modifier / expected_mil_modifier / energy_gain_multiplier 不是合法 modifier；change_influence_percentage 不是合法 effect | 删除这些无效行（它们本来就不生效） |
| gfx/entities/*（4 个文件） | 引用已废弃的 Kiana_HerrscherofVoid_pdx | 改为重做后的 Kiana_HerrscherofVoid_Body_pdx |

另：日志里大量 “not in script_enum_equipment_bonus_type” 是引擎的**文档性提示**（原文说 enum 只用于文档），不影响装备加成生效，未处理。

---

## 4. 第一组刻印：救世（Deliverance，2026-11-25 第一版）

### 4.1 设计

- 原作：救世刻印只在“开启必杀技后”的窗口内生效（7 秒），核心Ⅰ延长/强化窗口，核心Ⅱ改成“命中 40 次进入救世之战”的常驻。
- HOI4 映射：战争期间出现决议「发动必杀技（救世）」，点击后按已拥有的刻印发放对应的临时国家精神（窗口），默认 7 天；拥有「救世者的余响」则 9 天；冷却 30 天。
- 核心Ⅱ另给决议「进入救世之战」，把加成常驻 14 天（冷却 60 天）。

### 4.2 数值映射（粗略，后续平衡）

| 原作 | HOI4 修正 |
|---|---|
| 全伤害 | army_attack_factor |
| 物理伤害 / 物理穿透 | breakthrough_factor |
| 元素伤害 / 元素穿透 | army_defence_factor |
| 每秒回能 | army_org_regain |

### 4.3 14 枚刻印

| ID | 名称 | 类型 | 窗口修正 |
|---|---|---|---|
| 101 | 施予者的金杯 | 普通 | attack +35% |
| 102 | 守望者的坠饰 | 普通 | breakthrough +30% |
| 103 | 不死者的烙印 | 普通 | defence +30% |
| 104 | 猎杀者的假面 | 普通 | breakthrough +35% |
| 105 | 制约者的圣器 | 普通 | defence +20% |
| 106 | 求道者的法衣 | 普通 | org_regain +3% |
| 107 | 救世者的王剑 | 核心Ⅰ | attack +17% / breakthrough +15% / defence +15% |
| 108 | 救世者的麇集 | 增幅 | attack +20% |
| 109 | 救世者的远征 | 增幅 | attack +14% |
| 110 | 救世者的余响 | 增幅 | 只改持续时间 7→9 天 |
| 111 | 救世者的孤影 | 核心Ⅱ | 常驻 attack +5%（并解锁救世之战决议） |
| 112 | 救世者的残梦 | 增幅 | attack +21% / breakthrough +18% / defence +18% |
| 113 | 救世者的决断 | 增幅 | attack +50% |
| 114 | 救世者的凯旋 | 增幅 | breakthrough +50% |

### 4.4 抽卡与 UI

- 抽取池：救世 101~114；普通刻印少于 3 枚时只出 101~106，达到 3 枚后全部都可能出现（对应“3 枚同系普通解锁核心”的规则）。
- 候选 UI 改成 3 座传送门（180x427，列 x=560/790/1020），图标统一显示救世徽记，名字由 scripted localisation 按 c1/c2/c3 动态显示。
- 授予：点击后由 BH3_ER_grant_c1/c2/c3 按变量派发到具体刻印，设置国家标记并计数。

### 4.5 已知未完成

- 核心刻印的前置判定目前只在抽取池层面粗过滤，尚未做“必须持有核心才能抽到增幅”的严格判定；
- 命中计数（40 次）没有真实接入，核心Ⅱ用“手动决议”代替；
- 刻印等级（+1/+2/+3）尚未实现，全部按 lv0 数值；
- 12 系全部实装后需要把 UI 改成按系分页/分池。

### 4.6 第二版改动（2026-11-25 晚）

1. **窗口效果改为动态修正（每系一个）**：删除 14 个临时国家精神，也放弃“一印一修正”的写法，改为**每个英桀只挂一个动态修正**，数值由 4 个变量累加：
   - 修正：BH3_ER_dm_dlv（唯一一个救世 DM），值取 BH3_ER_dlv_atk / _bth / _def / _org
   - 变量由刻印授予时累加（同一刻印只加一次），例如 101 → atk +0.35，107 → atk +0.17 / bth +0.15 / def +0.15
   - enable = 窗口天数 > 0 或已永久化；DM 在 BH3_ER_init_run 一次性挂载
   - 12 系全部实装后也只有 12 个 DM（BH3_ER_dm_<系>），不会出现上百个国家精神
2. **能量花费**：「发动必杀技（救世）」决议增加 cost = 50 政治点。
3. **核心Ⅱ改为累计释放解锁**：
   - 每次发动必杀技把 BH3_ER_dlv_ult_count +1；
   - 累计 ≥ 40 且持有「救世者的孤影」时，决议「救世之战：常驻化」出现，点击后置 BH3_ER_dlv_permanent，所有已拥有刻印的动态修正变为常驻。
4. **窗口计时**：BH3_ER_dlv_window 记录剩余天数（默认 7，拥有余响 9），on_daily 每天 -1；为 0 时 DM 自动失效。
5. **测试决议**（is_debug 可见）：
   - 获得全部救世刻印 / 清空救世刻印与窗口 / 立即发动一次必杀技 / 必杀技计数设为 40 / 再触发一次窗口。

### 4.7 调试总控（2026-11-25）

- 新增调试总控变量 BH3_ER_dbg_open（0 = 全部收起，1~12 = 展开对应系）
- 调试组首屏是 12 个「展开【XX】刻印测试」决议；点击后设置变量，其余系的决议自动隐藏，另有「收起当前系测试」
- 救世展开后的测试决议：
  - 获得 6 枚普通刻印（101~106）
  - 获得核心Ⅰ及 3 枚增幅（107~110）——点击时会先清掉核心Ⅱ组，保证两套核心互斥
  - 获得核心Ⅱ及 3 枚增幅（111~114）——同样先清掉核心Ⅰ组
  - 清空救世刻印与状态 / 立即发动一次必杀技 / 必杀技计数设为 40
- 其余 11 系展开后显示灰色的「该系刻印尚未实装」占位决议（available = always = no）
- 新增本地化文件 localisation/BH3_ER_debug_l_*.yml

---

## 5. 映射口径统一（2026-11-25 晚）

**所有“穿透 / 无视防御 / 降低抗性”类词条统一映射为两个独立词条：**

- army_attack_against_major_factor（对主要国家的攻击）
- army_attack_against_minor_factor（对次要国家的攻击）

两者都按原数值给满（视为独立加成）。据此回改救世：

| 刻印 | 原映射 | 新映射 |
|---|---|---|
| 104 猎杀者的假面（物理穿透 35%） | breakthrough +35% | 对主要/次要国家攻击各 +35% |
| 105 制约者的圣器（元素穿透 20%） | defence +20% | 对主要/次要国家攻击各 +20% |
| 114 救世者的凯旋（无视防御） | breakthrough +50% | 对主要/次要国家攻击各 +50% |

救世 DM 因此新增 BH3_ER_dlv_maj / BH3_ER_dlv_min 两个变量与对应 DM 字段。

**易伤乘区（敌人受到的全伤害提高）统一映射为“特种攻击”：**

- 词条：special_forces_attack_factor（原版词条，简单可靠）
- 以后所有“敌人受到伤害提高 / 易伤 / 沉醉”类效果都走这一个词条
- 代价：只作用于特种部队，覆盖率比逐兵种映射小；换来的是不用维护 4 个分类修正、也没有自定义分类未注册的风险
- 备选（未采用）：modifier_army_sub_unit_category_ValkyrieMeele / Comprehensive / Artillery / Armor _attack_factor 逐兵种给加成的写法已实测口径但依赖自定义分类注册


## 6. 第二组刻印：黄金（Gold，2026-11-25 第二版）

### 6.1 设计（政治点 = 能量）

- **普通刻印**：按**当前政治点数**给动态修正。引擎无法直接读取政治点数值，因此用“每 25 点一档”的阈值检查（on_daily 更新档位），档位 × 25 作为近似政治点，再换算成各类加成。
- **核心Ⅰ 咏叹**：按**累计回复量**工作。每日用档位变化累计回复的政治点；累计每满 100 点触发一次【咏叹的雷鸣】，给予 3 天的限时加成（对主要/次要国家攻击各 +20%，代表雷鸣+沉醉）。
- **核心Ⅱ 余音**：按**累计消耗量**工作。每日用档位下降累计消耗的政治点；拥有核心Ⅱ时，终末余音增伤 = 累计消耗 × 0.2%（上限 +160%），直接并入全伤害。
- 全系仍只有 1 个动态修正 BH3_ER_dm_gold，5 个输出变量由 recalc 每日重算。

### 6.2 变量

| 变量 | 含义 |
|---|---|
| BH3_ER_gold_bucket / _prev | 当前/上次政治点档位（25 点一档） |
| BH3_ER_gold_gain | 累计回复的政治点 |
| BH3_ER_gold_spend | 累计消耗的政治点 |
| BH3_ER_gold_atk / _def / _pp / _maj / _min | 输出给 DM 的最终数值（穿透/降防走 _maj/_min） |
| BH3_ER_gold_usp | 易伤乘区：特种攻击（special_forces_attack_factor） |
| BH3_ER_gold_aria_timer / _on | 咏叹限时加成的剩余天数/是否生效 |

### 6.3 14 枚刻印

| ID | 名称 | 类型 | 数值 |
|---|---|---|---|
| 201 | 乐园的宣叙 | 普通 | atk += 当前政治点 × 0.3%（上限 150%） |
| 202 | 溪流的宣叙 | 普通 | atk += 当前政治点 × 0.25%（上限 125%） |
| 203 | 飞鸟的宣叙 | 普通 | def += 当前政治点 × 0.25%（上限 80%） |
| 204 | 果林的宣叙 | 普通 | pp +2%（百分比修正） |
| 205 | 美酒的宣叙 | 普通 | 固定量每日 +0.5 政治点（BH3_ER_gold_daily 里直接 add_political_power，按浮点计算） |
| 206 | 宝玉的宣叙 | 普通 | pp +3%，授予时一次性 +50 政治点 |
| 207 | 黄金的咏叹 | 核心Ⅰ | 累计回复每 100 点 → 3 天限时：特种攻击 +15%（雷鸣+沉醉） |
| 208 | 丰壤的咏叹 | 增幅 | 易伤乘区：特种攻击 +15% |
| 209 | 生命的咏叹 | 增幅 | pp +5% |
| 210 | 黎明的咏叹 | 增幅 | 对主要/次要国家攻击各 +20% |
| 211 | 黄金的余音 | 核心Ⅱ | atk += 累计消耗 × 0.2%（上限 160%） |
| 212 | 枯壤的余音 | 增幅 | pp +10% |
| 213 | 凄风的余音 | 增幅 | atk +15% |
| 214 | 寂夜的余音 | 增幅 | 对主要/次要国家攻击各 +20% |

### 6.4 调试

展开【黄金】后：
- 获得 6 枚普通 / 获得核心Ⅰ+增幅（清核心Ⅱ）/ 获得核心Ⅱ+增幅（清核心Ⅰ）/ 清空
- **+150 政治点**：抬高当前档位，测试 201/202/203 的随政治点变化
- **-150 政治点**：降低档位，累积消耗量，测试 211 的终末余音
- 每次调试决议都会立即调用一次 BH3_ER_gold_daily，不需要等日结

---

## 7. 统一额外伤害接口（unit_damage，2026-11-25）

所有“额外伤害 / 真伤 / 结算伤害”类刻印效果统一走 common/scripted_effects/BH3_ER_unit_damage.txt，不要各写 damage_units。

### 7.1 输入

| 变量 | 含义 |
|---|---|
| BH3_UD_mode | 1=当前州敌军（需在州作用域调用） 2=敌国全体陆军 3=敌国海军 4=陆军+海军 |
| BH3_UD_org | 组织度伤害比例（0~1，ratio 模式） |
| BH3_UD_str | 兵力伤害比例（0~1） |
| BH3_UD_calls / _total_org / _total_str | 调试计数与累计量 |

### 7.2 调用

BH3_UD_begin = yes
set_variable = { BH3_UD_mode = 2 }
set_variable = { BH3_UD_org = 0.05 }
set_variable = { BH3_UD_str = 0.05 }
BH3_UD_apply = yes

也可用封装：BH3_UD_hit_enemy_army / BH3_UD_hit_enemy_navy / BH3_UD_hit_current_state。

### 7.3 约定（2026-11-25 实测确认）

- damage_units 必须有 location（州）：不带 state / province / region 时完全不生效（对照实验 A 无效、B 有效）
- 标准写法：every_enemy_country → every_owned_state → damage_units { state = THIS ... }
- is_enemy 不是 1.19 的合法触发器，统一用 has_war_with = ROOT
- else 块里不能带 limit，必须用 else_if
- 统一 ratio = yes：按部队当前总组织/兵力比例扣除，天然无视防御
- 变量参数（org_damage = BH3_UD_org）可用，接口实测生效
- 海军只能在港口/沿海州结算，mode 3/4 同样是逐州写法
- 接口自带 clamp（0~1）
- 伤害是“即时结算”，不进入战斗流程，数值要小（一般 0.01~0.05）

### 7.4 调试

调试组新增：
- 【调试】额外伤害：敌国陆军 -5% 组织/兵力
- 【调试】额外伤害：敌国海军 -5% 组织/兵力

点一下就能验证接口是否生效（看敌方部队组织度）。

---

## 8. 第三组刻印：刹那（Setsuna，2026-11-25）

### 8.1 设计

原作以极限闪避为触发器，核心把闪避变成结界或业狩。HOI4 没有闪避，用**决议「极限闪避」**代替触发：

- 决议「刹那：极限闪避」：自定义冷却（基础 10 天；有「藤」9 天；有「菊」5 天），点击后开启 8 天窗口、累计闪避计数
- 核心Ⅰ「樱上幕」：累计 3 次闪避后解锁决议「樱幕结界」——对敌国施加限时冻结 debuff（速度 -90%、攻击 -25%、突破 -30%，3 天；有「猪鹿蝶」5 天），并通过 BH3_UD 结算 12%/10% 比例伤害
- 核心Ⅱ「苦夜叉」：决议「业狩」（10 天冷却）通过 BH3_UD 结算 5%/4% 伤害；「万象无明」每释放一次叠 1 层攻击（上限 8 层）

### 8.2 变量

| 变量 | 含义 |
|---|---|
| BH3_ER_sts_atk / _spd / _usp / _maj / _min | 输出给 DM 的数值（易伤走 _usp，穿透走 _maj/_min） |
| BH3_ER_sts_w_atk / _spd / _usp / _w_on | 窗口临时加值记录（到期扣回） |
| BH3_ER_sts_window | 窗口剩余天数 |
| BH3_ER_sts_cd / _gouge_cd | 闪避 / 业狩 冷却 |
| BH3_ER_sts_dodge / _charge | 闪避计数 / 结界解锁标记 |
| BH3_ER_sts_stack | 万象无明叠层 |

### 8.3 14 枚刻印

| ID | 名称 | 类型 | HOI4 效果 |
|---|---|---|---|
| 301 | 缭乱百花「梅」 | 普通 | 窗口：atk +25%、spd +40% |
| 302 | 缭乱百花「红叶」 | 普通 | 窗口：易伤（特种攻击）+30% |
| 303 | 缭乱百花「牡丹」 | 普通 | 窗口：atk +40% |
| 304 | 缭乱百花「菊」 | 普通 | 闪避冷却 10 → 5 天 |
| 305 | 缭乱百花「藤」 | 普通 | 闪避冷却 10 → 9 天 |
| 306 | 缭乱百花「菖蒲」 | 普通 | 闪避时 +12 政治点 |
| 307 | 刹那一刀「樱上幕」 | 核心Ⅰ | 穿透 maj/min +35%/+20%；解锁结界 |
| 308 | 刹那一刀「雨四光」 | 增幅 | 结界时 +30 政治点 |
| 309 | 刹那一刀「月见酒」 | 增幅 | 易伤 +15% |
| 310 | 刹那一刀「猪鹿蝶」 | 增幅 | 冻结 3 → 5 天 |
| 311 | 刹那一刀「苦夜叉」 | 核心Ⅱ | 穿透 maj/min +35%/+20%；解锁业狩 |
| 312 | 刹那一刀「一瞬森罗」 | 增幅 | 3 次闪避自动触发业狩 |
| 313 | 刹那一刀「无间恶刹」 | 增幅 | 业狩后闪避冷却 -2 天 |
| 314 | 刹那一刀「万象无明」 | 增幅 | 业狩叠层：每层 atk +2.5%（上限 8 层） |

### 8.4 抽取与调试

- 抽取池扩展为 42 枚（救世 + 黄金 + 刹那）
- 传送门候选槽新增刹那徽记（signet_Setsuna）
- 调试总控「展开【刹那】刻印测试」：普通 / 核心Ⅰ+增幅（清核心Ⅱ）/ 核心Ⅱ+增幅（清核心Ⅰ）/ 清空 / 极限闪避 / 樱幕结界 / 业狩

### 8.5 已知近似

- 原作“极限闪避”是战斗内主动技能，这里用决议 + 自定义冷却模拟
- 「樱上幕」按期间受到伤害 40% 结算 → 用固定 12%/10% 比例真伤近似
- 「月见酒」「雨四光」的冷却重置/附加伤害折成易伤与政治点
- 结界冻结用敌方限时国家精神表达，不是真正的行动锁定
