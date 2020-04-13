#!/usr/bin/python3
from enum import IntEnum
import json
import sys
sys.path.insert(0, '..')

from gamerules.exit_effect_kind import ExitEffectKind
from gamerules.exit_kind import ExitKind
from utils.generator_utils import DEFAULT_MSG_ID, lookup_description, split_integer


DESC_FILE = './json/desc.json'
LINES_FILE = './json/lines.json'
OBJECT_FILE = './json/objects.json'
ROOMDESC_FILE = './json/roomdesc.json'

with open(DESC_FILE) as f:
  DESCS = json.load(f)
with open(LINES_FILE) as f:
  LINES = json.load(f)
with open(OBJECT_FILE) as f:
  OBJECTS = json.load(f)
with open(ROOMDESC_FILE) as f:
  ROOMDESCS = json.load(f)


def make_room(roomdesc):
  record_id = roomdesc["id"]
  print(f'@dig/tel {roomdesc["nice_name"]};room_{record_id}')
  print('#')
  if 'primary' in roomdesc:
    desc_idx = roomdesc['primary'] - 1
    if desc_idx >= 0 and desc_idx < len(DESCS):
      desc = DESCS[desc_idx]
      print('@desc')
      print('\n'.join(desc['lines']))
      print('#')
  if 'secondary' in roomdesc:
    secondary_id = roomdesc['secondary']
    secondary_desc = lookup_description(secondary_id, DESCS, LINES)
    if secondary_desc:
      print(f"@set here/secondary_desc = \"{secondary_desc}\"")
      print('#')
  if roomdesc['which']:
    print(f"@set here/which_desc = {roomdesc['which']}")
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


def maybe_set_desc(desc_id, exit_name, attr_name):
  if not desc_id or desc_id == 0 or desc_id == DEFAULT_MSG_ID:
    return
  desc = lookup_description(desc_id, DESCS, LINES)
  print(f"@set {exit_name}/{attr_name} = \"{desc}\"")
  print('#') 


def find_object(objects, obj_id):
  for obj in objects:
    if obj['id'] == obj_id:
      return obj
  return None

def make_exit(exit, come_out_exit):
  exit_kind = ExitKind(exit['kind'])
  direction = exit['direction']
  direction_letter = direction[0]
  to_room_id = f'room_{exit["to_loc"]}'
  # req_verb is only used in a single exit - maybe by error?
  # req_verb = exit['req_verb']

  # if exit_kind == ExitKind.NO_EXIT:
  #   # skip, I guess?
  #   return
  # elif exit_kind == ExitKind.OPEN:
  #   room_class = 'Room'
  #   pass  
  # elif exit_kind == ExitKind.NEED_KEY:
  #   # TODO
  #   pass
  # elif exit_kind == ExitKind.NEED_NO_KEY:
  #   # TODO
  #   pass
  # elif exit_kind == ExitKind.RANDOM_FAIL:
  #   # TODO
  #   pass
  # elif exit_kind == ExitKind.ACCEPT:
  #   # TODO
  #   pass
  # elif exit_kind == ExitKind.NEED_OBJECT:
  #   # TODO
  #   pass
  # elif exit_kind == ExitKind.OPEN_CLOSE:
  #   # aka timed door
  #   # TODO
  #   pass
  # elif exit_kind == ExitKind.PASSWORDED:
  #   # TODO
  #   pass

  alias = exit['alias']
  if alias:
    exit_names = f"{direction};{direction_letter};{alias}"
  else:
    exit_names = f"{direction};{direction_letter}"

  print(f'@open {exit_names} = {to_room_id}')
  print('#')

  exit_name = exit_names.split(';')[0]
  print(f"@set {exit_name}/exit_kind = {exit_kind}")
  print('#')

  if alias:
    print(f"@set {exit_name}/password = \"{alias}\"")
    print('#')

  # there are several different flavors of invisible exit
  if (alias
    or exit_kind == ExitKind.NO_EXIT
    or exit_kind == ExitKind.PASSWORDED):
    print(f"@lock {exit_name} = view:none()")
    print('#')

  # and several flavors of impassable exit
  if (exit['req_alias']
    or exit_kind == ExitKind.NO_EXIT
    or exit_kind == ExitKind.PASSWORDED):
    print(f"@lock {exit_name} = traverse:none()")
    print('#')

  # and then there's hidden, too
  hidden_id = exit['hidden']
  if hidden_id is not None and hidden_id != 0:
    # TODO: handle 32000 default ?
    hidden_desc = lookup_description(hidden_id, DESCS, LINES)
    if hidden_desc:
      print(f"@set {exit_name}/hidden_desc = \"{hidden_desc}\"")
      print('#')
      print(f"@set {exit_name}/hiding = 1")
      print('#')
      print(f"@lock {exit_name} = traverse:none(); view:perm(see_hidden)")
      print('#')

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

  door_effect = exit['door_effect']
  if door_effect:
    exit_effect_value, exit_effect_kind = split_integer(door_effect)
    print(f"@set {exit_name}/exit_effect_kind = {exit_effect_kind}")
    print('#')
    print(f"@set {exit_name}/exit_effect_value = {exit_effect_value}")
    print('#')

  obj_req_id = exit['obj_req']
  if obj_req_id:
    obj_req = find_object(OBJECTS, obj_req_id)
    if obj_req:
      print(f"@set {exit_name}/required_object = \"{obj_req['obj_name']}\"")
      print('#')
      if exit_kind == ExitKind.OBJECT_REQUIRED:
        print(f"@lock {exit_name} = traverse:holds({obj_req['obj_name']})")
        print('#')
      elif exit_kind == ExitKind.OBJECT_FORBIDDEN:
        print(f"@lock {exit_name} = traverse: NOT holds({obj_req['obj_name']})")
        print('#')
      elif exit_kind == ExitKind.ONLY_EXISTS_WITH_OBJECT:
        print(f"@lock {exit_name} = traverse:holds({obj_req['obj_name']})")
        print('#')
        print(f"@lock {exit_name} = view:holds({obj_req['obj_name']})")
        print('#')


def main():
  """Command-line script."""
  print("""# Monster batchcommand build file.
#
# To nuke the database first:
# $ evennia stop
# $ rm -f /opt/monsterdata/monster.db3
# $ evennia migrate
# $ evennia start [and set up god account]
# [connect to game as god account]
# @batchcommands monster.world.build
#
#
# Step 1: Create all rooms.
#""")

  for roomdesc in ROOMDESCS:
    make_room(roomdesc)

  print("""#
#
# Step 2: Make exits between rooms.
#""")

  for roomdesc in ROOMDESCS:
    print(f'@tel room_{roomdesc["id"]}')
    print('#')
    for exit in roomdesc['exits']:
      to_loc = exit['to_loc']
      if not to_loc:
        continue
      # stupid slot / come_out msg logic
      come_out_exit = None
      come_out_slot = exit['slot']
      if come_out_slot:
        to_room = ROOMDESCS[to_loc-1]
        to_exits = to_room['exits']
        come_out_exit = to_exits[come_out_slot - 1]
      make_exit(exit, come_out_exit)

  print("""#
#
# Step 3: Apply manual build edits.
#
#INSERT world.build_edits
#""")


if __name__ == "__main__":
  main()

