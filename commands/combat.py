from commands.command import QueuedCommand
from gamerules.combat import resolve_attack
from gamerules.hiding import find_unhidden
from gamerules.special_room_kind import SpecialRoomKind


class CmdAttack(QueuedCommand):
  """Attack the enemy."""
  key = "attack"
  aliases = ["att", "atta", "attac"]
  locks = "cmd:all()"
  help_category = "Monster"

  def check_preconditions(self):
    if not self.args:
      self.caller.msg("Usage: attack <target>")
      return False
    if self.caller.location.is_special_kind(SpecialRoomKind.NO_COMBAT):
      self.caller.msg("You cannot fight here.")
      return False
    self.target = find_unhidden(self.caller, self.args.strip())
    if not self.target:
      return False

  def pre_freeze(self):
    return self.caller.attack_speed / 200.0

  def post_freeze(self):
    return self.caller.attack_speed / 200.0

  def inner_func(self):
    resolve_attack(self.caller, self.target)


class CmdBleed(QueuedCommand):
  key = "bleed"
  aliases = ["ble", "blee"]
  locks = "cmd:all()"
  help_category = "Monster"

  def inner_func(self):
    if hasattr(self.caller, "gain_health"):
      self.caller.gain_health(-50)
      self.caller.gain_mana(-10)


class CmdRest(QueuedCommand):
  key = "rest"
  aliases = ["res"]
  locks = "cmd:all()"
  help_category = "Monster"

  def inner_func(self):
    if hasattr(self.caller, "gain_health"):
      self.caller.gain_health(50)
      self.caller.gain_mana(50)
