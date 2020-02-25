from commands.command import Command
from evennia import CmdSet
from random import randint


class CmdSetWeapon(CmdSet):
  """Holds the attack command."""

  def at_cmdset_creation(self):
    """called at first object creation."""
    self.add(CmdAttack())


def attacker_msg(target_name, weapon_name, damage):
  if damage > 500:
    return f"You vaporize {target_name}'s putrid body."
  elif damage > 400:
    return f"You attack {target_name} with blinding speed and power!!!"
  elif damage > 300:
    return f"You deliver an almost deadly blow to {target_name} with your {weapon_name}!!"
  elif damage > 200:
    return f"Your {weapon_name} creams {target_name}'s poor little body!!"
  elif damage > 150:
    return f"Your {weapon_name} hits {target_name} very hard!"
  elif damage > 100:
    return f"Your {weapon_name} hits {target_name} hard!"
  elif damage > 50:
    return f"You hits {target_name}, good."
  elif damage > 0:
    return f"{target_name} is grazed by your {weapon_name}."
  else:
    return f"You miss {target_name} with your {weapon_name}."


def target_msg(attacker_name, weapon_name, damage):
  if damage > 500:
    return f"{attacker_name} vaporizes you!"
  elif damage > 400:
    return f"{attacker_name} attacks you with blinding speed and power, ARRRG!!"
  elif damage > 300:
    return f"{attacker_name}'s {weapon_name} nearly splits you in two!!!"
  elif damage > 200:
    return f"{attacker_name}'s {weapon_name} creams your poor little body!!"
  elif damage > 150:
    return f"{attacker_name}Your {weapon_name} hits {target_name} very hard!"
  elif damage > 100:
    return f"{attacker_name}'s {weapon_name} hits you hard!"
  elif damage > 50:
    return f"{attacker_name}'s {weapon_name} hits you, good."
  elif damage > 0:
    return f"You are grazed by {attacker_name}'s {weapon_name}."
  else:
    return f"{attacker_name} missed you with a {weapon_name}."


def bystander_msg(attacker_name, target_name, weapon_name, damage):
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





class CmdAttack(Command):
  """
  Attack the enemy. Commands:

    attack <enemy>
  """
  key = "attack"
  aliases = ["att", "atta", "attac"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    """Implements the attack."""
    cmdstring = self.cmdstring
    if not self.args:
      self.caller.msg("Who do you attack?")
      return
    target = self.caller.search(self.args.strip())
    if not target:
      return

    # TODO: have some target validity check
    if self.caller.key == target.key:
      self.caller.msg("You can't attack yourself!")
      return

    weapon = self.caller.db.equipped_weapon
    if not weapon:
      self.caller.msg("You have no equipped weapon!")
      return

    # TODO: apply attacker level etc to damage calc
    damage = weapon.db.base_damage + randint(0, weapon.db.random_damage)

    self.caller.msg(attacker_msg(target.key, weapon.key, damage))
    location_msg = bystander_msg(self.caller.key, target.key, weapon.key, damage)
    self.caller.location.msg_contents(location_msg, exclude=[self.caller, target])

    if hasattr(target, "at_weapon_hit"):
      target.at_weapon_hit(self.caller.key, weapon, damage)


class CmdBleed(Command):
  key = "bleed"
  aliases = ["ble", "blee"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    new_health = self.caller.db.health - 50
    self.caller.db.health = new_health
    self.caller.msg(f"Your health is now {new_health}.")


class CmdRest(Command):
  key = "rest"
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    new_health = self.caller.db.health + 50
    self.caller.db.health = new_health
    self.caller.msg(f"Your health is now {new_health}.")
