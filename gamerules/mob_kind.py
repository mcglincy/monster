from enum import IntEnum

class MobKind(IntEnum):
  FIGHTER = 1
  NPC = 2
  SPELL_CASTER = 3
  FIGHTER_SPELL_CASTER = 4
  THIEF = 5
  CUTTHROAT = 6
  UNDEAD = 7
  MULTIPLIER = 8
  MANA_CHARGER = 9