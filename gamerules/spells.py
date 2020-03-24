import random
from gamerules.freeze import freeze
from gamerules.hiding import find_unhidden, reveal
from gamerules.spell_effect_kind import SpellEffectKind


def make_saving_throw(target, spell):
  # TODO: original monster save % is MyExperience DIV 1000, aka 1% per level...
  # but that code also checks if >80, which would never happen. WTF?
  # Maybe it was supposed to be 10% per level? or max 8%?
  chance_to_save = target.level
  if random.randint(0, 100) <= chance_to_save:
    target.msg(f"You resisted the {spell.key} spell.")
    target.location.msg_contents(
      f"{target.ket} resisted the {spell.key} spell.", exclude=[target])
    return True
  return False


def mana_cost(caster, spell):
  return spell.mana + spell.level_mana * caster.level


def can_cast_spell(caster, spell):
  # TODO: convert to character_class.key?
  if spell.class_id and spell.class_id != caster.character_class.record_id:
    caster.msg("You are the wrong class to cast that spell.")
    return False

  if spell.group and spell.group != caster.character_class.group:
    caster.msg("You are the wrong group to cast that spell.")
    return False

  if spell.min_level > caster.level:
    caster.msg(f"Your level is too low to cast {spell.key}.")
    return False

  if mana_cost(caster, spell) > caster.db.mana:
    caster.msg("You do not have enough mana.")
    return False

  return True


def cast_spell(caster, spell, target=None,
  direction=None, distance_target_name=None):
  if not can_cast_spell(caster, spell):
    return

  # deduct mana
  mana = mana_cost(caster, spell)
  caster.gain_mana(-mana)

  # possibly reveal caster
  if spell.reveals and caster.is_hiding:
      reveal(caster)

  # possibly fail
  if spell.failure_chance and random.randint(0, 100) < spell.failure_chance:
    if spell.failure_desc:
      caster.msg(spell.failure_desc)
    else:
      caster.msg("Your spell failed!")
    return

  # verify we have a target if spell needs one.
  # We do this in cast_spell() and not before, so mis-targeting still
  # deducts mana and reveals caster.
  if spell.should_prompt and not target:
    # we already did a find_hidden() call that msg'd caller with any find
    # failure, so just silently bail
    return

  send_cast_messages(caster, spell)
  if not spell.is_distance:
    # TODO: where to do this?
    send_effect_messages(caster, spell, target)

  # apply spell effects
  for effect in spell.effects:
    apply_spell_effect(spell, effect, caster, target,
      direction, distance_target_name)


def send_cast_messages(caster, spell):
  # TODO: handle spell.silent checks for messaging
  caster.msg(f"You cast {spell.key}.")
  caster.location.msg_contents(
    f"{caster.key} casts {spell.key}.", exclude=[caster])
  # where should caster_desc be sent? cast or effect?
  if spell.caster_desc:
    caster.msg(spell.caster_desc)


# TODO: figure out distance vs. not for messaging
def send_effect_messages(caster, spell, target):
  # TODO: our room descriptions / alignment field??? seem off. DEBUG and look at old pascal code.
  #if spell.room_desc:
  #  caster.location.msg_contents(spell.room_desc, exclude=[caster, target])
  # TODO: do we need to consider effect vs. room for msgs?
  if spell.victim_desc:
    victim_desc = spell.victim_desc.replace("#", caster.key)
    if spell.affects_room:
      caster.location.msg_contents(victim_desc, exclude=[caster])
    elif target:
      target.msg(victim_desc)


def effect_targets(effect, caster, target):
  if not effect.affects_room:
    # single target
    return [target]
  # everyone in room
  targets = []
  for occupant in caster.location.contents:
    if (occupant != caster 
      and occupant.is_typeclass("typeclasses.characters.Character")):
      targets.append(occupant)
  return targets  


def is_deflectable(effect):  
  if effect.effect_kind == SpellEffectKind.CURE_POISON:
    # we should just have separate POISON and CURE_POISON effects
    return effect.param_1 > 0
  else:
    return effect.effect_kind in [
      SpellEffectKind.HURT, SpellEffectKind.SLEEP,
      SpellEffectKind.PUSH, SpellEffectKind.WEAK, SpellEffectKind.SLOW]


def remove_spell_deflections(effect, targets):
  deflected = []
  for target in targets:
    if target.spell_deflect_armor:
      if random.randint(0, 100) < target.spell_deflect_armor:
        target.msg("The spell has been deflected by your armor!")
        target.location.msg_contents(
          f"The spell was deflected by {target.key}'s armor.", exclude=[target])
        deflected.append(target)
  # remove deflections
  return [x for x in targets if x not in deflected]


def apply_spell_effect(spell, effect, caster, 
  target=None, direction=None, distance_target_name=None):

  if effect.effect_kind == SpellEffectKind.DISTANCE_HURT:
    # distance has fundamentally different handling for effect delivery
    apply_distance_hurt_effect(effect, caster, target)
    return

  # single target or room
  targets = effect_targets(effect, caster, target)
  # check spell deflection before applying the actual effect
  if is_deflectable(effect):
    targets = remove_spell_deflections(caster, targets)

  if effect.effect_kind == SpellEffectKind.CURE_POISON:
    apply_cure_poison_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.STRENGTH:
    apply_strength_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.SPEED:
    apply_speed_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.INVISIBLE:
    apply_invisible_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.SEE_INVISIBLE:
    apply_see_invisible_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.HEAL:
    apply_heal_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.HURT:
    apply_hurt_effect(spell, effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.SLEEP:
    apply_sleep_effect(spell, effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.PUSH:
    apply_push_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.ANNOUNCE:
    apply_announce_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.COMMAND:
    apply_command_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.DETECT_MAGIC:
    apply_detect_magic_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.FIND_PERSON:
    apply_find_person_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.LOCATE:
    apply_locate_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.WEAK:
    apply_weak_effect(effect, caster, targets)
  elif effect.effect_kind == SpellEffectKind.SLOW:
    apply_slow_effect(effect, caster, targets)


def apply_cure_poison_effect(effect, caster, target):
  cure_or_poison = effect.param_1
  # TODO


def apply_strength_effect(effect, caster, target):
  strength_modifier = effect.param_1
  level_strength_modifier = effect.param_2
  # TODO


def apply_speed_effect(effect, caster, target):
  speed_modifier = effect.param_1
  level_speed_modifier = effect.param_2
  # TODO


def apply_invisible_effect(effect, caster, target):
  pass


def apply_see_invisible_effect(effect, caster, target):
  pass


def apply_heal_effect(effect, caster, target):
  base = effect.param_1
  level_base = effect.param_2
  rand = effect.param_3
  level_rand = effect.param_4
  base_heal = base + level_base * caster.level
  random_heal = rand + level_rand * caster.level
  heal = base_heal + random.randint(0, random_heal)
  target.gain_health(heal, damager=None)


def spell_armor_adverb(amount):
  if amount <= 33:
    return "slightly"
  elif amount <=66:
    return "significantly"
  elif amount <= 99:
    return "greatly"
  else:
    return "totally"


def apply_hurt_effect(spell, effect, caster, targets):
  # calculate damage
  base = effect.param_1
  level_base = effect.param_2
  rand = effect.param_3
  level_rand = effect.param_4
  base_dmg = base + level_base * caster.level
  random_dmg = rand + level_rand * caster.level
  damage = base_dmg + random.randint(0, random_dmg)
  caster.msg(f"Your {spell.key} spell does {damage} damage.")

  for target in targets:
    if not hasattr(target, "gain_health"):
      continue
    # apply spell armor, if any
    target_damage = damage
    spell_armor = target.spell_armor
    if spell_armor:
      target_damage = int(target_damage * (100 - spell_armor) / 100)
      adverb = spell_armor_adverb(spell_armor)
      caster.msg(f"Your spell is {adverb} diffused by {target.key}'s armor.")
      target.msg(f"{caster.key}'s spell is {adverb} diffused by your armor.")
      target.location.msg_contents(
        f"{caster.key}'s spell is {adverb} diffused by {target.key}'s armor.",
        exclude=[caster, target])
    target.gain_health(-target_damage, damager=caster)

  if effect.affects_caster and hasattr(caster, "gain_health"):
    # TODO: handle caster as targets.append()?
    caster.gain_health(-damage, damager=None)


def apply_sleep_effect(spell, effect, caster, targets):
  base = effect.param_1
  level_base = effect.param_2
  rand = effect.param_3
  level_rand = effect.param_4
  base_sleep_time = base + level_base * caster.level
  random_sleep_time = rand + level_rand * caster.level
  sleep_time = base_sleep_time + random.randint(0, random_sleep_time)
  freeze_duration = sleep_time / 100.0

  for target in targets:
    if make_saving_throw(target, spell):
      # We already msg in make_saving_throw()...
      # caster.msg(f"{target.key} is not affected by the spell.")
      # target.msg("You are not affected by the spell.")
      continue
    freeze(target, freeze_duration)


def apply_push_effect(effect, caster, target):
  push_direction = effect.param_1
  # TODO


def apply_announce_effect(effect, caster, target):
  pass


def apply_command_effect(effect, caster, target):
  pass


def apply_distance_hurt_effect(effect, caster, target):
  distance_behavior = effect.param_4
  # TODO


def apply_detect_magic_effect(effect, caster, target):
  pass


def apply_find_person_effect(effect, caster, target):
  pass


def apply_locate_effect(effect, caster, target):
  pass


def apply_weak_effect(effect, caster, target):
  strength_modifier = effect.param_1
  level_strength_modifier = effect.param_2
  # TODO


def apply_slow_effect(effect, caster, target):
  speed_modifier = effect.param_1
  level_speed_modifier = effect.param_2
  # TODO

