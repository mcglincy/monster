from commands.command import QueuedCommand


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
    caller = self.caller
    if not self.args:
      caller.msg("Drop what?")
      return

    # Because the DROP command by definition looks for items
    # in inventory, call the search function using location = caller
    obj = caller.search(
      self.args,
      location=caller,
      nofound_string="You aren't carrying %s." % self.args,
      multimatch_string="You carry more than one %s:" % self.args,
    )
    if not obj:
      return

    # Call the object script's at_before_drop() method.
    if not obj.at_before_drop(caller):
      return

    obj.move_to(caller.location, quiet=True)
    caller.msg("You drop %s." % (obj.name,))
    caller.location.msg_contents("%s drops %s." % (caller.name, obj.name), exclude=caller)
    # Call the object script's at_drop() method.
    obj.at_drop(caller)



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
    caller = self.caller
    if not self.args:
      caller.msg("Get what?")
      return
    obj = caller.search(self.args, location=caller.location)
    if not obj:
      return
    if caller == obj:
      caller.msg("You can't get yourself.")
      return
    if not obj.access(caller, "get"):
      if obj.db.get_err_msg:
          caller.msg(obj.db.get_err_msg)
      else:
          caller.msg("You can't get that.")
      return

    # calling at_before_get hook method
    if not obj.at_before_get(caller):
      return

    obj.move_to(caller, quiet=True)
    caller.msg("You pick up %s." % obj.name)
    caller.location.msg_contents("%s picks up %s." % (caller.name, obj.name), exclude=caller)
    # calling at_get hook method
    obj.at_get(caller)


class CmdInventory(QueuedCommand):
  """View inventory."""
  key = "inventory"
  aliases = ["i", "inv", "inve", "inven", "invent", "invento", "inventor"]
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





