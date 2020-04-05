from gamerules.character_classes import reset_character_class, set_character_class
from gamerules.exit_effect_kind import ExitEffectKind
from gamerules.talk import msg_global
from gamerules.xp import gain_xp, set_xp


def apply_exit_effect(target, source_location, exit_effect_kind, exit_effect_value):
  if exit_effect_kind == ExitEffectKind.XP:
    # TODO: how is XP different from XP_MODIFIED?
    gain_xp(target, exit_effect_value)
  elif exit_effect_kind == ExitEffectKind.WEALTH:
    if target.has_attr("gain_gold"):
      target.gain_gold(exit_effect_value)
  elif exit_effect_kind == ExitEffectKind.BANK_WEALTH:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.HEALTH:
    target.gain_health(exit_effect_value)
  elif exit_effect_kind == ExitEffectKind.MANA:
    target.gain_mana(exit_effect_value)
  elif exit_effect_kind == ExitEffectKind.XP_SET:
    set_xp(target, exit_effect_value)
  elif exit_effect_kind == ExitEffectKind.CLASS_RESET:
    if target.db.character_class_key:
      reset_character_class(target, exit_effect_value)
  elif exit_effect_kind == ExitEffectKind.CLASS_SET:
    if target.db.character_class_key:
      set_character_class(target, exit_effect_value)
  elif exit_effect_kind == ExitEffectKind.ALARMED:
    sound_alarm(target, source_location)
  elif exit_effect_kind == ExitEffectKind.HEALTH_LESS:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.GUARDIAN:
    # TODO
    pass
  elif exit_effect_kind == ExitEffectKind.XP_MODIFIED:
    gain_xp(target, exit_effect_value)


def sound_alarm(target, source_location):
  # TODO: output, parse, and handle NamePrint field
  # CASE HereDesc.NamePrint OF
  #   1 : s := s + 'in';
  #   2 : s := s + 'at';
  #   3 : s := s + 'in the';
  #   4 : s := s + 'at the';  
  msg_global(f"{target.name} set off an alarm in {source_location.name}.")