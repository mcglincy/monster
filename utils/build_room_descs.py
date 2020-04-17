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
with open('./json/roomdesc.json') as f:
  ROOMDESCS = json.load(f)


def make_room(roomdesc):
  record_id = roomdesc["id"]
  print('###############################################################################')
  print(f'# {roomdesc["nice_name"]}')
  print('###############################################################################')
  print(f'@tel room_{record_id}')
  print('#')
  if 'primary' in roomdesc:
    desc_idx = roomdesc['primary'] - 1
    if desc_idx >= 0 and desc_idx < len(DESCS):
      desc = DESCS[desc_idx]
      print('@desc')
      print('\n'.join(desc['lines']))
      print('#')  


def main():
  """Command-line script."""
  for roomdesc in ROOMDESCS:
    make_room(roomdesc)


if __name__ == "__main__":
  main()

