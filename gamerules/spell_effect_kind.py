from enum import IntEnum

class SpellEffectKind(IntEnum):
  CURE_POISON = 1
  STRENGTH = 2
  SPEED = 3
  INVISIBLE = 4
  SEE_INVISIBLE = 5
  HEAL = 6
  HURT = 7
  SLEEP = 8
  PUSH = 9
  ANNOUNCE = 10
  COMMAND = 11
  DISTANCE_HURT = 12
  DETECT_MAGIC = 13
  FIND_PERSON = 14
  LOCATE = 15
  WEAK = 16
  SLOW = 17