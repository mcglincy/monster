from commands.command import QueuedCommand
from gamerules.find import find_first_unhidden
from gamerules.hiding import hide, hide_object, reveal, search



class CmdHide(QueuedCommand):
  key = "hide"
  aliases = ["hid"]  
  help_category = "Monster"

  def pre_freeze(self):
    return 0.5 + self.caller.hide_delay

  def inner_func(self):
    if self.args:
      # arg, trying to hide an object
      # must be unhidden in the room
      obj = find_first_unhidden(self.caller.location, self.args.strip())
      if obj is None:
        self.caller.msg("I see no such object here.")
        return
      hide_object(self.caller, obj)
    else:
      # no arg, just hide self
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
