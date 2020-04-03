"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""
import random

from evennia import CmdSet, Command, DefaultExit, DefaultObject
from evennia.utils import delay, search

from gamerules.equipment_slot import EquipmentSlot
from gamerules.health import MIN_HEALTH, health_msg
from gamerules.object_kind import ObjectKind
from gamerules.special_room_kind import SpecialRoomKind
from userdefined.models import Spell


class Object(DefaultObject):
  """
  This is the root typeclass object, implementing an in-game Evennia
  game object, such as having a location, being able to be
  manipulated or looked at, etc. If you create a new typeclass, it
  must always inherit from this object (or any of the other objects
  in this file, since they all actually inherit from BaseObject, as
  seen in src.object.objects).

  The BaseObject class implements several hooks tying into the game
  engine. By re-implementing these hooks you can control the
  system. You should never need to re-implement special Python
  methods, such as __init__ and especially never __getattribute__ and
  __setattr__ since these are used heavily by the typeclass system
  of Evennia and messing with them might well break things for you.


  * Base properties defined/available on all Objects

   key (string) - name of object
   name (string)- same as key
   dbref (int, read-only) - unique #id-number. Also "id" can be used.
   date_created (string) - time stamp of object creation

   account (Account) - controlling account (if any, only set together with
                     sessid below)
   sessid (int, read-only) - session id (if any, only set together with
                     account above). Use `sessions` handler to get the
                     Sessions directly.
   location (Object) - current location. Is None if this is a room
   home (Object) - safety start-location
   has_account (bool, read-only)- will only return *connected* accounts
   contents (list of Objects, read-only) - returns all objects inside this
                     object (including exits)
   exits (list of Objects, read-only) - returns all exits from this
                     object, if any
   destination (Object) - only set if this object is an exit.
   is_superuser (bool, read-only) - True/False if this user is a superuser

  * Handlers available

   aliases - alias-handler: use aliases.add/remove/get() to use.
   permissions - permission-handler: use permissions.add/remove() to
                 add/remove new perms.
   locks - lock-handler: use locks.add() to add new lock strings
   scripts - script-handler. Add new scripts to object with scripts.add()
   cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
   nicks - nick-handler. New nicks with nicks.add().
   sessions - sessions-handler. Get Sessions connected to this
              object with sessions.get()
   attributes - attribute-handler. Use attributes.add/remove/get.
   db - attribute-handler: Shortcut for attribute-handler. Store/retrieve
          database attributes using self.db.myattr=val, val=self.db.myattr
   ndb - non-persistent attribute handler: same as db but does not create
          a database entry when storing data

  * Helper methods (see src.objects.objects.py for full headers)

   search(ostring, global_search=False, attribute_name=None,
           use_nicks=False, location=None, ignore_errors=False, account=False)
   execute_cmd(raw_string)
   msg(text=None, **kwargs)
   msg_contents(message, exclude=None, from_obj=None, **kwargs)
   move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
   copy(new_key=None)
   delete()
   is_typeclass(typeclass, exact=False)
   swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
   access(accessing_obj, access_type='read', default=False)
   check_permstring(permstring)

  * Hooks (these are class methods, so args should start with self):

   basetype_setup()     - only called once, used for behind-the-scenes
                          setup. Normally not modified.
   basetype_posthook_setup() - customization in basetype, after the object
                          has been created; Normally not modified.

   at_object_creation() - only called once, when object is first created.
                          Object customizations go here.
   at_object_delete() - called just before deleting an object. If returning
                          False, deletion is aborted. Note that all objects
                          inside a deleted object are automatically moved
                          to their <home>, they don't need to be removed here.

   at_init()            - called whenever typeclass is cached from memory,
                          at least once every server restart/reload
   at_cmdset_get(**kwargs) - this is called just before the command handler
                          requests a cmdset from this object. The kwargs are
                          not normally used unless the cmdset is created
                          dynamically (see e.g. Exits).
   at_pre_puppet(account)- (account-controlled objects only) called just
                          before puppeting
   at_post_puppet()     - (account-controlled objects only) called just
                          after completing connection account<->object
   at_pre_unpuppet()    - (account-controlled objects only) called just
                          before un-puppeting
   at_post_unpuppet(account) - (account-controlled objects only) called just
                          after disconnecting account<->object link
   at_server_reload()   - called before server is reloaded
   at_server_shutdown() - called just before server is fully shut down

   at_access(result, accessing_obj, access_type) - called with the result
                          of a lock access check on this object. Return value
                          does not affect check result.

   at_before_move(destination)             - called just before moving object
                      to the destination. If returns False, move is cancelled.
   announce_move_from(destination)         - called in old location, just
                      before move, if obj.move_to() has quiet=False
   announce_move_to(source_location)       - called in new location, just
                      after move, if obj.move_to() has quiet=False
   at_after_move(source_location)          - always called after a move has
                      been successfully performed.
   at_object_leave(obj, target_location)   - called when an object leaves
                      this object in any fashion
   at_object_receive(obj, source_location) - called when this object receives
                      another object

   at_traverse(traversing_object, source_loc) - (exit-objects only)
                            handles all moving across the exit, including
                            calling the other exit hooks. Use super() to retain
                            the default functionality.
   at_after_traverse(traversing_object, source_location) - (exit-objects only)
                            called just after a traversal has happened.
   at_failed_traverse(traversing_object)      - (exit-objects only) called if
                     traversal fails and property err_traverse is not defined.

   at_msg_receive(self, msg, from_obj=None, **kwargs) - called when a message
                           (via self.msg()) is sent to this obj.
                           If returns false, aborts send.
   at_msg_send(self, msg, to_obj=None, **kwargs) - called when this objects
                           sends a message to someone via self.msg().

   return_appearance(looker) - describes this object. Used by "look"
                               command by default
   at_desc(looker=None)      - called by 'look' whenever the
                               appearance is requested.
   at_get(getter)            - called after object has been picked up.
                               Does not stop pickup.
   at_drop(dropper)          - called when this object has been dropped.
   at_say(speaker, message)  - by default, called if an object inside this
                               object speaks
  """
  def at_object_creation(self):
    super().at_object_creation()
    self.db.record_id = None
    self.db.article = None
    self.db.components = []
    self.db.get_fail_msg = None
    self.db.get_object_required = None
    self.db.get_success_msg = None
    self.db.line_desc = None
    self.db.object_kind = None
    self.db.sticky = False
    self.db.num_exist = None
    self.db.use_fail_msg = None
    self.db.use_object_required = None
    self.db.use_success_msg = None
    self.db.weight = 0
    self.db.worth = 0

  def at_before_get(self, getter, **kwargs):
    if self.db.sticky:
      if self.db.get_fail_msg:
        getter.msg(self.db.get_fail_msg)
      return False
    return True

  def at_get(self, getter, **kwargs):
    if self.db.get_success_msg:
      getter.msg(self.db.get_success_msg)


  def at_before_use(self, user, **kwargs):
    if self.db.use_object_required:
      # TODO: check that user has object by id
      if self.db.use_fail_msg:
        user.msg(self.db.use_fail_msg)
      return False
    return True

  def at_use(self, user, **kwargs):
    if self.db.use_success_msg:
      user.msg(self.db.use_success_msg)


class StackableObject(Object):
  def at_object_creation(self):
    super().at_object_creation()
    self.db.amount= 0
    self.db.stack_name = "stack"
    self.db.singular_object_name = "thingy"
    self.db.plural_object_name = "thingies"

  def _stack_name(self):
    n = f"{self.db.stack_name} of {self.db.amount} "
    if self.db.amount == 1:
      n += self.db.singular_object_name 
    else:
      n += self.db.plural_object_name 
    return n

  def get_display_name(self, looker, **kwargs):
    n = self._stack_name()
    if self.locks.check_lockstring(looker, "perm(Builder)"):
      return f"{n} (#{self.id})"
    return n

  def return_appearance(self, *args, **kwargs):
    return f"A {self._stack_name()}."

  def add(self, amount):
    self.db.amount = self.db.amount + amount
    self.db.desc = f"A {self._stack_name()}."
    if self.db.amount <= 0:
      self.delete()

  def at_get(self, getter, **kwargs):
    # see if getter already has a stack of this kind
    existing = [x for x in getter.contents if x.typeclass_path == self.path and x != self]
    if existing:
      # add our count to the existing object
      obj = existing[0]
      obj.add(self.db.amount)
      self.delete()

  def at_drop(self, dropper, **kwargs):
    # see if dropped-to location already has a stack of this kind
    existing = [x for x in self.location.contents if x.typeclass_path == self.path and x != self]
    if existing:
      # add our count to the existing object
      obj = existing[0]
      obj.add(self.db.amount)
      self.delete()


class Gold(StackableObject):
  def at_object_creation(self):
    super().at_object_creation()
    self.db.stack_name = "bag"
    self.db.singular_object_name = "gold"
    self.db.plural_object_name = "gold"


class Bland(Object):
  def at_object_creation(self):
    super().at_object_creation()
    self.db.object_kind = ObjectKind.BLAND


class Equipment(Object):
  def at_object_creation(self):
    super().at_object_creation()
    self.db.object_kind = ObjectKind.EQUIPMENT
    # equipment effects
    # TODO: keep as a sparse dict instead of fields?
    # {EquipmentEffectKind:value}
    # self.db.effects = {}
    self.db.attack_speed = 0
    self.db.base_armor = 0
    self.db.base_claw_damage = 0
    self.db.base_health = 0
    self.db.base_mana = 0
    self.db.base_move_silent = 0
    self.db.base_steal = 0
    self.db.base_weapon_damage = 0
    self.db.base_weapon_use = 0    
    self.db.bomb_base = 0
    self.db.bomb_random = 0
    self.db.bomb_time = 0
    self.db.break_chance = 0
    self.db.break_magnitude = 0
    self.db.cast_spell = 0
    self.db.character_class = 0
    self.db.charges = 0
    self.db.condition = 100
    self.db.control = 0
    self.db.crystal_radius = 0
    self.db.cursed = 0
    self.db.deflect_armor = 0
    self.db.drop_destroy = 0
    self.db.equipment_slot = EquipmentSlot.NOT_EQUIPPABLE
    self.db.group = 0
    self.db.heal_speed = 0
    self.db.hear_noise = 0
    self.db.invisible = 0
    self.db.largest_fit = 0
    self.db.level_claw_damage = 0    
    self.db.level_health = 0
    self.db.level_mana = 0
    self.db.level_move_silent = 0
    self.db.level_steal = 0
    self.db.level_weapon_use = 0
    self.db.move_speed = 0
    self.db.no_throw = 0
    self.db.poison = 0
    self.db.random_claw_damage = 0    
    self.db.random_weapon_damage = 0
    self.db.see_invisible = 0
    self.db.size = 0
    self.db.smallest_fit = 0
    self.db.spell = 0
    self.db.spell_armor = 0
    self.db.spell_deflect_armor = 0
    self.db.teleport = 0
    self.db.throw_base = 0
    self.db.throw_behavior = 0
    self.db.throw_random = 0
    self.db.throw_range = 0
    self.db.trap = 0
    self.db.xp = 0

  def at_drop(self, dropper, **kwargs):
    if (self.db.drop_destroy
      or dropper.location.is_special_kind(SpecialRoomKind.OBJECT_DESTROY)):
     dropper.msg(f"The {self.key} was destroyed.")
     dropper.location.msg_contents(
      f"The {self.key} was destroyed when {dropper.key} dropped it.",
      exclude=[dropper])
     self.delete()

  def is_weapon(self):
    return self.db.base_weapon_damage or self.db.random_weapon_damage


class Scroll(Object):
  def at_object_creation(self):
    super().at_object_creation()
    self.db.object_kind = ObjectKind.SCROLL
    self.db.spell_key = None
    self.db.charges = 0


class Wand(Object):
  def at_object_creation(self):
    super().at_object_creation()
    self.db.object_kind = ObjectKind.WAND
    self.db.charges = 0


class Missile(Object):
  def at_object_creation(self):
    super().at_object_creation()
    self.db.object_kind = ObjectKind.MISSILE
    self.db.charges = 0


class MissileLauncher(Object):
  def at_object_creation(self):
    super().at_object_creation()
    self.db.object_kind = ObjectKind.MISSILE_LAUNCHER


class Spellbook(Equipment):
  def at_object_creation(self):
    super().at_object_creation()
    self.db.object_kind = ObjectKind.SPELLBOOK
    self.db.spell_keys = []

  @property
  def spells(self):
    return Spell.objects.filter(db_key__in=self.db.spell_keys)

  def find_spell(self, name):
    for spell in self.spells:
      if spell.key.lower().startswith(name.lower()):
        return spell
    return None

class BankingMachine(Object):
  def at_object_creation(self):
    super().at_object_creation()
    self.db.object_kind = ObjectKind.BANKING_MACHINE



