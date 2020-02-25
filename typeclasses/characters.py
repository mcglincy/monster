"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from evennia.commands import cmdhandler
from commands.combat import target_msg


class Character(DefaultCharacter):
  """
  The Character defaults to reimplementing some of base Object's hook methods with the
  following functionality:

  at_basetype_setup - always assigns the DefaultCmdSet to this object type
                (important!)sets locks so character cannot be picked up
                and its commands only be called by itself, not anyone else.
                (to change things, use at_object_creation() instead).
  at_after_move(source_location) - Launches the "look" command after every move.
  at_post_unpuppet(account) -  when Account disconnects from the Character, we
                store the current location in the pre_logout_location Attribute and
                move it to a None-location so the "unpuppeted" character
                object does not need to stay on grid. Echoes "Account has disconnected"
                to the room.
  at_pre_puppet - Just before Account re-connects, retrieves the character's
                pre_logout_location Attribute and move it back on the grid.
  at_post_puppet - Echoes "AccountName has entered the game" to the room.

  """
  def at_object_creation(self):
    """Called at initial creation."""
    super().at_object_creation()
    self.db.health = 1000
    self.db.brief_descriptions = False

  def execute_cmd(self, raw_string, session=None, **kwargs):
    """Support execute_cmd(), like account and object."""
    return cmdhandler.cmdhandler(
        self, raw_string, callertype="account", session=session, **kwargs
    )

  def at_after_move(self, source_location, **kwargs):
    if self.location.access(self, "view"):
      self.msg(self.at_look(self.location, brief=self.db.brief_descriptions))

  def at_weapon_hit(self, attacker, weapon, damage):
    self.msg(target_msg(attacker.key, weapon.key, damage))
    # TODO: apply armor
    new_health = self.db.health - damage
    if new_health <= 0:
      # death
      self.db.health = 0
    else:
      self.db.health = new_health
    self.msg(self_health_msg)

    if self.db.health <= 0:
      # TODO: go to the void
      pass

  def self_health_msg(self, health):
    health = self.db.health
    if health >= 1700:
      return "You are in ultimate health."
    elif health > 1400:
      return "You are in incredible health."
    elif health > 1200:
      return "You are in extraordinary health."
    elif health > 1000:
      return "You are in tremendous health."
    elif health > 850:
      return "You are in superior condition."
    elif health > 700:
      return "You are in exceptional health."
    elif health > 500:
      return "You are in good health."
    elif health > 350:
      return "You feel a little bit dazed."
    elif health > 200:
      return "You have some minor cuts and abrasions."
    elif health > 100:
      return "You are suffering from some serious wounds."
    elif health > 50:
      return "You are in critical condition."
    elif health > 1:
      return "You are near death."
    else:
      return "You are dead."
