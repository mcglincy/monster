from commands.command import Command


class CmdCast(Command):
  key = "cast"
  aliases = ["cas"]
  help_category = "Monster"

  def func(self):
    self.not_implemented_yet()


class CmdLearn(Command):
  key = "learn"
  aliases = ["lea", "lear"]
  help_category = "Monster"

  def func(self):
    self.not_implemented_yet()
