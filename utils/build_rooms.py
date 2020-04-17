#!/usr/bin/python3
from enum import IntEnum
import json
import sys
sys.path.insert(0, '..')

from gamerules.exit_effect_kind import ExitEffectKind
from gamerules.exit_kind import ExitKind
from utils.generator_utils import *


with open('./json/roomdesc.json') as f:
  ROOMDESCS = json.load(f)


def make_room(roomdesc):
  record_id = roomdesc["id"]
  print(f'@dig {roomdesc["nice_name"]};room_{record_id}')
  print('#')


def main():
  for roomdesc in ROOMDESCS:
    make_room(roomdesc)


if __name__ == "__main__":
  main()

