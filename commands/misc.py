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

"""
> she
--------------- Character Sheet ------------------
Name        :King Kickass
Class       :Troll
Size        :      9'
Exp/level   :   1630/1
Health/Max  :   2638/2638
Move delay  :     38/100 seconds
Attack delay:    280/100 seconds
Weapon usage:    100%
Poison chnce:      5%
Move silent :     10%
Armor       :     20%
Total Kills :      3
Money       :     44
Money in Bank:      70
Weapon      :claws 250/395
--------------------------------------------------
"""
class CmdSheet(Command):
  """Show character sheet."""
  key = "sheet"
  aliases = ["she", "shee"]
  locks = "cmd:all()"
  help_category = "Monster"

  def func(self):
    account = self.account

    # table = self.styled_table(
    #   "|wStat",
    #   "|wValue",
    # )
    table = self.styled_table(
      "|wCharacter Sheet",
    )
#    utils.crop(account.get_display_name(account), width=25),
    # table.add_row("Name", utils.crop(account.get_display_name(account), width=25))
    # table.add_row("Class", "Peasant")
    # table.add_row("Size", "6'")
    # table.add_row("Exp/evel", "0/1")
    # table.add_row("Health/Max", "")
    # table.add_row("Move delay", "0")
    # table.add_row("Attack delay", "0")
    # table.add_row("Weapon usage", "100%")
    # table.add_row("Poison chnce", "0%")
    # table.add_row("Move silent", "0%")
    # table.add_row("Armor", "0/0/0")
    # table.add_row("Total Kills", "0")
    # table.add_row("Money", "0")
    # table.add_row("Money in Bank", "0")
    # table.add_row("Weapon", "???")
    table.add_row(f"Name         : {utils.crop(account.get_display_name(account), width=25)}")
    table.add_row(f"Class        : Peasant")
    table.add_row(f"Size         : 6'")
    table.add_row(f"Exp/level    : 0/1")
    table.add_row(f"Health/Max   : {int(account.character.db.health)}/{int(account.character.db.max_health)}")
    table.add_row(f"Move delay   : 0")
    table.add_row(f"Attack delay : 0")
    table.add_row(f"Weapon usage : 100%")
    table.add_row(f"Poison chnce : 0%")
    table.add_row(f"Move silent  : 0%")
    base_armor = 0
    deflect_armor = 0
    spell_armor = 0
    armor = account.character.db.equipped_armor
    if armor:
      base_armor = armor.db.base_armor
      deflect_armor = armor.db.deflect_armor
      spell_armor = armor.db.spell_armor
    table.add_row(f"Armor        : {base_armor}/{deflect_armor}/{spell_armor}")
    table.add_row(f"Total Kills  : 0")
    table.add_row(f"Money        : 0")
    table.add_row(f"Money in Bank: 0")
    base_damage = 0
    random_damage = 0
    weapon = account.character.db.equipped_weapon
    if weapon:
      base_damage = weapon.db.base_damage
      random_damage = weapon.db.random_damage
    table.add_row(f"Weapon       : {base_damage}/{random_damage}")
    self.msg("%s" % table)


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
          "1",
          "Peasant",
          utils.crop(location, width=25),            
      )
    self.msg(
      "|w                     Monster Status\n                  26-FEB-1991  8:38pm\n                  * - Monster Operator|n\n%s"
      % table
    )
