
DEFAULT_MSG_ID = 32000


def split_integer(i):
  # some old pascal integers were packed with 2 values
  high = int(i / 100)
  low = i % 100
  return (high, low)


def escaped(s):
  return s.replace('"', '\\"')


def lookup_description(id, descs, lines):
  if not id:
    return None
  elif id > 0:
    # use descs
    desc_idx = id - 1
    # TODO: special handling for default description id 32000
    if desc_idx < len(descs):
      return escaped(' '.join(descs[desc_idx]['lines']))
  elif id < 0:
    # use lines
    line_idx = -id -1
    if line_idx < len(lines):
      return escaped(lines[line_idx]['line'])
  return None