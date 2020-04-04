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


class CmdDebug(BaseCommand):
  key = "debug"
  aliases = ["deb", "debu"]
  help_category = "Monster"

  def func(self):
    arg = self.args.strip()
    if arg.lower() == "on":
      self.caller.ndb.debug = True
    elif arg.lower() == "off":
      self.caller.ndb.debug = False
    self.caller.msg(f"Debug: {self.caller.ndb.debug}")


def debug_msg(caller, msg):
  if caller.ndb.debug:
    caller.msg("|w" + msg)
