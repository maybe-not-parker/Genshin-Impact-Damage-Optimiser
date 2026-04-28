def clear_set_effects(character):
    for key in character.set_effect_stats:
        character.total_stats[key] -= character.set_effect_stats[key]
        character.set_effect_stats[key] = 0

def pale_flame(file, character, stacks=2):
    clear_set_effects(character)
    stacks = min(stacks, 2)
    character.artifact_total_stats[file["PF"]["4p"].split("_")[0]] += int(file["PF"]["4p"].split("_")[1])*stacks
    character.set_effect_stats[file["PF"]["4p"].split("_")[0]] += int(file["PF"]["4p"].split("_")[1])*stacks
    if stacks == 2:
        character.artifact_total_stats[file["PF"]["2p"].split("_")[0]] += int(file["PF"]["2p"].split("_")[1])
        character.set_effect_stats[file["PF"]["2p"].split("_")[0]] += int(file["PF"]["2p"].split("_")[1])

def marechaussee(file, character, stacks = 3):
    clear_set_effects(character)
    stacks = min(stacks, 3)
    character.total_stats[file["MH"]["4p"].split("_")[0]] += int(file["MH"]["4p"].split("_")[1])*stacks
    character.set_effect_stats[file["MH"]["4p"].split("_")[0]] += int(file["MH"]["4p"].split("_")[1])*stacks
    