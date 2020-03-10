from commands.command import Command


class CmdHide(Command):
  key = "hide"
  aliases = ["hid"]  
  help_category = "Monster"

  def func(self):
    if self.caller.db.hidden:
      self.caller.msg("You are already hidden")
      return
    self.caller.db.hidden = True


class CmdReveal(Command):
  key = "reveal"
  aliases = ["rev", "reve", "revea"]  
  help_category = "Monster"

  def func(self):
    if not self.caller.db.hidden:
      self.caller.msg("You aren't hidden")
      return
    self.caller.db.hidden = False


class CmdSearch(Command):
  key = "search"
  aliases = ["sea", "sear", "searc"]
  help_category = "Monster"

  def func(self):
    self.not_implemented_yet()
