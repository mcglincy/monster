from commands.command import Command


class CmdBrief(Command):
  """Toggle brief descriptions."""
  key = "brief"
  aliases = ["bri", "brie"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    if self.caller.db.brief_descriptions:
      self.caller.db.brief_descriptions = False
      self.caller.msg("Brief mode now off.")
    else:
      self.caller.db.brief_descriptions = True
      self.caller.msg("Brief mode now on.")


class CmdDot(Command):
  """Repeat the last command."""
  key = "."
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    last_command = self.caller.ndb.last_command
    if last_command:
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

