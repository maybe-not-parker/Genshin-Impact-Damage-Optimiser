import json
import helper_functions
from collections import Counter
import artifact_effects
import weapon_effects

with open("character_data.json", "r") as file:
      character_list = json.load(file)
with open("weapon_data.json", "r") as file:
      weapon_list = json.load(file)
with open("artifact_data.json", "r") as file:
      artifact_list = json.load(file)
with open("roll_data.json", "r") as file:
      artifact_roll_data = json.load(file)

enemy_level = 100
weapon_effects = {
      "azurelight" : weapon_effects.azurelight
}
class Enemy():
      def __init__(self, level=90):
            self.enemy_level = level

class Character():
      def __init__(self, character, level, constellation=0, talents=[9,9,9]):
            self.character_level = level
            self.constellation = constellation
            self.talents = talents
            self.energy = 0

            for name, data in character_list.items():
                  if name == character:
                        self.character_data = data
                        break
            multiplier_map = ["normal_attack_multiplier", "skill_multiplier", "burst_multiplier", "a1_multiplier", "a4_multiplier"]
            for header, multiplier in self.character_data.items():
                  if header in multiplier_map:
                        setattr(self, header, multiplier)
            
            return
      def init_base_stats(self):
            self.base_stats = {}
            for header, multipliers in self.character_data.items():
                  if header == "base_stats":
                        self.base_stats["HP"] = multipliers["HP"]
                        self.base_stats["ATK"] = multipliers["ATK"]
                        self.base_stats["DEF"] = multipliers["DEF"]
                        self.base_stats["CR"] = multipliers["CR"]
                        self.base_stats["CD"] = multipliers["CD"]
                        self.base_stats["EM"] = 0
                        self.base_stats["ATK%"] = 0
                        self.base_stats["HP%"] = 0
                        self.base_stats["DEF%"] = 0
                        #self.bonus_ascension = bonus_ascension
                        self.bonus_stat = [multipliers["bonus_ascension"].split("_")[0], multipliers["bonus_ascension"].split("_")[1]]
                        
                        
                        break
             
            return
      def insert_artifact(self, main_stat, sub_stat, artifact_type, artifact_set):
            valid_types = {"flower", "feather", "sands", "circlet", "goblet"}
            if artifact_type not in valid_types:
                  raise ValueError(f"Invalid artifact type: {artifact_type}")            
            setattr(self, f"{artifact_type}_main_stat", {main_stat: helper_functions.main_stat_values(main_stat)})
            setattr(self, f"{artifact_type}_sub_stats", sub_stat)
            setattr(self, f"{artifact_type}_type", artifact_type)
            setattr(self, f"{artifact_type}_set", artifact_set)
                  
      def flower_artifact(self, main_stat, sub_stat):
            self.flower_main_stat = {main_stat: helper_functions.main_stat_values(main_stat)}
            self.flower_sub_stats = sub_stat
            return
      def feather_artifact(self, main_stat, sub_stat):
            self.feather_main_stat = {main_stat: helper_functions.main_stat_values(main_stat)}
            self.feather_sub_stats = sub_stat            
            return
      def sands_artifact(self, main_stat, sub_stat):
            self.sands_main_stat = {main_stat: helper_functions.main_stat_values(main_stat)}
            self.sands_sub_stats = sub_stat            
            return
      def circlet_artifact(self, main_stat, sub_stat):
            self.circlet_main_stat = {main_stat: helper_functions.main_stat_values(main_stat)}
            self.circlet_sub_stats = sub_stat            
            return
      def goblet_artifact(self, main_stat, sub_stat):
            self.goblet_main_stat = {main_stat: helper_functions.main_stat_values(main_stat)}
            self.goblet_sub_stats = sub_stat            
            return      
      def init_weapon(self, look_up_weapon_name):
            for weapon_type, weapon_info in weapon_list.items():
                  if weapon_type == self.character_data["weapon_archetype"]:
                        for weapon_name, weapon_data in weapon_info.items():
                              if weapon_name == look_up_weapon_name:
                                    self.weapon_name = weapon_name
                                    self.weapon = weapon_data
      def get_base_stats(self, stat):
            return self.base_stats[stat]
      def calculate_artifact_total_stats(self):
            self.artifact_total_stats = {"ATK": 0,
                                    "ATK%": 0,
                                    "HP": 0,
                                    "HP%": 0,
                                    "DEF": 0,
                                    "DEF%": 0,
                                    "ER": 0,
                                    "EM": 0,
                                    "CR": 0,
                                    "CD": 0,
                                    "PHYSICAL": 0,
                                    "CRYO": 0,
                                    "PYRO": 0,
                                    "DENDRO": 0,
                                    "GEO": 0,
                                    "ANEMO": 0,
                                    "ELECTRO": 0,
                                    "HYDRO": 0,
                                    "NA%": 0,
                                    "CA%": 0,
                                    "SKILL%": 0,
                                    "BURST%": 0}
            self.set_effect_stats = {key: 0 for key in self.artifact_total_stats}
            self.weapon_effect_stats = {key: 0 for key in self.artifact_total_stats}
            self.constellation_effect_stats = {key: 0 for key in self.artifact_total_stats}
            artifact_types = ["flower", "feather", "sands", "circlet", "goblet"]

            for artifact in artifact_types:
                  if not hasattr(self, f"{artifact}_main_stat"):
                        continue
                  for key, value in getattr(self, f"{artifact}_main_stat").items():
                        try:
                              self.artifact_total_stats[key] += value
                        except KeyError:
                            pass

                  for key, value in getattr(self, f"{artifact}_sub_stats").items():
                        try:
                              self.artifact_total_stats[key] += sum(helper_functions.calculate_roll(value, key, artifact_roll_data))
                        except KeyError:
                            pass    

              
            #calculate set effect
            
            artifact_types = ["flower", "feather", "sands", "goblet", "circlet"]
            set_count = Counter(
                  getattr(self, f"{artifact}_set")
                  for artifact in artifact_types
                  if hasattr(self, f"{artifact}_set")
            )
            for set_name, count in set_count.items():
                  
                  # if count >= 4:
                  #       for name, detail in artifact_list.items():
                  #             if set_name == name:
                  #                   self.artifact_total_stats[detail["2p"].split("_")[0]] += int(detail["2p"].split("_")[1])
                  #                   if "active" in detail["4p"]:
                  #                         for i in detail["4p"]:
                  #                               if i != "active":
                  #                                     self.bonus_artifact_stats = [i for i in detail]
                  #                   else:
                  #                         for i in detail["4p"]:
                  #                               self.artifact_total_stats[i.split("_")[0]] += int(i.split("_")[1])
                  #                   break
                  if count >= 2:
                        detail = artifact_list.get(set_name)
                        if detail:
                              if "/" in detail["2p"]:
                                    for i in detail["2p"].split("/"):
                                          self.artifact_total_stats[i.split("_")[0]] += int(i.split("_")[1])
                              else:
                                    self.artifact_total_stats[detail["2p"].split("_")[0]] += int(detail["2p"].split("_")[1])
            return None
      def calculate_weapon_stats(self):
            self.weapon_stats = {"ATK": 0,
                                    "ATK%": 0,
                                    "HP": 0,
                                    "HP%": 0,
                                    "DEF": 0,
                                    "DEF%": 0,
                                    "ER": 0,
                                    "EM": 0,
                                    "CR": 0,
                                    "CD": 0,
                                    "PHYSICAL": 0,
                                    "CRYO": 0,
                                    "PYRO": 0,
                                    "DENDRO": 0,
                                    "GEO": 0,
                                    "ANEMO": 0,
                                    "ELECTRO": 0,
                                    "HYDRO": 0,
                                    "NA%": 0,
                                    "CA%": 0,
                                    "SKILL%": 0,
                                    "BURST%": 0}
            self.weapon_stats[self.weapon["bonus"].split("_")[0]] += float(self.weapon["bonus"].split("_")[1])
            try:
                  self.weapon_stats[self.weapon["affix"].split("_")[0]] += float(self.weapon["affix"].split("_")[1])
            except:
                pass
            
            return None
      def calculate_total_stats(self):
            self.total_base_atk = self.weapon["base_atk"] + self.base_stats["ATK"]
            
            self.total_stats = {}
            for key in self.artifact_total_stats:
                  self.total_stats[key] = self.artifact_total_stats[key] + self.weapon_stats[key]
            self.total_stats["CR"] += self.base_stats["CR"]
            self.total_stats["CD"] += self.base_stats["CD"]
            self.total_stats[self.bonus_stat[0]] += float(self.bonus_stat[1])
            self.total_atk = self.total_base_atk * (1+self.total_stats["ATK%"]/100) + self.total_stats["ATK"]
            self.total_hp = self.base_stats["HP"] * (1+self.total_stats["HP%"]/100) + self.total_stats["HP"]
            self.total_def = self.base_stats["DEF"] * (1+self.total_stats["DEF%"]/100) + self.total_stats["DEF"]

            conditional = self.weapon.get("conditional_affix")
            if isinstance(conditional, dict):
                  passive = conditional.get("passive")
                  if passive:
                        source_value = getattr(self, f"total_{passive['source'].lower()}", 0)
                        bonus = source_value * passive["source_multiplier"]/100
                        self.total_stats[passive["target"]] += bonus
                        

                        return None
      def external_buffs(self, buffs):
            if not hasattr(self, '_pre_buff_stats'):
                  self._pre_buff_stats = self.total_stats.copy()
                  self._pre_buff_atk = self.total_atk

            for key, value in buffs.items():
                  if key in self.total_stats:
                        self.total_stats[key] += value
            self.total_atk = self.total_base_atk * (1+self.total_stats["ATK%"]/100) + self.total_stats["ATK"]
            self.total_hp = self.total_base_atk * (1+self.total_stats["HP%"]/100) + self.total_stats["HP"]
            self.total_def = self.total_base_atk * (1+self.total_stats["DEF%"]/100) + self.total_stats["DEF"]


      def reset_external_buffs(self):
        if hasattr(self, '_pre_buff_stats'):
            self.total_stats = self._pre_buff_stats.copy()
            self.total_atk = self._pre_buff_atk
            del self._pre_buff_stats
            del self._pre_buff_atk
      def calculate_total_atk(self):
            return self.total_base_atk * (1+self.total_stats["ATK%"]/100) + self.total_stats["ATK"]
      def add_temporary_buff(self, buff):
            for key, value in buff.items():
                  if key in self.total_stats:
                        self.total_stats[key] += value
class Eula(Character):
      def __init__(self , character, level, constellation=0, talents=[9,9,9]):
            super().__init__(character, level, constellation, talents)
            self.grimheart = 0
            self.burst_stacks = 0
            self.burst_active = False
            if self.constellation >= 5:
                  self.talents[2] += 3
                  self.talents[1] += 3
            elif self.constellation >= 3:
                  self.talents[2] += 3
      def calculate_damage(self, attack):
            if attack[0] == 'n':
                  if int(attack[1]) in [1, 2, 4]:
                        self.burst_stacks += 1 if self.burst_active == True else 0
                  elif int(attack[1]) in [3, 5]:
                        self.burst_stacks += 2 if self.burst_active == True else 0
                  return helper_functions.damage_formula(self.normal_attack_multiplier[self.talents[0] - 1][int(attack[1])-1],
                                                  self.total_atk,
                                                  self.total_stats["CR"],
                                                  self.total_stats["CD"],
                                                  self.character_level,
                                                  enemy_level,
                                                  self.total_stats["EM"],
                                                  0,
                                                  0,
                                                  False,
                                                  
                                                  0,
                                                  0,
                                                  0.1,
                                                  0,
                                                  1,
                                                  0,
                                                  self.total_stats["PHYSICAL"],
                                                  0)
            elif "e" in attack:
                  if attack[:2] == "te":
                        self.burst_stacks += 1 if self.burst_active == True else 0
                        self.grimheart += 1 if self.grimheart < 2 else 0
                        return helper_functions.damage_formula(self.skill_multiplier[self.talents[1] - 1]["tap"],
                                                  self.total_atk,
                                                  self.total_stats["CR"],
                                                  self.total_stats["CD"],
                                                  self.character_level,
                                                  enemy_level,
                                                  self.total_stats["EM"],
                                                  0,
                                                  0,
                                                  False,
                                                  0,
                                                  0,
                                                  0.1,
                                                  0,
                                                  1,
                                                  0,
                                                  self.total_stats["CRYO"],
                                                  0)
                  elif attack[:2] == "he":
                        damage_num = 0
                        self.burst_stacks += 4 if self.grimheart == 2 and self.burst_active == True else (1 + self.grimheart)
                        damage_num += helper_functions.damage_formula(self.skill_multiplier[self.talents[1] - 1]["hold"],
                                                  self.total_atk,
                                                  self.total_stats["CR"],
                                                  self.total_stats["CD"],
                                                  self.character_level,
                                                  enemy_level,
                                                  self.total_stats["EM"],
                                                  0,
                                                  0,
                                                  False,
                                                  0,
                                                  0,
                                                  0.1,
                                                  0,
                                                  1,
                                                  0,
                                                  self.total_stats["CRYO"],
                                                  0)
                        damage_num += helper_functions.damage_formula(self.skill_multiplier[self.talents[1] - 1]["icewhirl"]*self.grimheart,
                                                  self.total_atk,
                                                  self.total_stats["CR"],
                                                  self.total_stats["CD"],
                                                  self.character_level,
                                                  enemy_level,
                                                  self.total_stats["EM"],
                                                  0,
                                                  0,
                                                  False,
                                                  0,
                                                  0,
                                                  0.1,
                                                  0,
                                                  1,
                                                  0,
                                                  self.total_stats["CRYO"],
                                                  0)
                        
                        damage_num += helper_functions.damage_formula(self.burst_multiplier[self.talents[2] - 1]["base"]/2,
                                                  self.total_atk,
                                                  self.total_stats["CR"],
                                                  self.total_stats["CD"],
                                                  self.character_level,
                                                  enemy_level,
                                                  self.total_stats["EM"],
                                                  0,
                                                  0,
                                                  False,
                                                  0,
                                                  0,
                                                  0.1,
                                                  0,
                                                  1,
                                                  0,
                                                  self.total_stats["PHYSICAL"],
                                                  0) if self.grimheart == 2 else 0
                        
                        self.grimheart = 0
                        return damage_num
            elif "q" in attack:
                  if self.burst_active == True:
                        damage_num = self.detonate_burst()
                        self.burst_active = False
                        self.burst_stacks = 0
                        return damage_num
                  else:
                        
                        self.grimheart += 1 if self.grimheart < 2 else 0
                        self.burst_active = True
                        return helper_functions.damage_formula(self.burst_multiplier[self.talents[2] - 1]["skill"],
                                                      self.total_atk,
                                                      self.total_stats["CR"],
                                                      self.total_stats["CD"],
                                                      self.character_level,
                                                      enemy_level,
                                                      self.total_stats["EM"],
                                                      0,
                                                      0,
                                                      False,
                                                      0,
                                                      0,
                                                      0.1,
                                                      0,
                                                      1,
                                                      0,
                                                      self.total_stats["CRYO"],
                                                      0)
      def detonate_burst(self):            
            return helper_functions.damage_formula(self.burst_multiplier[self.talents[2] - 1]["stack"]*self.burst_stacks + self.burst_multiplier[self.talents[2] - 1]["base"],
                                                  self.total_atk,
                                                  self.total_stats["CR"],
                                                  self.total_stats["CD"],
                                                  self.character_level,
                                                  enemy_level,
                                                  self.total_stats["EM"],
                                                  0,
                                                  0,
                                                  False,
                                                  0,
                                                  0,
                                                  0.1,
                                                  0,
                                                  1,
                                                  0,
                                                  self.total_stats["PHYSICAL"],
                                                  0)

class Bennett(Character):
      def __init__(self , character, level, constellation=0, talents=[9,9,9]):
            super().__init__(character, level, constellation, talents)
            if self.constellation >= 5:
                  self.talents[1] += 3
                  self.talents[2] += 3
            elif self.constellation >= 3:
                  self.talents[1] += 3
      def calculate_damage(self, attack):
            pass
      def burst_support_buff(self):
            buff_value = self.total_base_atk * self.burst_multiplier[self.talents[2]-1]["buff"]/100 if self.constellation == 0 else self.total_base_atk * (self.burst_multiplier[self.talents[2]-1]["buff"]+20)/100
            return {"ATK" : buff_value}


class Skirk(Character):
      def __init__(self , character, level, constellation=2, talents=[1,9,9]):
            super().__init__(character, level, constellation, talents)
            self.seven_phase_flash = False
            self.serpent_subtlety = 0
            self.void_rifts = 0
            self.death_crossing = 0
            self.death_crossing_multipliers_normal = [110, 120, 170]
            self.death_crossing_multipliers_burst = [105, 115, 160]
            self.trigger_quota = 0
            self.trigger_quota_multiplier = 0
      def calculate_damage(self, attack):
            attack = attack.lower()
            if not self.seven_phase_flash and "n" in attack:
                  return helper_functions.damage_formula(self.normal_attack_multiplier[self.talents[0] - 1][int(attack[1])-1], 
                                                      self.calculate_total_atk(),
                                                      self.total_stats["CR"],
                                                      self.total_stats["CD"],
                                                      self.character_level,
                                                      enemy_level,
                                                      self.total_stats["EM"],
                                                      0,
                                                      0,
                                                      False,
                                                      0,
                                                      0,
                                                      0.1,
                                                      0,
                                                      1,
                                                      0,
                                                      self.total_stats["PHYSICAL"] + self.total_stats["NA%"],
                                                      0)
            elif "n" in attack:
                  
                  damage = helper_functions.damage_formula(self.skill_multiplier[self.talents[1] - 1][int(attack[1])-1], 
                                                      self.calculate_total_atk(),
                                                      self.total_stats["CR"],
                                                      self.total_stats["CD"],
                                                      self.character_level,
                                                      enemy_level,
                                                      self.total_stats["EM"],
                                                      0,
                                                      0,
                                                      False,
                                                      0,
                                                      0,
                                                      0.1,
                                                      0,
                                                      1,
                                                      0,
                                                      self.total_stats["CRYO"] + self.total_stats["NA%"] + self.trigger_quota_multiplier if self.trigger_quota > 0 else self.total_stats["CRYO"] + self.total_stats["NA%"],
                                                      0)
                  if self.trigger_quota > 0 and int(attack[1]) in [1, 2,5]:
                        self.trigger_quota -= 1
                  elif self.trigger_quota > 0 and int(attack[1]) in [3, 4]:
                        self.trigger_quota -= 2
                  return damage
            elif "ca" in attack:
                  return helper_functions.damage_formula(self.skill_multiplier[self.talents[1] - 1][5] if self.seven_phase_flash else self.normal_attack_multiplier[self.talents[0] - 1][5], 
                                                      self.calculate_total_atk(),
                                                      self.total_stats["CR"],
                                                      self.total_stats["CD"],
                                                      self.character_level,
                                                      enemy_level,
                                                      self.total_stats["EM"],
                                                      0,
                                                      0,
                                                      False,
                                                      0,
                                                      0,
                                                      0.1,
                                                      0,
                                                      1,
                                                      0,
                                                      self.total_stats["CRYO"] + self.total_stats["CA%"] if self.seven_phase_flash else self.total_stats["PHYSICAL"] + self.total_stats["CA%"],
                                                      0)
            elif "e" in attack:

                  weapon_effect = weapon_effects.get(self.weapon_name)
                  if weapon_effect:
                        weapon_effect(self.weapon, self, attack)

                  if attack[0] == "t":
                        self.seven_phase_flash = True
                        self.serpent_subtlety += 45
                        return 0
                  elif attack[0] == "h":
                        self.void_rifts = 0
                        self.serpent_subtlety += 45
                        return 0
            elif "q" in attack:
                  if self.seven_phase_flash:
                        self.trigger_quota = 10
                        self.trigger_quota_multiplier = 8 + 4 * self.void_rifts
                        self.void_rifts = 0
                        for key in list(self.constellation_effect_stats):
                              self.total_stats[key] -= self.constellation_effect_stats[key]
                              self.constellation_effect_stats[key] = 0
                        if self.constellation >= 2:
                              self.total_stats["ATK%"] += 70
                              self.constellation_effect_stats["ATK%"] += 70

                              pass
                        return 0
                  else:
                        overflow_bonus = self.calculate_total_atk() * (self.serpent_subtlety - 50) * self.burst_multiplier[self.talents[2] - 1]["subtlety"]/100 if self.serpent_subtlety > 50 else 0
                        damage = 0
                        damage += helper_functions.damage_formula(self.burst_multiplier[self.talents[2] - 1]["slash"], 
                                                      self.calculate_total_atk(),
                                                      self.total_stats["CR"],
                                                      self.total_stats["CD"],
                                                      self.character_level,
                                                      enemy_level,
                                                      self.total_stats["EM"],
                                                      0,
                                                      0,
                                                      False,
                                                      0,
                                                      0,
                                                      0.1,
                                                      0,
                                                      1,
                                                      overflow_bonus,
                                                      self.total_stats["CRYO"],
                                                      0)
                        damage += helper_functions.damage_formula(self.burst_multiplier[self.talents[2] - 1]["final_slash"], 
                                                      self.calculate_total_atk(),
                                                      self.total_stats["CR"],
                                                      self.total_stats["CD"],
                                                      self.character_level,
                                                      enemy_level,
                                                      self.total_stats["EM"],
                                                      0,
                                                      0,
                                                      False,
                                                      0,
                                                      0,
                                                      0.1,
                                                      0,
                                                      1,
                                                      overflow_bonus,
                                                      self.total_stats["CRYO"],
                                                      0)
                        self.serpent_subtlety = 0
                        return damage
      def skirk_reset(self):
            self.seven_phase_flash = False
            self.serpent_subtlety = 0
            self.void_rifts = 0
            self.trigger_quota = 0
            self.trigger_quota_multiplier = 0
            for key in self.weapon_effect_stats:
                  self.total_stats[key] -= self.weapon_effect_stats[key]
                  self.weapon_effect_stats[key] = 0
            for key in self.constellation_effect_stats:
                  self.total_stats[key] -= self.constellation_effect_stats[key]
                  self.constellation_effect_stats[key] = 0
      def passive_talent_check(self, team):
            if all(character.character_data["element"] in ("Cryo", "Hydro") and team.count("cryo") > 0 and team.count("hydro") > 0 for character in team):
                  for i in team:
                        i.talents[1] += 1
      
class Escoffier(Character):
      def __init__(self, character, level, constellation=0, talents=[9,10,9]):
             super().__init__(character, level, constellation, talents)
      
      def a1_passive(self, team):
           if len(team) < 4:
                 return
           a4_passive_count = 0
           team_elements = [character.character_data["element"] for character in team]
           for element in team_elements:
                 if element == "cryo" or element == "hydro":
                       a4_passive_count += 1
      def calculate_damage(self, attack):
            attack = attack.lower()
            if "n" in attack:
                  pass
            elif "e" in attack:
                  return helper_functions.damage_formula(self.skill_multiplier[self.talents[1] - 1]["skill"] + self.skill_multiplier[self.talents[1] - 1]["summon"]*20 + self.skill_multiplier[self.talents[1] - 1]["arkhe"], 
                                                      self.calculate_total_atk(),
                                                      self.total_stats["CR"],
                                                      self.total_stats["CD"],
                                                      self.character_level,
                                                      enemy_level,
                                                      self.total_stats["EM"],
                                                      0,
                                                      0,
                                                      False,
                                                      0,
                                                      0,
                                                      0.1,
                                                      0,
                                                      1,
                                                      0,
                                                      self.total_stats["CRYO"],
                                                      0)
            elif "q" in attack:
                  pass
           
                  
class create_team():
      def __init__(self, characters):
            self.characters = characters
            self.max_team_size = 4
            self.team_buffs = {}
            self.onfield_buff = {}
            self.active_character = None
            self.apply_team_resonance()
      def apply_team_resonance(self):
            resonance_buff = helper_functions.team_resonance(self.characters)
            for character in self.characters:
                  character.external_buffs(resonance_buff)
      def switch_character(self, character):
            if character in self.characters:
                  if self.active_character:
                        self.active_character.reset_external_buffs()
                  self.active_character = character

      def insert_character(self, character):
            if len(self.characters) < self.max_team_size:
                  self.characters.append(character)
            self.apply_team_resonance()
      def remove_character(self, character):
            if character in self.characters:
                  self.characters.remove(character)
            self.apply_team_resonance()
def main():
      eula = Eula("Eula", 90, 2, [10, 10, 10])
      eula.init_base_stats()
      eula.init_weapon("song_of_broken_pines")
      eula.insert_artifact("CR", {"ATK%": 15.2, "HP%": 5.8, "CD": 27.2, "DEF": 21}, "circlet", "PF")
      eula.insert_artifact("PHYSICAL", {"EM": 19, "ATK%": 15.2, "CD": 14.0, "CR": 7.4}, "goblet", "SR")
      eula.insert_artifact("ATK", {"ATK%": 14.0, "DEF": 23, "CD": 14.8, "CR": 11.3}, "feather", "PF")
      eula.insert_artifact("ATK%", {"DEF%": 5.1, "ATK": 14, "CD": 6.2, "CR": 16.3}, "sands", "PF")
      eula.insert_artifact("HP", {"ATK%": 5.3, "ATK": 18, "CD": 11.7, "CR": 17.1}, "flower", "PF")
      eula.calculate_artifact_total_stats()
      eula.calculate_weapon_stats()
      eula.calculate_total_stats()

      bennett = Bennett("Bennett", 90, 6, [9, 9, 10])
      bennett.init_base_stats()
      bennett.init_weapon("aquila_favonia")
      bennett.calculate_artifact_total_stats()
      bennett.calculate_weapon_stats()
      bennett.calculate_total_stats()

      #eula.external_buffs(bennett.burst_support_buff())
      #base_damage = eula_combo(eula)
      
      skirk = Skirk("Skirk", 90, 2, [1, 10, 10])
      skirk.init_base_stats()
      skirk.init_weapon("azurelight")
      skirk.insert_artifact("HP", {"CR": 7.4, "ATK%": 9.3, "CD": 25.6, "DEF%": 5.8}, "flower", "MH")
      skirk.insert_artifact("ATK", {"CD": 14.8, "CR": 6.6, "HP%": 5.3, "ATK%": 14.6}, "feather", "MH")
      skirk.insert_artifact("ATK%", {"CD": 36.5, "CR": 2.7, "ER": 6.5, "HP": 538}, "sands", "PF")
      skirk.insert_artifact("ATK%", {"CD": 37.3, "DEF": 39, "CR": 3.5, "ATK": 16}, "goblet", "SR")
      skirk.insert_artifact("ATK%", {"CR": 3.5, "CD": 24.1, "DEF": 19, "HP%": 9.3}, "circlet", "MH")
      skirk.calculate_artifact_total_stats()
      skirk.calculate_weapon_stats()
      skirk.calculate_total_stats()
      artifact_effects.marechaussee(artifact_list, skirk, stacks=3)
      num = 0

      escoffier = Escoffier("Escoffier", 90, 0, [1, 1, 1])
      escoffier.init_base_stats()
      escoffier.init_weapon("staff_of_homa")
      escoffier.calculate_artifact_total_stats()
      escoffier.calculate_weapon_stats()
      escoffier.calculate_total_stats()

      #skirk.calculate_damage("te")
      #num += skirk.calculate_damage("n1")
      #num += skirk.calculate_damage("n2")
      #skirk.calculate_damage("q")
      #num += skirk.calculate_damage("n1")
      #num += skirk.calculate_damage("n2")
      control = helper_functions.skirk_combo(skirk)
      skirk.skirk_reset()
      skirk.total_stats["ATK%"] += 20
      response = helper_functions.skirk_combo(skirk)
      #print(f"{(response/control - 1)*100:.2f}%")
      
      team = create_team([skirk, eula])
      print(escoffier.calculate_damage("e"))
if __name__ == "__main__":
      main()