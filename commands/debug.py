from evennia import Command as BaseCommand


class CmdClear(BaseCommand):
  key = "clear"
  aliases = ["cle", "clea"]  
  help_category = "Monster"

  def func(self):
    self.caller.msg("Clearing character state.")
    self.caller.ndb.active_command = None
    self.caller.ndb.command_queue.clear()
    self.caller.ndb.frozen_until = 0
    self.caller.ndb.hiding = 0
