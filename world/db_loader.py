import json
from gamerules.spell_effect_kind import SpellEffectKind
from userdefined.models import CharacterClass, Spell, SpellEffect


CLASSREC_FILE = "utils/json/classrec.json"
DESC_FILE = 'utils/json/desc.json'
LINES_FILE = 'utils/json/lines.json'
SPELLS_FILE = "utils/json/spells.json"

# TODO: refactor


def escaped(s):
  return s.replace('"', '\\"')


def lookup_description(id, descs, lines):
  if not id:
    return None
  elif id > 0:
    # use descs
    desc_idx = id - 1
    # TODO: special handling for default description id 32000
    if desc_idx < len(descs):
      return escaped(' '.join(descs[desc_idx]['lines']))
  elif id < 0:
    # use lines
    line_idx = -id -1
    if line_idx < len(lines):
      return escaped(lines[line_idx]['line'])
  return None


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


def create_spells():
  with open(DESC_FILE) as f:
    descs = json.load(f)
  with open(LINES_FILE) as f:
    lines = json.load(f)
  with open(SPELLS_FILE) as f:
    spells = json.load(f)

  for rec in spells:
    print(f"doing spell {rec['name']}")
    new_spell = Spell(
      db_record_id = rec["id"],
      db_key = rec["name"],
      db_mana = rec["mana"],
      db_level_mana = rec["level_mana"],
      db_caster_desc = lookup_description(rec["caster_desc"], descs, lines),
      db_victim_desc = lookup_description(rec["victim_desc"], descs, lines),
      db_room_desc = lookup_description(rec["alignment"], descs, lines),
      db_failure_desc = lookup_description(rec["failure_desc"], descs, lines),
      db_min_level = rec["min_level"],
      db_class_id = rec["class"],
      db_group = rec["group"],
      db_room = rec["room"],
      db_failure_chance = rec["chance_of_failure"],
      db_casting_time = rec["casting_time"],
      db_object_required = rec["obj_required"],
      db_object_consumed = rec["obj_consumed"],
      db_silent = rec["silent"],
      db_reveals = rec["reveals"],
      db_memorize = rec["memorize"],
      db_command = rec["command"],
      db_command_priv = rec["command_priv"]
      # TODO: extra1, extra2, extra3 ???
    )
    new_spell.save()

    effect_kind_ids = set(k.value for k in SpellEffectKind)
    for eff in rec["effects"]:
      effect_kind_id = eff["effect"]
      if not effect_kind_id in effect_kind_ids:
        # goofball out of range data, so skip
        continue
      new_effect = SpellEffect(
        db_effect_kind = SpellEffectKind(effect_kind_id).value,
        db_affects_room =  eff["all"],
        db_affects_caster = eff["caster"],
        db_target_prompt = eff["prompt"],
        db_param_1 = eff["m1"],
        db_param_2 = eff["m2"],
        db_param_3 = eff["m3"],
        db_param_4 = eff["m4"],
      )
      new_effect.spell = new_spell
      new_effect.save()
