#!/usr/bin/python3
from enum import IntEnum
import json
import sys
sys.path.insert(0, '..')

from gamerules.exit_effect_kind import ExitEffectKind
from gamerules.exit_kind import ExitKind
from utils.generator_utils import *

with open('./json/objects.json') as f:
  OBJECTS = json.load(f)
with open('./json/roomdesc.json') as f:
  ROOMDESCS = json.load(f)
with open('./json/rooms.json') as f:
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
    store["name"] = roomdesc["nice_name"]
    room_id = roomdesc["id"]
    room = find_object(ROOMS, room_id)
    object_names = []
    for packed_int in room["objs"]:
      if packed_int:
        low_digits = packed_int % 1000
        object_id = low_digits
        obj = find_object(OBJECTS, object_id)
        object_names.append(obj["obj_name"])
    store["objects"] = object_names
    stores.append(store)
  print(json.dumps(stores, indent=2))

if __name__ == "__main__":
  main()
