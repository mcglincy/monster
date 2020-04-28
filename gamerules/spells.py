import random
from gamerules.combat import find_first_attackable
from gamerules.direction import Direction
from gamerules.distance_spell_behavior import DistanceSpellBehavior
from gamerules.find import find_all_unhidden, find_exit, find_first_unhidden
from gamerules.freeze import freeze
from gamerules.hiding import reveal
from gamerules.saving_throw import make_saving_throw
from gamerules.spell_effect_kind import SpellEffectKind


def do_cast(caster, spell, input1, input2, deduct_mana=False):
  """Generic 'apply inputs' cast function useful for command classes."""
  target = None
  direction = None
  distance_target_key = None
  if spell.is_distance:
    direction = Direction.from_string(input1)
    distance_target_key = input2
  elif spell.should_prompt:
    key = input1
    target = find_first_attackable(caster.location, key)
    if not target:
      user.msg(f"Could not find '{key}'.")
  if deduct_mana:
    mana = mana_cost(caster, spell)
    caster.gain_mana(-mana)
  cast_spell(caster, spell, target=target, 
    direction=direction, distance_target_key=distance_target_key)


def poof(target, to_room):
  # TODO: use Priv'd target messages? 
  # 'Great wisps of blue smoke drift out of the shadows.'
  # 'Some wisps of blue smoke drift about in the shadows.'
  # TODO: do we need to handle failure?
  # 'There is a crackle of electricity, but the poof fails.'
  target.msg("|wYou feel yourself pulled through the fabric of time and space...")
  target.location.msg_contents(
    f"{target.name} vanishes from the room in a cloud of blue smoke.",
    exclude=target)
  target.move_to(to_room, quiet=True)
  to_room.msg_contents(
    f"In an explosion of golden light {target.name} poofs into the room.",
    exclude=target)


def first_prompt(spell):
  if spell.is_distance:
    return "Direction?"
  elif spell.should_prompt:
    return "At who?"
  return None


def second_prompt(spell):
  distance_effect = spell.distance_effect
  if spell.distance_effect:
    behavior = DistanceSpellBehavior(spell.distance_effect.db_param_4)
    if behavior != DistanceSpellBehavior.DAMAGES_ENTIRE_PATH:
      return "Person to target?"
  return None


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
  direction=None, distance_target_key=None):
  # we do no checks on whether caster can actually cast this spell; 
  # call can_cast_spell() for that

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

  # make sure distance spells have a valid initial exit
  if spell.is_distance:
    # find exit
    exit = find_exit(caster.location, direction)
    if not exit:
      caster.msg(f"Invalid direction {direction.name}.")
      return

  # verify we have a target if spell needs one.
  # We do this in cast_spell() and not before, so mis-targeting still
  # deducts mana and reveals caster.
  if not spell.is_distance and spell.should_prompt and not target:
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
      direction, distance_target_key)


def send_cast_messages(caster, spell):
  # TODO: handle spell.silent checks for messaging
  # where should caster_desc be sent? cast or effect?
  if spell.caster_desc:
    caster.msg("|w" + spell.caster_desc)
  else:
    caster.msg(f"|wYou cast {spell.key}.")
  caster.location.msg_contents(
    f"{caster.key} casts {spell.key}.", exclude=[caster])


# TODO: figure out distance vs. not for messaging
def send_effect_messages(caster, spell, target):
  # TODO: our room descriptions / alignment field??? seem off. DEBUG and look at old pascal code.
  #if spell.room_desc:
  #  caster.location.msg_contents(spell.room_desc, exclude=[caster, target])
  # TODO: do we need to consider effect vs. room for msgs?
  if spell.victim_desc:
    victim_desc = spell.victim_desc.replace("#", caster.key)
    if spell.affects_room:
      caster.location.msg_contents("|w" + victim_desc, exclude=[caster])
    elif target:
      target.msg("|w" + victim_desc)


def is_targetable(obj):
  return (obj.is_typeclass("typeclasses.characters.Character")
    or obj.is_typeclass("typeclasses.mobs.Mob", exact=False))


def pick_targets(effect, caster, target):
  targets = []
  if effect.affects_room:
    # everyone in room
    for obj in caster.location.contents:
      if obj != caster and is_targetable(obj):
        targets.append(obj)
  elif target:
    # single target
    targets.append(target)
  if effect.affects_caster:
    targets.append(caster)
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
  target=None, direction=None, distance_target_key=None):

  if effect.effect_kind == SpellEffectKind.DISTANCE_HURT:
    # distance has fundamentally different handling for effect delivery
    apply_distance_hurt_effect(spell, effect, caster, target, direction, distance_target_key)
    return

  # single target or room, possibly including self
  targets = pick_targets(effect, caster, target)
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


def apply_cure_poison_effect(effect, caster, targets):
  is_poison = effect.param_1
  for target in targets:
    if is_poison:
      if not target.is_poisoned:
        target.db.poisoned = False
        target.msg("|wYour blood begins to boil!")
        target.location.msg_contents(
          f"{target.name} is poisoned!", exclude=[target])
    else:
      # cure
      if target.is_poisoned:
        target.db.poisoned = False
        target.msg("|wYour blood runs clean.")
        target.location.msg_contents(
          f"{target.name} is no longer poisoned.", exclude=[target])


def apply_strength_effect(effect, caster, targets):
  # TODO
  strength_modifier = effect.param_1
  level_strength_modifier = effect.param_2
  for target in targets:
    pass


def apply_speed_effect(effect, caster, targets):
  # TODO
  speed_modifier = effect.param_1
  level_speed_modifier = effect.param_2
  for target in targets:    
    pass


def apply_invisible_effect(effect, caster, targets):
  # TODO
  for target in targets:
    pass


def apply_see_invisible_effect(effect, caster, targets):
  # TODO
  for target in targets:
    pass


def apply_heal_effect(effect, caster, targets):
  base = effect.param_1
  level_base = effect.param_2
  rand = effect.param_3
  level_rand = effect.param_4
  base_heal = base + level_base * caster.level
  random_heal = rand + level_rand * caster.level
  heal = base_heal + random.randint(0, random_heal)
  for target in targets:
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


def give_spell_damage(spell, caster, target, damage):
  if not hasattr(target, "gain_health"):
    return
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
    give_spell_damage(spell, caster, target, damage)


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
    if make_saving_throw(target, spell.key):
      # We already msg in make_saving_throw()...
      # caster.msg(f"{target.key} is not affected by the spell.")
      # target.msg("You are not affected by the spell.")
      continue
    freeze(target, freeze_duration)


def apply_push_effect(effect, caster, target):
  push_direction = effect.param_1
  # TODO
  for target in targets:
    pass


def apply_announce_effect(effect, caster, target):
  pass


def apply_command_effect(effect, caster, target):
  pass


def apply_distance_hurt_effect(spell, effect, caster, 
  target=None, direction=None, distance_target_key=None):
  damage_base = effect.param_1
  damage_rand = effect.param_2
  damage = damage_base + random.randint(0, damage_rand)
  max_range = effect.param_3
  behavior = DistanceSpellBehavior(effect.param_4)

  # we've already checked direction vs. current-room exits
  # TODO: should effect.name be populated?
  caster.location.msg_contents(
    f"{caster.key} fires a {spell.key} heading {direction.name.lower()}.",
    exclude=[caster])

  current_range = 0
  current_room = caster.location
  while True:
    # send messaging
    if current_room == caster.location:
      caster.msg(f"The {spell.key} is in your room.")
    else:
      caster.msg(f"The {spell.key} travels into {current_room.key}.")
      current_room.msg_contents(
        f"You see a {spell.key} from {caster.key} heading {direction.name.lower()}.",
        exclude=[caster])

    victim_desc = None
    if spell.victim_desc:
      victim_desc = spell.victim_desc.replace("#", caster.key)

    # deal damage, if any
    if behavior == DistanceSpellBehavior.DAMAGES_ENTIRE_PATH:
      # damage everyone unhidden in the room except the caster
      for unhidden in find_all_unhidden(current_room):
        if unhidden != caster and hasattr(unhidden, "gain_health"):
          caster.msg(f"The {spell.key} hits {unhidden.key} for {damage} damage.")
          if victim_desc:
            unhidden.msg("|w" + victim_desc)
          current_room.msg_contents(f"{unhidden.key} is hit by {caster.key}'s {spell.key}.",
            exclude=[caster, unhidden])
          give_spell_damage(spell, caster, unhidden, damage)
    else:
      # single target; see if they're in this room
      target = find_first_unhidden(current_room, distance_target_key)
      if target and hasattr(target, "gain_health"):
        caster.msg(f"The {spell.key} hits {target.key} for {damage} damage.")
        if victim_desc:
          target.msg(victim_desc)
        # TODO: look at room_desc... Green Dart has it, but do others?
        current_room.msg_contents(f"{target.key} is hit by {caster.key}'s {spell.key}.",
          exclude=[caster, target])
        give_spell_damage(spell, caster, target, damage)
        if (behavior in [DistanceSpellBehavior.NORMAL,
          DistanceSpellBehavior.BOUNCES_OFF_WALLS]):
          # we hit our target, so we're done
          break

    # RETURNS_TO_CASTER should go max range and then turn around
    if (current_range == max_range and
      behavior == DistanceSpellBehavior.RETURNS_TO_CASTER):
      current_range = 0
      direction = direction.opposite()
      current_room.msg_contents(
        f"You see a {spell.key} from {caster.key} bounce {direction.name.lower()}.",
        exclude=[caster])

    # try to advance to the next room
    exit = find_exit(current_room, direction)
    if ((current_range == max_range or not exit) and 
      behavior in [DistanceSpellBehavior.BOUNCES_OFF_WALLS, 
        DistanceSpellBehavior.RETURNS_TO_CASTER]):
      direction = direction.opposite()
      exit = find_exit(current_room, direction)
      current_room.msg_contents(
        f"You see a {spell.key} from {caster.key} bounce {direction.name.lower()}.",
        exclude=[caster])
      if behavior == DistanceSpellBehavior.RETURNS_TO_CASTER:
        max_range = current_range  # how many rooms it took to get here
        current_range = 0  # starting all over again
      behavior = DistanceSpellBehavior.NORMAL  # don't keep bouncing

    if not exit:
      # we didn't reverse direction and there's nowhere else to go
      break

    current_room = exit.destination
    current_range = current_range + 1

    if current_range > max_range:
      # we're done
      break



def apply_detect_magic_effect(effect, caster, targets):
  pass


def apply_find_person_effect(effect, caster, targets):
  pass


def apply_locate_effect(effect, caster, targets):
  pass


def apply_weak_effect(effect, caster, targets):
  strength_modifier = effect.param_1
  level_strength_modifier = effect.param_2
  # TODO


def apply_slow_effect(effect, caster, targets):
  speed_modifier = effect.param_1
  level_speed_modifier = effect.param_2
  # TODO

