from enum import IntEnum


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


