from itertools import combinations_with_replacement

def main_stat_values(main_stat):
       main_values = {"HP%": 46.6,
                      "HP": 4780,
                      "ATK%": 46.6,
                      "ATK": 311,
                      "DEF%": 58.3,
                      "EM": 186.5,
                      "ER%": 51.8,
                      "CR": 31.1,
                      "CD": 62.2,
                      "PHYSICAL": 58.3,
                      "PYRO": 46.6,
                      "HYDRO": 46.6,
                      "ELECTRO": 46.6,
                      "GEO": 46.6,
                      "DENDRO": 46.6,
                      "ANEMO": 46.6,
                      "CRYO": 46.6}
       return main_values[main_stat]

def damage_formula(
    talent_multiplier = 0,
    stat_scaling = 0,
    crit_rate = 0.05,
    crit_damage = 0.5,
    character_level = 90,
    enemy_level = 90,
    elemental_mastery = 0,
    reaction_multiplier = 0,
    reaction_bonus = 0,
    reaction = False,
    defense_reduction = 0,
    defense_ignore = 0,
    enemy_base_resistance = 0.1,
    resistance_reduction = 0,
    base_damage_multiplier=1,
    additive_base_damage_bonus=0,
    damage_bonus = 0,
    damage_reduction_target=0
):
       #crit = 1 + crit_rate/100 * crit_damage/100 if crit_rate < 100 else 1 + crit_damage/100
       crit = 1 + crit_damage/100
       enemy_defense_mult = (character_level+100)/((character_level+100)+(enemy_level+100)*(1-defense_ignore)*(1-defense_reduction))
       resistance = enemy_base_resistance - resistance_reduction
       if resistance < 0:
              enemy_res_mult = 1 - (resistance/2)
       elif resistance >= 0 and resistance < 0.75:
              enemy_res_mult = 1 - resistance
       elif resistance >= 0.75:
              enemy_res_mult = 1/(4 * resistance + 1)
       base_damage = (talent_multiplier/100)*stat_scaling
       damage = ((base_damage*base_damage_multiplier) + additive_base_damage_bonus) * (1+(damage_bonus/100)-damage_reduction_target) *crit * enemy_defense_mult * enemy_res_mult
       if reaction:
              amplifying_reaction = reaction_multiplier * (1 + ((2.78*elemental_mastery) / (1400 + elemental_mastery) + reaction_bonus))
              damage *= amplifying_reaction
       
       return damage

def calculate_roll(roll, roll_type, roll_data):
       possible_rolls = roll_data[roll_type]
       best = None
       max_rolls = 6
       best_diff = float('inf')
       
       for r in range(1, max_rolls + 1):
              for combo in combinations_with_replacement(possible_rolls, r):
                     diff = abs(sum(combo) - roll)
                     if diff < best_diff:
                            best_diff = diff
                            best = combo
       
       return best

def apply_weapon_conditional(file, character, trigger):
       conditionals = character.weapon.get("conditionals", {})
       effect = conditionals.get(trigger, {})
       for stat, value in effect.items():
              character.total_stats[stat] += value
              character.set_effect_stats[stat] += value

def clear_weapon_conditionals(file, character, trigger):
       conditionals = character.weapon.get("conditionals", {})
       effect = conditionals.get(trigger, {})
       for stat, value in effect.items():
              character.total_stats[stat] -= value
              character.set_effect_stats[stat] -= value

def skirk_combo(skirk):
       num = 0
       num += skirk.calculate_damage("te")
       num += skirk.calculate_damage("n1")
       num += skirk.calculate_damage("n2")
       num += skirk.calculate_damage("q")
       num += skirk.calculate_damage("n1")
       num += skirk.calculate_damage("n2")
       return num

def team_resonance(team):
       character_elements = [character.character_data["element"].lower() for character in team]
       if character_elements.count("cryo") >= 2:
              return {"CR": 15}
       if character_elements.count("hydro") >= 2:
              return {"HP%": 25}
       if character_elements.count("pyro") >= 2:
              return {"ATK%": 25}
       if character_elements.count("electro") >= 2:
              return {"ELECTRO%": 15}
       if character_elements.count("anemo") >= 2:
              return #{"ANEMO%": 15}
       if character_elements.count("geo") >= 2:
              return #{"GEO%": 15}
       if character_elements.count("dendro") >= 2:
              return #{"DENDRO%": 15}