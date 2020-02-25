"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from random import randint
from evennia import DefaultCharacter, search_object
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
    # TODO: figure health etc from level and class
    self.db.max_health = 1000
    self.db.health = 1000
    self.db.brief_descriptions = False
    # TODO: support various equipment slots
    self.db.equipped_weapon = None
    self.db.equipped_armor = None


  def execute_cmd(self, raw_string, session=None, **kwargs):
    """Support execute_cmd(), like account and object."""
    return cmdhandler.cmdhandler(
        self, raw_string, callertype="account", session=session, **kwargs
    )

  def at_after_move(self, source_location, **kwargs):
    # override to apply our brief descriptions setting
    if self.location.access(self, "view"):
      self.msg(self.at_look(self.location, brief=self.db.brief_descriptions))

  def at_object_leave(self, obj, target_location):
    # called when an object leaves this object in any fashion
    super().at_object_leave(obj, target_location)
    # unequip if equipped
    if obj == self.db.equipped_armor:
      self.db.equipped_armor = None
    elif obj == self.db.equipped_weapon:
      self.db.equipped_weapon = None

  def at_weapon_hit(self, attacker, weapon, damage):
    self.msg(target_msg(attacker.key, weapon.key, damage))
    # TODO: apply armor
    armor = self.db.equipped_armor
    if armor:
      if armor.db.deflect_armor > 0 and randint(0, 100) < armor.db.deflect_armor:
        self.msg("The attack is deflected by your armor.")
        attacker.msg(f"Your weapon is deflected by {self.key}'s armor.")
        damage = int(damage / 2)
      if armor.db.base_armor > 0:
        self.msg("The attack is partially blocked by your armor.")
        attacker.msg(f"Your weapon is partially blocked by {self.key}'s armor.")
        damage = int(damage * ((100 - armor.db.base_armor) / 100))
    self.at_damage(damage)

  def at_damage(self, damage):
    self.db.health = max(self.db.health - damage, 0)
    self.msg(f"You take {damage} damage.")
    self.msg(self.self_health_msg())
    self.location.msg_contents(self.health_msg(), exclude=[self])
    if self.db.health <= 0:
      self.die()

  def at_heal(self, amount):
    self.db.health = min(self.db.health + amount, self.db.max_health)
    self.msg(self.self_health_msg())
    self.location.msg_contents(self.health_msg(), exclude=[self])

  def die(self):
    # drop everything we're holding
    for obj in self.contents:
      # TODO: possible destroy chance?
      self.execute_cmd(f"drop {obj.key}")

    # TODO: go to the actual void room
    the_void = search_object("Limbo")[0]
    if the_void:
      self.move_to(the_void)
    self.db.health = 200

  def health_msg(self):
    health = self.db.health
    if health >= 1700:
      return f"{self.key} is in ultimate health."
    elif health > 1400:
      return f"{self.key} is in incredible health."
    elif health > 1200:
      return f"{self.key} is in extraordinary health."
    elif health > 1000:
      return f"{self.key} is in tremendous health."
    elif health > 850:
      return f"{self.key} is in superior condition."
    elif health > 700:
      return f"{self.key} is in exceptional health."
    elif health > 500:
      return f"{self.key} is in good health."
    elif health > 350:
      return f"{self.key} looks a little bit dazed."
    elif health > 200:
      return f"{self.key} has some minor wounds."
    elif health > 100:
      return f"{self.key} is suffering from some serious wounds."
    elif health > 50:
      return f"{self.key} is in critical condition."
    elif health > 1:
      return f"{self.key} is near death."
    else:
      return f"{self.key} is dead."

  def self_health_msg(self):
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

