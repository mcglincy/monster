from enum import IntEnum


class Alignment(IntEnum):
  GOOD = 33
  NEUTRAL = 66
  EVIL = 99


def parse_alignment(num):
  if num < 0 or num > 99:
    # bad alignment
    return None
  if num <= 33:
    # 0-33
    return Alignment.GOOD
  elif num <= 66:
    # 34-66
    return Alignment.NEUTRAL
  elif num <= 99:
    # 67-99
    return Alignment.EVIL