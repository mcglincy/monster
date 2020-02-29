from random import randint

from evennia.utils.search import search_object

from gamerules.xp import kill_xp


def resolve_attack(attacker, target):
  # verify attacker/target validity
  weapon = attacker.db.equipped_weapon
  if not weapon:
    attacker.msg("You have no equipped weapon!")
    return
  if attacker.key == target.key:
    attacker.msg("You can't attack yourself!")
    return
  # TODO: add more rigorous can-attack checks
  if not hasattr(target, "at_damage"):
    attacker.msg("You can't attack that.")
    return

  # calculate damage
  damage = attack_damage(attacker, weapon)

  # attack message for attacker
  attacker.msg(attack_attacker_msg(target.key, weapon.key, damage))

  # attack message for target
  target.msg(attack_target_msg(attacker.key, weapon.key, damage))

  # attack message for room bystanders
  location_msg = attack_bystander_msg(attacker.key, target.key, weapon.key, damage)
  attacker.location.msg_contents(location_msg, exclude=[attacker, target])

  # resolve damage
  armor = target.db.equipped_armor
  if armor:
    if armor.db.deflect_armor > 0 and randint(0, 100) < armor.db.deflect_armor:
      target.msg("The attack is deflected by your armor.")
      attacker.msg(f"Your weapon is deflected by {self.key}'s armor.")
      damage = int(damage / 2)
    if armor.db.base_armor > 0:
      target.msg("The attack is partially blocked by your armor.")
      attacker.msg(f"Your weapon is partially blocked by {self.key}'s armor.")
      damage = int(damage * ((100 - armor.db.base_armor) / 100))
  target.at_damage(damage, damager=attacker)


def attack_damage(attacker, weapon):
  # TODO: apply attacker level etc to damage calc
  return weapon.db.base_damage + randint(0, weapon.db.random_damage)


def attack_attacker_msg(target_name, weapon_name, damage):
  if damage > 500:
    return f"You vaporize {target_name}'s putrid body. [{damage}]"
  elif damage > 400:
    return f"You attack {target_name} with blinding speed and power!!! [{damage}]"
  elif damage > 300:
    return f"You deliver an almost deadly blow to {target_name} with your {weapon_name}!! [{damage}]"
  elif damage > 200:
    return f"Your {weapon_name} creams {target_name}'s poor little body!! [{damage}]"
  elif damage > 150:
    return f"Your {weapon_name} hits {target_name} very hard! [{damage}]"
  elif damage > 100:
    return f"Your {weapon_name} hits {target_name} hard! [{damage}]"
  elif damage > 50:
    return f"You hits {target_name}, good. [{damage}]"
  elif damage > 0:
    return f"{target_name} is grazed by your {weapon_name}."
  else:
    return f"You miss {target_name} with your {weapon_name}."


def attack_target_msg(attacker_name, weapon_name, damage):
  if damage > 500:
    return f"{attacker_name} vaporizes you! [{damage}]"
  elif damage > 400:
    return f"{attacker_name} attacks you with blinding speed and power, ARRRG!! [{damage}]"
  elif damage > 300:
    return f"{attacker_name}'s {weapon_name} nearly splits you in two!!! [{damage}]"
  elif damage > 200:
    return f"{attacker_name}'s {weapon_name} creams your poor little body!! [{damage}]"
  elif damage > 150:
    return f"{attacker_name}'s {weapon_name} hits you very hard! [{damage}]"
  elif damage > 100:
    return f"{attacker_name}'s {weapon_name} hits you hard! [{damage}]"
  elif damage > 50:
    return f"{attacker_name}'s {weapon_name} hits you, good. [{damage}]"
  elif damage > 0:
    return f"You are grazed by {attacker_name}'s {weapon_name}. [{damage}]"
  else:
    return f"{attacker_name} missed you with a {weapon_name}. [{damage}]"


def attack_bystander_msg(attacker_name, target_name, weapon_name, damage):
  if damage > 500:
    return f"{attacker_name} vaporizes {target_name}'s putrid body."
  elif damage > 400:
    return f"{attacker_name} attacks {target_name} with blinding speed and power!!!"
  elif damage > 300:
    return f"{attacker_name}'s {weapon_name} nearly splits {target_name} in two!!!"
  elif damage > 200:
    return f"{attacker_name}'s {weapon_name} creams {target_name}'s poor little body!!"
  elif damage > 150:
    return f"{attacker_name}'s {weapon_name} hits {target_name} very hard!"
  elif damage > 100:
    return f"{attacker_name}'s {weapon_name} hits {target_name} with incredible force!"
  elif damage > 50:
    return f"{attacker_name} hits {target_name}, good."
  elif damage > 0:
    return f"{target_name} is grazed by {attacker_name}'s {weapon_name}."
  else:
    return f"{attacker_name} misses {target_name} with a {weapon_name}."


def character_death(killed, killer=None):
  # killed drops everything it was holding before leaving room
  for obj in killed.contents:
    if obj.db.worth:
      # only drop things with value
      # TODO: possible destroy chance?
      killed.execute_cmd(f"drop {obj.key}")
    else:
      # nuke worthless objects
      obj.delete()

  # killed goes to the void
  the_void = search_object("Void")[0]
  if the_void:
    killed.move_to(the_void)

  # reduce killed xp/level
  killed.at_set_xp(int(killed.db.xp / 2))  

  # killed gets back a bit of health
  killed.db.health = 200

  # award xp to the killer
  if killer:
    killer.msg(f"You killed {killed.key}!")
    xp = kill_xp(killer.db.xp, killed.db.xp)
    killer.at_gain_xp(xp)


def mob_death(mob, killer=None):
  death_msg = f"{mob.key} disappears in a cloud of greasy black smoke."
  mob.location.msg_contents(death_msg, exclude=[mob])
  mob.location = None
  mob.delete()
  if killer:
    killer.msg(f"You killed {mob.key}!")
    # TODO: what should mob xp be?
    xp = kill_xp(killer.db.xp, 300)
    killer.at_gain_xp(xp)
