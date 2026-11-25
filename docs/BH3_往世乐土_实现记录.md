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
