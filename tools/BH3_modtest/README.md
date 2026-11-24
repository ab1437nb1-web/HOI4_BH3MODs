# BH3 Modifier Test — 受伤倍率最小测试

目的：实测 HOI4 是否接受

    str_damage_multiplier = -1.0
    org_damage_multiplier = -1.0

即「部队完全不损失兵力与组织度」。这是【浮生】「战士的回忆」无敌效果的关键前提。

## 一、这个 mod 里有什么

| 内容 | 说明 |
|---|---|
| 5 个国家精神（ideas） | -100% / -50% / 仅兵力 -100% / 仅组织度 -100% / +100%（对照） |
| 6 个决议（decisions） | 分别添加上面 5 个精神 + 一键全部移除 |
| 中英文本地化 | 精神与决议的 tooltip |

精神列表：

| 精神 ID | 效果 |
|---|---|
| BH3_test_immune | str -1.0 / org -1.0 |
| BH3_test_half | str -0.5 / org -0.5 |
| BH3_test_str_only | str -1.0 |
| BH3_test_org_only | org -1.0 |
| BH3_test_double | str +1.0 / org +1.0（对照） |

## 二、启用

1. 文件夹已放在：文档/Paradox Interactive/Hearts of Iron IV/mod/BH3_modtest
2. 启动器 → 模组 → 勾选「BH3 Modifier Test - Damage Taken」
3. 新开一局（任意国家都行，推荐德国，方便立刻打波兰）

如果启动器没显示，用启动参数：-mod=mod/BH3_modtest

## 三、测试步骤（按顺序，每步记录）

### 步骤 1：确认 modifier 被游戏识别

1. 控制台输入：add_ideas BH3_test_immune
2. 打开国家精神面板，悬停「TEST: Damage Taken -100%」
3. 看 tooltip 里是否出现两行：
   - Organization Damage Taken: -100.0%
   - Strength Damage Taken: -100.0%

判定 A：两行都出现 → 词条被识别，继续步骤 2。
判定 B：没有出现或显示 0 → 该 modifier 在 ideas 里无效，测试直接结束，记录结论。

### 步骤 2：实战验证

1. 德国对波兰开战，挑一个双方都有 2~3 个师的省，进攻或防守 12~24 小时
2. 记录：我方师的组织度数值变化、兵力（strength）数值变化
3. 对照组：remove_ideas BH3_test_immune，同样打 12~24 小时，再记录一次

判定 A：完全免疫 → 数值纹丝不动，且敌方一样打不动你。
判定 B：只免疫一半（组织度不掉、兵力照掉，或反过来）→ 说明某个 modifier 被忽略。
判定 C：完全无效 → 数值正常下降，说明引擎钳制或忽略 -1.0。
判定 D：变成回血或异常 → 说明 -1.0 被当成乘数反转，属于危险写法。

### 步骤 3：符号方向对照

1. 换 add_ideas BH3_test_double（+100%）
2. 同样打一仗

若这时掉血明显变快 → 符号方向确认（负数=减伤）。
若没变化 → 说明这组 modifier 在 ideas 里整体失效，步骤 1 的判定要改成 B。

### 步骤 4：单变量定位

分别测 BH3_test_str_only 与 BH3_test_org_only，确认两个 modifier 各自的归属（兵力/组织度），避免把两者混为一谈。

### 步骤 5：查日志

打完一仗后看：

    Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log

搜索 str_damage_multiplier / org_damage_multiplier / unknown modifier，若有报错直接贴出来。

## 四、记录模板

| 测试 | tooltip 显示 | 组织度变化 | 兵力变化 | 结论 |
|---|---|---|---|---|
| BH3_test_immune | | | | |
| BH3_test_half | | | | |
| BH3_test_str_only | | | | |
| BH3_test_org_only | | | | |
| BH3_test_double | | | | |

## 五、已知边界（写测试前就确定的部分）

- 这些 modifier 是国家级 的，不能只作用于某个师。
- 它们只影响常规陆战伤害；CAS 伤害走 cas_damage_reduction，脚本 damage_units 直接改 org/str，理论上都不吃这两个倍率（需要另做测试确认）。
- -1.0 是否被引擎 clamp、-2.0 会怎样，官方文档没写，只能靠本测试确认。


---

## 六、v2：指挥官技能测试（2026-11-25 追加）

第一轮结论：**在国家精神（ideas）里这两个 modifier 会显示但没有实战效果**。
所以把它们搬到原版真正使用它们的地方——指挥官技能的 unit_modifiers 里。

新增 5 个技能（都在 common/abilities/BH3_modtest_abilities.txt）：

| 技能 ID | 效果 | 时长 |
|---|---|---|
| BH3_test_ability_immune | str -1.0 / org -1.0 | 168 小时 |
| BH3_test_ability_half | str -0.5 / org -0.5 | 168 小时 |
| BH3_test_ability_str_only | str -1.0 | 168 小时 |
| BH3_test_ability_org_only | org -1.0 | 168 小时 |
| BH3_test_ability_double | str +1.0 / org +1.0 | 168 小时 |

### 测试步骤

1. 新开一局德国（或读取已有存档，只要技能没变）。
2. 把 2~3 个师编给一个有指挥权的将领（ Corps Commander 即可，技能在将领面板下方那一排按钮里）。
3. 对荷兰/波兰进攻，开打后**暂停**，点「测试技能：受伤 -100%」（cost 0，立刻可用）。
4. 观察 168 小时内：我方师的组织度、兵力是否变化；敌方是否打不动你。
5. 对照：
   - 同一场战斗，等技能过期后再看一次；
   - 或换 BH3_test_ability_double（+100%），看掉血是否明显变快（验证符号）；
   - 或分别用 str_only / org_only 定位两个 modifier 各自管什么。

### 判定

| 现象 | 结论 |
|---|---|
| 技能生效期间组织度/兵力完全不动 | **unit_modifiers 里 -1.0 有效** → 浮生可用“能力版无敌” |
| 只一项不动 | 只有部分 modifier 在 unit_modifiers 里被接受 |
| 完全没变化 | unit_modifiers 也不接受 -1.0（或被钳制），改用 org_loss_at_low_org_factor 方案 |
| 掉血变快/异常 | 符号被反转，禁止使用 |

### 注意

- 技能按钮若没出现：确认将领是 Corps Commander（不是 Army Group 司令），并检查 error.log 里有没有 ability 相关报错。
- 技能是“作用于该将领麾下部队”，所以必须让被测师归属该将领。
- ideas 里的那 5 个精神仍然保留，作为“国家级无效”的对照证据。
