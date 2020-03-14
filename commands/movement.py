from commands.command import Command
from gamerules.exit_kind import ExitKind

# see also evennia commands.py ExitCommand
class CmdExit(Command):
  """Re-implement so it's a dot-repeatable command."""  
  obj = None

  def func(self):
    # TODO: maybe move to superclass check/ivar
    if self.caller.is_hiding:
      self.caller.msg("You can't do that while you're hiding.")
      return

    if self.obj.access(self.caller, "traverse"):
      # we may traverse the exit.
      self.obj.at_traverse(self.caller, self.obj.destination)
    else:
      # exit is locked
      if self.obj.db.password and self.obj.db.password == self.raw_string:
        # we used the exit's password, so bypass the lock
        self.obj.at_traverse(self.caller, self.obj.destination)
      else:
        # failed to traverse the exit.
        if self.obj.db.err_traverse:
          # if exit has a better error message, let's use it.
          self.caller.msg(self.obj.db.err_traverse)
        else:
          # No shorthand error message. Call hook.
          self.obj.at_failed_traverse(self.caller)

  def get_extra_info(self, caller, **kwargs):
    """Shows a bit of information on where the exit leads.

    Args:
        caller (Object): The object (usually a character) that entered an ambiguous command.
        **kwargs (dict): Arbitrary, optional arguments for users
            overriding the call (unused by default).

    Returns:
        A string with identifying information to disambiguate the command, conventionally with a preceding space.
    """
    if self.obj.destination:
        return " (exit to %s)" % self.obj.destination.get_display_name(caller)
    else:
        return " (%s)" % self.obj.get_display_name(caller)  
