#!/usr/bin/python3
from enum import IntEnum
import json
import sys
sys.path.insert(0, '../..')

from gamerules.exit_effect_kind import ExitEffectKind
from gamerules.exit_kind import ExitKind
from generator_utils import *


def make_room(roomdesc):
  record_id = roomdesc["id"]
  print(f'@dig {roomdesc["nice_name"]};room_{record_id}')
  print('#')


def main():
  print('# Add an obvious non-destination for room id 0')
  print(f'@dig NOWHERE;room_0')
  print('#')  
  for roomdesc in ROOMDESCS:
    make_room(roomdesc)


if __name__ == "__main__":
  main()

