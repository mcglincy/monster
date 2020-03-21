from commands.command import QueuedCommand
from gamerules.hiding import hide, reveal, search

class CmdHide(QueuedCommand):
  key = "hide"
  aliases = ["hid"]  
  help_category = "Monster"

  def inner_func(self):
    hide(self.caller)


class CmdReveal(QueuedCommand):
  key = "reveal"
  aliases = ["rev", "reve", "revea"]  
  help_category = "Monster"

  def inner_func(self):
    reveal(self.caller)


class CmdSearch(QueuedCommand):
  key = "search"
  aliases = ["sea", "sear", "searc"]
  help_category = "Monster"

  def check_preconditions(self):
    if self.caller.is_hiding:
      self.caller.msg("You can't do that while you're hiding.")
      return False

  def inner_func(self):
    search(self.caller)
