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
