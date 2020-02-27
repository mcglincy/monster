#!/usr/bin/python3

from enum import IntEnum
import json


ROOMDESC_FILE = './json/roomdesc.json'
DESC_FILE = './json/desc.json'


class RoomKind(IntEnum):
  MARKET = 0
  NO_COMBAT = 1
  NO_HIDE = 2
  HARD_TO_HIDE = 3
  OBJECT_DESTROY = 4
  TREASURE_DROP = 5
  MONSTER_GENERATOR = 6
  MONSTER_LAIR = 7
  MONSTER_GENERATOR_GROUP = 8
  MONSTER_GENERATOR_MIN_LEVEL = 9
  MONSTER_GENERATOR_MAX_LEVEL = 10
  HEAL = 11


class ExitKind(IntEnum):
  NO_EXIT = 0
  OPEN = 1
  OBJECT_REQUIRED = 2
  OBJECT_FORBIDDEN = 3
  RANDOM_FAIL = 4
  POTENTIAL_EXIT = 5
  ONLY_EXISTS_WHILE_HOLDING_OBJECT = 6
  TIMED = 7
  PASSWORDED = 8


class ExitEffectKind(IntEnum):
  XP = 1
  WEALTH = 2
  BANK_WEALTH = 3
  HEALTH = 4
  MANA = 5
  XP_SET = 6
  CLASS_RESET = 7
  CLASS_SET = 8
  ALARMED = 9
  HEALTH_LESS = 10
  GUARDIAN = 11
  XP_MODIFIED = 12


def main():
  """Command-line script."""  
  with open(ROOMDESC_FILE) as f:
    roomdescs = json.load(f)

  with open(DESC_FILE) as f:
    descs = json.load(f)

  print("""# evmonster batchcommand build file.
  #
  # To nuke the database first:
  # $ evennia stop
  # $ rm -f evmonster/server/evennia.db
  # $ evennia migrate
  # $ evennia start
  # [connect to game]
  # @batchcommands evmonster.world.build
  #
  # We start from Limbo
  @tel #2
  #
  #
  # Step 1: Create all rooms first.
  #""")

  for roomdesc in roomdescs:
    print(f'@dig/tel {roomdesc["nice_name"]};room_id_{roomdesc["id"]}')
    print('#')
    if 'primary' in roomdesc:
      desc_idx = roomdesc['primary'] - 1
      if desc_idx >= 0 and desc_idx < len(descs):
        desc = descs[desc_idx]
        print('@desc')
        print('\n'.join(desc['lines']))
        print('#')

  print("""#
  #
  # Step 2: Make exits between rooms.
  #""")

  for roomdesc in roomdescs:
    print(f'@tel room_id_{roomdesc["id"]}')
    print('#')
    for exit in roomdesc['exits']:
      print(f'@open {exit["direction"]};{exit["direction"][0]} = room_id_{exit["to_loc"]}')
      print('#')


if __name__ == "__main__":
  main()

