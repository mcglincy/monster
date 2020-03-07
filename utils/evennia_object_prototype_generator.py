#!/usr/bin/python3
import json
import sys
sys.path.insert(0, '..')

from typeclasses.equipment_effect_kind import EquipmentEffectKind
from typeclasses.equipment_slot import EquipmentSlot
from typeclasses.object_kind import ObjectKind
from utils.generator_utils import DEFAULT_MSG_ID, lookup_description, split_integer


DESC_FILE = './json/desc.json'
LINES_FILE = './json/lines.json'
OBJECT_FILE = './json/objects.json'

DEFAULT_ARTICLE = 1


def lookup_effect(obj, effect):
  for parm in obj['parms']:
    eff_num, eff = split_integer(parm)
    if eff == effect:
      return eff_num


def camel_case(s):
  """Convert an object name to a useful python class name.

  E.g., 'Hammer of the gods' => 'HammerOfTheGods'
  """
  s = s.strip()
  done = False
  chars = []
  idx = 0
  s_len = len(s)
  while not done:
    c = s[idx]
    if idx == 0:
      chars.append(c.upper())
      idx = idx + 1
    elif c == ' ':
      chars.append(s[idx+1].upper())
      idx = idx + 2
    elif c == "'":
      # skip quote
      idx = idx + 1
    else:
      chars.append(c)
      idx = idx + 1
    if idx >= s_len:
      done = True
  return ''.join(chars)


def snake_case(s):
  """Convert an object name to a snake case.

  E.g., 'Hammer of the gods' => 'HAMMER_OF_THE_GODS'
  """
  s = s.strip()
  chars = []
  for c in s:
    if c == ' ' or c == '-':
      chars.append('_')
    elif c == "'":
      pass
    else:
      chars.append(c.upper())
  return ''.join(chars)


def maybe_desc(value, field_name, except_if=None):
  if value and value != except_if:
    print(f"  '{field_name}': {value},")


def maybe_desc_field(desc_id, field_name, descs, lines):
  if desc_id and desc_id != DEFAULT_MSG_ID:
    desc = lookup_description(desc_id, descs, lines)
    if desc:
      print(f"  '{field_name}': \"{desc}\",")


def maybe_effect(obj, effect_kind, field_name):
   value = lookup_effect(obj, effect_kind)
   if value:
    print(f"  '{field_name}': {value},")


def output_common_fields(obj, prototype_parent, descs, lines):
  obj_name = obj['obj_name']
  print(f"{snake_case(obj_name)} = {{")
  # TODO: add better quote escaping for key and desc
  print(f"  'key': \"{obj_name}\",")
  print(f"  'prototype_parent': '{prototype_parent}',")
  maybe(obj['particle'], 'article', except_if=DEFAULT_ARTICLE)
  maybe(obj['components'], 'components')
  maybe_desc_field(obj['examine'], 'desc', descs, lines)
  maybe(obj['get_obj_req'], 'get_object_required')
  maybe_desc_field(obj['get_fail'], 'get_fail_msg', descs, lines)
  maybe_desc_field(obj['get_success'], 'get_success_msg', descs, lines)
  maybe_desc_field(obj['line_desc'], 'line_desc', descs, lines)
  maybe(obj['num_exist'], 'num_exist')
  maybe(obj['sticky'], 'sticky')
  maybe(obj['use_obj_req'], 'use_object_required')
  maybe_desc_field(obj['use_fail'], 'use_fail_msg', descs, lines)
  maybe_desc_field(obj['use_success'], 'use_success_msg', descs, lines)
  maybe(obj['weight'], 'weight')
  maybe(obj['worth'], 'worth')


def output_blands(objs, descs, lines):
  print("""#
# 'Bland' objects
#

BASE_BLAND = {
  'typeclass': 'typeclasses.objects.Bland',
  'key': 'base_bland',
}
""")
  for obj in objs:
    output_common_fields(obj, 'base_bland', descs, lines)
    print('}')
    print()


def output_equipment(objs, descs, lines):
  print("""#
# other equipment
#

BASE_EQUIPMENT = {
  'typeclass': 'typeclasses.objects.Equipment',
  'key': 'base_equipment',
}
""")
  for obj in objs:
    output_common_fields(obj, 'base_equipment', descs, lines)
    slot_num = obj['wear']
    slot = EquipmentSlot(slot_num)
    print(f"  'equipment_slot': EquipmentSlot.{slot.name},")
    for effect_kind in EquipmentEffectKind:
      maybe_effect(obj, effect_kind, effect_kind.name.lower())
    print('}')
    print()


def output_scrolls(objs, descs, lines):
  print("""#
# Scroll objects
#

BASE_SCROLL = {
  'typeclass': 'typeclasses.objects.Scroll',
  'key': 'base_scroll',
}
""")
  for obj in objs:
    output_common_fields(obj, 'base_scroll', descs, lines)
    # TODO: figure out parms
    print('}')
    print()


def output_wands(objs, descs, lines):
  print("""#
# Wand objects
#

BASE_WAND = {
  'typeclass': 'typeclasses.objects.Wand',
  'key': 'base_wand',
}
""")
  for obj in objs:
    output_common_fields(obj, 'base_wand', descs, lines)
    # TODO: figure out parms
    print('}')
    print()


def output_missiles(objs, descs, lines):
  print("""#
# Missile objects
#

BASE_MISSILE = {
  'typeclass': 'typeclasses.objects.Missile',
  'key': 'base_missile',
}
""")
  for obj in objs:
    output_common_fields(obj, 'base_missile', descs, lines)
    # TODO: figure out parms
    print('}')
    print()


def output_missile_launchers(objs, descs, lines):
  print("""#
# Missile launcher objects
#

BASE_MISSILE_LAUNCHER = {
  'typeclass': 'typeclasses.objects.MissileLauncher',
  'key': 'base_missile_launcher',
}
""")
  for obj in objs:
    output_common_fields(obj, 'base_missile_launcher', descs, lines)
    # TODO: figure out parms
    print('}')
    print()


def output_spellbooks(objs, descs, lines):
  print("""#
# Spellbook objects
#

BASE_SPELLBOOK = {
  'typeclass': 'typeclasses.objects.Spellbook',
  'key': 'base_spellbook',
}
""")
  for obj in objs:
    output_common_fields(obj, 'base_spellbook', descs, lines)
    # TODO: figure out parms
    print('}')
    print()


def output_banking_machines(objs, descs, lines):
  print("""#
# Banking machine objects
#

BASE_BANKING_MACHINE = {
  'typeclass': 'typeclasses.objects.BankingMachine',
  'key': 'banking machine',
}
""")
  for obj in objs:
    output_common_fields(obj, 'base_banking_machine', descs, lines)
    # TODO: figure out parms
    print('}')
    print()





def main():
  """Command-line script."""
  with open(DESC_FILE) as f:
    descs = json.load(f)
  with open(LINES_FILE) as f:
    lines = json.load(f)
  with open(OBJECT_FILE) as f:
    objects = json.load(f)

  # divide objects by kind
  obj_by_kind = {}
  for obj in objects:
    obj_by_kind.setdefault(obj['kind'], []).append(obj)
  for arr in obj_by_kind.values():
    arr.sort(key=lambda x: x['obj_name'].upper())

  print("""#
# Generated object prototypes
#
from typeclasses.equipment_slot import EquipmentSlot
""")
  output_blands(obj_by_kind[ObjectKind.BLAND], descs, lines)
  output_equipment(obj_by_kind[ObjectKind.EQUIPMENT], descs, lines)
  output_scrolls(obj_by_kind[ObjectKind.SCROLL], descs, lines)
  output_wands(obj_by_kind[ObjectKind.WAND], descs, lines)
  output_missiles(obj_by_kind[ObjectKind.MISSILE], descs, lines)
  output_missile_launchers(obj_by_kind[ObjectKind.MISSILE_LAUNCHER], descs, lines)
  output_spellbooks(obj_by_kind[ObjectKind.SPELLBOOK], descs, lines)
  output_banking_machines(obj_by_kind[ObjectKind.BANKING_MACHINE], descs, lines)


if __name__ == "__main__":
  main()