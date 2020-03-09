#!/usr/bin/python3
import json
import sys
sys.path.insert(0, '..')

from gamerules.exit_effect_kind import ExitEffectKind
from gamerules.exit_kind import ExitKind
from gamerules.room_kind import RoomKind
from utils.generator_utils import DEFAULT_MSG_ID, lookup_description, split_integer


DESC_FILE = './json/desc.json'
LINES_FILE = './json/lines.json'
ROOMDESC_FILE = './json/roomdesc.json'


def make_room(roomdesc, descs):
  record_id = roomdesc["id"]
  print(f'@dig/tel {roomdesc["nice_name"]};room_{record_id}')
  print('#')
  # TODO: do we want to handle secondary descript?
  if 'primary' in roomdesc:
    desc_idx = roomdesc['primary'] - 1
    if desc_idx >= 0 and desc_idx < len(descs):
      desc = descs[desc_idx]
      print('@desc')
      print('\n'.join(desc['lines']))
      print('#')
  print(f'@set here/record_id = {record_id}')
  print('#')
  if roomdesc["trap_chance"]:
    print(f'@set here/trap_chance = {roomdesc["trap_chance"]}')
    print('#')
    print(f'@set here/trap_to = {roomdesc["trap_to"]}')
    print('#')


def maybe_set_desc(desc_id, exit_name, attr_name, descs, lines):
  if not desc_id or desc_id == 0 or desc_id == DEFAULT_MSG_ID:
    return
  desc = lookup_description(desc_id, descs, lines)
  print(f"@set {exit_name}/{attr_name} = {desc}")
  print('#') 


def opposite_dir(key):
  if key == "north":
    return "south"
  if key == "south":
    return "north"
  if key == "east":
    return "west"
  if key == "west":
    return "east"
  if key == "up":
    return "down"
  if key == "down":
    return "up"
  return None


def find_opposite_exit(roomdescs, roomdesc, exit):
  # TODO: use a global data structure instead of brute-forcing every call
  room_id = roomdesc['id']
  direction = exit['direction']
  opposite_direction = opposite_dir(direction)
  for other_room in roomdescs:
    if other_room['id'] == room_id:
      # same room
      continue
    for other_exit in other_room['exits']:
      if (other_exit['to_loc'] == room_id
        and other_exit['direction'] == opposite_direction):
        return other_exit
  return None


def make_exit(exit, opposite_exit, descs, lines):
  exit_kind = ExitKind(exit['kind'])
  direction = exit['direction']
  direction_letter = direction[0]
  to_room_id = f'room_{exit["to_loc"]}'
  # req_verb is only used in a single exit - maybe by error?
  # req_verb = exit['req_verb']
  req_alias = exit['req_alias']
  alias = exit['alias']
  obj_req = exit['obj_req']
  hidden = exit['hidden']

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

  #if exit_kind == ExitKind.PASSWORDED or (alias and req_alias):
    # alias and req_alias == passworded door
    # TODO: should these be two different flavors of exit? 
  #  exit_names = alias
  #  hidden = True

  # TODO: how to handle req_alias? we want to show the exit (e.g., "east"),
  # but not show the alias password, and require using the alias

  if alias:
    exit_names = f"{direction};{direction_letter};{alias}"
  else:
    exit_names = f"{direction};{direction_letter}"

  print(f'@open {exit_names} = {to_room_id}')
  print('#')

  exit_name = exit_names.split(';')[0]

  print(f"@set {exit_name}/exit_kind = {exit_kind}")
  print('#')

  if exit_kind == ExitKind.NO_EXIT:
    print(f"@lock {exit_name} = traverse:none()")
    print('#')

  if hidden:
    print(f"@lock {exit_name} = view:perm(see_hidden_exits)")
    print('#')

  # TODO: obj lock with something like
  # print(f"@lock {exit_name} = traverse:holds(obj_id_or_key)")

  maybe_set_desc(exit['exit_desc'], exit_name, 'exit_desc', descs, lines)
  maybe_set_desc(exit['fail'], exit_name, 'fail_msg', descs, lines)
  maybe_set_desc(exit['success'], exit_name, 'success_msg', descs, lines)
  maybe_set_desc(exit['go_in'], exit_name, 'go_in_msg', descs, lines)
  # TODO: we could search all rooms/exits for our opposite and then use its come_out_msg
  # maybe_set_desc(exit['come_out'], exit_name, 'come_out_msg', descs, lines)
  if opposite_exit:
    maybe_set_desc(opposite_exit['come_out'], exit_name, 'come_out_msg', descs, lines)
    

  door_effect = exit['door_effect']
  if door_effect:
    exit_effect_value, exit_effect_kind = split_integer(door_effect)
    print(f"@set {exit_name}/exit_effect_kind = {exit_effect_kind}")
    print('#')
    print(f"@set {exit_name}/exit_effect_value = {exit_effect_value}")
    print('#')


def main():
  """Command-line script."""  
  # TODO: use a class and keep descs/lines/roomsdescs as ivars
  # Alternately make them globals
  with open(DESC_FILE) as f:
    descs = json.load(f)
  with open(LINES_FILE) as f:
    lines = json.load(f)
  with open(ROOMDESC_FILE) as f:
    roomdescs = json.load(f)


  print("""# Monster batchcommand build file.
#
# To nuke the database first:
# $ evennia stop
# $ rm -f /opt/monsterdata/monster.db3
# $ evennia migrate
# $ evennia start
# [connect to game]
# @batchcommands monster.world.build
#
#
# Step 1: Create all rooms first.
#""")

  for roomdesc in roomdescs:
    make_room(roomdesc, descs)

  print("""#
#
# Step 2: Make exits between rooms.
#""")

  for roomdesc in roomdescs:
    print(f'@tel room_{roomdesc["id"]}')
    print('#')
    for exit in roomdesc['exits']:
      opposite_exit = find_opposite_exit(roomdescs, roomdesc, exit)
      make_exit(exit, opposite_exit, descs, lines)


if __name__ == "__main__":
  main()

