# BH3 mod 开发避坑指南

> 记录本项目实际踩过的坑，按“最容易再犯”排序。新写内容前先扫一遍。

---

## 1. 文件编码与换行（最高频）

| 坑 | 现象 | 正确做法 |
|---|---|---|
| PowerShell 5.1 读取无 BOM 的 UTF-8 脚本 | 中文路径变成乱码、Test-Path 找不到文件 | 脚本存 UTF-8 with BOM；或路径放环境变量 |
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
