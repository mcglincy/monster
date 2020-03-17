from enum import IntEnum


class DistanceSpellBehavior(IntEnum):
  NORMAL = 0
  BOUNCES_OFF_WALLS = 1
  RETURNS_TO_CASTER = 2
  DAMAGES_ENTIRE_PATH = 3