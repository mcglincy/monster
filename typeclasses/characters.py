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
from typeclasses.alignment import Alignment
from typeclasses.equipment_slot import EquipmentSlot
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
    if self.db.equipment is None:
      # dict of {EquipmentSlot:object}
      self.db.equipment = {}

  def execute_cmd(self, raw_string, session=None, **kwargs):
    """Support execute_cmd(), like account and object."""
    return cmdhandler.cmdhandler(
        self, raw_string, callertype="account", session=session, **kwargs
    )

  def announce_move_from(self, destination, msg=None, mapping=None, **kwargs):
    """Override superclass to support custom exit messaging.

    Called if the move is to be announced. This is
    called while we are still standing in the old
    location.

    Args:
        destination (Object): The place we are going to.
        msg (str, optional): a replacement message.
        mapping (dict, optional): additional mapping objects.
        **kwargs (dict): Arbitrary, optional arguments for users
            overriding the call (unused by default).

    You can override this method and call its parent with a
    message to simply change the default message.  In the string,
    you can use the following as mappings (between braces):
        object: the object which is moving.
        exit: the exit from which the object is moving (if found).
        origin: the location of the object before the move.
        destination: the location of the object after moving.
    """
    if not self.location:
      return
    success_msg = kwargs.get("success_msg")
    go_in_msg = kwargs.get("go_in_msg")
    location = self.location
    exits = [
      o for o in location.contents if o.location is location and o.destination is destination
    ]
    if msg:
      string = msg
    elif go_in_msg:
      # msgs may have a '#' placeholder
      string = go_in_msg.replace("#", self.key)
    else:
      if exits:
        string = f"{self.key} has gone {exits[0].key}."
      else:
        # Evennia default:
        string = "{object} is leaving {origin}, heading for {destination}."        
    if not mapping:
      mapping = {}
    mapping.update({
      "object": self,
      "exit": exits[0] if exits else "somewhere",
      "origin": location or "nowhere",
      "destination": destination or "nowhere",
    })
    location.msg_contents(string, exclude=(self,), mapping=mapping)
    if success_msg:
      self.msg(success_msg)

  def announce_move_to(self, source_location, msg=None, mapping=None, **kwargs):
    """Override superclass to support custom exit messaging.
    Called after the move if the move was not quiet. At this point
    we are standing in the new location.

    Args:
        source_location (Object): The place we came from
        msg (str, optional): the replacement message if location.
        mapping (dict, optional): additional mapping objects.
        **kwargs (dict): Arbitrary, optional arguments for users
            overriding the call (unused by default).

    Notes:
        You can override this method and call its parent with a
        message to simply change the default message.  In the string,
        you can use the following as mappings (between braces):
            object: the object which is moving.
            exit: the exit from which the object is moving (if found).
            origin: the location of the object before the move.
            destination: the location of the object after moving.

    """
    origin = source_location
    destination = self.location
    exits = []
    if origin:
      exits = [
        o for o in destination.contents if o.location is destination and o.destination is origin
      ]
    if source_location:
      come_out_msg = kwargs.get("come_out_msg")
      if msg:
        string = msg
      elif come_out_msg:
        # msgs may have a '#' placeholder
        string = come_out_msg.replace("#", self.key)
      else:
        if exits:
          string = f"{self.key} has come into the room from: {exits[0].key}"
        else:
          # Evennia default
          string = "{object} arrives to {destination} from {origin}."
    else:
      string = "{object} arrives to {destination}."
    if not mapping:
      mapping = {}
    mapping.update({
      "object": self,
      "exit": exits[0] if exits else "somewhere",
      "origin": origin or "nowhere",
      "destination": destination or "nowhere",
    })
    destination.msg_contents(string, exclude=(self,), mapping=mapping)


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

  def size(self):
    return self.character_class().size

  def alignment(self):
    try:
      alignment = Alignment(self.character_class().alignment)
    except ValueError:
      # handle non-33/66/99 values for classes, just in case
      alignment = Alignment.NEUTRAL
    return alignment

  def max_health(self):
    return (self.character_class().base_health +
      self.character_class().level_health * self.level())

  def max_mana(self):
    return (self.character_class().base_mana +
      self.character_class().level_mana * self.level())

  # our damage, armor, etc is the sum of our equipped objects

  def base_weapon_damage(self):
    return sum(o.db.base_weapon_damage for o in self.db.equipment.values())

  # note: there is no level_weapon_damage stat or effect

  def random_weapon_damage(self):
    return sum(o.db.random_weapon_damage for o in self.db.equipment.values())

  def base_weapon_use(self):
    class_use = self.character_class().base_weapon_use
    item_use = sum(o.db.base_weapon_use for o in self.db.equipment.values())
    return class_use + item_use

  def level_weapon_use(self):
    class_use = self.character_class().level_weapon_use
    item_use = sum(o.db.level_weapon_use for o in self.db.equipment.values())
    return class_use + item_use

  def total_weapon_use(self):
    return self.base_weapon_use() + self.level_weapon_use() * self.level()

  def base_armor(self):
    class_armor = self.character_class().armor
    item_armor = sum(o.db.base_armor for o in self.db.equipment.values())
    return class_armor + item_armor

  def deflect_armor(self):
    # note that CharacterClasses do NOT have deflect_armor
    return sum(o.db.deflect_armor for o in self.db.equipment.values())

  def spell_armor(self):
    class_armor = self.character_class().spell_armor
    item_armor = sum(o.db.spell_armor for o in self.db.equipment.values())
    return class_armor + item_armor

  def spell_deflect_armor(self):
    # note that CharacterClasses do NOT have spell_deflect_armor
    return sum(o.db.spell_deflect_armor for o in self.db.equipment.values())

  def base_claw_damage(self):
    class_dmg = self.character_class().base_claw_damage
    item_dmg = sum(o.db.base_claw_damage for o in self.db.equipment.values())
    return class_dmg + item_dmg

  def level_claw_damage(self):
    class_dmg = self.character_class().level_claw_damage
    item_dmg = sum(o.db.level_claw_damage for o in self.db.equipment.values())
    return class_dmg + item_dmg

  def total_claw_damage(self):
    return self.base_claw_damage() + self.level_claw_damage() * self.level()

  def random_claw_damage(self):
    class_dmg = self.character_class().random_claw_damage
    item_dmg = sum(o.db.random_claw_damage for o in self.db.equipment.values())
    return class_dmg + item_dmg

  # TODO: level/base/total hide, steal, etc

  # TODO: move equipment stuff to gamerules, or keep it OOP?

  def equipped_weapon(self):
    # TODO: should claw classes be able to equip anything in TWO_HAND/SWORD_HAND?
    if EquipmentSlot.TWO_HAND in self.db.equipment:
      return self.db.equipment[EquipmentSlot.TWO_HAND]
    if EquipmentSlot.SWORD_HAND in self.db.equipment:
      return self.db.equipment[EquipmentSlot.SWORD_HAND]
    # TODO: does SHIELD_HAND count?
    # TODO: handle claws
    return None

  def has_claws(self):
    # TODO: should an item be able to give you claws?
    clazz = self.character_class()
    return (clazz.base_claw_damage or clazz.level_claw_damage or clazz.random_claw_damage)

  def equip(self, obj):
    if not obj.is_typeclass("typeclasses.objects.Equipment"):
      return
    slot = obj.db.equipment_slot
    if (slot == EquipmentSlot.SWORD_HAND 
      or slot == EquipmentSlot.SHIELD_HAND):
      self.db.equipment.pop(EquipmentSlot.TWO_HAND, None)
    elif slot == EquipmentSlot.TWO_HAND:
      self.db.equipment.pop(EquipmentSlot.SWORD_HAND, None)
      self.db.equipment.pop(EquipmentSlot.SHIELD_HAND, None)
    self.db.equipment[slot] = obj
    self.msg(f"You equip the {obj.key} to {slot.name.upper()}.")

  def unequip(self, obj):
    if not obj.is_typeclass("typeclasses.objects.Equipment"):
      return
    slot = obj.db.equipment_slot      
    if slot in self.db.equipment:
      del self.db.equipment[slot]
      self.msg(f"You unequip the {obj.key}.")
    else:
      self.msg("Not currently equipped.")

  # at_* event notifications

  def at_after_move(self, source_location, **kwargs):
    # override to apply our brief descriptions setting
    if self.location.access(self, "view"):
      self.msg(self.at_look(self.location, brief=self.db.brief_descriptions))

  def at_object_leave(self, obj, target_location):
    # called when an object leaves this object in any fashion
    #super().at_object_leave(obj, target_location)
    # unequip if equipped
    if self.db.equipment.get(obj.db.equipment_slot) == obj:
      self.msg("Unequipping")
      del self.db.equipment[obj.db.equipment_slot]

  def at_damage(self, damage, damager=None):
    damage = max(0, damage)
    self.db.health = max(self.db.health - damage, MIN_HEALTH)
    self.msg(f"You take {damage} damage.")
    self.msg(health_msg("You", self.db.health))
    self.location.msg_contents(health_msg(self.key, self.db.health), exclude=[self])
    if self.db.health <= 0:
      character_death(self, damager)

  def at_heal(self, amount):
    amount = max(0, amount)
    self.db.health = min(self.db.health + amount, self.max_health())
    self.msg(health_msg("You", self.db.health))
    self.location.msg_contents(health_msg(self.key, self.db.health), exclude=[self])
