#!/usr/bin/python3
from enum import IntEnum
import json
import sys
sys.path.insert(0, '..')

from gamerules.exit_effect_kind import ExitEffectKind
from gamerules.exit_kind import ExitKind
from utils.generator_utils import *


with open('./json/desc.json') as f:
  DESCS = json.load(f)
with open('./json/lines.json') as f:
  LINES = json.load(f)
with open('./json/objects.json') as f:
  OBJECTS = json.load(f)
with open('./json/roomdesc.json') as f:
  ROOMDESCS = json.load(f)


def maybe_set_desc(desc_id, exit_name, attr_name):
  if not desc_id or desc_id == 0 or desc_id == DEFAULT_MSG_ID:
    return
  desc = lookup_description(desc_id, DESCS, LINES)
  print(f"@set {exit_name}/{attr_name} = {repr(desc)}")
  print('#') 


def make_exit(exit, to_loc, come_out_exit):
  exit_kind = ExitKind(exit['kind'])
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
  exit_name = exit_names.split(';')[0]

  maybe_set_desc(exit['exit_desc'], exit_name, 'exit_desc')
  maybe_set_desc(exit['fail'], exit_name, 'fail_msg')
  maybe_set_desc(exit['success'], exit_name, 'success_msg')
  maybe_set_desc(exit['go_in'], exit_name, 'go_in_msg')
  # TODO: we could search all rooms/exits for our opposite and then use its come_out_msg
  # maybe_set_desc(exit['come_out'], exit_name, 'come_out_msg')
  if come_out_exit:
    maybe_set_desc(come_out_exit['come_out'], exit_name, 'come_out_msg')
  # if opposite_exit:
  #   maybe_set_desc(opposite_exit['come_out'], exit_name, 'come_out_msg')


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

