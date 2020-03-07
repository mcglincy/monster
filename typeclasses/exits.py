"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia import DefaultExit
from commands.movement import CmdExit
from gamerules.exit_effects import apply_exit_effect
from typeclasses.exit_kind import ExitKind



class Exit(DefaultExit):
  """
  Exits are connectors between rooms. Exits are normal Objects except
  they defines the `destination` property. It also does work in the
  following methods:

   basetype_setup() - sets default exit locks (to change, use `at_object_creation` instead).
   at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
                            rebuild the Exit cmdset along with a command matching the name
                            of the Exit object. Conventionally, a kwarg `force_init`
                            should force a rebuild of the cmdset, this is triggered
                            by the `@alias` command when aliases are changed.
   at_failed_traverse() - gives a default error message ("You cannot
                          go there") if exit traversal fails and an
                          attribute `err_traverse` is not defined.

  Relevant hooks to overload (compared to other types of Objects):
      at_traverse(traveller, target_loc) - called to do the actual traversal and calling of the other hooks.
                                          If overloading this, consider using super() to use the default
                                          movement implementation (and hook-calling).
      at_after_traverse(traveller, source_loc) - called by at_traverse just after traversing.
      at_failed_traverse(traveller) - called by at_traverse if traversal failed for some reason. Will
                                      not be called if the attribute `err_traverse` is
                                      defined, in which case that will simply be echoed.
  """
  # use our own exit command, to track last command for '.'
  exit_command = CmdExit

  def at_object_creation(self):
    super().at_object_creation()
    self.db.exit_kind = ExitKind.OPEN
    self.db.exit_desc = None
    self.db.exit_effect_kind = None
    self.db.exit_effect_value = None
    # do these msgs exist for DefaultExit already? vvvv
    self.db.fail_message = None
    self.db.success_message = None
    # alias + req_alias = passworded door, no NSEWUD link
    # goin/come_out fields are always 32000 (default msg) in the JSON
    # hidden is always 0 in the JSON
    # do we care about auto_look?

  def at_after_traverse(self, traversing_object, source_location, **kwargs):
    if self.db.success_message:
      traversing_object.msg(self.db.success_message)
    if self.db.exit_effect_kind:
      apply_exit_effect(traversing_object, self.db.exit_effect_kind, self.db.exit_effect_value)

  def at_failed_traverse(self, traversing_object, **kwargs):
    # TODO: instead of overriding at_failed_traverse we could also just 
    # set err_traverse and let superclass send that
    if self.db.fail_message:
      traversing_object.msg(self.db.fail_message)

  def get_display_name(self, looker, **kwargs):
    if self.db.exit_desc:
      return self.db.exit_desc
    elif self.name in ["north", "south", "east", "west"]:
      return f"To the {self.name} is {self.destination.key}."
    elif self.name in ["up", "down"]:
      return f"The {self.destination.key} is {self.name} from here."
  
    if self.locks.check_lockstring(looker, "perm(Builder)"):
      return "{}(#{})".format(self.name, self.id)
    return self.name
