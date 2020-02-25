import time
from commands.command import Command
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import utils


class CmdBrief(Command):
  """Toggle brief descriptions."""
  key = "brief"
  aliases = ["bri", "brie"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    if self.caller.db.brief_descriptions:
      self.caller.db.brief_descriptions = False
      self.caller.msg("Brief mode now off.")
    else:
      self.caller.db.brief_descriptions = True
      self.caller.msg("Brief mode now on.")


class CmdDot(Command):
  """Repeat the last command."""
  key = "."
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    last_command = self.caller.ndb.last_command
    if last_command:
      self.caller.execute_cmd(last_command.raw_string)

  def at_post_cmd(self):
    # override to do nothing; we don't want dot as our last_command
    pass


class CmdSheet(Command):
  """Show character sheet."""
  key = "sheet"
  aliases = ["she", "shee"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    self.not_implemented_yet()


class CmdWho(Command):
  """list who is currently online"""

  key = "who"
  locks = "cmd:all()"

  # this is used by the parent
  account_caller = True

  def func(self):
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
          utils.crop(location, width=25),
          session.cmd_total,
          session.protocol_key,
          isinstance(session.address, tuple) and session.address[0] or session.address,
        )
    else:
      # unprivileged
      table = self.styled_table(
        "|wAccount name", 
        "|wOn for", 
        "|wIdle",
        "|wRoom",
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
          utils.crop(location, width=25),            
      )
    is_one = naccounts == 1
    self.msg(
      "|wAccounts:|n\n%s\n%s unique account%s logged in."
      % (table, "One" if is_one else naccounts, "" if is_one else "s")
    )
