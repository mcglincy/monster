#!/usr/bin/python3
from enum import IntEnum
import json
import sys
sys.path.insert(0, '../..')

from gamerules.exit_effect_kind import ExitEffectKind
from gamerules.exit_kind import ExitKind
from generator_utils import *


with open('./og_monster_data/desc.json') as f:
  DESCS = json.load(f)
with open('./og_monster_data/lines.json') as f:
  LINES = json.load(f)
with open('./og_monster_data/objects.json') as f:
  OBJECTS = json.load(f)
with open('./og_monster_data/roomdesc.json') as f:
  ROOMDESCS = json.load(f)


def make_room(roomdesc):
  record_id = roomdesc["id"]
  print('###############################################################################')
  print(f'# {roomdesc["nice_name"]}')
  print('###############################################################################')
  print(f'@tel room_{record_id}')
  print('#')
  if 'secondary' in roomdesc:
    secondary_id = roomdesc['secondary']
    secondary_desc = lookup_description(secondary_id, DESCS, LINES)
    if secondary_desc:
      print(f"@set here/secondary_desc = {repr(secondary_desc)}")
      print('#')
  if roomdesc['which']:
    print(f"@set here/which_desc = {roomdesc['which']}")
    print('#')
  if roomdesc['magic_obj']:
    magic_obj = find_object(OBJECTS, roomdesc['magic_obj'])
    if magic_obj:
      print(f"@set here/magic_object = {repr(magic_obj['obj_name'])}")
      print('#')
  print(f'@set here/record_id = {record_id}')
  print('#')
  if roomdesc["spc_room"]:
    print(f'@set here/special_kind_bitmask = {roomdesc["spc_room"]}')
    print('#')
    print(f'@set here/magnitudes = {roomdesc["magnitudes"]}')
    print('#')
  if roomdesc["trap_chance"] and roomdesc["trap_direction"]:
    print(f'@set here/trap_chance = {roomdesc["trap_chance"]}')
    print('#')
    print(f'@set here/trap_direction = "{roomdesc["trap_direction"]}"')
    print('#')
  details = roomdesc["details"]
  detail_ids = roomdesc["detail_descs"]
  if details and detail_ids:
    detail_dict = {}
    for detail, detail_id in zip(details, detail_ids):
      detail_desc = lookup_description(detail_id, DESCS, LINES)
      if detail_desc:
        detail_dict[detail] = detail_desc
    print(f"@set here/details = {detail_dict}")
    print('#')


def main():
  """Command-line script."""
  for roomdesc in ROOMDESCS:
    make_room(roomdesc)


if __name__ == "__main__":
  main()

