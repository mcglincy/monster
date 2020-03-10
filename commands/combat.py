from commands.command import Command
from gamerules.combat import resolve_attack


class CmdAttack(Command):
  """Attack the enemy."""
  key = "attack"
  aliases = ["att", "atta", "attac"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    if not self.args:
      self.caller.msg("Usage: attack <target>")
      return

    # TODO: change to pick first matching target
    target = self.caller.search(self.args.strip())
    if not target:
      return

    resolve_attack(self.caller, target)


class CmdBleed(Command):
  key = "bleed"
  aliases = ["ble", "blee"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    if hasattr(self.caller, "gain_health"):
      self.caller.gain_health(-50)


class CmdRest(Command):
  key = "rest"
  aliases = ["res"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    if hasattr(self.caller, "gain_health"):
      self.caller.gain_health(50)
