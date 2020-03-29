"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
import time
from collections import deque
from random import randint

from evennia import DefaultCharacter, search_object, TICKER_HANDLER
from evennia.commands import cmdhandler

from gamerules.alignment import Alignment
from gamerules.combat import character_death
from gamerules.comms import msg_global
from gamerules.equipment_slot import EquipmentSlot
from gamerules.health import MIN_HEALTH, health_msg, add_health_ticker
from gamerules.mana import MIN_MANA, add_mana_ticker
from gamerules.mobs import add_mob_generator_ticker
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
    self.ndb.active_command = None
    self.ndb.command_queue = deque()
    self.ndb.frozen_until = 0
    self.ndb.hiding = 0
    self.ndb.poisoned = False
    self.ndb.resting = False
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
    self.db.health_ticker_key = None
    self.db.mana_ticker_key = None
    self.db.mob_generator_ticker_key = None
  
  def at_init(self):
    self.ndb.active_command = None
    self.ndb.command_queue = deque()
    self.ndb.frozen_until = 0
    self.ndb.hiding = 0
    self.ndb.poisoned = False
    self.ndb.resting = False
    # TODO: verify whether this should be in at_object_creation()
    add_health_ticker(self)
    add_mana_ticker(self)
    add_mob_generator_ticker(self)

  def at_post_puppet(self, **kwargs):
    super().at_post_puppet(**kwargs)
    msg_global(f"({self.name} once again roams the land.)")
    # TODO: add date, maybe replace super() call
    # "Welcome back, King Kickass.  Your last play was on 24-FEB-1991 at 3:35pm.
    self.msg(f"Welcome back, {self.name}.")

  def at_post_unpuppet(self, account, session=None, **kwargs):
    super().at_post_unpuppet(account, session, **kwargs)
    msg_global(f"({self.name} has returned to sleep.)")

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
      string = go_in_msg.replace("#", self.name)
    else:
      if exits:
        string = f"{self.name} has gone {exits[0].key}."
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
        string = come_out_msg.replace("#", self.name)
      else:
        if exits:
          string = f"{self.name} has come into the room from: {exits[0].key}"
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

  @property
  def character_class(self):
    if not self.ndb.character_class or self.ndb.character_class.key != self.db.character_class_key:
      self.ndb.character_class = CharacterClass.objects.get(db_key=self.db.character_class_key)
    return self.ndb.character_class

  @property
  def carried_gold_amount(self):
    gold = self.search("gold",
      candidates=self.contents, typeclass="typeclasses.objects.Gold", quiet=True)
    if len(gold) > 0:
      return gold[0].db.amount
    return 0

  @property
  def level(self):
    return level_from_xp(self.db.xp)

  @property
  def classname(self):
    return self.character_class.key

  @property
  def size(self):
    return self.character_class.size

  @property
  def alignment(self):
    try:
      alignment = Alignment(self.character_class.alignment)
    except ValueError:
      # handle non-33/66/99 values for classes, just in case
      alignment = Alignment.NEUTRAL
    return alignment

  @property
  def max_health(self):
    return self.base_plus_level_attr("base_health", "level_health")

  @property
  def max_mana(self):
    return self.base_plus_level_attr("base_mana", "level_mana")

  @property
  def is_frozen(self):
    now = time.time()
    return self.ndb.frozen_until > now

  @property
  def is_hiding(self):
    return self.ndb.hiding > 0

  @property
  def is_poisoned(self):
    return self.ndb.poisoned

  @property
  def is_resting(self):
    return self.ndb.resting

  @property
  def attack_speed(self):
    return self.class_plus_equipped_attr("attack_speed")

  @property
  def move_speed(self):
    # TODO: consider equipment weight?
    return self.class_plus_equipped_attr("move_speed")

  @property
  def heal_speed(self):
    val = self.class_plus_equipped_attr("heal_speed")
    if self.is_resting:
      return 2 * val
    else:
      return val

  # our damage, armor, etc is the sum of our equipped objects

  def base_plus_level_attr(self, base_attr_name, level_attr_name):
    clazz = self.character_class
    base_val = getattr(clazz, base_attr_name)
    level_val = getattr(clazz, level_attr_name)
    return base_val + level_val * self.level

  def equipped_attr(self, attr_name):
    # TODO: there may be None values in the dict post-dequip
    equipped = filter(None, self.db.equipment.values())
    # TODO: we need to consider equipment condition... condition/100 * val
    # AttackSpeed := AttackSpeed + ROUND(AllStats.MyHold.Condition[OSlot] / 100 *
    #            ( LookupEffect(Obj, EF_AttackSpeed)));
    return sum(getattr(e.db, attr_name) for e in equipped)

  def class_plus_equipped_attr(self, attr_name):
    class_val = getattr(self.character_class, attr_name)
    equipped_val = self.equipped_attr(attr_name)
    return class_val + equipped_val

  @property
  def base_weapon_damage(self):
    return self.equipped_attr("base_weapon_damage")

  # note: there is no level_weapon_damage stat or effect

  @property
  def random_weapon_damage(self):
    return self.equipped_attr("random_weapon_damage")

  @property
  def base_weapon_use(self):
    return self.class_plus_equipped_attr("base_weapon_use")

  @property
  def level_weapon_use(self):
    return self.class_plus_equipped_attr("level_weapon_use")

  @property
  def total_weapon_use(self):
    return self.base_plus_level_attr("base_weapon_use", "level_weapon_use")

  @property
  def base_armor(self):
    # TODO: ivars are named differently :P
    class_armor = self.character_class.armor
    equipped = filter(None, self.db.equipment.values())
    item_armor = sum(o.db.base_armor for o in equipped)
    return class_armor + item_armor

  @property
  def deflect_armor(self):
    # note that CharacterClasses do NOT have deflect_armor
    return self.equipped_attr("deflect_armor")

  @property
  def spell_armor(self):
    return self.class_plus_equipped_attr("spell_armor")

  @property
  def spell_deflect_armor(self):
    # note that CharacterClasses do NOT have spell_deflect_armor
    return self.equipped_attr("spell_deflect_armor")

  @property
  def base_claw_damage(self):
    return self.class_plus_equipped_attr("base_claw_damage")

  @property
  def level_claw_damage(self):
    return self.class_plus_equipped_attr("level_claw_damage")

  @property
  def total_claw_damage(self):
    return self.base_plus_level_attr("base_claw_damage", "level_claw_damage")

  @property
  def random_claw_damage(self):
    return self.class_plus_equipped_attr("random_claw_damage")

  @property
  def shadow_damage_percent(self):
    return self.character_class.shadow_damage_percent

  @property
  def base_move_silent(self):
    return self.class_plus_equipped_attr("base_move_silent")

  @property
  def level_move_silent(self):
    return self.class_plus_equipped_attr("level_move_silent")

  @property
  def total_move_silent(self):
    return self.base_plus_level_attr("base_move_silent", "level_move_silent")

  @property
  def base_steal(self):
    return self.class_plus_equipped_attr("base_steal")

  @property
  def level_steal(self):
    return self.class_plus_equipped_attr("level_steal")

  @property
  def total_steal(self):
    return self.base_plus_level_attr("base_steal", "level_steal")

  @property
  def poison_chance(self):
    # TODO: rename equipment effect kind to POISON_CHANCE?
    return (self.character_class.poison_chance
      + self.equipped_attr("poison"))
  
  # TODO: move equipment stuff to gamerules, or keep it OOP?

  @property
  def has_claws(self):
    # TODO: should an item be able to give you claws?
    clazz = self.character_class
    return (clazz.base_claw_damage or clazz.level_claw_damage or clazz.random_claw_damage)

  @property
  def equipped_weapon(self):
    # TODO: should claw classes be able to equip anything in TWO_HAND/SWORD_HAND?
    if EquipmentSlot.TWO_HAND in self.db.equipment:
      return self.db.equipment[EquipmentSlot.TWO_HAND]
    if EquipmentSlot.SWORD_HAND in self.db.equipment:
      return self.db.equipment[EquipmentSlot.SWORD_HAND]
    # TODO: does SHIELD_HAND count?
    # TODO: handle claws
    return None

  @property
  def equipped_spellbook(self):
    if EquipmentSlot.BACKPACK in self.db.equipment:
      in_slot = self.db.equipment[EquipmentSlot.BACKPACK]
      if in_slot and in_slot.is_typeclass("typeclasses.objects.Spellbook"):
        return in_slot
    return None

  def equip(self, obj):
    if not obj.is_typeclass("typeclasses.objects.Equipment", exact=False):
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
    if not obj.is_typeclass("typeclasses.objects.Equipment", exact=False):
      return
    slot = obj.db.equipment_slot      
    if slot in self.db.equipment:
      del self.db.equipment[slot]
      self.msg(f"You unequip the {obj.key}.")
    else:
      self.msg("Not currently equipped.")

  def gain_health(self, amount, damager=None, weapon_name=None):
    if amount < 0:
      # aka damage
      damage = -amount
      self.db.health = max(self.db.health - damage, MIN_HEALTH)
      self.msg(f"You take {damage} damage.")
      self.msg(health_msg("You", self.db.health))
      self.location.msg_contents(health_msg(self.name, self.db.health), exclude=[self])
      if self.db.health <= 0:
        character_death(self, damager, weapon_name)
    else:
      # aka healing
      self.db.health = min(self.db.health + amount, self.max_health)
      self.msg(health_msg("You", self.db.health))
      self.location.msg_contents(health_msg(self.name, self.db.health), exclude=[self])

  def gain_mana(self, amount):
    # TODO: messages?
    self.db.mana = max(MIN_MANA, min(self.max_mana, self.db.mana + amount))

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
      del self.db.equipment[obj.db.equipment_slot]

