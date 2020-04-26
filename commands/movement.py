from commands.command import Command, QueuedCommand
from gamerules.exit_kind import ExitKind
from gamerules.find import find_first

# see also evennia commands.py ExitCommand
class CmdExit(QueuedCommand):
  """Re-implement CmdExit so it's a dot-repeatable command."""  
  obj = None

  def check_preconditions(self):
    if self.caller.is_hiding:
      self.caller.msg("You can't do that while you're hiding.")
      return False

  def pre_freeze(self):
    # TODO: exit fail should be only move_speed / 400
    return self.caller.move_speed / 100.0

  def inner_func(self):
    ok_to_traverse = False
    if self.obj.access(self.caller, "traverse"):
      # we satisfy any locks on the exit
      ok_to_traverse = True
    elif self.obj.db.password and self.obj.db.password.lower() == self.raw_string.lower():
      # we used the locked exit's password (case-insensitive)
      # TODO: maybe we should convert OPEN + alias_required to PASSWORDED?
      if (self.obj.db.exit_kind == ExitKind.OPEN 
        or self.obj.db.exit_kind == ExitKind.PASSWORDED):
        # passworded only
        ok_to_traverse = True
      elif ((self.obj.db.exit_kind == ExitKind.OBJECT_REQUIRED
       or self.obj.db.exit_kind == ExitKind.ONLY_EXISTS_WITH_OBJECT)
        and find_first(self.caller, self.obj.db.required_object)):
        # passworded and we have the required object
        ok_to_traverse = True
      elif (self.obj.db.exit_kind == ExitKind.OBJECT_FORBIDDEN and 
        not find_first(self.caller, self.obj.db.required_object)):
        # passworded and we don't have the forbidden object
        ok_to_traverse = True

    if ok_to_traverse:
      self.obj.at_traverse(self.caller, self.obj.destination)
    else:
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
