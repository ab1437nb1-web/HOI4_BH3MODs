# 往事乐土「刻印」系统移植方案（v2，仅方案，未实施）

范围：先做除 **真我（爱莉希雅）** 外的 **12 类刻印**；真我作为"定制刻印"生态位留到 P3。

**v2 变更（按用户 2026-10-06 决定）**：开启乐土改为**特殊项目**（与神之键/次时代同级）；项目完成后解锁决议组并可**制造「无瑕之钥」**；**每次抽取消耗钥匙**；**不再使用周期性事件**。

---

## 一、结论摘要

1. 原作乐土的体验是"**攒资源 → 抽刻印 → 凑核心 → 升增幅**"。HOI4 侧用「**特殊项目开门 → 生产钥匙 → 决议抽取（三选一）→ 分级 idea 承载**」即可复刻，且不需要新做 GUI。
2. 抽取的经济来源从"每层通关"换成"**生产「无瑕之钥」**"——抽取频率因此受产能约束，天然形成节奏。
3. 13 英桀 ↔ 13 刻印与各自象征物已**全部查证到可引用来源**；每枚刻印的层数与加成按主题给出**提案**，落地前建议逐条核对。
4. 12 类刻印各占一个**互不重叠的战术生态位**（突破/机动/预判/后勤/狂战/稳健/防御/机械/再生/压制/混编/经济），不与神之键（装备模块）、MIO（生产与特质）抢位。
5. 关键语法已用**游戏自带文档 + 原版真实用例**验证：`has_equipment = { <装备> >= N }`（触发器）、`add_equipment_to_stockpile = { amount = -N }`（扣库存）。

---

## 二、原作机制（已查证）

### 2.1 十三英桀 ↔ 十三刻印

来源：小米游戏中心《英桀刻印 LOGO 构图分析》[上篇](https://game.xiaomi.com/viewpoint/1190871803_1653663864318_13) / [下篇](http://game.xiaomi.com/viewpoint/1190871803_1654350730937_13)、九游《救世第二套刻印》[评测](https://www.9game.cn/bhxy3/10090735.html)（该文原文：*"在乐土之中一共有十三位英桀，因此，有十三种刻印。分别是救世、真我、戒律、黄金、螺旋、鏖灭、天慧、刹那、旭光、无限、繁星、浮生、空梦。"*）

| # | 刻印 | 英桀 | 象征物（考据结论） | 本次范围 |
|---|---|---|---|---|
| 1 | 救世 | 凯文 | 天火圣裁巨剑 + 碎裂晶体 | ✅ |
| 2 | **真我** | **爱莉希雅** | 花 | ❌（定制刻印，P3） |
| 3 | 戒律 | 阿波尼亚 | 蝴蝶 + 十字项链（密多罗） | ✅ |
| 4 | 黄金 | 伊甸 | 音符 + 胶卷盘 + 酒杯 | ✅ |
| 5 | 螺旋 | 维尔薇 | 扭曲怀表 + 齿轮 + 5 个人格 | ✅ |
| 6 | 鏖灭 | 千劫 | 木雕面具 + 飘带（非天/阿修罗） | ✅ |
| 7 | 天慧 | 苏 | 叶 + 四尖角（四大）+ 慧眼 | ✅ |
| 8 | 刹那 | 樱 | 樱花 + 太刀柄 | ✅ |
| 9 | 旭光 | 科斯魔 | 四角 + 六芒星 + 藤蔓（毗湿奴） | ✅ |
| 10 | 无限 | 梅比乌斯 | 三角 + 衔尾蛇（∞）+ 耳坠 | ✅ |
| 11 | 繁星 | 格蕾修 | 调色板 + 星星 + 画笔 | ✅ |
| 12 | 浮生 | 华 | 先天/后天八卦 + 太极（羽渡尘） | ✅ |
| 13 | 空梦 | 帕朵菲莉丝 | 猫爪 + 金币 + 珠宝 + Ω 圆环 | ✅ |

### 2.2 刻印的三层结构

- **核心刻印**：每派系 1 枚，是派系开关，提供机制性效果；
- **普通刻印**：每派系若干枚，互相叠加，是数值主体；
- **增幅刻印**：需**先有核心**才可获取，进一步放大普通刻印。

### 2.3 计数/阈值机制

以**救世**为例（来源：九游评测）：核心「救世者的孤影」= 必杀/爆发命中 50 次后进入【救世之战】，**普通刻印加成永久生效**；增幅「决断」每次命中 +0.5% 全伤（上限 +50%）、「残梦」状态中普通刻印 +50%、「凯旋」进入时 6~10 秒无视防御并留下 +20% 易伤。

**移植结论**：HOI4 无法逐击计数 → 一律换成可表达的状态量（战斗天数／是否进攻方／组织度百分比／是否满编／是否夜间／兵种类别／政治点余额等）。

---

## 三、系统流程（v2 主干）

```
① 特殊项目「开启往事乐土」
     project_output:
        enable_equipments = { BH3_FlawlessKey_equipment }      # 解锁无瑕之钥的生产
        add_ideas         = { BH3_ElysianRealm_unlocked }      # 决议组开门标记
   　　 (可选) enable_equipment_modules = { 刻印相关模块 }
        ↓
② 决议组「往事乐土」可见（available 用 has_idea = BH3_ElysianRealm_unlocked 门控）
     ├─ 抽取决议「进入乐土·试炼」：消耗 N 把无瑕之钥 → 触发三选一事件
     ├─ 决议「重置刻印」：清空全部刻印，返还 50% 已投入
     └─ 决议「查看刻印」：custom_effect_tooltip / show_ideas_tooltip 展示当前派系与层数
        ↓
③ 抽取（决议 → 事件 BH3_ElysianRealm.1）
     available = { has_equipment = { BH3_FlawlessKey_equipment >= 1 } }
     complete_effect = {
        add_equipment_to_stockpile = { type = BH3_FlawlessKey_equipment amount = -1 }   # 扣钥匙
        country_event = { id = BH3_ElysianRealm.1 }                                     # 三选一
     }
     事件三个选项 = random_list 抽出的三枚刻印（未持有的权重高；已有核心的派系可抽到增幅）
        ↓
④ 刻印落地为分级 idea（普通 Ⅰ/Ⅱ/Ⅲ、核心、增幅），槽位上限 6 个派系
```

### 3.1「无瑕之钥」装备

| 项 | 建议 |
|---|---|
| ID | `BH3_FlawlessKey_equipment` |
| 类型 | 建议新建材料类 `type = BH3_material`（不与步兵/支援装备混用）；若想省事可用原版 `support_equipment` |
| 可制造 | `is_buildable = yes` + `active = yes`（生产界面直接开线） |
| 造价 | **10~25 IC**（提案；越贵则刻印成型越慢，是唯一的节奏旋钮） |
| 单次抽取消耗 | **1 把**（提案；可调成 2~3 把以进一步放慢） |
| 图标 | 可直接用截图中「无瑕之钥」的粉色钥匙图标（用户可提供素材） |

### 3.2 已核验的语法（官方文档 + 原版用例）

| 用途 | 写法 | 证据 |
|---|---|---|
| 检查钥匙数量 | `has_equipment = { BH3_FlawlessKey_equipment >= 1 }` | 原版 `CZE.txt:168 has_equipment = { infantry_equipment > 5000 }` |
| 扣钥匙 | `add_equipment_to_stockpile = { type = BH3_FlawlessKey_equipment amount = -1 }` | 文档：*"Equipment will be removed if the value is negative"*；原版 `AFG.txt:1740 amount = -2000` |
| 项目给标记 idea | `project_output = { add_ideas = { ... } }` | 本 mod 已在 `project_output` 中使用 `add_ideas` |
| 项目解锁装备 | `project_output = { enable_equipments = { ... } }` | 本 mod 已在次时代/神之键项目中使用 |

---

## 四、载体与作用域

| 项 | 设计 |
|---|---|
| 决议组 | 新增 `common/decisions/BH3_ElysianRealm_decisions.txt`，门控用 `has_idea = BH3_ElysianRealm_unlocked` |
| 刻印载体 | 新增 `common/ideas/BH3_ElysianRealm_idea.txt`，普通/核心/增幅均为分级 idea（参照 mod 现有 `BHS_levelN_idea` 写法） |
| 抽取事件 | `events/BH3_ElysianRealm_event.txt`（仅由抽取决议触发，**不再挂 on_action**） |
| 陆军作用域 | `modifier_army_sub_unit_category_AllValkyrie_*` / `AllHerrscher_*`（本 mod 已有此类修正键） |
| 空军作用域 | `modifier_air_sub_unit_category_*` —— **P1 第一件事就是验证该前缀在本版本可用** |
| 国家层面 | 生产/政治点/补给/造价等常规修正 |

---

## 五、12 类刻印的移植映射（提案，待逐条确认）

| 刻印 | 英桀 | 原作主题 | HOI4 生态位 | 核心刻印提案 | 增幅方向 |
|---|---|---|---|---|---|
| 救世 | 凯文 | 巨剑、守护、爆发/大招 | **突破爆发** | 进攻方作战满 30 天后，本派系普通刻印效果 **×1.5**（对应"救世之战永久生效"） | 突破伤害、首日突击、无视堑壕 |
| 刹那 | 樱 | 樱花、太刀、极速 | **机动突进** | 师速度 +X%，**战斗首小时**攻击 +Y%（对应"刹那一刀"） | 主动性、撤退损失减免、受击减伤 |
| 天慧 | 苏 | 叶、慧眼、因果预知 | **情报预判** | 侦察 +X，计划加成上限提高 | 计划速度、反侦察、伏击抗性 |
| 黄金 | 伊甸 | 音符、酒杯、能量 | **后勤产能** | 政治点/燃油/补给产出 +X% | 生产效率、补给消耗、战略转移 |
| 鏖灭 | 千劫 | 面具、怒火、受伤换输出 | **狂战换血** | 组织度 <50% 时攻击 +X%（原作"失去生命加伤"） | 攻击↑/组织度↓、HP 换突破、溃败抗性 |
| 浮生 | 华 | 太极、八卦、无伤 | **稳健续航** | **未受损**（组织度 ≥90%）时全属性 +X% | 受损后回复、韧性、持续作战 |
| 戒律 | 阿波尼亚 | 修女、蝴蝶、蓄力格挡 | **防御抵抗** | 防御 +X%、堑壕上限 +1 | 反装甲、抗压制、要塞加成 |
| 螺旋 | 维尔薇 | 怀表、齿轮、机械 | **装备机械** | 可靠性 +X%、装甲 +Y% | 维修速度、装备损失减免、缴获率 |
| 无限 | 梅比乌斯 | 衔尾蛇、∞、生命 | **再生补员** | 补员 +X%、人力损耗 −Y% | HP 上限、伤兵回收、组织度回复 |
| 旭光 | 科斯魔 | 黑暗、压制、恶魔 | **压制夜战** | 对敌组织度伤害 +X%、夜战惩罚减半 | 夜间攻击、恐惧、镇压 |
| 繁星 | 格蕾修 | 调色板、画笔、创造 | **混编协同** | 每多一种兵种类别在场，全属性 +X% | 混编上限、协同攻击 |
| 空梦 | 帕朵菲莉丝 | 猫爪、金币、珠宝、终结 | **经济造价** | 装备造价 −X%、资源获取 +Y% | 生产效率、租借、贸易 |

---

## 六、数值口径（与现有 mod 尺度对齐）

| 项目 | 建议 |
|---|---|
| 单枚普通刻印 | +5%~+15%（作用域窄取高值） |
| 一派系满配（3 普通 + 核心 + 2 增幅） | 该生态位 +40%~+70% |
| 6 派系满配 | 总体 +120%~+200%（**低于**"圣芙蕾雅满 MIO + 神之键"量级，保持"配件 > 刻印"层级） |
| 造价/经济类 | 单枚 −5%~−10%，满派系 −25%~−35%；与 MIO 的 −40% 叠加后需复核，避免负造价 |
| 校验 | 沿用本项目口径：算"每 IC 战力"，确认刻印满配仍满足"≥2.7× 原版同级"且不破坏单调性 |

---

## 七、实现清单

| 文件 | 内容 |
|---|---|
| `common/units/equipment/BH3_ElysianRealm_material.txt` | `BH3_FlawlessKey_equipment`（可制造材料） |
| `common/special_projects/projects/BH3_special_projects.txt`（追加） | 特殊项目「开启往事乐土」：`enable_equipments` + `add_ideas` |
| `common/decisions/BH3_ElysianRealm_decisions.txt` | 决议组 + 抽取/重置/查看 |
| `events/BH3_ElysianRealm_event.txt` | 三选一抽取事件（仅决议触发） |
| `common/ideas/BH3_ElysianRealm_idea.txt` | 12 派系 ×（3 普通 + 1 核心 + 2 增幅）≈ 72 个 idea |
| `common/scripted_effects/BH3_ElysianRealm_scripted_effects.txt` | 抽取、去重、槽位上限判定、重置 |
| `localisation/simp_chinese/...` + 英文 | 决议/事件/idea/装备/提示（UTF-8 带 BOM） |
| `gfx/...` + `.gfx` | 13 枚刻印图标 + 无瑕之钥图标（可先用占位） |

---

## 八、分期实施（PDCA）

| 阶段 | 交付 | 验收点 |
|---|---|---|
| **P1 最小闭环** | 特殊项目 + 无瑕之钥装备 + 决议组 + 抽取事件 + **救世**完整一条线（3 普通 + 核心 + 2 增幅） | 项目完成后决议组出现；能造钥匙、能扣钥匙、能抽到刻印、能叠加与重置；`modifier_air_sub_unit_category_*` 是否可用得到确认 |
| **P2 铺开 12 派系** | 12 派系各 3 普通 + 核心；增幅先做救世/刹那 | 数值表过一遍；造价类不与 MIO 叠加出负数 |
| **P3 补全与定制刻印** | 其余增幅；**真我（爱莉希雅）定制刻印**（自选词条设计）；可选 scripted GUI | 与神之键/MIO 叠加上限复核 |

---

## 九、待你确认（落地前拍板）

1. **无瑕之钥造价**与**单次抽取消耗**（提案：10~25 IC / 每次 1 把）？
2. **槽位上限**几个派系？（提案 6）
3. 刻印是否对**空军（空中女武神 / 律者级）**同样生效？（生效则 P1 先验证 `modifier_air_sub_unit_category_*`）
4. **AI 是否也要能拿刻印**？（要则在 AI 启用链路里加自动选刻印逻辑）
5. 12 派系的**主题→生态位**映射是否认可？尤其 **繁星=混编**、**空梦=经济**、**旭光=压制** 这三条是设计化处理。
6. 「无瑕之钥」的**装备类型**：新建材料类 `BH3_material`（推荐）还是复用原版 `support_equipment`？

---

## 十、来源

- 十三刻印名单：[九游《崩坏3救世第二套刻印怎么样》](https://www.9game.cn/bhxy3/10090735.html)
- 刻印 ↔ 英桀 对应与象征物：[小米游戏中心《英桀刻印 LOGO 构图分析（上）》](https://game.xiaomi.com/viewpoint/1190871803_1653663864318_13) / [（下）](http://game.xiaomi.com/viewpoint/1190871803_1654350730937_13)
- 语法证据：游戏自带 `documentation/triggers_documentation.md`、`effects_documentation.md` + 原版 `CZE.txt`、`AFG.txt` 用例

---

## 十一、实施记录：P1 已完成（2026-10-06）

按用户决定落地：**特殊项目开门 + 可生产「无瑕之钥」+ 每次抽取消耗钥匙 + 刻印以民族精神承载（同时作用于陆军与空军）**。

### 已创建/修改的文件

| 文件 | 内容 |
|---|---|
| `common/units/equipment/BH3_ElysianRealm_material.txt` | 新增 `BH3_FlawlessKey_equipment`（archetype）+ `_0`（可生产）。**造价 250 IC**（比最便宜的神之键模块 300 IC 略低，符合"可以对标神之键但稍便宜"），`type = support_equipment`（不与本 mod 任何兵种的装备需求冲突） |
| `common/special_projects/projects/BH3_ElysianRealm_projects.txt` | 新增特殊项目 `BH3_sp_ElysianRealm_Open`（**独立新文件，避免冲突**）；`project_output` = `enable_equipments = { BH3_FlawlessKey_equipment_0 }` + `country_effects = { set_country_flag = BH3_ElysianRealm_unlocked }` |
| `common/ideas/BH3_ElysianRealm_idea.txt` | 救世 5 个民族精神：普通 Ⅰ/Ⅱ/Ⅲ（各 突破 +8%、陆军攻击 +4%、空军攻击 +4%）、核心「救世者的孤影」（突破 +20%、陆军攻击 +8%、**空军攻击 +10%**、组织度 +5、计划速度 +15%）、增幅「救世者的残梦」（突破 +25%、陆军攻击 +10%、**空军攻击 +15%**、核心省份攻击 +10%） |
| `common/decisions/BH3_ElysianRealm_decisions.txt` | 决议组「往事乐土」：`抽取刻印`（`available` = 有标记 + `has_equipment = { BH3_FlawlessKey_equipment >= 1 }`；`complete_effect` = `amount = -1` 扣钥匙 + 触发事件）、`重置刻印`（移除 5 个精神 + 返还 3 把钥匙） |
| `events/BH3_ElysianRealm_event.txt` | `BH3_ElysianRealm.1`（`is_triggered_only`）：**5 个带 `trigger` 的选项**按 Ⅰ→Ⅱ→Ⅲ→核心→增幅 的持有关系呈现，另有兜底选项（+25 政治点）避免"事件无选项"卡死 |
| `common/special_projects/project_tags/BH3_special_projects_tags.txt`（追加） | 新增 `BH3_sp_tag_BH3_ElysianRealm` |
| `localisation/simp_chinese/BH3_ElysianRealm_l_simp_chinese.yml` + 英文 | 29 键 × 2（装备/项目/tag/决议/事件/5 个精神），UTF-8 **带 BOM** |

### 与方案的差异与说明

1. **图标暂用占位**：项目图标复用 `GFX_BH3_sp_ValkyrieArmor_Engine_HonkaiImproved`，决议图标复用 `GFX_decision_BH3_SaintFreyaCollege`（两者均已确认存在），等有刻印/钥匙素材再替换；
2. **"三选一"在 P1 的实现**：因为 P1 只有救世一条线，事件改为**按进度呈现 5 个选项**（等价于"选下一步拿哪枚"）；P2 铺开 12 派系时再在选项内用 `random_list` 做跨派系随机；
3. **重置返还**：方案里的"返还 50%"在 P1 用固定 **3 把钥匙**近似（精确按持有计算需要额外脚本，留到 P2）；
4. **空军加成**：直接使用国家修正 `air_attack_factor`（已确认原版存在），因此**不需要**验证 `modifier_air_sub_unit_category_*`，空军自然受益；
5. **`breakthrough_factor`** 而非 `army_breakthrough_factor`（后者不存在，已查原版修正表确认）。

### 待办（P1 之后的下一步）

- P2：12 派系铺开（每派系 3 普通 + 核心），事件改为跨派系 `random_list`；
- P2：把 `无瑕之钥` 的**生产条件**与 mod 的研究设施/特殊化挂钩（当前项目完成后即可生产）；
- P3：增幅刻印补全 + **真我（爱莉希雅）定制刻印**；
- 素材：13 枚刻印图标 + 无瑕之钥图标（当前占位）。

### 追加改造：刻印改为"状态触发式"（同日，按用户指示）

**问题**：原作所有刻印都是**状态触发式**效果（例：凯文的加成几乎只在开启必杀技后生效），而首版 P1 写成了无条件常驻加成，丢掉了刻印的灵魂。

**改法**：
- 加成从民族精神里**移出**，改为 **`common/dynamic_modifiers/` 动态修正**，每个刻印一个，统一 `enable = { has_war = yes }` → **只在开战状态下持续生效**（对应"开启必杀技后生效"的移植）。
  - 说明：HOI4 的民族精神**不支持条件修正**，所以"可见的刻印"（民族精神，纯标记）与"真正的加成"（动态修正）分离；抽取时两者同时授予，重置时同时移除。
  - 实现依据：原版 `documentation/effects_documentation.md` 的 `add_dynamic_modifier` / `remove_dynamic_modifier` + 动态修正示例中的 `enable` 字段（本 mod 自身也在用 `add_dynamic_modifier`）。
- **完全体数值对标神之键「第零额定功率」**：参照物见 `BH3_TheDivineKeys_decisions.txt`（天火圣裁 `army_attack_factor = 1.5`、10 天；涤罪七雷 `air_attack_factor = 1`、180 天）。改后救世**满配合计**：

| 属性 | 首版（已废弃） | 现在（开战状态下） |
|---|---|---|
| 陆军攻击 | +22% | **+105%** |
| 突破 | +49% | **+124%** |
| 空军攻击 | +27% | **+105%** |
| 其他 | 组织度 +5、计划速度 +15% | 组织度 +5、核心省份攻击 +15%、计划速度 +25% |

（分档：普通 Ⅰ/Ⅱ/Ⅲ 各 陆军攻击 +15%/突破 +18%/空军攻击 +15%；核心 陆军攻击 +25%/突破 +30%/空军攻击 +25%/组织度 +5；增幅 陆军攻击 +35%/突破 +40%/空军攻击 +35%/核心省份攻击 +15%/计划速度 +25%。）

**P2 需要同步调整**：其余 11 派系全部按此模式落地（每派系 5 个民族精神=标记 + 5 个动态修正），且各自的"状态"可按主题细化（例：鏖灭=组织度低于 50%、浮生=组织度高于 90%、旭光=夜间，而不再统一用 `has_war`）。
---

## 十四、往事乐土 P1 验收与排错记录（2026-10-06）

### 验收结果：**P1 在游戏内实测可用** ✓

用户实测（德国 1936 档）：项目完成后，决议「进入乐土·抽取刻印」可点击，消耗钥匙抽取刻印成功；**开战时出现 5 个带图标的加成**（正是设计意图：动态修正 `enable = { has_war = yes }`），停战后消失。

存档证据（`GER_1936_01_17_14.hoi4`）：

| token | 次数 | 含义 |
|---|---|---|
| `BH3_ElysianRealm_unlocked` | 1 | 项目 `country_effects` 的标记已置 |
| `BH3_ElysianRealm_draw` | 1 | 抽取决议成功执行（修复前为 0） |
| `BH3_FlawlessKey_equipment_0` | 449 | 钥匙存在于存档 |
| `BH3_ER_Savior_1_dm` … `_Amp_dm` | 各 1，紧邻 | 5 个动态修正已挂到国家上 |

### 排错过程发现并修掉的问题（按发现顺序）

| # | 问题 | 状态 |
|---|---|---|
| 1 | 特殊项目文件里 `enable_equipment_modules` 混入了装备名 `BH3_ValkyrieAir_ala_4`（应只在 `enable_equipments`） | 已修 |
| 2 | 描述符 `supported_version = "1.*"` → 启动器判定非法 | 已修为 `1.19.*`（三处） |
| 3 | 独立本地化文件会导致装载期崩溃（**29 键/3 键/纯 ASCII 三版均崩；同键并入 mod 现成文件后正常**） | **已绕开**：键并入 `BH3_equipment_l_simp_chinese.yml` 与 `BH3_equipment_l_english.yml`；**根本原因未查明**，留待后续 |
| 4 | 事件描述键 `.1.d` 与"选项 d"撞车（mod 惯例是 `.t`/`.d`/`.a~.c`，我用了 6 个选项） | 已修：描述改用 `.1.desc` |
| 5 | 装备 `type` 写成原型名（`support_equipment`）→ 非法取值 | 已修为 `infantry`（与已验证的"女武神作战人员"装备一致） |
| 6 | 可生产装备缺 `graphic_db` 图标池（全 mod 唯一例外） | 已补 `BH3_ElysianRealm_icons.txt`（图标取自陆战装甲池） |
| 7 | 决议 `available` 用了 `has_equipment = { ... >= 1 }`；**原版 20 处用例只有 `>` / `<`，`>=` 不受支持** → 条件恒不满足 → 决议永远灰着 | 已修为 `> 0` |

### 遗留事项

1. **崩坏研究设施前置条件**：`BH3_Build_HonkaiFacility` 仅在"世界上已有他国原版研究设施"时才建（1936 开局通常没有），导致崩坏系特殊项目（含本 mod 原有神之键项目）可能无处可研究——待用户决定是否改为"直接建/定期补建"；
2. **独立本地化文件崩溃之谜**：现象稳定复现（我自己的 yml 文件在场即崩，不在场即正常），但内容/编码/行尾/键名均已排除；当前以"并入 mod 文件"绕开，后续若要新增独立 loc 文件需先做小样本验证；
3. **P2**：其余 11 派系（每派系 3 普通 + 核心 + 增幅）、跨派系随机抽签、重置按持有精确返还；各派系的"状态条件"按主题细化（鏖灭=组织度低、浮生=组织度高、旭光=夜间等）；
4. **P3**：真我（爱莉希雅）定制刻印；13 枚刻印与钥匙的专属美术。

---

## 十二、实施记录：抽取机制原作化 + GUI 化（2026-10-09）

### 目标

1. **抽卡机制与原作一致**：原作每层是"三扇传送门 → 门内三枚刻印选其一"；旧实现是"决议 → 事件选类别 → 盲抽派系"。改为**一次性给出三个具体候选（系徽可见），点选其一获得该系下一枚刻印**。
2. **整体迁出决议组**：往事乐土的全部交互（抽取 / 放弃 / 重置 / 12 系持有展示 / 无限增殖 / 空梦交易所）从决议列表迁入 GUI 窗口。
   - 2026-10-09 白天版：挂在决议分类面板上（`context_type = decision_category` 内嵌）——**当晚被用户否定**（用户要求接入崩坏3主菜单体系，而非在决议界面自创界面）。
   - 2026-10-09 夜晚定稿：**主菜单子窗口模式**，与「女武神科技」「作战学说」并列。

### 新抽取规则（与原作逐条对应）

| 原作 | mod 实现 |
|---|---|
| 进入刻印门，门内随机 3 枚刻印，三选一 | 点「进入试炼」（50 把钥匙）→ `random_list`（变量权重）生成 3 个互不重复的候选派系（`BH3_ER_cand1/2/3`）→ 界面显示 3 张候选卡（系徽图标，悬停显示该系**下一枚**刻印的完整名称与效果） |
| 重复获得同系刻印 = 升级 | 同系自动递进 Ⅰ→Ⅱ→Ⅲ→核心→增幅（授予链 `BH3_ER_grant_<系>` 按持有进度给下一枚） |
| 集齐 3 枚普通 → 核心入池 | 权重规则：未到 Ⅲ 的系权重 1；有 Ⅲ 无核心 → 候选给核心；有核心无增幅 → 候选给增幅；全齐 → 权重 0 |
| 门数恒为 3 | 候选不足 3 个时给出「放弃本次（全额返还 50 钥匙）」；全部集齐后抽取按钮禁用 |
| —（原作无） | 重置按钮：清空全部刻印返还 25 钥匙（沿用旧口径） |

### 文件清单

| 文件 | 内容 |
|---|---|
| `common/scripted_effects/BH3_ElysianRealm_scripted_effects.txt`（新） | `BH3_ER_roll_candidates`（权重计算+三轮抽取，抽中即清零权重防重复）、`BH3_ER_cancel_draw`、`BH3_ER_reset`、`BH3_ER_grant_<系>`×12（含各系核心/增幅的多动态修正组合与刹那核心特技）、`BH3_ER_pardofelis_sell_<1..3>`；**10-09 夜修复权重 bug**：原逻辑「无Ⅲ才给权重」导致集齐 Ⅲ 后核心/增幅永不可抽、候选随持有数增加而缺失，改为「有增幅=0，其余均为 1」（授予链自动递进，核心/增幅自然入候选） |
| `common/scripted_guis/BH3_ElysianRealm_scripted_gui.txt`（新，主菜单版） | `BH3_ER_menu`：`context_type = player_context`，`parent_window_name = "BH3_main_menu"`，`visible = has_country_flag = BH3_ER_menu_open`；3 主按钮 + 36 候选卡（3 槽 × 12 系）+ 7 无限增殖 + 3 空梦交易 + 12 系徽 + 返回钮的 effects/triggers |
| `interface/BH3_ER_menu.gui`（新） | **全屏覆盖式主界面**（1400×700 UPPER_LEFT，与科技/学说菜单同规格；10-09 夜由 460×545 悬浮窗改为全覆盖，背景换 `GFX_BH3_tech_menu_bg` 深蓝底以提升白系徽可读性；右上 `GFX_BH3_return_btn` 返回主菜单 + ESCAPE 快捷键）：标题 → 抽取钮 → 三候选卡 → 放弃/重置 → 12 系徽 6×2 → 无限增殖 3×3 → 空梦交易，整体居中 |
| ~~`interface/BH3_ElysianRealm_window.gui`~~ | **已删除**（决议面板内嵌版，被主菜单方案取代）；`common/decisions/categories/Valkyrie_categories.txt` 中的 `scripted_gui = BH3_ElysianRealm_window` 行同步移除，`BH3_ElysianRealm_group` 分类保留为空分类 |
| `interface/BH3_tech.gui`（改） | 主菜单**原「作战学说」位置**（700,250）改放往事乐土入口 `BH3_main_menu_er_btn`（复用六边形 `GFX_BH3_main_menu_item`）+ 图标 `icon_BH3_main_menu_er`（爱莉希雅系徽，scale 2.3 放大至约 138×156）+ 文字框（790,440）；**学说按钮三件套已移除**（学说系统将按精通度学说重置后再恢复，贴图 `GFX_BH3_main_menu_doctrine` 保留未删） |
| `interface/BH3_tech.gfx`（改） | 新增 `GFX_BH3_main_menu_elysianrealm` → `gfx/interface/elysianrealm/signet_Elysia.png` |
| `common/scripted_guis/BH3_tech_scripted_gui.txt`（改） | `BH3_main_menu_er_btn_click`：置 `BH3_ER_menu_open`，同时清 `BH3_tech_menu_open` / `BH3_Valkyrie_Doctrine_on`（入口互斥）；主菜单关闭钮、科技入口同步清 `BH3_ER_menu_open`；`BH3_main_menu_doctrine_btn_click` 随按钮一并移除 |
| `common/scripted_guis/BH3_ElysianRealm_scripted_gui.txt`（改，10-09 夜） | 返回钮效果改为「清 `BH3_ER_menu_open` + 置 `BH3_main_menu_open`」（同科技菜单 X 钮惯例） |
| `common/scripted_guis/BH3_misc_scripted_gui.txt`（改） | 两处打开主菜单的 effect（`BH3_Hyperion_Menu_btn_click` / `_Secretary_btn_click`）追加 `clr_country_flag = BH3_ER_menu_open`，防残留 |
| `common/scripted_localisation/BH3_ElysianRealm_scripted_loc.txt`（改，10-09 深夜） | 新增 `BHER_lock_tip` 动态文本：未解锁时主菜单按钮 tooltip 显示「请先在特殊项目中完成往事乐土项目」提示；`BH3_tech.gui` 按钮 tooltip 改为 `[BHER_lock_tip]`，`BH3_main_menu_er_btn_click_enabled` 要求 `BH3_ElysianRealm_unlocked`（未解锁按钮置灰） |
| `common/scripted_localisation/BH3_ElysianRealm_scripted_loc.txt`（新） | `BHER_cand1/2/3_card`（每槽 60 条件项：候选派系 × 该系下一档 → 卡面 loc）+ `BHER_stat_<系>`×12（持有状态 tooltip，6 态） |
| `common/decisions/BH3_ElysianRealm_decisions.txt` | **已删除**（原 13 个决议全部 GUI 化） |
| `events/BH3_ElysianRealm_event.txt` | **已删除**（三选一事件由 GUI 取代；其 loc 键留作无害孤儿） |
| `common/decisions/categories/Valkyrie_categories.txt`（改） | 移除 `scripted_gui` 行（见上） |
| `common/on_actions/BH3_ElysianRealm_on_actions.txt`（改） | `on_weekly` 追加两个冷却变量递减（`BH3_ER_mobius_cd` / `BH3_ER_pardofelis_cd`，每周 −1，=4 约 30 天，粒度与原 `days_re_enable = 30` 一致） |
| `localisation/BH3_equipment_l_english.yml` / `simp_chinese/...`（追加 174+1 键 ×2） | 候选卡面 60（名+效果说明）、系状态 72、GUI 按钮/提示、`BH3_ER_menu_title`（窗口标题/主菜单按钮 tooltip）；沿用「并入现有 yml」规避独立 loc 崩溃问题 |
| `localisation/BH3_tech_l_english.yml` / `simp_chinese/...`（追加 1 键 ×2） | `BH3_main_menu_er_btn_TextBox_tt`（往事乐土 / Elysian Realm） |
| `tools/gen_elysian_gui.py` | 全部上述重复内容的生成器（可复跑，yml 追加幂等） |

### 附带修正

- 旧事件授予逻辑里浮生/戒律/旭光核心的动态修正组合与重置清单不一致（重置漏 `Bodhi_Core_dm`）；新版 `grant` 与 `reset` 共用同一生成源（`TIER_DM` 表），必然一致。

### 待游戏内验证（建议清单）

1. 打开崩坏3主菜单（Hyperion 舰桥界面），右侧出现第三个大按钮「往事乐土」（爱莉希雅系徽图标）；
2. 点「往事乐土」→ 弹出往事乐土子窗口（标题「往事乐土 · 刻印试炼」、可拖动、右上可关闭）；再点「女武神科技」/「作战学说」应互斥切换，关主菜单后子窗口不残留；
3. 钥匙 ≥50 时「进入试炼」可点，点击后出现 3 张系徽候选卡，悬停显示正确的「下一枚刻印」名称与效果；
4. 点选候选卡后获得对应刻印（民族精神 + 开战时动态修正），候选区清空、按钮恢复；
5. 「放弃本次」全额返还 50 钥匙；「重置全部刻印」清空并返还 25；
6. 无限增殖 7 按钮消耗 50 PP、约 30 天冷却；空梦交易所 3 按钮拆厂换资源；
7. 12 系徽 tooltip 显示已持有列表与下一枚；
8. 全部 60 枚集齐后抽取按钮禁用；
9. 决议分类「往事乐土」不再显示自定义窗口（恢复为空分类，入口仅走主菜单）。

### 已知限制

- 主菜单第三个按钮的图标直接复用爱莉希雅系徽白图（60×68），比科技/学说的大图标小，风格上是白图线稿系徽，观感待肉眼确认；
- 窗口为舰桥背景平铺（`GFX_BH3_main_menu_bg` cornered tile），与主菜单同底图；若太花可换 `GFX_BH3_tech_menu_bg` 或加纯色底板；
- 候选卡的「卡面文字」是 60 个静态组合（由生成器产出），新增/调整刻印数值后需复跑生成器同步文案；
- AI 不会与窗口交互（与原决议 `ai_will_do = 0` 一致）。
