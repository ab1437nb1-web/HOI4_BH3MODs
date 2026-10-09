# -*- coding: utf-8 -*-
"""按崩坏3往世乐土原作命名为 60 枚刻印的显示名赋值（只改本地化值，不改键名/机制）。"""
import re, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CN = {
    # 救世（凯文）——核心/增幅沿用现名（本就含原名）
    "BH3_ER_Savior_1":    "救世·Ⅰ 猎杀者的假面",
    "BH3_ER_Savior_2":    "救世·Ⅱ 施予者的金杯",
    "BH3_ER_Savior_3":    "救世·Ⅲ 守望者的坠饰",
    "BH3_ER_Setsuna_1":   "刹那·Ⅰ 缭乱百花「梅」",
    "BH3_ER_Setsuna_2":   "刹那·Ⅱ 缭乱百花「红叶」",
    "BH3_ER_Setsuna_3":   "刹那·Ⅲ 缭乱百花「牡丹」",
    "BH3_ER_Setsuna_Core":  "刹那·核心刻印：刹那一刀「樱上幕」",
    "BH3_ER_Setsuna_Amp":   "刹那·增幅刻印：雨四光",
    "BH3_ER_Bodhi_1":     "天慧·Ⅰ 宿命之箴言",
    "BH3_ER_Bodhi_2":     "天慧·Ⅱ 天眼之箴言",
    "BH3_ER_Bodhi_3":     "天慧·Ⅲ 天耳之箴言",
    "BH3_ER_Bodhi_Core":  "天慧·核心刻印：天慧之真言",
    "BH3_ER_Bodhi_Amp":   "天慧·增幅刻印：寂静之真言",
    "BH3_ER_Gold_1":      "黄金·Ⅰ 乐园的宣叙",
    "BH3_ER_Gold_2":      "黄金·Ⅱ 溪流的宣叙",
    "BH3_ER_Gold_3":      "黄金·Ⅲ 美酒的宣叙",
    "BH3_ER_Gold_Core":   "黄金·核心刻印：黄金的余音",
    "BH3_ER_Gold_Amp":    "黄金·增幅刻印：枯壤的余音",
    "BH3_ER_Kalpas_1":    "鏖灭·Ⅰ 狂信·狂人·狂言",
    "BH3_ER_Kalpas_2":    "鏖灭·Ⅱ 命路·命舛·命刻",
    "BH3_ER_Kalpas_3":    "鏖灭·Ⅲ 无妄·无心·无归",
    "BH3_ER_Kalpas_Core": "鏖灭·核心刻印：鏖斗·鏖战·鏖杀·鏖灭",
    "BH3_ER_Kalpas_Amp":  "鏖灭·增幅刻印：非人·非鬼·非神·非天",
    "BH3_ER_Fusheng_1":   "浮生·Ⅰ 行路漫漫",
    "BH3_ER_Fusheng_2":   "浮生·Ⅱ 日月蹉跎",
    "BH3_ER_Fusheng_3":   "浮生·Ⅲ 玄衣不再",
    "BH3_ER_Fusheng_Core": "浮生·核心刻印：浮生历历，百态无常",
    "BH3_ER_Fusheng_Amp": "浮生·增幅刻印：似曾相识，却又相忘",
    "BH3_ER_Aponia_1":    "戒律·Ⅰ 其一，不可背叛",
    "BH3_ER_Aponia_2":    "戒律·Ⅱ 其二，不可欺瞒",
    "BH3_ER_Aponia_3":    "戒律·Ⅲ 其三，不可暴戾",
    "BH3_ER_Aponia_Core": "戒律·核心刻印：汝，当为戒律所佑",
    "BH3_ER_Aponia_Amp":  "戒律·增幅刻印：汝，当见诸恶得惩",
    "BH3_ER_Spiral_1":    "螺旋·Ⅰ 第一幕「魔术」",
    "BH3_ER_Spiral_2":    "螺旋·Ⅱ 第二幕「钟摆」",
    "BH3_ER_Spiral_3":    "螺旋·Ⅲ 第三幕「矛盾」",
    "BH3_ER_Spiral_Core": "螺旋·核心刻印：幕间剧「逆转的螺旋」",
    "BH3_ER_Spiral_Amp":  "螺旋·增幅刻印：第七幕「虚掩的门扉」",
    "BH3_ER_Mobius_1":    "无限·Ⅰ 利齿的「V」",
    "BH3_ER_Mobius_2":    "无限·Ⅱ 缠环的「P」",
    "BH3_ER_Mobius_3":    "无限·Ⅲ 静默的「B」",
    "BH3_ER_Mobius_Core": "无限·核心刻印：无限的「X」",
    "BH3_ER_Mobius_Amp":  "无限·增幅刻印：死亡的「X」",
    "BH3_ER_Kosma_1":     "旭光·Ⅰ 亵渎不归之「爪」",
    "BH3_ER_Kosma_2":     "旭光·Ⅱ 掩蔽血月之「翼」",
    "BH3_ER_Kosma_3":     "旭光·Ⅲ 撕裂暗空之「角」",
    "BH3_ER_Kosma_Core":  "旭光·核心刻印：旭光，长明不落",
    "BH3_ER_Kosma_Amp":   "旭光·增幅刻印：英雄，独担兴衰",
    "BH3_ER_Griseo_1":    "繁星·Ⅰ 红色的，热烈的",
    "BH3_ER_Griseo_2":    "繁星·Ⅱ 黄色的，暖暖的",
    "BH3_ER_Griseo_3":    "繁星·Ⅲ 蓝色的，冷冷的",
    "BH3_ER_Griseo_Core": "繁星·核心刻印：像是繁星，闪耀着的",
    "BH3_ER_Griseo_Amp":  "繁星·增幅刻印：像是野花，飞散了的",
    "BH3_ER_Pardofelis_1": "空梦·Ⅰ 值钱的，闪闪的",
    "BH3_ER_Pardofelis_2": "空梦·Ⅱ 行商者的哲学",
    "BH3_ER_Pardofelis_3": "空梦·Ⅲ 街巷的宣叙",
    "BH3_ER_Pardofelis_Core": "空梦·核心刻印：空梦·空集·空我·空欢",
    "BH3_ER_Pardofelis_Amp":  "空梦·增幅刻印：即兴短剧「老板」",
}

EN = {
    "BH3_ER_Savior_1":    "Deliverance I: Mask of the Hunter",
    "BH3_ER_Savior_2":    "Deliverance II: Goblet of the Giver",
    "BH3_ER_Savior_3":    "Deliverance III: Pendant of the Watcher",
    "BH3_ER_Setsuna_1":   "Setsuna I: Ryouran Hyakka 'Ume'",
    "BH3_ER_Setsuna_2":   "Setsuna II: Ryouran Hyakka 'Kouyou'",
    "BH3_ER_Setsuna_3":   "Setsuna III: Ryouran Hyakka 'Botan'",
    "BH3_ER_Setsuna_Core":  "Setsuna Core: Sakura Blade 'Sakuragami'",
    "BH3_ER_Setsuna_Amp":   "Setsuna Amp: 'Ushikou'",
    "BH3_ER_Bodhi_1":     "Bodhi I: Proverb of Destiny",
    "BH3_ER_Bodhi_2":     "Bodhi II: Proverb of the Divine Eye",
    "BH3_ER_Bodhi_3":     "Bodhi III: Proverb of the Divine Ear",
    "BH3_ER_Bodhi_Core":  "Bodhi Core: Mantra of Bodhi",
    "BH3_ER_Bodhi_Amp":   "Bodhi Amp: Mantra of Silence",
    "BH3_ER_Gold_1":      "Gold I: Recitative of Paradise",
    "BH3_ER_Gold_2":      "Gold II: Recitative of the Stream",
    "BH3_ER_Gold_3":      "Gold III: Recitative of Fine Wine",
    "BH3_ER_Gold_Core":   "Gold Core: Echo of Gold",
    "BH3_ER_Gold_Amp":    "Gold Amp: Echo of the Withered Land",
    "BH3_ER_Kalpas_1":    "Kalpas I: Zealotry, Madman, Wild Words",
    "BH3_ER_Kalpas_2":    "Kalpas II: Fate, Misfortune, Destiny",
    "BH3_ER_Kalpas_3":    "Kalpas III: Innocence, Heartlessness, No Return",
    "BH3_ER_Kalpas_Core": "Kalpas Core: Strife, War, Slaughter, Kalpas",
    "BH3_ER_Kalpas_Amp":  "Kalpas Amp: Inhuman, Unholy, Ungodly, Unworldly",
    "BH3_ER_Fusheng_1":   "Vicissitude I: The Long Road",
    "BH3_ER_Fusheng_2":   "Vicissitude II: Wasted Years",
    "BH3_ER_Fusheng_3":   "Vicissitude III: The Black Robe No More",
    "BH3_ER_Fusheng_Core": "Vicissitude Core: A Life of Vicissitudes",
    "BH3_ER_Fusheng_Amp": "Vicissitude Amp: Familiar, Yet Forgotten",
    "BH3_ER_Aponia_1":    "Discipline I: First, Thou Shalt Not Betray",
    "BH3_ER_Aponia_2":    "Discipline II: Second, Thou Shalt Not Deceive",
    "BH3_ER_Aponia_3":    "Discipline III: Third, Thou Shalt Not Rage",
    "BH3_ER_Aponia_Core": "Discipline Core: Thou Shalt Be Blessed by Discipline",
    "BH3_ER_Aponia_Amp":  "Discipline Amp: Thou Shalt See the Wicked Punished",
    "BH3_ER_Spiral_1":    "Helix I: Act I 'Magic'",
    "BH3_ER_Spiral_2":    "Helix II: Act II 'Pendulum'",
    "BH3_ER_Spiral_3":    "Helix III: Act III 'Paradox'",
    "BH3_ER_Spiral_Core": "Helix Core: Interlude 'Reversing Spiral'",
    "BH3_ER_Spiral_Amp":  "Helix Amp: Act VII 'The Ajar Door'",
    "BH3_ER_Mobius_1":    "Infinity I: Fangs 'V'",
    "BH3_ER_Mobius_2":    "Infinity II: Coils 'P'",
    "BH3_ER_Mobius_3":    "Infinity III: Silence 'B'",
    "BH3_ER_Mobius_Core": "Infinity Core: Infinity 'X'",
    "BH3_ER_Mobius_Amp":  "Infinity Amp: Death 'X'",
    "BH3_ER_Kosma_1":     "Daybreak I: Claws of Profanity",
    "BH3_ER_Kosma_2":     "Daybreak II: Wings of the Blood Moon",
    "BH3_ER_Kosma_3":     "Daybreak III: Horns that Rend the Dark Sky",
    "BH3_ER_Kosma_Core":  "Daybreak Core: Daybreak, Everlasting",
    "BH3_ER_Kosma_Amp":   "Daybreak Amp: Hero, Bearer of Rise and Fall",
    "BH3_ER_Griseo_1":    "Stars I: Red, the Warm",
    "BH3_ER_Griseo_2":    "Stars II: Yellow, the Cozy",
    "BH3_ER_Griseo_3":    "Stars III: Blue, the Cold",
    "BH3_ER_Griseo_Core": "Stars Core: Like Stars, Shining",
    "BH3_ER_Griseo_Amp":  "Stars Amp: Like Wildflowers, Scattered",
    "BH3_ER_Pardofelis_1": "Reverie I: Shiny, Valuable",
    "BH3_ER_Pardofelis_2": "Reverie II: Philosophy of the Peddler",
    "BH3_ER_Pardofelis_3": "Reverie III: Street Recitative",
    "BH3_ER_Pardofelis_Core": "Reverie Core: Empty Dream, Empty Set, Empty Self, Empty Joy",
    "BH3_ER_Pardofelis_Amp":  "Reverie Amp: Improv 'The Boss'",
}

FILES = [
    (os.path.join(ROOT, "localisation", "simp_chinese", "BH3_equipment_l_simp_chinese.yml"), CN),
    (os.path.join(ROOT, "localisation", "BH3_equipment_l_english.yml"), EN),
]

def main():
    for path, mapping in FILES:
        raw = open(path, "rb").read()
        had_bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        lines = text.splitlines(True)
        replaced = set()
        out = []
        for line in lines:
            m = re.match(r'^(\s*([A-Za-z0-9_]+):0\s*")(.*)("\s*(?:\r?\n)?)$', line)
            if m and m.group(2) in mapping:
                key = m.group(2)
                if key in replaced:
                    print(f"DUPLICATE KEY {key} in {path}", file=sys.stderr); sys.exit(1)
                out.append(m.group(1) + mapping[key] + m.group(4))
                replaced.add(key)
            else:
                out.append(line)
        missing = set(mapping) - replaced
        if missing:
            print(f"MISSING KEYS in {path}: {sorted(missing)}", file=sys.stderr); sys.exit(1)
        data = "".join(out).encode("utf-8")
        if had_bom:
            data = b"\xef\xbb\xbf" + data
        open(path, "wb").write(data)
        print(f"OK {os.path.basename(path)}: {len(replaced)} keys renamed")

if __name__ == "__main__":
    main()
