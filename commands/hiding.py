from commands.command import Command


class CmdHide(Command):
  key = "hide"
  aliases = ["hid"]  
  help_category = "Monster"

  def func(self):
    self.not_implemented_yet()


class CmdReveal(Command):
  key = "reveal"
  aliases = ["rev", "reve", "revea"]  
  help_category = "Monster"

  def func(self):
    self.not_implemented_yet()


class CmdSearch(Command):
  key = "search"
  aliases = ["sea", "sear", "searc"]
  help_category = "Monster"

  def func(self):
    self.not_implemented_yet()
