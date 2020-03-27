from commands.command import QueuedCommand


class CmdLook(QueuedCommand):
  """
  look at location or object

  Usage:
    look
    look <obj>
    look *<account>

  Observes your location or objects in your vicinity.
  """

  key = "look"
  aliases = ["l", "ls", "loo"]
  locks = "cmd:all()"
  arg_regex = r"\s|$"
  help_category = "Monster"

  def inner_func(self):
    """Handle the looking."""
    caller = self.caller
    if not self.args:
      target = caller.location
      if not target:
        caller.msg("You have no location to look at!")
        return
    else:
      target = caller.search(self.args)
      if not target:
        return
    self.msg((caller.at_look(target), {"type": "look"}), options=None)
