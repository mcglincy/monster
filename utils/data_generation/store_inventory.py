#!/usr/bin/python3
from enum import IntEnum
import json
import sys
sys.path.insert(0, '../..')

from gamerules.exit_effect_kind import ExitEffectKind
from gamerules.exit_kind import ExitKind
from generator_utils import *

with open('./og_monster_data/objects.json') as f:
  OBJECTS = json.load(f)
with open('./og_monster_data/roomdesc.json') as f:
  ROOMDESCS = json.load(f)
with open('./og_monster_data/rooms.json') as f:
  ROOMS = json.load(f)


# TODO: move this somewhere (utils?)
def check_bit(num, offset):
  mask = 1 << offset
  return(num & mask)


def main():
  """Command-line script."""
  stores = []
  for roomdesc in ROOMDESCS:
    # we want MARKET SpecialRoomKind
    if not check_bit(roomdesc["spc_room"], 0):
      continue
    store = {}
    store["room"] = roomdesc["nice_name"]
    room_id = roomdesc["id"]
    room = find_object(ROOMS, room_id)
    inventory = []
    for packed_object_int, packed_hide_int in zip(room["objs"], room["obj_hides"]):
      if packed_object_int:
        object_id = packed_object_int % 1000
        quantity = packed_hide_int % 1000
        obj = find_object(OBJECTS, object_id)
        inventory.append({"object": obj["obj_name"], "quantity": quantity})
    store["inventory"] = inventory
    stores.append(store)
  print(json.dumps(stores, indent=2))

if __name__ == "__main__":
  main()
