# -*- coding: utf-8 -*-
"""往事乐土 GUI 化改造生成器：
1) common/scripted_effects/BH3_ElysianRealm_scripted_effects.txt  —— 候选生成/授予/重置/放弃
2) common/scripted_guis/BH3_ElysianRealm_scripted_gui.txt        —— 窗口交互
3) interface/BH3_ElysianRealm_window.gui                         —— 窗口布局
4) common/scripted_localisation/BH3_ElysianRealm_scripted_loc.txt—— 候选卡/系状态的动态文本
5) 追加本地化键到两个现有 yml（保持 BOM 与行尾）
"""
import os, re, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTIONS = [
    ("Savior", 1, "救世", "凯文", "Deliverance"),
    ("Setsuna", 2, "刹那", "樱", "Setsuna"),
    ("Bodhi", 3, "天慧", "苏", "Bodhi"),
    ("Gold", 4, "黄金", "伊甸", "Gold"),
    ("Kalpas", 5, "鏖灭", "千劫", "Kalpas"),
    ("Fusheng", 6, "浮生", "华", "Vicissitude"),
    ("Aponia", 7, "戒律", "阿波尼亚", "Discipline"),
    ("Spiral", 8, "螺旋", "维尔薇", "Helix"),
    ("Mobius", 9, "无限", "梅比乌斯", "Infinity"),
    ("Kosma", 10, "旭光", "科斯魔", "Daybreak"),
    ("Griseo", 11, "繁星", "格蕾修", "Stars"),
    ("Pardofelis", 12, "空梦", "帕朵菲莉丝", "Reverie"),
]
TIERS = ["1", "2", "3", "Core", "Amp"]
RES = ["steel", "aluminium", "rubber", "tungsten", "chromium", "oil", "coal"]
RES_CN = {"steel": "钢", "aluminium": "铝", "rubber": "橡胶", "tungsten": "钨",
          "chromium": "铬", "oil": "石油", "coal": "煤"}
RES_EN = {"steel": "Steel", "aluminium": "Aluminium", "rubber": "Rubber", "tungsten": "Tungsten",
          "chromium": "Chromium", "oil": "Oil", "coal": "Coal"}

# 读取现有 yml 的刻印名/描述（raw，保留转义）
def load_loc(path):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8-sig")
    d = {}
    for m in re.finditer(r'^\s*([A-Za-z0-9_.]+):0\s*"(.*)"\s*$', text, re.M):
        d[m.group(1)] = m.group(2)
    return d

cn = load_loc(os.path.join(ROOT, "localisation/simp_chinese/BH3_equipment_l_simp_chinese.yml"))
en = load_loc(os.path.join(ROOT, "localisation/BH3_equipment_l_english.yml"))

def sig_name(lang, f, t): return lang[f"BH3_ER_{f}_{t}"]
def sig_desc(lang, f, t): return lang.get(f"BH3_ER_{f}_{t}_desc", "")

# ---------------------------------------------------------------- 1. scripted_effects
def grant_body(f):
    lines = []
    for i, t in enumerate(TIERS):
        key = "if" if i == 0 else "else_if"
        lines.append(f"\t{key} = {{")
        lines.append(f"\t\tlimit = {{ NOT = {{ has_idea = BH3_ER_{f}_{t} }} }}")
        lines.append(f"\t\tadd_ideas = BH3_ER_{f}_{t}")
        for dm in TIER_DM.get((f, t), [f"BH3_ER_{f}_{t}_dm"]):
            lines.append(f"\t\tadd_dynamic_modifier = {{ modifier = {dm} }}")
        for ef in CORE_EFFECTS.get(f, []) if t == "Core" else []:
            lines.append(f"\t\t{ef}")
        lines.append("\t}")
    return lines

# 每系每档实际挂的动态修正（默认 BH3_ER_{f}_{tier}_dm；以下为覆盖）
TIER_DM = {
    ("Fusheng", "Core"): ["BH3_ER_Fusheng_Advantage_dm", "BH3_ER_Fusheng_Disadvantage_dm"],
    ("Fusheng", "Amp"): ["BH3_ER_Fusheng_AmpAdv_dm", "BH3_ER_Fusheng_AmpDis_dm"],
    ("Aponia", "Core"): ["BH3_ER_Aponia_Low_dm", "BH3_ER_Aponia_High_dm", "BH3_ER_Aponia_Overflow_dm"],
    ("Kosma", "Core"): ["BH3_ER_Kosma_T1_dm", "BH3_ER_Kosma_T2_dm", "BH3_ER_Kosma_T3_dm", "BH3_ER_Kosma_T4_dm"],
}
CORE_EFFECTS = {
    "Setsuna": ["unlock_subunit = hq_support_company", "every_army_leader = { add_unit_leader_trait = BH3_ER_trait_Setsuna }"],
}

DM_REMOVE = [x for f, *_ in FACTIONS for t in TIERS for x in TIER_DM.get((f, t), [f"BH3_ER_{f}_{t}_dm"])]

se = []
se.append("# 往事乐土·GUI 化的脚本化效果（2026-10-09 抽取机制改写：原作式「三候选选其一」）")
se.append("")
# ---- 候选生成 ----
se.append("BH3_ER_roll_candidates = {")
se.append("\t# ---- 各派系可抽权重（0/1）：未到Ⅲ→抽普通；有Ⅲ无核心→抽核心；有核心无增幅→抽增幅 ----")
for f, *_ in FACTIONS:
    se.append(f"\tif = {{ limit = {{ NOT = {{ has_idea = BH3_ER_{f}_3 }} }} set_variable = {{ BH3_ER_w_{f} = 1 }} }}")
    se.append(f"\telse = {{ set_variable = {{ BH3_ER_w_{f} = 0 }} }}")
for slot in (1, 2, 3):
    se.append(f"\t# ---- 候选 {slot}（抽中派系后清零其权重，保证三候选不重复）----")
    se.append("\trandom_list = {")
    for f, fid, *_ in FACTIONS:
        se.append(f"\t\tBH3_ER_w_{f} = {{ set_variable = {{ BH3_ER_cand{slot} = {fid} }} }}")
    se.append(f"\t\t1 = {{ set_variable = {{ BH3_ER_cand{slot} = 0 }} }}")
    se.append("\t}")
    for f, fid, *_ in FACTIONS:
        se.append(f"\tif = {{ limit = {{ check_variable = {{ BH3_ER_cand{slot} = {fid} }} }} set_variable = {{ BH3_ER_w_{f} = 0 }} }}")
se.append("\tset_variable = { BH3_ER_drawing = 1 }")
se.append("}")
se.append("")
# ---- 放弃 ----
se.append("BH3_ER_cancel_draw = {")
se.append("\tadd_equipment_to_stockpile = { type = BH3_FlawlessKey_equipment amount = 50 }")
for slot in (1, 2, 3):
    se.append(f"\tset_variable = {{ BH3_ER_cand{slot} = 0 }}")
se.append("\tset_variable = { BH3_ER_drawing = 0 }")
se.append("}")
se.append("")
# ---- 授予（每系一个，按持有进度自动给下一枚）----
for f, *_ in FACTIONS:
    se.append(f"BH3_ER_grant_{f} = {{")
    se += grant_body(f)
    for slot in (1, 2, 3):
        se.append(f"\tset_variable = {{ BH3_ER_cand{slot} = 0 }}")
    se.append("\tset_variable = { BH3_ER_drawing = 0 }")
    se.append("}")
    se.append("")
# ---- 重置 ----
se.append("BH3_ER_reset = {")
se.append("\tremove_ideas = {")
for f, *_ in FACTIONS:
    for t in TIERS:
        se.append(f"\t\tBH3_ER_{f}_{t}")
se.append("\t}")
for dm in DM_REMOVE:
    se.append(f"\tremove_dynamic_modifier = {{ modifier = {dm} }}")
se.append("\tadd_equipment_to_stockpile = { type = BH3_FlawlessKey_equipment amount = 25 }")
for slot in (1, 2, 3):
    se.append(f"\tset_variable = {{ BH3_ER_cand{slot} = 0 }}")
se.append("\tset_variable = { BH3_ER_drawing = 0 }")
se.append("}")
open(os.path.join(ROOT, "common/scripted_effects/BH3_ElysianRealm_scripted_effects.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(se) + "\n")
print("scripted_effects:", len(se), "lines")

# ---------------------------------------------------------------- 2. scripted_gui
ANY_AMP = "\n".join(f"\t\t\t\t\tNOT = {{ has_idea = BH3_ER_{f}_Amp }}" for f, *_ in FACTIONS)
ANY_IDEA = "\n".join(f"\t\t\t\thas_idea = BH3_ER_{f}_{t}" for f, *_ in FACTIONS for t in TIERS)
sg = []
sg.append("scripted_gui = {")
sg.append("\t# 往事乐土主窗口（decision_category 内嵌，取代原决议列表）")
sg.append("\tBH3_ElysianRealm_window = {")
sg.append("\t\tcontext_type = decision_category")
sg.append("\t\twindow_name = BH3_ElysianRealm_window")
sg.append("\t\tvisible = { always = yes }")
sg.append("")
sg.append("\t\teffects = {")
sg.append("\t\t\tBH3_ER_draw_btn_click = {")
sg.append("\t\t\t\tadd_equipment_to_stockpile = { type = BH3_FlawlessKey_equipment amount = -50 }")
sg.append("\t\t\t\tBH3_ER_roll_candidates = yes")
sg.append("\t\t\t}")
sg.append("\t\t\tBH3_ER_cancel_btn_click = { BH3_ER_cancel_draw = yes }")
sg.append("\t\t\tBH3_ER_reset_btn_click = { BH3_ER_reset = yes }")
for slot in (1, 2, 3):
    for f, *_ in FACTIONS:
        sg.append(f"\t\t\tBH3_ER_take_{slot}_{f}_click = {{ BH3_ER_grant_{f} = yes }}")
for r in RES:
    sg.append(f"\t\t\tBH3_ER_mob_{r}_click = {{")
    sg.append("\t\t\t\tadd_political_power = -50")
    sg.append(f"\t\t\t\tadd_to_variable = {{ BH3_ER_Mobius_{r} = 5 }}")
    sg.append("\t\t\t\tset_variable = { BH3_ER_mobius_cd = 4 }")
    sg.append("\t\t\t}")
for i in (1, 2, 3):
    pp = {1: 0, 2: 0, 3: 0}[i]
    sg.append(f"\t\t\tBH3_ER_pard_{i}_click = {{")
    sg.append(f"\t\t\t\tBH3_ER_pardofelis_sell_{i} = yes")
    sg.append("\t\t\t\tset_variable = { BH3_ER_pardofelis_cd = 4 }")
    sg.append("\t\t\t}")
sg.append("\t\t}")
sg.append("")
sg.append("\t\ttriggers = {")
sg.append("\t\t\tBH3_ER_draw_btn_click_enabled = {")
sg.append("\t\t\t\thas_country_flag = BH3_ElysianRealm_unlocked")
sg.append("\t\t\t\thas_equipment = { BH3_FlawlessKey_equipment > 49 }")
sg.append("\t\t\t\tNOT = { check_variable = { BH3_ER_drawing = 1 } }")
sg.append("\t\t\t\tOR = {")
sg.append(ANY_AMP)
sg.append("\t\t\t\t}")
sg.append("\t\t\t}")
sg.append("\t\t\tBH3_ER_cancel_btn_visible = { check_variable = { BH3_ER_drawing = 1 } }")
sg.append("\t\t\tBH3_ER_reset_btn_click_enabled = {")
sg.append("\t\t\t\tOR = {")
sg.append(ANY_IDEA)
sg.append("\t\t\t\t}")
sg.append("\t\t\t}")
for slot in (1, 2, 3):
    for f, fid, *_ in FACTIONS:
        sg.append(f"\t\t\tBH3_ER_take_{slot}_{f}_visible = {{ check_variable = {{ BH3_ER_cand{slot} = {fid} }} }}")
for r in RES:
    sg.append(f"\t\t\tBH3_ER_mob_{r}_visible = {{ has_idea = BH3_ER_Mobius_Core }}")
    sg.append(f"\t\t\tBH3_ER_mob_{r}_click_enabled = {{")
    sg.append("\t\t\t\thas_political_power > 49")
    sg.append("\t\t\t\tNOT = { check_variable = { BH3_ER_mobius_cd > 0 } }")
    sg.append("\t\t\t}")
for i in (1, 2, 3):
    sg.append(f"\t\t\tBH3_ER_pard_{i}_visible = {{ has_idea = BH3_ER_Pardofelis_Core }}")
    sg.append(f"\t\t\tBH3_ER_pard_{i}_click_enabled = {{")
    sg.append("\t\t\t\tnum_of_civilian_factories > 0")
    sg.append("\t\t\t\tNOT = { check_variable = { BH3_ER_pardofelis_cd > 0 } }")
    sg.append("\t\t\t}")
sg.append("\t\t}")
sg.append("\t}")
sg.append("}")
open(os.path.join(ROOT, "common/scripted_guis/BH3_ElysianRealm_scripted_gui.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(sg) + "\n")
print("scripted_gui:", len(sg), "lines")

# Pardofelis 拆除工厂的效果单独生成（需要 random_owned_controlled_state 作用域）
pard = ["# 空梦交易所：变卖工厂换政治点与地图外资源"]
pard.append("BH3_ER_pardofelis_sell_1 = {")
pard.append("\trandom_owned_controlled_state = { limit = { is_fully_controlled_by = ROOT } remove_building = { type = industrial_complex level = 1 } }")
pard.append("\tadd_political_power = 50")
pard.append("\tadd_to_variable = { BH3_ER_Pardofelis_steel = 3 }")
pard.append("}")
pard.append("BH3_ER_pardofelis_sell_2 = {")
pard.append("\trandom_owned_controlled_state = { limit = { is_fully_controlled_by = ROOT } remove_building = { type = industrial_complex level = 3 } }")
pard.append("\tadd_political_power = 180")
pard.append("\tadd_to_variable = { BH3_ER_Pardofelis_steel = 10 }")
pard.append("\tadd_to_variable = { BH3_ER_Pardofelis_aluminium = 5 }")
pard.append("}")
pard.append("BH3_ER_pardofelis_sell_3 = {")
pard.append("\trandom_owned_controlled_state = { limit = { is_fully_controlled_by = ROOT } remove_building = { type = industrial_complex level = 6 } }")
pard.append("\tadd_political_power = 400")
pard.append("\tadd_to_variable = { BH3_ER_Pardofelis_steel = 20 }")
pard.append("\tadd_to_variable = { BH3_ER_Pardofelis_aluminium = 10 }")
pard.append("\tadd_to_variable = { BH3_ER_Pardofelis_rubber = 5 }")
pard.append("}")
open(os.path.join(ROOT, "common/scripted_effects/BH3_ElysianRealm_scripted_effects.txt"), "a", encoding="utf-8", newline="\n").write("\n" + "\n".join(pard) + "\n")

# ---------------------------------------------------------------- 3. .gui 布局
def btn(name, x, y, sprite, tt, text=None, font="hoi_16mbs"):
    s = [f"\t\tbuttonType = {{",
         f"\t\t\tname = \"{name}\"",
         f"\t\t\tposition = {{ x = {x} y = {y} }}",
         f"\t\t\tspriteType = \"{sprite}\"",
         f"\t\t\tpdx_tooltip = \"{tt}\""]
    if text:
        s.append(f"\t\t\tbuttonText = \"{text}\"")
        s.append(f"\t\t\tbuttonFont = \"{font}\"")
    s.append("\t\t}")
    return s

gui = ["guiTypes = {", "",
       "\t# 往事乐土主窗口（2026-10-09：取代原决议列表，原作式三候选抽取）",
       "\tcontainerWindowType = {",
       "\t\tname = \"BH3_ElysianRealm_window\"",
       "\t\tposition = { x = 0 y = 0 }",
       "\t\tsize = { width = 100% height = 545 }"]
gui += btn("BH3_ER_draw_btn", 15, 8, "GFX_BH3_Intro_400x50_btn", "BH3_ER_gui_draw_tt", "BH3_ER_gui_draw")
for slot, x in ((1, 15), (2, 160), (3, 305)):
    for f, *_ in FACTIONS:
        gui += btn(f"BH3_ER_take_{slot}_{f}", x, 66, f"GFX_idea_BH3_ER_{f}", f"BH3_ER_cand{slot}_tt")
gui += btn("BH3_ER_cancel_btn", 15, 160, "GFX_BH3_Intro_200x50_alpha_btn", "BH3_ER_gui_cancel_tt", "BH3_ER_gui_cancel")
gui += btn("BH3_ER_reset_btn", 215, 160, "GFX_BH3_Intro_200x50_alpha_btn", "BH3_ER_gui_reset_tt", "BH3_ER_gui_reset")
for i, (f, *_ ) in enumerate(FACTIONS):
    x = 15 + (i % 6) * 68
    y = 222 if i < 6 else 316
    gui += [f"\t\ticonType = {{",
            f"\t\t\tname = \"BH3_ER_fac_{f}\"",
            f"\t\t\tposition = {{ x = {x} y = {y} }}",
            f"\t\t\tspriteType = \"GFX_idea_BH3_ER_{f}\"",
            f"\t\t\tpdx_tooltip = \"BH3_ER_fac_{f}_tt\"",
            f"\t\t}}"]
for i, r in enumerate(RES):
    x = 15 + (i % 3) * 110
    y = 414 + (i // 3) * 30
    gui += btn(f"BH3_ER_mob_{r}", x, y, "GFX_BH3_Hyperion_Change_SecretaryX_btn", f"BH3_ER_gui_mob_{r}_tt", f"BH3_ER_gui_mob_{r}")
for i in (1, 2, 3):
    gui += btn(f"BH3_ER_pard_{i}", 15 + (i - 1) * 110, 510, "GFX_BH3_Hyperion_Change_SecretaryX_btn", f"BH3_ER_gui_pard_{i}_tt", f"BH3_ER_gui_pard_{i}")
gui += ["\t}", "}"]
open(os.path.join(ROOT, "interface/BH3_ElysianRealm_window.gui"), "w", encoding="utf-8", newline="\n").write("\n".join(gui) + "\n")
print("gui:", len(gui), "lines")

# ---------------------------------------------------------------- 4. scripted_localisation
sl = ["# 往事乐土动态文本（候选卡面 / 各系持有状态）"]
for slot in (1, 2, 3):
    sl.append(f"defined_text = {{")
    sl.append(f"\tname = BHER_cand{slot}_card")
    for f, fid, *_ in FACTIONS:
        for i, t in enumerate(TIERS):
            if t == "1":
                cond = f"NOT = {{ has_idea = BH3_ER_{f}_1 }}"
            elif t in ("2", "3"):
                cond = f"has_idea = BH3_ER_{f}_{int(t)-1}\n\t\t\tNOT = {{ has_idea = BH3_ER_{f}_{t} }}"
            elif t == "Core":
                cond = f"has_idea = BH3_ER_{f}_3\n\t\t\tNOT = {{ has_idea = BH3_ER_{f}_Core }}"
            else:
                cond = f"has_idea = BH3_ER_{f}_Core\n\t\t\tNOT = {{ has_idea = BH3_ER_{f}_Amp }}"
            sl.append("\ttext = {")
            sl.append("\t\ttrigger = {")
            sl.append(f"\t\t\tcheck_variable = {{ BH3_ER_cand{slot} = {fid} }}")
            sl.append(f"\t\t\t{cond}")
            sl.append("\t\t}")
            sl.append(f"\t\tlocalization_key = BH3_ER_card_{f}_{t}")
            sl.append("\t}")
    sl.append("\ttext = { localization_key = BH3_ER_card_none }")
    sl.append("}")
    sl.append("")
for f, fid, cn_name, cn_hero, en_name in FACTIONS:
    sl.append("defined_text = {")
    sl.append(f"\tname = BHER_stat_{f}")
    states = [("Amp", f"has_idea = BH3_ER_{f}_Amp"), ("Core", f"has_idea = BH3_ER_{f}_Core"),
              ("3", f"has_idea = BH3_ER_{f}_3"), ("2", f"has_idea = BH3_ER_{f}_2"),
              ("1", f"has_idea = BH3_ER_{f}_1")]
    for st, cond in states:
        sl.append("\ttext = {")
        sl.append(f"\t\ttrigger = {{ {cond} }}")
        sl.append(f"\t\tlocalization_key = BH3_ER_stat_{f}_{st}")
        sl.append("\t}")
    sl.append(f"\ttext = {{ localization_key = BH3_ER_stat_{f}_none }}")
    sl.append("}")
    sl.append("")
open(os.path.join(ROOT, "common/scripted_localisation/BH3_ElysianRealm_scripted_loc.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(sl) + "\n")
print("scripted_loc:", len(sl), "lines")

# ---------------------------------------------------------------- 5. 本地化追加
new_cn, new_en = {}, {}
def put(k, v_cn, v_en):
    new_cn[k] = v_cn; new_en[k] = v_en

for f, *_ in FACTIONS:
    for t in TIERS:
        put(f"BH3_ER_card_{f}_{t}",
            f"§Y{sig_name(cn, f, t)}§!\\n{sig_desc(cn, f, t)}",
            f"§Y{sig_name(en, f, t)}§!\\n{sig_desc(en, f, t)}")
put("BH3_ER_card_none", "（空）", "(Empty)")

# 系状态（6 态）——列出已持有与下一枚
TIER_LABEL_CN = {"1": "Ⅰ", "2": "Ⅱ", "3": "Ⅲ", "Core": "核心", "Amp": "增幅"}
TIER_LABEL_EN = {"1": "I", "2": "II", "3": "III", "Core": "Core", "Amp": "Amp"}
for f, fid, cn_name, cn_hero, en_name in FACTIONS:
    names_cn = {t: sig_name(cn, f, t) for t in TIERS}
    names_en = {t: sig_name(en, f, t) for t in TIERS}
    owned_seq = TIERS
    for idx, st in enumerate(["none"] + owned_seq):
        got = owned_seq[:idx]
        nxt = owned_seq[idx] if idx < len(owned_seq) else None
        head_cn = f"§Y{cn_name}（{cn_hero}）§!"
        head_en = f"§Y{en_name}§!"
        if not got:
            body_cn, body_en = "尚未获得该系刻印。", "No Signets of this series yet."
        else:
            body_cn = "已持有：" + "、".join(names_cn[t] for t in got)
            body_en = "Held: " + ", ".join(names_en[t] for t in got)
        if nxt:
            body_cn += f"\\n下一枚：{names_cn[nxt]}"
            body_en += f"\\nNext: {names_en[nxt]}"
        else:
            body_cn += "\\n§G已集齐该系全部刻印。§!"
            body_en += "\\n§GAll Signets of this series collected.§!"
        put(f"BH3_ER_stat_{f}_{st}", f"{head_cn}\\n{body_cn}", f"{head_en}\\n{body_en}")

# GUI 文本
put("BH3_ER_gui_draw", "进入试炼·刻印三选一（50 把无瑕之钥）", "Enter the Trial: Signets, Choose 1 of 3 (50 Flawless Keys)")
put("BH3_ER_gui_draw_tt",
    "消耗 §Y50 把无瑕之钥§!，开启一次与原作相同的刻印三选一：\\n随机出现三§Y位英桀的传送门§!，每位门内是其§Y下一枚刻印§!（普通 Ⅰ→Ⅱ→Ⅲ → 核心 → 增幅，同系自动递进，与原作重复获得即升级一致）。\\n\\n规则（与原作一致）：\\n· 未集齐 3 枚普通刻印的系 → 门内给下一枚普通刻印；\\n· 集齐 3 枚普通后 → 门内变为该系§Y核心刻印§!；\\n· 持有核心后 → 门内变为该系§Y增幅刻印§!；\\n· 三候选互不重复；候选不足时可放弃并全额返还钥匙。\\n\\n点选一张候选卡即获得对应刻印；点击候选卡可查看其完整名称与效果说明。",
    "Spend §Y50 Flawless Keys§! for a draw faithful to the original game:\\nThree §Yhero portals§! appear, each offering that hero's §Ynext Signet§! (Normal I->II->III -> Core -> Amplifier; the series advances automatically, matching the original's 'duplicates upgrade' rule).\\n\\nRules (as in the original):\\n· Series without 3 Normal Signets -> next Normal Signet;\\n· With 3 Normal Signets -> the series' §YCore Signet§!;\\n· With the Core -> the series' §YAmplifier Signet§!;\\n· The three candidates never repeat; if fewer remain, you may cancel for a full refund.\\n\\nClick a card to claim its Signet; hover a card for its full name and effects.")
put("BH3_ER_gui_cancel", "放弃本次（返还钥匙）", "Cancel (refund keys)")
put("BH3_ER_gui_cancel_tt", "放弃当前的三候选，§Y全额返还 50 把无瑕之钥§!。", "Abandon the current three candidates and §Yrefund all 50 Flawless Keys§!.")
put("BH3_ER_gui_reset", "重置全部刻印", "Reset all Signets")
put("BH3_ER_gui_reset_tt", "移除全部已持有刻印（含动态修正），返还 §Y25 把无瑕之钥§!（约为总投入的半数）。", "Removes all held Signets (including dynamic modifiers) and refunds §Y25 Flawless Keys§! (about half of the investment).")
for r in RES:
    put(f"BH3_ER_gui_mob_{r}", RES_CN[r], RES_EN[r])
    put(f"BH3_ER_gui_mob_{r}_tt",
        f"§Y无限增殖§!：消耗 §Y50 政治点§!，获得 5 点地图外{RES_CN[r]}（由「无限·核心刻印」的修正读取，持续生效）。约 30 天可执行一次。",
        f"§YInfinite Proliferation§!: spend §Y50 Political Power§! for 5 off-map {RES_EN[r]} (read by the 'Infinity' Core Signet's modifier). Usable about once per 30 days.")
put("BH3_ER_gui_pard_1", "小宗交易", "Small Deal")
put("BH3_ER_gui_pard_1_tt", "§Y空梦交易所§!：拆除 1 座民用工厂，换取 §Y50 政治点§!与 3 点地图外钢。约 30 天可执行一次。", "§YReverie Exchange§!: demolish 1 Civilian Factory for §Y50 Political Power§! and 3 off-map Steel. About once per 30 days.")
put("BH3_ER_gui_pard_2", "中宗交易", "Medium Deal")
put("BH3_ER_gui_pard_2_tt", "§Y空梦交易所§!：拆除 3 座民用工厂，换取 §Y180 政治点§!、10 点钢与 5 点铝。约 30 天可执行一次。", "§YReverie Exchange§!: demolish 3 Civilian Factories for §Y180 Political Power§!, 10 Steel and 5 Aluminium. About once per 30 days.")
put("BH3_ER_gui_pard_3", "大宗交易", "Grand Deal")
put("BH3_ER_gui_pard_3_tt", "§Y空梦交易所§!：拆除 6 座民用工厂，换取 §Y400 政治点§!、20 点钢、10 点铝与 5 点橡胶。约 30 天可执行一次。", "§YReverie Exchange§!: demolish 6 Civilian Factories for §Y400 Political Power§!, 20 Steel, 10 Aluminium and 5 Rubber. About once per 30 days.")
for i, (f, *_ ) in enumerate(FACTIONS):
    put(f"BH3_ER_fac_{f}_tt", f"[BHER_stat_{f}]", f"[BHER_stat_{f}]")
for slot in (1, 2, 3):
    put(f"BH3_ER_cand{slot}_tt", f"[BHER_cand{slot}_card]", f"[BHER_cand{slot}_card]")

def append_yml(path, mapping, eol):
    raw = open(path, "rb").read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    if not bom:
        raise SystemExit(f"no BOM: {path}")
    text = raw.decode("utf-8-sig")
    if not text.endswith(("\n", "\r")):
        text += "\n"
    existing = set(re.findall(r'^\s*([A-Za-z0-9_.]+):0', text, re.M))
    fresh = {k: v for k, v in mapping.items() if k not in existing}
    skipped = len(mapping) - len(fresh)
    add = "".join(f'{k}:0 "{v}"{eol}' for k, v in fresh.items())
    out = (text + add).encode("utf-8")
    open(path, "wb").write(b"\xef\xbb\xbf" + out)
    return len(fresh), skipped

n1, s1 = append_yml(os.path.join(ROOT, "localisation/simp_chinese/BH3_equipment_l_simp_chinese.yml"), new_cn, "\n")
n2, s2 = append_yml(os.path.join(ROOT, "localisation/BH3_equipment_l_english.yml"), new_en, "\r\n")
print("loc appended:", n1, "+ skipped", s1, "| en:", n2, "+ skipped", s2)
