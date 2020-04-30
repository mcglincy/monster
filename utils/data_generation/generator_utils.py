import json


DEFAULT_MSG_ID = 32000

# global data
with open('./og_monster_data/desc.json') as f:
  DESCS = json.load(f)
with open('./og_monster_data/lines.json') as f:
  LINES = json.load(f)
with open('./og_monster_data/objects.json') as f:
  OBJECTS = json.load(f)
with open('./og_monster_data/randoms.json') as f:
  RANDOMS = json.load(f)
with open('./og_monster_data/roomdesc.json') as f:
  ROOMDESCS = json.load(f)
with open('./og_monster_data/rooms.json') as f:
  ROOMS = json.load(f)
with open('./og_monster_data/spells.json') as f:
  SPELLS = json.load(f)


def load_json(filepath):
  with open(filepath) as f:
    data = json.load(filepath)
  return data

def load_descs():
  return load_json('./og_monster_data/desc.json')


def load_lines():
  return load_json('./og_monster_data/lines.json')


def load_objects():
  return load_json('./og_monster_data/objects.json')


def load_roomdescs():
  return load_json('./og_monster_data/roomdesc.json')


def find_object(objects, obj_id):
  for obj in objects:
    if obj['id'] == obj_id:
      return obj
  return None


def split_integer(i):
  # some old pascal integers were packed with 2 values
  high = int(i / 100)
  low = i % 100
  return (high, low)


def lookup_description(id, descs, lines):
  if not id:
    return None
  elif id > 0:
    # use descs
    desc_idx = id - 1
    # TODO: special handling for default description id 32000
    if desc_idx < len(descs):
      return "\n".join(descs[desc_idx]['lines'])
  elif id < 0:
    # use lines
    line_idx = -id -1
    if line_idx < len(lines):
      return lines[line_idx]['line']
  return None


def camel_case(s):
  """Convert an object name to a useful python class name.

  E.g., 'Hammer of the gods' => 'HammerOfTheGods'
  """
  s = s.strip()
  done = False
  chars = []
  idx = 0
  s_len = len(s)
  while not done:
    c = s[idx]
    if idx == 0:
      chars.append(c.upper())
      idx = idx + 1
    elif c == ' ':
      chars.append(s[idx+1].upper())
      idx = idx + 2
    elif c == "'":
      # skip quote
      idx = idx + 1
    else:
      chars.append(c)
      idx = idx + 1
    if idx >= s_len:
      done = True
  return ''.join(chars)


def snake_case(s):
  """Convert an object name to a snake case.

  E.g., 'Hammer of the gods' => 'HAMMER_OF_THE_GODS'
  """
  s = s.strip()
  chars = []
  for c in s:
    if c == ' ' or c == '-':
      chars.append('_')
    elif c == "'":
      pass
    else:
      chars.append(c.upper())
  return ''.join(chars)