import json
from userdefined.models import CharacterClass

CLASSREC_FILE = "utils/json/classrec.json"

def create_character_classes():
  with open(CLASSREC_FILE) as f:
    classrecs = json.load(f)
    for rec in classrecs:
      newclass = CharacterClass(
        db_record_id = rec["id"],
        db_key = rec["name"],
        db_who_name = rec["who_name"],
        db_group = rec["group"],
        db_size = rec["size"],
        db_alignment = rec["alignment"],
        db_move_speed = rec["move_speed"],
        db_attack_speed = rec["attack_speed"],
        db_heal_speed = rec["heal_speed"],
        db_base_health = rec["base_health"],
        db_level_health = rec["level_health"],
        db_base_mana = rec["base_mana"],
        db_level_mana = rec["level_mana"],
        db_base_weapon_use = rec["weapon_use"],
        db_level_weapon_use = 5,
        db_base_claw_damage = rec["base_damage"],
        db_level_claw_damage = rec["level_damage"],
        db_random_claw_damage = rec["rnd_damage"],
        db_base_steal = rec["base_steal"],
        db_level_steal = rec["level_steal"],
        db_base_move_silent = rec["move_silent"],
        db_level_move_silent = rec["level_move_silent"],
        db_poison_chance = rec["poison_chance"],
        db_shadow_damage_percent = rec["shadow_damage_percent"],
      )
      newclass.save()