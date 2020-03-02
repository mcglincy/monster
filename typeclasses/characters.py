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

from gamerules.combat import character_death
from gamerules.health import MIN_HEALTH, health_msg
from gamerules.xp import MIN_XP, level_from_xp
from userdefined.models import CharacterClass


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
    self.set_field_defaults()

  def set_field_defaults(self):
    """Set various field defaults in an idempotent way."""
    # TODO: dragging in the CharacterClass model f's with evennia's
    # initial creation of god_character, so we can't refer to max_health(), 
    # max_mana(), etc in at_object_created() / set_field_defaults().
    if self.db.character_class_key is None:
      self.db.character_class_key = "ghost"
      self.ndb.character_class = None
    if self.db.xp is None:
      self.db.xp = 0
    if self.db.health is None:
      self.db.health = 1000
    if self.db.mana is None:
      self.db.mana = 0
    if self.db.brief_descriptions is None:
      self.db.brief_descriptions = False      
    # TODO: support various equipment slots
    # checking None to set None is pointless
    if self.db.gold_in_bank is None:
      self.db.gold_in_bank = 0

  def execute_cmd(self, raw_string, session=None, **kwargs):
    """Support execute_cmd(), like account and object."""
    return cmdhandler.cmdhandler(
        self, raw_string, callertype="account", session=session, **kwargs
    )

  # helper getters

  def character_class(self):
    if not self.ndb.character_class or self.ndb.character_class.key != self.db.character_class_key:
      self.ndb.character_class = CharacterClass.objects.get(db_key=self.db.character_class_key)
    return self.ndb.character_class

  def carried_gold_amount(self):
    gold = self.search("gold",
      candidates=self.contents, typeclass="typeclasses.objects.Gold", quiet=True)
    if len(gold) > 0:
      return gold[0].db.amount
    return 0

  def level(self):
    return level_from_xp(self.db.xp)

  def classname(self):
    return self.character_class().key

  def weapon_use(self):
    return (self.character_class().base_weapon_use + 
      self.character_class().level_weapon_use * self.level())

  def max_health(self):
    return (self.character_class().base_health +
      self.character_class().level_health * self.level())

  def max_mana(self):
    return (self.character_class().base_mana +
      self.character_class().level_mana * self.level())

  # TODO: level/base/total hide, steal, etc

  # at_* event notifications

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

  def at_damage(self, damage, damager=None):
    self.db.health = max(self.db.health - damage, MIN_HEALTH)
    self.msg(f"You take {damage} damage.")
    self.msg(health_msg("You", self.db.health))
    self.location.msg_contents(health_msg(self.key, self.db.health), exclude=[self])
    if self.db.health <= 0:
      character_death(self, damager)

  def at_heal(self, amount):
    self.db.health = min(self.db.health + amount, self.max_health())
    self.msg(health_msg("You", self.db.health))
    self.location.msg_contents(health_msg(self.key, self.db.health), exclude=[self])
