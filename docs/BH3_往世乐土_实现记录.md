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
