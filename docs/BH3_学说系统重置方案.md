# 女武神作战学说·重置方案与实施记录（2026-10-09）

## 背景与目标

旧学说系统为 mod 自研 GUI（主菜单 →「作战学说」树状界面，`BH3_Valkyrie_Doctrine_*` 科技 + scripted GUI 手搓前置），按用户指示整体重置为**最新原版陆军学说界面**（`common/doctrines` 体系：主学说 Grand Doctrine + 子学说 Subdoctrine + 轨道 Track + 里程碑 Milestone），不再进入 mod 自研 GUI。

用户定下的设计口径：

1. **开门的第 1 个学说作为主学说**（旧 `BH3_Valkyrie_Doctrine_0`「对崩坏作战理论」）。
2. **后续子学说 7 条线**：步兵协同 / 战斗支援 / 装甲突击 / 纵深作战 / 近战攻坚 / 律者降临 / 女武神特战。**v2 修订（10-09 深夜）**：7 条轨道全部使用自定义轨道键（`valkyrie_*`），不再复用原版 4 轨——原版子学说因此**从机制上无法混入**本学说文件夹（原版子学说挂在原版轨道上）。
3. **互斥选项分别以两个子学说的形式设计**：旧树中的互斥对同轨成对安置。**v4 修订（10-10 凌晨，依据互斥核实结果）**：逐个核对旧 GUI 触发器后确认，旧树 24 节点中**唯一真正互斥的对是 3_5_1 优势兵力 / 3_5_2 精益求精**（互为 `NOT = { has_tech = 另一侧 }`）；此前以为互斥的 1_4（持久攻势/动态防御）、1_5（弱点洞悉/战场救火队）、2_4（分散支援/协调支援）、2_5（弹幕覆盖/联合兵种）全是"同层双分支"，两侧均可购买、可同时持有。v3 把这些分支拆成同轨不同子学说，而**每轨道只有一个槽位**（原版文档：Track = a slot for a subdoctrine；界面每轨仅一个 `sub_doctrine` 按钮）——等于人为制造互斥，完全体强度远逊于旧系统。**v4 起：非互斥的串行/分支内容全部整合进同一子学说**（base = 链首节点效果，rewards 按 mastery 阶梯逐级解锁，等同旧顺序解锁；同档多 reward 表示旧系统的同层双分支），只有 3_5 对做成同轨两个子学说，用 `available = { NOT = { has_doctrine = 另一侧 } }` 还原真互斥。
4. **收尾学说的效果分散在 7 条线的里程碑中**：旧 `BH3_Valkyrie_Doctrine_10`「为世界上所有美好而战」的全部效果按约 1/7 拆入主学说的 7 个里程碑（逐线完成时发放）。
5. **v2 修复（10-09 深夜，对应"新三线为空 / 效果不全"反馈）**：
   - 新三轨精通类别由 mod 自定义类别（`category_ValkyrieMeele` 等）改为原版校验过的类别（`category_special_forces` 等，女武神单位本身即 `category_special_forces`）；
   - 修饰键全部经原版 `common/doctrines` 逐键校验，替换/移除了学说语境不支持的键（被静默丢弃导致"效果不全"的元凶）：`max_planning_factor`→`max_planning`；`combat_width_factor` 移除；`special_forces_min`→`special_forces_cap`；`special_forces_defence_factor`（原版学说无此键）→ `special_forces_cap` / `category_AllValkyrie defense`。
6. **v3 修复（10-09 深夜二次，依据 error.log 定位）**：`error.log` 显示子学说文件在 `bh3_rwd_eyes_front` 的 `recon = 0.02` 处断 parse，此后 23 个子学说全部级联报错——**奖励（rewards）块内裸写的国家修饰是非法的**。按参考 mod（workshop/3673656844）证实的语法修复：奖励条目内的国家修饰必须包在 `modifier = { }` 中（该 mod 还示范了 `mastery = N` 门槛、`effect = { }` 脚本效果、地形子块 `urban = { ATTACK = x }` 等用法，后续可参考）。

## 旧 → 新映射总表

### 主学说

| 新 | 来源 | 内容 |
|---|---|---|
| `bh3_valkyrie_warfare`（对崩坏作战理论） | 旧 `_0` | 基础效果原样保留（category_army 全面加成 + special_forces_min 24 + 特攻特防 0.15）；7 个里程碑 = 旧 `_10` 效果按线分散 |

### 8 个子学说（v4 整合版：24 个旧节点全数保留，串行内容并入同一子学说）

| 轨道 | 子学说 | 结构（base → rewards，每档新增 mastery 均为 150） |
|---|---|---|
| valkyrie_infantry 步兵协同 | 近接歼灭战术 | 1_1(base) → 1_2 快速接敌 → 1_3 武装侦查 → 1_4_2 动态防御 → 1_5_2 战场救火队 → 1_6_2 后发制人（满级 750） |
| valkyrie_armor 装甲突击 | 持久攻势 | 1_4_1(base) → 1_5_1 弱点洞悉 → 1_6_1 天元突破（满级 300） |
| valkyrie_assault 近战攻坚 | 敌后作战 | 3_1(base) → 3_2 战斗穿插 → 3_3 空降突击 → 3_4 专业训练（满级 450） |
| valkyrie_support 战斗支援 | 远程压制战术 | 2_1(base) → 2_2 抵近观测 → 2_3 火力调配 → 2_5_1 弹幕覆盖 → 2_6 全域压制（满级 600） |
| valkyrie_operations 纵深作战 | 分散支援 | 2_4_1(base) → 2_4_2 协调支援 → 2_5_2 联合兵种 → 3_6 协同作战（满级 450） |
| valkyrie_herrscher 律者降临 | 律者觉醒 | 觉醒(base，新设) → 律者统御（新设，满级 150） |
| valkyrie_special 女武神特战 | 优势兵力 ★互斥 | 3_5_1(base) |
| valkyrie_special 女武神特战 | 精益求精 ★互斥 | 3_5_2(base) |

★ = 旧树**唯一**真互斥对，用 `available = { NOT = { has_doctrine = 另一侧 } }` 双向互锁；其余旧"对"均为同层双分支，已全部并入串学子学说，不再互斥。

- v4 强度口径：7 轨全部练满 = 旧系统 24 节点（除 3_5 二选一外）全效果，等同旧完全体。
- **mastery 语义与阶梯（2026-10-10 用户定调 + 实测修正）**：reward 的 `mastery = N` 是**相对上一档的新增精通需求，不是绝对值**（原版统一 50、参考 mod 统一 100 可证；曾按绝对值写成 150×n，实测步兵线要求累积 2250，已修正）。每档新增统一 **150 点**，即每个 reward 都写 `mastery = 150`，满级 = 150×档数（步兵协同 750 / 战斗支援 600 / 近战攻坚、纵深作战 450 / 装甲突击 300 / 律者 150）。原版 `MAX_MONTHLY_MASTERY_GAIN = 40`（每轨每月上限），每档最快约 3.75 个月——高成本高收益，与旧系统"陆军经验解锁成本从来不低"的数值口径一致。
- 奖励（reward）直接承载旧节点完整效果（不再是小额占位加成）；国家修饰键一律包 `modifier = { }`，单位类别块裸写（v3 语法规则沿用）。
- 地形加成：遵照用户指示**暂不引入**地形子块（旧系统本身无地形效果），先完全保留原系统总奖励。
- 新 3 条轨道的精通类别用原版校验过的类别：`category_special_forces`（近战攻坚、女武神特战）、`category_special_forces` + `category_all_armor`（律者）。
- 解锁口径：主学说 `available = has_country_flag = BH3_Hyperion_enabled`（沿用旧门槛）；子学说 always = yes（互斥对除外），XP 花费 100 陆军经验（与旧口径一致）；AI 由 doctrines 原生 `ai_will_do` 自动购买（旧 8 个 AI 决议已删）。

## 文件清单

| 文件 | 内容 |
|---|---|
| `common/doctrines/folders/BH3_doctrine_folders.txt`（新） | 学说页签文件夹 `valkyrie`（女武神作战学说，ledger=army，复用原版陆军页签图标） |
| `common/doctrines/grand_doctrines/BH3_valkyrie_grand_doctrine.txt`（新） | 主学说 `bh3_valkyrie_warfare` + 7 轨道声明 + 7 里程碑（收尾学说效果分散） |
| `common/doctrines/tracks/BH3_valkyrie_tracks.txt`（新） | 7 条自定义轨道（`valkyrie_*`，v2 起不再复用原版 4 轨，原版子学说无法混入；精通类别用原版校验过的类别，女武神线用 `category_special_forces`） |
| `common/doctrines/subdoctrines/land/BH3_valkyrie_subdoctrines.txt`（新） | 8 个子学说（v4 整合版：串行旧节点并入同一子学说，base+rewards@mastery 阶梯还原旧顺序解锁；仅 3_5 对双子学说互斥） |
| `localisation/BH3_doctrine_l_*.yml`（清理 78 旧键后追加 34 键 ×2） | 文件夹/主学说/轨道/子学说/奖励 名称与描述（中英），并入现有 yml |
| ~~`common/technologies/Valkyrie_Doctrine_Tech.txt`~~ | **已删除**（25 个旧学说科技由 doctrines 体系取代） |
| `interface/BH3_tech.gui`（改） | 删除「女武神学说界面」+ 树状视图两个容器窗口（共约 578 行） |
| `common/scripted_guis/BH3_tech_scripted_gui.txt`（改） | 删除 `BH3_Valkyrie_Doctrine` / `BH3_Valkyrie_Doctrine_Treeview` 两个 scripted GUI 及全部学说按钮 effect/property（约 664 行） |
| `common/decisions/BH3_cultivate_decision.txt`（改） | 删除 8 个 AI 自动买学说决议（`BH3_cultivate_Valkyrie_Doctrine_0..7_decision`，约 296 行；AI 改由 doctrines 原生 ai_will_do 驱动） |
| `tools/gen_valkyrie_doctrine.py`（新） | 上述学说文件与本地化的生成器（可复跑，loc 幂等） |

保留未删（无害孤儿，备后续美术/界面复用）：旧学说贴图 `GFX_BH3_Valkyrie_Doctrine_*` 系列、`GFX_BH3_main_menu_doctrine`（现用作主学说图标）、旧学说 loc 键、`BH3_Valkyrie_Doctrine_on` 旗帜的若干 clr 语句。

## 待游戏内验证清单

1. 学说界面（快捷键 F4 / 科技页学说页）出现「女武神作战学说」页签，未解锁国家不显示主学说；
2. 拥有 `BH3_Hyperion_enabled` 的国家可花 100 陆军经验采纳主学说「对崩坏作战理论」，获得其基础效果；
3. 7 条轨道可见（4 原版 + 3 新），每条轨道可花 XP 选择 1 个子学说，同轨互斥对二选一；
4. 各轨道 mastery 随相应兵种类别作战增长，奖励逐档解锁；
5. 逐线完成（track 完成）时发放对应里程碑（收尾学说效果分散验证）；
6. AI 国家在满足门槛后自动购买主学说与子学说（观察 AI 行为）；
7. 旧存档兼容性：旧档中已研究的旧学说科技随文件删除失效（预期行为，需开新档验证）。

## 已知限制

- 3 条新轨道图标/背景复用原版陆军图，后续可换崩坏3 风格美术；
- 主学说图标暂用 `GFX_BH3_main_menu_doctrine`（旧学说入口图）；
- mastery 每档新增 150 点为当前定调（见上），若游戏内实际积累节奏仍偏快/偏慢可再调该常数；
- 互斥对以 `available` 互锁实现（选中一侧后另一侧不可选），与原版的"选中即锁"口径一致。
