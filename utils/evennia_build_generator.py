#!/usr/bin/python3
import json
import sys
sys.path.insert(0, '..')

from typeclasses.exit_effect_kind import ExitEffectKind
from typeclasses.exit_kind import ExitKind
from typeclasses.room_kind import RoomKind
from utils.generator_utils import lookup_description, split_integer


DESC_FILE = './json/desc.json'
LINES_FILE = './json/lines.json'
ROOMDESC_FILE = './json/roomdesc.json'


def make_room(roomdesc, descs):
  record_id = roomdesc["id"]
  print(f'@dig/tel {roomdesc["nice_name"]};room_{record_id}')
  print('#')
  print(f'@set here/record_id = {record_id}')
  print('#')
  if roomdesc["trap_chance"]:
    print(f'@set here/trap_chance = {roomdesc["trap_chance"]}')
    print('#')
    print(f'@set here/trap_to = {roomdesc["trap_to"]}')
    print('#')
  # TODO: do we want to handle secondary descript?
  if 'primary' in roomdesc:
    desc_idx = roomdesc['primary'] - 1
    if desc_idx >= 0 and desc_idx < len(descs):
      desc = descs[desc_idx]
      print('@desc')
      print('\n'.join(desc['lines']))
      print('#')


def make_exit(exit, descs, lines):
  exit_kind = exit['kind']
  direction = exit['direction']
  direction_letter = direction[0]
  to_room_id = f'room_{exit["to_loc"]}'
  # req_verb is only used in a single exit - maybe by error?
  # req_verb = exit['req_verb']
  req_alias = exit['req_alias']
  alias = exit['alias']
  obj_req = exit['obj_req']
    # "hidden" field in the JSON seems to never be set
  hidden = False

  if exit_kind == ExitKind.NO_EXIT:
    # skip, I guess?
    return
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

  if exit_kind == ExitKind.PASSWORDED or (alias and req_alias):
    # alias and req_alias == passworded door
    # TODO: should these be two different flavors of exit? 
    exit_names = alias
    hidden = True
  elif alias:
    exit_names = f"{direction};{direction_letter};{alias}"
  else:
    exit_names = f"{direction};{direction_letter}"

  print(f'@open {exit_names} = {to_room_id}')
  print('#')

  exit_name = exit_names.split(';')[0]

  if hidden:
    print(f"@lock {exit_name} = view:perm(see_hidden_exits)")
    print('#')

  # TODO: obj lock with something like
  # print(f"@lock {exit_name} = traverse:holds(obj_id_or_key)")

  exit_desc = exit['exit_desc']
  if exit_desc == 0:
    pass
  elif exit_desc == 32000:
    # print(f"@set {exit_name}/exit_desc = 'blah blah default'")
    # print('#')
    pass
  else: 
    line = lookup_description(exit_desc, descs, lines)
    print(f"@set {exit_name}/exit_desc = '{line}'")
    print('#')    

  door_effect = exit['door_effect']
  if door_effect:
    exit_effect_value, exit_effect_kind = split_integer(door_effect)
    print(f"@set {exit_name}/exit_effect_kind = {exit_effect_kind}")
    print('#')
    print(f"@set {exit_name}/exit_effect_value = {exit_effect_value}")
    print('#')



def main():
  """Command-line script."""  
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
      make_exit(exit, descs, lines)


if __name__ == "__main__":
  main()

