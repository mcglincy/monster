#!/usr/bin/python3
import json
import sys
sys.path.insert(0, '..')

from gamerules.mob_kind import MobKind
from utils.generator_utils import DEFAULT_MSG_ID, camel_case, lookup_description, snake_case, split_integer


DESC_FILE = './json/desc.json'
LINES_FILE = './json/lines.json'
OBJECTS_FILE = './json/objects.json'
RANDOMS_FILE = './json/randoms.json'
SPELLS_FILE = './json/spells.json'


def output_mob(obj):
  obj_name = obj['name']
  print(f"{snake_case(obj_name)} = {{")
  print(f"  'key': \"{obj_name}\",")
  print(f"  'prototype_parent': 'mob',")
  record_id = obj['id']
  print(f"  'record_id': {record_id},")
  min_level = obj['min_level']
  # add tags for easier searchability
  tags = ['mob', f'min_level_{min_level}', f'record_id_{record_id}']
  print(f"  'prototype_tags': {tags},")
  kind = MobKind(obj['kind'])
  print(f"  'kind': MobKind.{kind.name},")  
  print(f"  'min_level': {min_level},")
  print(f"  'group': {obj['group']},")
  print(f"  'size': {obj['size']},")
  print(f"  'xp': {obj['experience']},")
  print(f"  'drop_gold': {obj['gold']},")
  print(f"  'drop_object_id': {obj['object']},")
  print(f"  'base_health': {obj['base_health']},")
  print(f"  'random_health': {obj['random_health']},")
  print(f"  'level_health': {obj['level_health']},")
  print(f"  'base_mana': {obj['base_mana']},")
  print(f"  'level_mana': {obj['level_mana']},")
  print(f"  'base_damage': {obj['base_damage']},")
  print(f"  'random_damage': {obj['random_damage']},")
  print(f"  'level_damage': {obj['level_damage']},")
  print(f"  'armor': {obj['armor']},")
  print(f"  'spell_armor': {obj['spell_armor']},")
  print(f"  'move_speed': {obj['move_speed']},")
  print(f"  'attack_speed': {obj['attack_speed']},")
  print(f"  'heal_speed': {obj['heal_speed']},")
  print(f"  'weapon_id': {obj['weapon']},")
  print(f"  'weapon_use': {obj['weapon_use']},")
  print(f"  'level_weapon_use': {obj['level_weapon_use']},")
  print(f"  'pursuit_chance': {obj['pursuit_chance']},")
  # TODO: decide how we want to handle these
  #print(f"  'spell_ids': {obj['']}")
  #print(f"  'sayings': {obj['']}")
  print('}')
  print()


def main():
  """Command-line script."""
  with open(DESC_FILE) as f:
    descs = json.load(f)
  with open(LINES_FILE) as f:
    lines = json.load(f)
  with open(OBJECTS_FILE) as f:
    objects = json.load(f)
  with open(RANDOMS_FILE) as f:
    rand_mobs = json.load(f)
  with open(SPELLS_FILE) as f:
    spells = json.load(f)

  print("""#
# Generated mob prototypes
#
from gamerules.mob_kind import MobKind


MOB = {
  'typeclass': 'typeclasses.mobs.Mob',
  'key': 'mob',
}

""")

  for rand_mob in rand_mobs:
    output_mob(rand_mob)


if __name__ == "__main__":
  main()
