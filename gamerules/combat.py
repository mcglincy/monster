import random

from evennia.utils.search import search_object
from gamerules.gold import give_starting_gold
from gamerules.hiding import reveal
from gamerules.talk import msg_global
from gamerules.xp import calculate_kill_xp, set_xp, gain_xp


def resolve_attack(attacker, target):
  if target.is_dead:
    # already dead
    return

  weapon = attacker.equipped_weapon
  if not weapon and not attacker.has_claws:
    attacker.msg("You have no equipped weapon!")
    return
  if attacker.key == target.key:
    attacker.msg("You can't attack yourself!")
    return
  # TODO: add more rigorous can-attack checks
  if not hasattr(target, "gain_health"):
    attacker.msg("You can't attack that.")
    return

  is_surprise = False
  if attacker.is_hiding:
    attacker.msg(f"You unexpectedly attack {target.name}!")
    target.msg("Surprise!!!")
    reveal(attacker)
    is_surprise = True

  # calculate damage
  damage = attack_damage(attacker, weapon, is_surprise)

  # attack message for attacker
  attack_name = weapon.key if weapon else "claws"
  attacker.msg(attack_attacker_msg(target.name, attack_name, damage))

  # attack message for target
  target.msg(attack_target_msg(attacker.name, attack_name, damage))

  # attack message for room bystanders
  location_msg = attack_bystander_msg(attacker.name, target.name, attack_name, damage)
  attacker.location.msg_contents(location_msg, exclude=[attacker, target])

  # apply armor to reduce damage
  damage = apply_armor(target, damage)

  # target takes the damage
  target.gain_health(-damage, damager=attacker, weapon_name=attack_name)


def apply_armor(target, damage):
  final_damage = damage
  base_armor = target.base_armor
  deflect_armor = target.deflect_armor
  if deflect_armor > 0 and random.randint(0, 100) < deflect_armor:
    target.msg("The attack is deflected by your armor.")
    final_damage = int(damage / 2)
  if base_armor > 0:
    target.msg("The attack is partially blocked by your armor.")
    final_damage = int(damage * ((100 - base_armor) / 100))
  return final_damage


def attack_damage(attacker, weapon, is_surprise=False):
  rand_multiplier = .7 if is_surprise else random.random()
  if weapon:
    # attacker weapon damages may be the sum of several equipped objects
    dmg = attacker.base_weapon_damage + int(attacker.random_weapon_damage * rand_multiplier)
    weapon_use = attacker.base_weapon_use + attacker.level_weapon_use * attacker.level
    dmg = int(dmg * weapon_use / 100)
  else:
    # claws
    dmg = (
      attacker.base_claw_damage
      + int(attacker.random_claw_damage * rand_multiplier)
      + attacker.level_claw_damage * attacker.level
      )
  if is_surprise:
    dmg = dmg + int(dmg * attacker.shadow_damage_percent / 100)
  return dmg


def attack_attacker_msg(target_name, weapon_name, damage):
  add_s = "" if weapon_name == "claws" else "s"
  if damage > 500:
    return f"You vaporize {target_name}'s putrid body. [{damage}]"
  elif damage > 400:
    return f"You attack {target_name} with blinding speed and power!!! [{damage}]"
  elif damage > 300:
    return f"You deliver an almost deadly blow to {target_name} with your {weapon_name}!! [{damage}]"
  elif damage > 200:
    return f"Your {weapon_name} cream{add_s} {target_name}'s poor little body!! [{damage}]"
  elif damage > 150:
    return f"Your {weapon_name} hit{add_s} {target_name} very hard! [{damage}]"
  elif damage > 100:
    return f"Your {weapon_name} hit{add_s} {target_name} hard! [{damage}]"
  elif damage > 50:
    return f"You hit {target_name}, good. [{damage}]"
  elif damage > 0:
    return f"{target_name} is grazed by your {weapon_name}."
  else:
    return f"You miss {target_name} with your {weapon_name}."


def attack_target_msg(attacker_name, weapon_name, damage):
  add_s = "" if weapon_name == "claws" else "s"  
  if damage > 500:
    return f"{attacker_name} vaporizes you! [{damage}]"
  elif damage > 400:
    return f"{attacker_name} attacks you with blinding speed and power, ARRRG!! [{damage}]"
  elif damage > 300:
    return f"{attacker_name}'s {weapon_name} nearly split{add_s} you in two!!! [{damage}]"
  elif damage > 200:
    return f"{attacker_name}'s {weapon_name} cream{add_s} your poor little body!! [{damage}]"
  elif damage > 150:
    return f"{attacker_name}'s {weapon_name} hit{add_s} you very hard! [{damage}]"
  elif damage > 100:
    return f"{attacker_name}'s {weapon_name} hit{add_s} you hard! [{damage}]"
  elif damage > 50:
    return f"{attacker_name}'s {weapon_name} hit{add_s} you, good. [{damage}]"
  elif damage > 0:
    return f"You are grazed by {attacker_name}'s {weapon_name}. [{damage}]"
  else:
    return f"{attacker_name} missed you with a {weapon_name}. [{damage}]"


def attack_bystander_msg(attacker_name, target_name, weapon_name, damage):
  add_s = "" if weapon_name == "claws" else "s"  
  if damage > 500:
    return f"{attacker_name} vaporizes {target_name}'s putrid body."
  elif damage > 400:
    return f"{attacker_name} attacks {target_name} with blinding speed and power!!!"
  elif damage > 300:
    return f"{attacker_name}'s {weapon_name} nearly split{add_s} {target_name} in two!!!"
  elif damage > 200:
    return f"{attacker_name}'s {weapon_name} cream{add_s} {target_name}'s poor little body!!"
  elif damage > 150:
    return f"{attacker_name}'s {weapon_name} hit{add_s} {target_name} very hard!"
  elif damage > 100:
    return f"{attacker_name}'s {weapon_name} hit{add_s} {target_name} with incredible force!"
  elif damage > 50:
    return f"{attacker_name} hits {target_name}, good."
  elif damage > 0:
    return f"{target_name} is grazed by {attacker_name}'s {weapon_name}."
  else:
    return f"{attacker_name} misses {target_name} with their {weapon_name}."


def character_death(victim, killer=None, weapon_name=None):
  # send an appropriate global death message
  if not killer:
    msg_global(f"{victim.name} has died of mysterious causes.")
  elif not weapon_name:
    msg_global(f"{victim.name} has been slain by {killer.name}.")
  else:
    msg_global(f"{victim.name} has been slain by {killer.name}'s {weapon_name}.")

  # award xp to the killer
  if killer is not None and killer.is_typeclass("typeclasses.characters.Character"):
    killer.msg(f"You killed {victim.name}!")
    xp = calculate_kill_xp(killer.db.xp, victim.db.xp)
    gain_xp(killer, xp)

  # victim drops everything it was holding before leaving room
  for obj in victim.contents:
    if obj.worth:
      # only drop things with value
      # TODO: possible destroy chance?
      victim.execute_cmd(f"drop {obj.key}")
    else:
      # nuke worthless objects
      obj.delete()

  # victim goes to the void
  the_void = search_object("Void")[0]
  if the_void:
    victim.location.msg_contents(
      f"{victim.name} disappears in a cloud of greasy black smoke.", exclude=[victim])
    victim.move_to(the_void, quiet=True)

  # reduce victim xp/level
  set_xp(victim, int(victim.db.xp / 2))

  # clear/reset various stats
  reset_victim_state(victim)

  # starting gold!
  give_starting_gold(victim)


def reset_victim_state(victim):
  # victim.db.health = 1
  victim.db.mana = 0
  victim.ndb.active_command = None
  victim.ndb.command_queue.clear()
  victim.ndb.frozen_until = 0
  victim.ndb.hiding = 0
  victim.ndb.poisoned = False
  victim.ndb.resting = False


