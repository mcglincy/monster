from commands.command import QueuedCommand
from gamerules.special_room_kind import SpecialRoomKind
from gamerules.find import find_first, find_first_unhidden


class CmdDrop(QueuedCommand):
  """Drop something.

  Usage:
    drop <obj>
  """
  key = "drop"
  locks = "cmd:all()"
  arg_regex = r"\s|$"
  help_category = "Monster"

  def inner_func(self):
    if not self.args:
      self.caller.msg("Drop what?")
      return
    key = self.args.strip()
    obj = find_first(self.caller, key)
    if not obj:
      self.caller.msg(f"You aren't carrying {key}.")
      return
    # before the drop
    if not obj.at_before_drop(self.caller):
      return
    # do the drop
    obj.move_to(self.caller.location, quiet=True)
    self.caller.msg(f"You drop {obj.name}.")
    self.caller.location.msg_contents(
      f"{self.caller.name} drops {obj.name}.", exclude=self.caller)
    # after the drop
    obj.at_drop(self.caller)



class CmdExpress(QueuedCommand):
  """Express a pose.

  Usage:
    express <pose text>
    express's <pose text>

  Example:
    pose is standing by the wall, smiling.
     -> others will see:
    Tom is standing by the wall, smiling.
  """
  key = "express"
  aliases = ["exp", "expr", "expre", "expres"]
  locks = "cmd:all()"
  help_category = "Monster"

  def parse(self):
    """
    Custom parse the cases where the emote
    starts with some special letter, such
    as 's, at which we don't want to separate
    the caller's name and the emote with a
    space.
    """
    args = self.args
    if args and not args[0] in ["'", ",", ":"]:
      args = " %s" % args.strip()
    self.args = args

  def inner_func(self):
    if not self.args:
      msg = "What do you want to do?"
      self.caller.msg(msg)
    else:
      msg = "%s%s" % (self.caller.name, self.args)
      self.caller.location.msg_contents(text=(msg, {"type": "pose"}), from_obj=self.caller)


class CmdGet(QueuedCommand):
  """Pick up something.

    Usage:
      get <obj>
    """
  key = "get"
  aliases = "grab"
  locks = "cmd:all()"
  arg_regex = r"\s|$"
  help_category = "Monster"

  def inner_func(self):
    if not self.args:
      self.caller.msg("Get what?")
      return
    key = self.args.strip()
    obj = find_first_unhidden(self.caller.location, key)
    if not obj:
      self.caller.msg(f"You can't find {key}.")
      return
    if self.caller == obj:
      self.caller.msg("You can't get yourself.")
      return
    if not obj.access(self.caller, "get"):
      if obj.db.get_err_msg:
        self.caller.msg(obj.db.get_err_msg)
      else:
        self.caller.msg("You can't get that.")
      return
    # before the get
    if not obj.at_before_get(self.caller):
      return
    # do the get
    obj.move_to(self.caller, quiet=True)
    self.caller.msg("You pick up %s." % obj.name)
    self.caller.location.msg_contents(
      f"{self.caller.name} picks up {obj.name}.", exclude=self.caller)
    # after the get
    obj.at_get(self.caller)


class CmdInventory(QueuedCommand):
  """View inventory."""
  key = "inventory"
  aliases = ["i", "in", "inv", "inve", "inven", "invent", "invento", "inventor"]
  locks = "cmd:all()"
  arg_regex = r"$"
  help_category = "Monster"

  def inner_func(self):
    items = self.caller.contents
    if not items:
      string = "You are not carrying anything."
    else:
      table = self.styled_table(border="header")
      for item in items:
        table.add_row("|C%s|n" % item.name, item.db.desc or "")
      string = "|wYou are carrying:\n%s" % table
    self.caller.msg(string)


class CmdLook(QueuedCommand):
  """Look at location or object.

  Usage:
    look
    look <obj>
    look *<account>
  """
  key = "look"
  aliases = ["l", "ls", "loo"]
  locks = "cmd:all()"
  arg_regex = r"\s|$"
  help_category = "Monster"

  def inner_func(self):
    """Handle the looking."""
    # OG Monster implementation was:
    # 1) LookDetail
    # 2) LookPerson
    # 3) DoExamine
    if not self.args:
      target = self.caller.location
      if not target:
        self.caller.msg("You have no location to look at!")
        return
    else:
      key = self.args.strip().lower()

      # see if we specified a room detail
      if self.caller.location and key in self.caller.location.db.details:
        self.caller.msg(self.caller.location.db.details[key])
        return

      # note that our look targeting works slightly differently from Evennia look - 
      # we don't include character contents.

      target = find_first_unhidden(self.caller.location, key)
      if not target:
        self.caller.msg(f"You can't find {key}.")
        return
    self.msg((self.caller.at_look(target), {"type": "look"}), options=None)

# BEGIN
#   Writeln;
#   Writeln('Exits             Lists exits you can inspect here');
#   Writeln('Details           Show details you can look at in this room');
#   Writeln('Experience (*)    Check players experience');
#   Writeln('Class      (*)    Check players class');
#   Writeln('Room              Check room slots');
#   Writeln('Hold              Check what I am holding.');
#   Writeln('Randoms           Check to see what types of randoms exist.');
#   Writeln('* - currently not available');
#   Writeln;
# END;


class CmdShow(QueuedCommand):
  key = "show"
  aliases = ["show"]
  locks = "cmd:all()"
  help_category = "Monster"

  # OG monster had:
  # ('exits', 'details', 'experience', 'class', 'room', 'hold', 'randoms');
  # Unclear if we need anything beyond details, given Evennia's examine command.
  show_commands = ["details"]

  def check_preconditions(self):
    if not self.args or not self.args.strip().lower() in self.show_commands:
      self.caller.msg(f"Show what? ({', '.join(self.show_commands)})")
      return False

  def inner_func(self):
    show_what = self.args.strip().lower()
    if show_what == self.show_commands[0]:
      self.show_details()
    # TODO: implement other show handling, if needed

  def show_details(self):
    if self.caller.location.db.details:
      msg = "Details here that you may inspect:\n"
      for key in self.caller.location.db.details.keys():
        msg += f"    {key}\n"
      self.caller.msg(msg)
    else:
      self.caller.msg("There are no details of this room that you can inspect.")

