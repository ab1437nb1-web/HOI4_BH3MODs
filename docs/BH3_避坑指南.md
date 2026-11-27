# BH3 mod 开发避坑指南

> 记录本项目实际踩过的坑，按“最容易再犯”排序。新写内容前先扫一遍。

---

## 1. 文件编码与换行（最高频）

| 坑 | 现象 | 正确做法 |
|---|---|---|
| PowerShell 5.1 读取无 BOM 的 UTF-8 脚本 | 中文路径变成乱码、Test-Path 找不到文件 | 脚本存 UTF-8 with BOM；或路径放环境变量 |
| 给**脚本 .txt**（abilities/decisions/effects 等）加 BOM | 整份文件不加载：技能消失、决议组消失，且日志不一定报错 | 脚本 .txt 一律**无 BOM**（UTF-8）；只有本地化 .yml 需要 BOM |
| HOI4 本地化 .yml 无 BOM | 文本不生效、界面显示 key | .yml 一律 UTF-8 BOM + l_english: 头 |
| Python 文本模式写文件（Windows） | 整个文件 LF→CRLF，GUI 出现 2281 行大 diff | 用 open(...,'wb') 写字节，或 newline='' |
| 仓库 .gitattributes 是 * -text | git 不做换行转换，字节即内容 | 改完看 git show --stat，行数异常=换行事故 |

---

## 2. GUI 与 Scripted GUI

1. window_name 必须等于 .gui 里 containerWindowType 的 name，差一个字母窗口就不显示。
2. 按钮效果名 = 元素 name + _click（如 BH3_ER_advance_btn → BH3_ER_advance_btn_click）。
3. 元素显隐/可用：在 scripted_gui 的 triggers 里写 <元素名>_visible / <元素名>_enabled（原版 MTG 有先例）。
4. parent_window_name 的父窗口必须在同一文件里更早注册，否则子窗口会跑到屏幕左上角。
5. 所有 spriteType / quadTextureSprite / iconType 引用的 sprite 必须真实存在；引用不存在的 sprite 通常是静默不显示，很难排查。
6. 窗口打不开的排查顺序：入口按钮 _enabled 触发器 → 父窗口 flag → 子窗口 flag → window_name 拼写 → sprite 路径。
7. 入口按钮点击时顺手把父窗口 flag 也置上（set_country_flag = BH3_main_menu_open），否则父窗口一关子窗口就“无反应”。
8. 背景图用 PNG 也能被 spriteType 引用（本 mod 已验证），不必强转 DDS；1400×700 实测可用。

---

## 3. 修饰符作用域（本项目最贵的教训）

| 写法 | 结果 |
|---|---|
| str_damage_multiplier / org_damage_multiplier 写在国家精神 / 动态修正 | tooltip 正常显示，实战无效 |
| 同样数值写在指挥官技能 unit_modifiers | 有效（实测锁血） |
| 指挥官技能 | 没有脚本激活接口，只能玩家点；数值静态，不能用变量 |

结论：

- “无敌 / 结界”类效果 → 只能做指挥官技能；
- 常驻减伤 → 用 army_defence_factor 等普通国家修正；
- 不要指望“层数变量 → 减伤百分比”这种渐变写法（国家级无效，技能数值静态）。

---

## 4. 伤害与空中支援

- CAS 伤害只能由真实 air wing 产生：约每 8 小时结算一次（HOURS_DELAY_AFTER_EACH_COMBAT = 4 双程），夜间 ×0.1，AA 最高 −75%，没有“无飞机注入 CAS”的接口。
- 需要持续真伤时用 damage_units（直接扣 org/str，天然无视防御），用 on_daily 按天 tick。
- 动态修正的数值可以取变量，但只对“国家级有效”的修正有意义。

---

## 5. 决议

- 决议必须挂在已存在的 category 下；category 的 icon 也要有效 sprite。
- has_equipment / add_equipment_to_stockpile 用 archetype（BH3_FlawlessKey_equipment），不是 _0 变体。
- 调试决议单独分组（is_debug），不要混进正常组，否则未解锁时根本看不到。
- 决议 icon 写 GFX_ 前缀的 sprite 名。

---

## 6. 数据抓取（官方百科）

- 官方百科是 Nuxt SPA，直接抓 HTML 只有空壳；用 chrome --headless=new --dump-dom 渲染后再解析。
- 往世乐土的分区：
  - 刻印：channel/map/22（12 个词条页）
  - 追忆（剧情）：channel/map/22/198
  - 物品（追忆之证）：channel/map/22/33 ← 之前漏过，别只看“追忆”栏目
- 本机不可达：fandom、米游社、hoyolab；可用：官方百科、9game、小米游戏中心、mcmod。
- 游戏本体的 common/defines/00_defines.lua 与 localisation/*.yml 是最可靠的字典（例如 ORG_UNIT_WEAK = 0.25、MODIFIER_ORG_LOSS_AT_LOW_ORG_FACTOR 的显示名）。

---

## 7. Git

- amend 后需 git push --force-with-lease；强推前确认没有别人拉过。
- 大文件（dds/wav/ogg/mesh/anim/psd）走 .gitignore，美术资源可复用但别入库。
- 每次提交后看 git show --stat：行数异常通常是换行/编码事故，先修再推。

---

## 8. 测试技巧

- 先用 is_debug 决议注入资源（+500 无瑕之钥）快速跑完流程，再测真实节奏。
- 逻辑先用决议验证，通过后再搬进 GUI（GUI 调试成本高很多）。
- 没有 ffmpeg 时可用 WPF MediaPlayer + RenderTargetBitmap 抽帧看录屏。
- 不要用 add_ideas 去测“可能无效”的修饰符——工具本身会误导结论。


---

## 9. 实测补充（2026-11-25 运行日志）

以下三条是这次跑游戏后从 error.log 确认的，属于硬约束：

1. **common/scripted_effects 的子目录不加载**：放在 BH3_ER_signets/ 里的效果全部报 “Unknown effect-type”，按钮点了没反应。解法：文件放根目录，用前缀命名（BH3_ER_signets_*.txt）。
2. **决议的 allowed 块不接受 has_country_flag / is_debug**：报 “Token ... is not supported within the allowed trigger”。解法：allowed 只写 always = yes，真正的条件全部放 visible；调试决议靠 visible 里的 is_debug 控制显示。
3. **决议分类必须单独定义在 common/decisions/categories/**：把 category 定义写进 decisions 文件会报 “Unknown category”，且后续决议全部 “Unexpected token”。测试 mod 已按这个规则拆分。


---

## 10. 脚本环境补充

1. **不要在 %TEMP% 里建 enum.py / re.py / glob.py / types.py 这类文件**：python 脚本所在目录是 sys.path[0]，会遮蔽标准库，报 “partially initialized module 'glob' has no attribute 'glob'”。脚本名统一加前缀（zz_ 之类）或用独立目录。
2. 引擎日志里的 “not in script_enum_*” 属于**文档性枚举提示**，只要不是 “Value does not belong to designated Script EnumType”，一般不影响实际效果，不必逐个改。


---

## 11. damage_units 实测约束（2026-11-25）

- 必须给 location：damage_units 只在 state / province / region 指定时生效；在国家作用域里不写 location 完全无效（对照实验 A 无效、B 逐州生效）
- 标准写法：every_enemy_country → every_owned_state → damage_units { state = THIS limit = { has_war_with = ROOT } ... }
- is_enemy 不是合法触发器，用 has_war_with = ROOT
- else 块里不能带 limit，多分支要用 else_if
- 变量参数（org_damage = 变量）可用
- 统一 ratio = yes，按当前组织/兵力比例扣，天然无视防御

---

## 12. 数值系统与动态修正（2026-11-26 黄金事件复盘）

这次“高政治点攻防异常”非常典型，按排查顺序记录。

### 12.1 症状与真因

| 症状 | 真因 |
|---|---|
| 政治点不足 100 时攻击已 +625%、防御 +500% | 旧存档里同一个动态修正被重复 add 了多次；每个实例都读取同一组变量，于是翻倍叠加 |
| 政治点 +100%（设计只有 +20%） | 同一原因：0.20 乘 5 个实例 |
| 日志报 Unknown trigger-type: political_power | 正确触发器是 has_political_power（is_enemy 也不存在，用 has_war_with） |
| 清空黄金刻印后立刻回落到 +25%/+200% | 说明那 600%/300% 就是黄金 DM 的叠加值，不是别家系统 |

识别特征：数值恰好等于你设的安全上限（当初 atk 3.0 / def 3.0 的 clamp），几乎可以断定是“多实例叠加”或“变量被反复累加”。

### 12.2 add_dynamic_modifier 必须防重复

- HOI4 的 add_dynamic_modifier 不会因为同名而自动去重，重复调用就会叠加。
- 用一个国家旗标保护：

    if = { limit = { NOT = { has_country_flag = BH3_ER_dm_added } }
        add_dynamic_modifier = { modifier = BH3_ER_dm_dlv }
        set_country_flag = BH3_ER_dm_added
    }

- 旧存档里已经叠加的 DM，靠脚本只能 remove_dynamic_modifier 再重加；所以给调试组留一个「重建动态修正」按钮。

### 12.3 少用中间变量管线

一开始的实现是：政治点 → 30 个阈值 if → bucket → 乘 25 → 临时变量 gt → multiply/clamp → 输出变量。
层级越多，任何一步写错（触发器名、变量复制、clamp）都会让结果失真且难以定位。

改成直接按阈值累加后：

    set_variable = { BH3_ER_gold_atk = 0 }
    if = { limit = { has_political_power > 99 } add_to_variable = { BH3_ER_gold_atk = 0.15 } }
    if = { limit = { has_political_power > 199 } add_to_variable = { BH3_ER_gold_atk = 0.30 } }

可读、可核对、无中间态。

### 12.4 触发器名要查文档，不要凭记忆

- 政治点：has_political_power（不是 political_power）
- 交战：has_war_with（不是 is_enemy）
- 每日政治点：political_power_daily
- 变量里没有“读取国家数值”的通用接口，所以阈值触发是唯一可靠手段

### 12.5 没有办法打印变量时，用 log 标记

HOI4 没有“读取变量并显示”的接口，但可以用 log 效果往 game.log 写标记，再用 if 分档：

    if = { limit = { check_variable = { BH3_ER_gold_atk > 1.0 } } log = "BH3GOLD atk_100_200pct" }
    else = { log = "BH3GOLD atk_lt100pct" }

配合调试决议（点一次输出一段），就能在不改游戏 UI 的情况下读到变量所在区间。
这次就是靠 BH3GOLD 日志确认“重建后数值完全正常”。

### 12.6 录像排障

- 有 mp4 但没 ffmpeg 时，可以 pip install imageio imageio-ffmpeg，然后用 imageio.get_reader(path) 按帧号取图，比 WPF MediaPlayer 稳定。
- 逐帧对比“点按钮前/后”的数值，能直接算出某个系统贡献了多少。

### 12.7 检查清单（以后写数值系统先过一遍）

1. 所有 add_dynamic_modifier 是否都有旗标保护？
2. 触发器名是否在 triggers_documentation.md 里查过？
3. 有没有 else 块里塞 limit？（必须 else_if）
4. 输出变量是否每次 recalc 都先归零再累加？
5. 数值是否被安全 clamp 兜底？上限值是否和“疑似叠加值”重合（重合就先查叠加，别急着调 clamp）？
6. 是否留了 log 诊断决议和“重建 DM”调试按钮？

---

## 13. 伤害倍率的作用范围（2026-11-26 修正）

- unit_modifiers 里的 str_damage_multiplier / org_damage_multiplier = -1.0 只影响**陆战伤害**
- 不影响：核导弹袭击、战略轰炸等特殊打击；测试时它们照常生效
- 因此“无敌类”效果在描述里要写清楚是“陆战无敌/受到陆战伤害 -100%”，不要写成泛指的“免疫一切伤害”
- 测试方法论：单次随机事件（袭击成功/失败、判定命中）不能作为结论依据；至少重复 3~5 次或对比多组样本再下结论

## 14. GUI 里的脚本化本地化（defined_text）

- defined_text 不能直接用于 GUI 的 text= 或 pdx_tooltip=，会显示原始 key
- text 正确写法：context_aware_text = "[定义名]"
- tooltip 正确写法：context_aware_tooltip = "静态loc_key"，静态 key 的值写成 [定义名]（holder 中转）
- GUI 图标/按钮都用 name 区分，脚本化 GUI 的 <元素名>_visible 触发缺失时元素会常驻显示，新增图标务必逐槽补 visible 条件
