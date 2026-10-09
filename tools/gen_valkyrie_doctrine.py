# -*- coding: utf-8 -*-
"""女武神作战学说重置生成器 v2（2026-10-09 深夜修订）：
- 7 条轨道全部用自定义键（valkyrie_*），不复用原版 4 轨 → 原版子学说不会混入本文件夹
- 轨道精通类别只用原版校验过的类别（含 category_special_forces，女武神单位即特战）
- 修饰键全部经原版 doctrines 文件校验：max_planning_factor→max_planning；
  combat_width_factor 移除（学说语境不支持）；special_forces_min→special_forces_cap；
  special_forces_defence_factor→改用 special_forces_cap / category 防御（原版学说无此键）
- 本地化追加到现有 BH3_doctrine_l_*.yml（幂等），不新建独立 loc 文件
"""
import io, os

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------- 文件夹 ----------------
FOLDER = '''valkyrie = {
    allowed = {
        always = yes
    }
    name = "BH3_doctrine_folder_valkyrie"
    ledger = army
    ledger_gfx = GFX_land_doctrine_folder_icon
    tab_gfx = GFX_landdoctrine_tab_large
    color_frame = 1
    sound = ui_doctrine_tab_land
}
'''

# ---------------- 主学说 ----------------
GRAND = '''bh3_valkyrie_warfare = {
    folder = valkyrie

    name = BH3_grand_doctrine_valkyrie
    description = BH3_grand_doctrine_valkyrie_desc
    icon = GFX_BH3_main_menu_doctrine

    available = {
        has_country_flag = BH3_Hyperion_enabled
    }

    xp_cost = 100
    xp_type = army

    ai_will_do = {
        base = 1
    }

    tracks = {
        valkyrie_infantry
        valkyrie_support
        valkyrie_armor
        valkyrie_operations
        valkyrie_assault
        valkyrie_herrscher
        valkyrie_special
    }

    # 主学说效果（= 旧 BH3_Valkyrie_Doctrine_0「对崩坏作战理论」；special_forces_min/defence_factor 按学说语境换为 cap/attack）
    category_army = {
        soft_attack = 0.15
        hard_attack = 0.15
        armor_value = 0.15
        ap_attack = 1
        max_organisation = 50
        max_strength = 25
        defense = 1
    }
    special_forces_cap = 0.10
    special_forces_attack_factor = 0.15

    # 里程碑 ×7：旧收尾学说 BH3_Valkyrie_Doctrine_10「为世界上所有美好而战」的效果按线分散
    milestones = {
        {
            # 步兵协同线
            category_AllValkyrie = {
                soft_attack = 0.07
                hard_attack = 0.07
            }
            category_army = {
                soft_attack = 0.15
                hard_attack = 0.15
            }
        }
        {
            # 战斗支援线
            category_AllValkyrie = {
                armor_value = 0.07
            }
            category_army = {
                ap_attack = 0.15
                armor_value = 0.07
            }
        }
        {
            # 装甲突击线
            category_AllValkyrie = {
                defense = 0.15
            }
            category_army = {
                breakthrough = 0.15
                defense = 0.20
            }
        }
        {
            # 纵深作战线
            category_AllValkyrie = {
                max_organisation = 4
            }
            category_army = {
                max_organisation = 15
                maximum_speed = 0.25
            }
        }
        {
            # 近战攻坚线
            category_AllValkyrie = {
                default_morale = 0.07
            }
            category_army = {
                defense = 0.30
                default_morale = 0.15
            }
        }
        {
            # 律者降临线
            category_AllHerrscher = {
                soft_attack = 0.15
                hard_attack = 0.15
                defense = 0.15
                max_organisation = 500
            }
            category_army = {
                defense = 0.35
            }
        }
        {
            # 女武神特战线
            category_AllHerrscher = {
                max_organisation = 500
                default_morale = 0.15
            }
        }
    }
}
'''

# ---------------- 7 条自定义轨道 ----------------
TRACKS = '''valkyrie_infantry = {
    name = BH3_doctrine_track_infantry
    background = "GFX_grand_battleplan_bg"
    icon = "GFX_doctrine_milestone_infantry_land"
    icon_frame = "GFX_doctrine_decor_land"
    mastery = {
        multiplier = 1.0
        categories = {
            category_all_infantry
        }
    }
}
valkyrie_support = {
    name = BH3_doctrine_track_support
    background = "GFX_sup_firepower_bg"
    icon = "GFX_doctrine_milestone_artillery_land"
    icon_frame = "GFX_doctrine_decor_land"
    mastery = {
        multiplier = 8.0
        categories = {
            category_line_artillery
            category_artillery
            category_support_battalions
        }
    }
}
valkyrie_armor = {
    name = BH3_doctrine_track_armor
    background = "GFX_mob_warfare_bg"
    icon = "GFX_doctrine_milestone_armored_land"
    icon_frame = "GFX_doctrine_decor_land"
    mastery = {
        multiplier = 10.0
        categories = {
            category_tanks
            category_all_armor
        }
    }
}
valkyrie_operations = {
    name = BH3_doctrine_track_operations
    background = "GFX_tac_operation_bg"
    icon = "GFX_doctrine_milestone_operations_land"
    icon_frame = "GFX_doctrine_decor_land"
    mastery = {
        multiplier = 0.7
        categories = {
            category_all_infantry
            category_line_artillery
            category_artillery
            category_tanks
            category_all_armor
        }
    }
}
valkyrie_assault = {
    name = BH3_doctrine_track_assault
    background = "GFX_mob_warfare_bg"
    icon = "GFX_doctrine_milestone_infantry_land"
    icon_frame = "GFX_doctrine_decor_land"
    mastery = {
        multiplier = 5.0
        categories = {
            category_special_forces
            category_all_infantry
        }
    }
}
valkyrie_herrscher = {
    name = BH3_doctrine_track_herrscher
    background = "GFX_tac_operation_bg"
    icon = "GFX_doctrine_milestone_armored_land"
    icon_frame = "GFX_doctrine_decor_land"
    mastery = {
        multiplier = 0.5
        categories = {
            category_special_forces
            category_all_armor
        }
    }
}
valkyrie_special = {
    name = BH3_doctrine_track_special
    background = "GFX_sup_firepower_bg"
    icon = "GFX_doctrine_milestone_artillery_land"
    icon_frame = "GFX_doctrine_decor_land"
    mastery = {
        multiplier = 2.0
        categories = {
            category_special_forces
        }
    }
}
'''

# ---------------- 子学说（v4 整合版） ----------------
# 核实结论（git 旧 GUI 触发器）：旧树 24 节点中唯一真互斥对 = 3_5_1 优势兵力 / 3_5_2 精益求精；
# 1_4、2_4、2_5 等"对"均为同层双分支，两侧可同时持有 → 全部整合进同一子学说（base + mastery 阶梯 rewards）。
# 单轨单槽：每轨只放 1 个子学说（special 轨放互斥对 2 个），杜绝人为互斥，完全体强度 = 旧 24 节点总和。
# 结构: (key, track, cn名, en名, icon, base效果块, [(reward键, cn, en, 效果块)...], available附加条件或None, cn_desc, en_desc)
# mastery 阶梯不在数据中，由 subdoctrine_block 按 150×档位数 自动生成（2026-10-10 用户定调：每档新增 150 点）
# 效果块写法：国家修饰键必须手包 modifier = { }；单位类别块（category_*）裸写。
SD = [
 # —— 步兵协同轨：旧线1主干 + 防御分叉 β（1_1→1_2→1_3→1_4_2→1_5_2→1_6_2） ——
 ("bh3_sd_close_combat","valkyrie_infantry","近接歼灭战术","Close Quarters Annihilation Tactics","GFX_doctrine_assault_infantry_medium",
  """category_ValkyrieMeele = { hard_attack = 0.15 }
\tcategory_ValkyrieComprehensive = { hard_attack = 0.1 ap_attack = 0.05 }
\tcategory_ValkyrieArtillery = { hard_attack = 0.05 ap_attack = 0.05 }
\tcategory_ValkyrieArmor = { hard_attack = 0.05 ap_attack = 0.05 }""",
  [("bh3_rwd_1_2","快速接敌","Rapid Engagement",
    """modifier = {
\t\t\t\tarmy_speed_factor = 0.15
\t\t\t\tplanning_speed = 0.25
\t\t\t}
\t\t\tcategory_AllValkyrie = { breakthrough = 0.15 }"""),
   ("bh3_rwd_1_3","武装侦查","Armed Reconnaissance",
    """modifier = {
\t\t\t\torg_loss_at_low_org_factor = -0.15
\t\t\t}
\t\t\tcategory_AllValkyrie = { recon = 0.1 }"""),
   ("bh3_rwd_1_4_2","动态防御","Dynamic Defense",
    """modifier = {
\t\t\t\tland_reinforce_rate = 0.03
\t\t\t}
\t\t\tcategory_army = { defense = 0.25 max_organisation = 5 }
\t\t\tcategory_AllValkyrie = { maximum_speed = 0.05 defense = 0.1 max_organisation = 5 }"""),
   ("bh3_rwd_1_5_2","战场救火队","Fire Brigade Tactics",
    """category_ValkyrieMeele = { max_organisation = 8 defense = 0.1 }
\t\t\tcategory_ValkyrieArtillery = { max_organisation = 3 defense = 0.05 }
\t\t\tcategory_ValkyrieArmor = { max_organisation = 3 defense = 0.05 }"""),
   ("bh3_rwd_1_6_2","后发制人","Counteroffensive Doctrine",
    """modifier = {
\t\t\t\tland_reinforce_rate = 0.03
\t\t\t\tplanning_speed = 0.25
\t\t\t}
\t\t\tcategory_army = { max_organisation = 10 default_morale = 0.25 }""")],
  None,
  "整合旧学说树近战线主干与防御分叉：近接歼灭→快速接敌→武装侦查→动态防御→战场救火队→后发制人。随轨道精通逐级解锁，全部达成后等同旧线完全体。",
  "Integrates the old melee line trunk and its defensive branch: Annihilation→Rapid Engagement→Armed Recon→Dynamic Defense→Fire Brigade→Counteroffensive. Unlocks step by step with track mastery; full mastery equals the old line's complete form."),
 # —— 装甲突击轨：旧线1进攻分叉 α（1_4_1→1_5_1→1_6_1） ——
 ("bh3_sd_persistence","valkyrie_armor","持久攻势","Sustained Offensive","GFX_doctrine_human_infantry_offensive_medium",
  """modifier = {
\t\tland_reinforce_rate = 0.03
\t}
\tcategory_army = { breakthrough = 0.15 }
\tcategory_AllValkyrie = { max_organisation = 5 breakthrough = 0.1 }""",
  [("bh3_rwd_1_5_1","弱点洞悉","Weakness Analysis",
    """category_ValkyrieMeele = { hard_attack = 0.15 soft_attack = 0.15 ap_attack = 0.15 }
\t\t\tcategory_ValkyrieComprehensive = { hard_attack = 0.15 soft_attack = 0.15 ap_attack = 0.15 }
\t\t\tcategory_ValkyrieArmor = { hard_attack = 0.05 soft_attack = 0.05 ap_attack = 0.05 }"""),
   ("bh3_rwd_1_6_1","天元突破","Heaven-Piercing Assault",
    """modifier = {
\t\t\t\tmax_planning = 0.15
\t\t\t\tland_night_attack = 0.15
\t\t\t}
\t\t\tcategory_AllValkyrie = { hard_attack = 0.05 soft_attack = 0.05 breakthrough = 0.25 default_morale = 0.5 }""")],
  None,
  "整合旧学说树近战线进攻分叉：持久攻势→弱点洞悉→天元突破。反装甲输出与总攻能力的极致。",
  "Integrates the old melee line's offensive branch: Sustained Offensive→Weakness Analysis→Heaven-Piercing Assault. The pinnacle of anti-armor output and grand assault."),
 # —— 近战攻坚轨：旧线3前段（3_1→3_2→3_3→3_4） ——
 ("bh3_sd_rear_ops","valkyrie_assault","敌后作战","Behind Enemy Lines","GFX_doctrine_commandos_medium",
  """modifier = {
\t\tspecial_forces_no_supply_grace = 240
\t\tout_of_supply_factor = -0.2
\t\tpocket_penalty = -0.2
\t}""",
  [("bh3_rwd_3_2","战斗穿插","Combat Penetration",
    "category_AllValkyrie = { soft_attack = 0.1 hard_attack = 0.1 }"),
   ("bh3_rwd_3_3","空降突击","Airborne Assault",
    """modifier = {
\t\t\t\tspecial_forces_no_supply_grace = 240
\t\t\t\tair_cas_present_factor = 0.15
\t\t\t\tair_range_factor = 0.25
\t\t\t}"""),
   ("bh3_rwd_3_4","专业训练","Specialized Training",
    """modifier = {
\t\t\t\tspecial_forces_attack_factor = 0.15
\t\t\t}
\t\t\tcategory_AllValkyrie = { armor_value = 0.15 defense = 0.15 }""")],
  None,
  "整合旧学说树特战线前段：敌后作战→战斗穿插→空降突击→专业训练。女武神小队的特种作战体系。",
  "Integrates the old special-ops line's first half: Behind Enemy Lines→Combat Penetration→Airborne Assault→Specialized Training. The Valkyrie squads' special operations doctrine."),
 # —— 战斗支援轨：旧线2主干 + 弹幕支线 + 终点（2_1→2_2→2_3→2_5_1→2_6） ——
 ("bh3_sd_ranged_suppression","valkyrie_support","远程压制战术","Long-Range Suppression Tactics","GFX_doctrine_fire_concentration_medium",
  """category_ValkyrieMeele = { soft_attack = 0.05 }
\tcategory_ValkyrieComprehensive = { soft_attack = 0.1 }
\tcategory_ValkyrieArtillery = { soft_attack = 0.15 }
\tcategory_ValkyrieArmor = { soft_attack = 0.05 }""",
  [("bh3_rwd_2_2","抵近观测","Close Observation",
    """category_ValkyrieMeele = { maximum_speed = 0.05 max_organisation = 5 }
\t\t\tcategory_ValkyrieComprehensive = { maximum_speed = 0.05 max_organisation = 5 }
\t\t\tcategory_ValkyrieArtillery = { soft_attack = 0.1 hard_attack = 0.1 ap_attack = 0.05 }
\t\t\tcategory_ValkyrieArmor = { maximum_speed = 0.05 }"""),
   ("bh3_rwd_2_3","火力调配","Firepower Allocation",
    """modifier = {
\t\t\t\tadditional_brigade_column_size = 1
\t\t\t\tmax_planning = 0.15
\t\t\t}
\t\t\tcategory_army = { max_organisation = 5 }"""),
   ("bh3_rwd_2_5_1","弹幕覆盖","Barrage Coverage",
    "category_army = { soft_attack = 0.3 hard_attack = 0.05 }"),
   ("bh3_rwd_2_6","全域压制","Full-Spectrum Suppression",
    """modifier = {
\t\t\t\tarmy_bonus_air_superiority_factor = 0.15
\t\t\t\tair_cas_present_factor = 0.15
\t\t\t}
\t\t\tcategory_ValkyrieArtillery = { soft_attack = 0.1 air_attack = 0.2 max_organisation = 10 }
\t\t\tcategory_ValkyrieArmor = { soft_attack = 0.05 }
\t\t\tcategory_army = { air_attack = 0.2 }""")],
  None,
  "整合旧学说树支援线：远程压制→抵近观测→火力调配→弹幕覆盖→全域压制。以火力与制空为核心的支援体系。",
  "Integrates the old support line: Suppression→Close Observation→Firepower Allocation→Barrage Coverage→Full-Spectrum Suppression. A support system built on firepower and air dominance."),
 # —— 纵深作战轨：旧线2协同分叉 + 线3终点（2_4_1→2_4_2→2_5_2→3_6） ——
 ("bh3_sd_dispersed_support","valkyrie_operations","分散支援","Dispersed Support","GFX_doctrine_dispersed_operations_medium",
  """modifier = {
\t\tcoordination_bonus = 0.05
\t\tland_reinforce_rate = 0.05
\t\tsupply_consumption_factor = -0.10
\t}
\tcategory_army = { max_organisation = 5 }""",
  [("bh3_rwd_2_4_2","协调支援","Coordinated Support",
    """modifier = {
\t\t\t\tcoordination_bonus = 0.10
\t\t\t\tland_reinforce_rate = 0.05
\t\t\t}
\t\t\tcategory_army = { soft_attack = 0.1 hard_attack = 0.1 }"""),
   ("bh3_rwd_2_5_2","联合兵种","Combined Arms",
    "category_army = { soft_attack = 0.1 hard_attack = 0.1 max_organisation = 10 }"),
   ("bh3_rwd_3_6","协同作战","Joint Operations",
    """modifier = {
\t\t\t\tcoordination_bonus = 0.10
\t\t\t\tsupply_consumption_factor = -0.05
\t\t\t}
\t\t\tcategory_army = { soft_attack = 0.05 hard_attack = 0.05 maximum_speed = 0.1 }""")],
  None,
  "整合旧学说树支援线协同分叉与特战线终点：分散支援→协调支援→联合兵种→协同作战。大军团协同与纵深作战。",
  "Integrates the old support line's coordination branch and the special-ops line's finale: Dispersed Support→Coordinated Support→Combined Arms→Joint Operations. Mass-army coordination and deep operations."),
 # —— 律者降临轨：新设（觉醒 base + 统御 reward@100） ——
 ("bh3_sd_herrscher_awaken","valkyrie_herrscher","律者觉醒","Herrscher Awakening","GFX_doctrine_deep_battle_medium",
  """category_AllHerrscher = { max_organisation = 50 default_morale = 0.25 }
\tmodifier = {
\t\tarmy_speed_factor = 0.05
\t}""",
  [("bh3_rwd_herrscher_rule","律者统御","Herrscher Domination",
    "category_AllHerrscher = { soft_attack = 0.25 hard_attack = 0.25 defense = 0.25 }")],
  None,
  "律者之力降临战场。轨道精通达到 100 时，进一步解锁「律者统御」。",
  "The Herrscher's power descends upon the battlefield. At 100 track mastery, 'Herrscher Domination' is further unlocked."),
 # —— 女武神特战轨：旧线3互斥对（3_5_1 vs 3_5_2，旧系统唯一真互斥） ——
 ("bh3_sd_superior_numbers","valkyrie_special","优势兵力","Superior Numbers","GFX_doctrine_peoples_war_medium",
  """modifier = {
\t\tadditional_brigade_column_size = 1
\t\tspecial_forces_cap = 0.10
\t}""",
  [],
  "NOT = { has_doctrine = bh3_sd_refined }",
  "以数量与编制宽度取胜：旅编制额外一列，特种兵力上限提升。与「精益求精」互斥。",
  "Win through numbers and formation width: +1 brigade column, higher special forces cap. Mutually exclusive with 'Perfectionism'."),
 ("bh3_sd_refined","valkyrie_special","精益求精","Perfectionism","GFX_doctrine_mission_type_tactics_medium",
  """category_AllValkyrie = { soft_attack = 0.15 hard_attack = 0.15 armor_value = 0.15 }""",
  [],
  "NOT = { has_doctrine = bh3_sd_superior_numbers }",
  "以质量强化取胜：全体女武神攻击与装甲全面提升。与「优势兵力」互斥。",
  "Win through quality: all Valkyries gain attack and armor. Mutually exclusive with 'Superior Numbers'."),
]

def subdoctrine_block(t):
    key, track, cn, en, icon, fx, rewards, avail_extra, cn_desc, en_desc = t
    avail = avail_extra if avail_extra else "always = yes"
    rewards_txt = ""
    if rewards:
        blocks = []
        # mastery 语义 = 相对上一档的【新增】精通需求（原版/参考 mod 均统一常数：原版 50、参考 mod 100），
        # 非绝对值。用户定调（2026-10-10）：每档新增统一 150 点 → 每档 mastery = 150，满级 = 150×档数。
        for rkey, rcn, ren, rfx in rewards:
            mastery = 150
            blocks.append(f'''\t\t{rkey} = {{
\t\t\tmastery = {mastery}
{rfx}
\t\t}}''')
        rewards_txt = "\n\trewards = {\n" + "\n".join(blocks) + "\n\t}\n"
    else:
        rewards_txt = ""
    rewards_block = f"""
{rewards_txt}""" if rewards_txt else ""
    return f'''{key} = {{
    track = {track}
    name = BH3_sd_{key}
    description = BH3_sd_{key}_desc
    icon = {icon}

    xp_cost = 100
    xp_type = army

    available = {{
        {avail}
    }}

    ai_will_do = {{
        base = 1
    }}

    # 基础效果（= 旧学说链首节点）
{fx}
{rewards_block}}}
'''

SUBDOCTRINES = ''.join(subdoctrine_block(t) for t in SD)

# ---------------- 本地化 ----------------
CN_EXTRA = {
 "BH3_doctrine_folder_valkyrie": "女武神作战学说",
 "BH3_grand_doctrine_valkyrie": "对崩坏作战理论",
 "BH3_grand_doctrine_valkyrie_desc": "以女武神小队为核心、面向崩坏兽与常规战争的双重作战体系。解锁后可在七条学说线中继续钻研：步兵协同 / 战斗支援 / 装甲突击 / 纵深作战 / 近战攻坚 / 律者降临 / 女武神特战。",
 "BH3_doctrine_track_infantry": "步兵协同",
 "BH3_doctrine_track_support": "战斗支援",
 "BH3_doctrine_track_armor": "装甲突击",
 "BH3_doctrine_track_operations": "纵深作战",
 "BH3_doctrine_track_assault": "近战攻坚",
 "BH3_doctrine_track_herrscher": "律者降临",
 "BH3_doctrine_track_special": "女武神特战",
}
EN_EXTRA = {
 "BH3_doctrine_folder_valkyrie": "Valkyrie Combat Doctrine",
 "BH3_grand_doctrine_valkyrie": "Anti-Honkai Combat Theory",
 "BH3_grand_doctrine_valkyrie_desc": "A dual-purpose combat system centered on Valkyrie squads, aimed at both Honkai beasts and conventional warfare. Once unlocked, delve into seven doctrine tracks: Infantry / Combat Support / Armor / Deep Operations / Close Assault / Herrscher Advent / Valkyrie Special Ops.",
 "BH3_doctrine_track_infantry": "Infantry Coordination",
 "BH3_doctrine_track_support": "Combat Support",
 "BH3_doctrine_track_armor": "Armored Assault",
 "BH3_doctrine_track_operations": "Deep Operations",
 "BH3_doctrine_track_assault": "Close Assault",
 "BH3_doctrine_track_herrscher": "Herrscher Advent",
 "BH3_doctrine_track_special": "Valkyrie Special Ops",
}
def cn_entry(t):
    key, track, cn, en, icon, fx, rewards, avail_extra, cn_desc, en_desc = t
    rows = [f"BH3_sd_{key}:0 \"§Y{cn}§!\"", f"BH3_sd_{key}_desc:0 \"{cn_desc}\""]
    for rkey, rcn, ren, rfx in rewards:
        rows.append(f"{rkey}:0 \"{rcn}\"")
    return rows
def en_entry(t):
    key, track, cn, en, icon, fx, rewards, avail_extra, cn_desc, en_desc = t
    rows = [f"BH3_sd_{key}:0 \"§Y{en}§!\"", f"BH3_sd_{key}_desc:0 \"{en_desc}\""]
    for rkey, rcn, ren, rfx in rewards:
        rows.append(f"{rkey}:0 \"{ren}\"")
    return rows

def purge_old(path):
    """清除 v3 及以前遗留的 bh3_sd_/bh3_rwd_/BH3_sd_ 死键，避免 yml 里堆积未引用条目。"""
    with io.open(path, encoding='utf-8-sig') as f:
        lines = f.read().split('\n')
    keep = [l for l in lines if not l.lstrip().startswith(('BH3_sd_bh3_', 'bh3_rwd_'))]
    removed = len(lines) - len(keep)
    if removed:
        nl = '\n' if path.endswith('simp_chinese.yml') else '\r\n'
        with io.open(path, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(nl.join(keep))
        print(f"清理 {removed} 旧键: {path}")

def append_loc(path, entries, extra):
    with io.open(path, encoding='utf-8-sig') as f:
        content = f.read()
    new_keys = []
    for k, v in extra.items():
        new_keys.append(f"{k}:0 \"{v}\"")
    for e in entries:
        new_keys.extend(e)
    add = [l for l in new_keys if l.split(':')[0] not in content]
    if not add:
        print(f"跳过（已存在）: {path}")
        return
    with io.open(path, 'a', encoding='utf-8', newline='') as f:
        for l in add:
            f.write("\n" + l if path.endswith('simp_chinese.yml') else "\r\n" + l)
    print(f"追加 {len(add)} 键: {path}")

# ---------------- 写出 ----------------
def w(rel, text):
    p = os.path.join(WS, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print("写出", rel)

w('common/doctrines/folders/BH3_doctrine_folders.txt', FOLDER)
w('common/doctrines/grand_doctrines/BH3_valkyrie_grand_doctrine.txt', GRAND)
w('common/doctrines/tracks/BH3_valkyrie_tracks.txt', TRACKS)
w('common/doctrines/subdoctrines/land/BH3_valkyrie_subdoctrines.txt', SUBDOCTRINES)
CN_LOC = os.path.join(WS, 'localisation/simp_chinese/BH3_doctrine_l_simp_chinese.yml')
EN_LOC = os.path.join(WS, 'localisation/BH3_doctrine_l_english.yml')
purge_old(CN_LOC)
purge_old(EN_LOC)
append_loc(CN_LOC, [cn_entry(t) for t in SD], CN_EXTRA)
append_loc(EN_LOC, [en_entry(t) for t in SD], EN_EXTRA)
print("完成：", len(SD), "个子学说 / 7 条轨道")
