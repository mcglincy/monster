
from evennia.server.sessionhandler import SESSIONS
from commands.command import QueuedCommand
from gamerules.hiding import hide, reveal, search


class CmdShout(QueuedCommand):
  key = "shout"
  aliases = ["sho", "shou"]  
  help_category = "Monster"

  def check_preconditions(self):
    if not self.args:
      self.caller.msg("Usage: shout <message>")
      return False

  def inner_func(self):
    message = f"{self.caller.key} shouts, \"{self.args.strip()}\""
    SESSIONS.announce_all(message)