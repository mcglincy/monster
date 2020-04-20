#!/usr/bin/python3
import json
import sys


ZONES = [
  'admin',
  'arthurs_tomb',
  'cave',
  'druid_palace',
  'dungeons_of_solace',
  'dwarven_stair',
  'forest_lake',
  'forgotten_fortress',
  'goblin_caves',
  'ice_wastes',
  'improbable_structure',
  'keep',
  'lost_city',
  'maze',
  'orphaned',
  'outside',
  'pyramid',
  'sewer',
  'smoking_ruins',
  'tai_tastigon',
  'temple_of_apollo',
  'tower_of_useth',
  'troll_caverns',
  'tutorial',
  'void',
  'warlords_fortress',
  'wilted_lothlorien',
]

with open('../json/roomdesc.json') as f:
  ROOMDESCS = json.load(f)


def room_names_in_zone(zone):
  with open(f'../zones/{zone}.txt') as f:
    return [x.strip() for x in f.readlines()]


def ids_for_room_names(room_names):
  ids = []
  for roomdesc in ROOMDESCS:
    name = roomdesc["nice_name"]
    if name not in room_names:
      continue
    ids.append(roomdesc["id"])
  return ids


def output_zone(zone):
  room_names = room_names_in_zone(zone)
  room_ids = ids_for_room_names(room_names)

  outfile_name = f'{zone}.dot'
  with open(f'{zone}.dot', 'w') as f:
    print('digraph monster {', file=f)
    for roomdesc in ROOMDESCS:
      name = roomdesc["nice_name"]
      if name not in room_names:
        continue
      record_id = roomdesc["id"]
      # room_0 [label="NOWHERE"];
      print(f'room_{record_id} [label="{roomdesc["nice_name"]}"];', file=f)
      for exit in roomdesc['exits']:
        to_loc = exit['to_loc']
        direction = exit['direction']
        direction_letter = direction[0]    
        if to_loc in room_ids:
          # room_1 -> room_0 [label="n"];
          print(f'room_{record_id} -> room_{to_loc} [label="{direction_letter}"];', file=f)
    print('}', file=f)


def output_zones():
  for zone in ZONES:
    output_zone(zone)


if __name__ == "__main__":
  output_zones()

