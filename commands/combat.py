
from evennia import CmdSet, Command


class CmdSetWeapon(CmdSet):
  """Holds the attack command."""

  def at_cmdset_creation(self):
    """called at first object creation."""
    self.add(CmdAttack())


class CmdAttack(Command):
  """
  Attack the enemy. Commands:

    attack <enemy>
  """
  key = "attack"
  aliases = [
    # "att" ????
  ]
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

    damage = self.obj.db.damage
    string = "You stab with %s. " % self.obj.key
    tstring = "%s stabs at you with %s. " % (self.caller.key, self.obj.key)
    ostring = "%s stabs at %s with %s. " % (
        self.caller.key, target.key, self.obj.key)

    # call enemy hook
    if hasattr(target, "at_hit"):
      # should return True if target is defeated, False otherwise.
      target.at_hit(self.obj, self.caller, damage)
      return
    elif target.db.health:
      target.db.health -= damage
    else:
      # sorry, impossible to fight this enemy ...
      self.caller.msg("The enemy seems unaffected.")
      return


class CmdHide(Command):
  key = "hide"
  help_category = "Monster"

  def func(self):
    pass


class CmdReveal(Command):
  key = "reveal"
  help_category = "Monster"

  def func(self):
    pass


class CmdEquip(Command):
  key = "equip"
  help_category = "Monster"

  def func(self):
    pass


class CmdUnequip(Command):
  key = "unequip"
  help_category = "Monster"

  def func(self):
    pass

