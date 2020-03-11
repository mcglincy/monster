from commands.command import Command
from gamerules.hiding import hide, reveal

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
    self.not_implemented_yet()
