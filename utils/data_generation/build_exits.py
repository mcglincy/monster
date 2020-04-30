#!/usr/bin/python3
from enum import IntEnum
import json
import sys
sys.path.insert(0, '../..')

from generator_utils import *


def maybe_set_desc(desc_id, exit_name, attr_name):
  if not desc_id or desc_id == 0 or desc_id == DEFAULT_MSG_ID:
    return
  desc = lookup_description(desc_id, DESCS, LINES)
  print(f"@set {exit_name}/{attr_name} = {repr(desc)}")
  print('#') 


def make_exit(exit, to_loc, come_out_exit):
  direction = exit['direction']
  direction_letter = direction[0]
  to_room_id = f'room_{to_loc}'
  # req_verb is only used in a single exit - maybe by error?
  # req_verb = exit['req_verb']

  alias = exit['alias']
  if alias:
    exit_names = f"{direction};{direction_letter};{alias}"
  else:
    exit_names = f"{direction};{direction_letter}"

  print(f'@open {exit_names} = {to_room_id}')
  print('#')


def main():
  """Command-line script."""
  for roomdesc in ROOMDESCS:
    print('###############################################################################')
    print(f'# {roomdesc["nice_name"]}')
    print('###############################################################################')
    print(f'@tel room_{roomdesc["id"]}')
    print('#')
    for exit in roomdesc['exits']:
      to_loc = exit['to_loc']
      # stupid slot / come_out msg logic
      come_out_exit = None
      come_out_slot = exit['slot']
      if come_out_slot:
        to_room = ROOMDESCS[to_loc-1]
        to_exits = to_room['exits']
        come_out_exit = to_exits[come_out_slot - 1]
      make_exit(exit, to_loc, come_out_exit)


if __name__ == "__main__":
  main()

