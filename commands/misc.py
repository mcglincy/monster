from commands.command import Command


class CmdBrief(Command):
  """Toggle brief descriptions."""
  key = "brief"
  aliases = ["bri", "brie"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    self.not_implemented_yet()


class CmdDot(Command):
  """Repeat the last command."""
  key = "."
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    last_command = self.caller.ndb.last_command
    if last_command:
      self.caller.msg(last_command.raw_string)
      self.caller.execute_cmd(last_command.raw_string)

  def at_post_cmd(self):
    # override to do nothing; we don't want dot as our last_command
    pass


class CmdSheet(Command):
  """Show character sheet."""
  key = "sheet"
  aliases = ["she", "shee"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    self.not_implemented_yet()

