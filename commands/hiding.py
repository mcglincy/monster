from commands.command import Command
from gamerules.hiding import hide, reveal, search

class CmdHide(Command):
  key = "hide"
  aliases = ["hid"]  
  help_category = "Monster"

  def func(self):
    hide(self.caller)


class CmdReveal(Command):
  key = "reveal"
  aliases = ["rev", "reve", "revea"]  
  help_category = "Monster"

  def func(self):
    reveal(self.caller)


class CmdSearch(Command):
  key = "search"
  aliases = ["sea", "sear", "searc"]
  help_category = "Monster"

  def func(self):
    # TODO: maybe move to superclass check/ivar
    if self.caller.is_hiding():
      self.caller.msg("You can't do that while you're hiding.")
      return
    search(self.caller)
