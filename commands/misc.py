import time
from commands.command import QueuedCommand
from evennia.commands import cmdhandler
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import utils


class CmdBrief(QueuedCommand):
  """Toggle brief descriptions."""
  key = "brief"
  aliases = ["bri", "brie"]
  locks = "cmd:all()"
  help_category = "Monster"

  def inner_func(self):
    if self.caller.db.brief_descriptions:
      self.caller.db.brief_descriptions = False
      self.caller.msg("Brief mode now off.")
    else:
      self.caller.db.brief_descriptions = True
      self.caller.msg("Brief mode now on.")


class CmdDot(QueuedCommand):
  """Repeat the last command."""
  key = "."
  locks = "cmd:all()"
  help_category = "Monster"

  def inner_func(self):
    last_command = self.caller.ndb.last_command
    if last_command:
      # self.caller.execute_cmd(last_command.raw_string)
      self.caller.msg(last_command.raw_string)
      cmdhandler.cmdhandler(self.session, last_command.raw_string)

  def at_post_cmd(self):
    # override to do nothing; we don't want dot as our last_command
    pass


"""
> who
                     Monster Status
                  26-FEB-1991  8:38pm
                  * - Monster Operator

Username   Game Name             Level     Class  Where
v112pfsd   Turin Deathstalker        7     Thief  royal passageway
v130qmty   Friendly Druid            1  HelDruid  void
v063j3h4   Magog                     1      Mage  the maze
v056mdht   sorry freeon it           2     Troll  northwest corner
v051lpqa  *opp'n along               9  GameMstr  the maze
v059nqal   Soulcatcher               3      Mage  the maze
v125qqna   Hanged Man                3     Mummy  bordering forest
v999rbqh   Freeon it                 1     Troll  east base of hill
v125qqml   Puzzeledfrog              1   Warrior  lothlorien shop
masproj1   King Kickass              1     Troll  necromancer street.
v108npa5   Mummy                     1     Troll  the maze
"""
class CmdWho(QueuedCommand):
  """list who is currently online"""
  key = "who"
  locks = "cmd:all()"
  help_category = "Monster"

  # this is used by the parent
  account_caller = True

  def inner_func(self):
    """Get all connected accounts by polling session."""
    account = self.account
    session_list = SESSIONS.get_sessions()
    session_list = sorted(session_list, key=lambda o: o.account.key)
    show_session_data = account.check_permstring("Developer") or account.check_permstring(
        "Admins"
    )
    naccounts = SESSIONS.account_count()
    if show_session_data:
      # privileged info
      table = self.styled_table(
          "|wAccount Name",
          "|wOn for",
          "|wIdle",
          "|wPuppeting",
          "|wLevel",
          "|wClass",
          "|wRoom",
          "|wCmds",
          "|wProtocol",
          "|wHost",
      )
      for session in session_list:
        if not session.logged_in:
            continue
        delta_cmd = time.time() - session.cmd_last_visible
        delta_conn = time.time() - session.conn_time
        account = session.get_account()
        puppet = session.get_puppet()
        location = puppet.location.key if puppet and puppet.location else "None"
        table.add_row(
          utils.crop(account.get_display_name(account), width=25),
          utils.time_format(delta_conn, 0),
          utils.time_format(delta_cmd, 1),
          utils.crop(puppet.get_display_name(account) if puppet else "None", width=25),
          puppet.level if hasattr(puppet, "level") else 0,
          puppet.classname if hasattr(puppet, "classname") else "None",
          utils.crop(location, width=25),
          session.cmd_total,
          session.protocol_key,
          isinstance(session.address, tuple) and session.address[0] or session.address,
        )
    else:
      # unprivileged
      table = self.styled_table(
        "|wUsername", 
        "|wGame Name", 
        "|wLevel", 
        "|wClass", 
        "|wWhere",
      )
      for session in session_list:
        if not session.logged_in:
            continue
        delta_cmd = time.time() - session.cmd_last_visible
        delta_conn = time.time() - session.conn_time
        account = session.get_account()
        puppet = session.get_puppet()        
        location = puppet.location.key if puppet and puppet.location else "None"
        table.add_row(
          utils.crop(account.get_display_name(account), width=25),
          utils.crop(puppet.get_display_name(account) if puppet else "None", width=25),
          puppet.level if hasattr(puppet, "level") else 0,
          puppet.classname if hasattr(puppet, "classname") else "None",
          utils.crop(location, width=25),            
      )
    self.msg(
      "|w                     Monster Status\n                  26-FEB-1991  8:38pm\n                  * - Monster Operator|n\n%s"
      % table
    )
