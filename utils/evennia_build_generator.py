#!/usr/bin/python3

import json


ROOMDESC_FILE = './json/roomdesc.json'
DESC_FILE = './json/desc.json'


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