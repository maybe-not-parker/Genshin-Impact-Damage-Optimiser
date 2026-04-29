def azurelight(weapon, character, attack):
        if "e" not in attack:
             return
        for key in list(character.weapon_effect_stats):
              character.total_stats[key] -= character.weapon_effect_stats[key]
              character.weapon_effect_stats[key] = 0


        stat, value = weapon["conditional_affix"]["on_skill"].split("_")
        character.total_stats[stat] += int(value)
        character.weapon_effect_stats[stat] += int(value)

        if character.energy == 0:
            for effect in weapon["conditional_affix"]["energy"].split("/"):
                stat, value = effect.split("_")
                character.total_stats[stat] += int(value)
                character.weapon_effect_stats[stat] += int(value)

        return

def staff_of_homa(weapon, character):
        for key in list(character.weapon_effect_stats):
                character.total_stats[key] -= character.weapon_effect_stats[key]
                character.weapon_effect_stats[key] = 0
    
        character.total_stats["ATK"] += character.total_stats["HP"] * 0.008
        character.weapon_effect_stats["ATK"] += character.total_stats["HP"] * 0.008
    
        return
