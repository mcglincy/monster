#!/usr/bin/python3
from enum import IntEnum
import json
import sys
sys.path.insert(0, '../..')

from generator_utils import *


# TODO: move this somewhere (utils?)
def check_bit(num, offset):
  mask = 1 << offset
  return(num & mask)


def main():
  """Command-line script."""
  room_inv = []
  for roomdesc in ROOMDESCS:
    if check_bit(roomdesc["spc_room"], 0):
      # skip STORE rooms
      continue    
    rec = {}
    rec["room"] = roomdesc["nice_name"]
    room_id = roomdesc["id"]
    room = find_object(ROOMS, room_id)
    inventory = []
    for packed_object_int, packed_hide_int in zip(room["objs"], room["obj_hides"]):
      if packed_object_int:
        object_id = packed_object_int % 1000
        condition = int(packed_object_int / 1000)
        hide = packed_hide_int % 1000
        charges = int(packed_hide_int / 1000)
        obj = find_object(OBJECTS, object_id)
        inventory.append({
          "object": obj["obj_name"],
          "condition": condition,
          "charges": charges,
          "hide": hide,
        })
    if inventory:
      # only include rooms with objects
      rec["inventory"] = inventory
      room_inv.append(rec)
  print(json.dumps(room_inv, indent=2))

if __name__ == "__main__":
  main()
