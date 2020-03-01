from gamerules.character_classes import reset_character_class, set_character_class
from gamerules.xp import gain_xp, set_xp


def apply_exit_effect(target, exit_effect_kind, exit_effect_value):
  if exit_effect_kind == ExitEffectKind.XP:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.WEALTH:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.BANK_WEALTH:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.HEALTH:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.MANA:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.XP_SET:
    set_xp(target, exit_effect_value)
  elif exit_effect_kind == ExitEffectKind.CLASS_RESET:
    if target.db.character_class_name:
      reset_character_class(target, exit_effect_value)
  elif exit_effect_kind == ExitEffectKind.CLASS_SET:
    if target.db.character_class_name:
      set_character_class(target, exit_effect_value)
  elif exit_effect_kind == ExitEffectKind.ALARMED:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.HEALTH_LESS:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.GUARDIAN:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.XP_MODIFIED:
    gain_xp(target, exit_effect_value)
