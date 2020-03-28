from commands.command import QueuedCommand
from gamerules.combat import resolve_attack
from gamerules.health import tick_health
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
    self.caller.gain_health(-50)
    self.caller.gain_mana(-10)


class CmdRest(QueuedCommand):
  key = "rest"
  aliases = ["res"]
  locks = "cmd:all()"
  help_category = "Monster"

  def check_preconditions(self):
    if not self.caller.location.is_special_kind(SpecialRoomKind.HEAL):
      self.caller.msg("You cannot rest here.")
      return False
    # TODO: putting meaningful code in check_preconditions is a hack.
    self.caller.msg("You begin to rest.")
    self.caller.location.msg_contents(
      f"{self.caller.name} begins to rest.", exclude=self.caller)
    self.caller.ndb.resting = True

  def input_prompt1(self):
    # TODO: we're cheating, any input will terminate
    return "Type exit to continue: "

  def inner_func(self):
    self.caller.ndb.resting = False
    self.caller.msg("You stop resting.")
    self.caller.location.msg_contents(
      f"{self.caller.name} stops resting.", exclude=self.caller)

  def post_freeze(self):
    # Freeze(AllStats.Stats.MoveSpeed * HereDesc.Mag[rm$b_heal] / 100, AllStats);
    room_magnitude = self.caller.location.magnitude(SpecialRoomKind.HEAL)
    return self.caller.move_speed * room_magnitude / 100.0



