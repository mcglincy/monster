from enum import IntEnum
import random
from evennia import GLOBAL_SCRIPTS, logger, TICKER_HANDLER
from gamerules.health import MIN_HEALTH, health_msg
from gamerules.mob_kind import MobKind
from gamerules.mobs import mob_death, resolve_mob_attack
from gamerules.ticker_mixin import TickerMixin
from gamerules.xp import level_from_xp
from typeclasses.objects import Object


# TODO: refactor/optimize state machine for patrolling vs. lair monster:
# patrolling monster: starts in state PATROLLING and added to global ticker
# lair monster: unhooked from global ticker, when someone enters the room, 
# goes to attacking state and adds self to global ticker
# if not target available, goes to IDLE and unhooks from global ticker

class MobBehavior(IntEnum):
  IDLE = 0
  PATROLLING = 1
  HUNTING = 2
  ATTACKING = 3


class OldMob(Object, TickerMixin):
  """Non-player monster aka mob aka Monster 'random'.

  Ticker code lifted from evennia.contrib.tutorial_world.mob.
  """  
  def at_object_creation(self):
    super().at_object_creation()
    # self.db.record_id
    # self.db.kind = MobKind.FIGHTER
    # self.db.min_level = 0
    # self.db.group = 0
    # self.db.size = 0
    # self.db.xp = 0
    # self.db.drop_gold = 0
    # self.db.drop_object_id = 0
    # self.db.base_health = 0
    # self.db.random_health = 0
    # self.db.level_health = 0
    # self.db.base_mana = 0
    # self.db.level_mana = 0
    # self.db.base_damage = 0
    # self.db.random_damage = 0
    # self.db.level_damage = 0
    # self.db.armor = 0
    # self.db.spell_armor = 0
    # self.db.move_speed = 0
    # self.db.attack_speed = 0
    # self.db.heal_speed = 0
    # self.db.weapon_id = 0
    # self.db.weapon_use = 0
    # self.db.level_weapon_use = 0
    # self.db.pursuit_chance = 0
    # self.db.spell_ids = []
    # self.db.sayings = []
    # self.db.attack_name = None

    # whether the mob moves between rooms
    self.db.moves_between_rooms = True

    # whether the mob immediately attacks targets in its room
    self.db.aggressive = True
    self.db.patrolling = True    
    self.db.patrolling_pace = 6
    self.db.attacking_pace = 2
    self.db.hunting_pace = 1    
    # we store the call to the tickerhandler
    # so we can easily deactivate the last
    # ticker subscription when we switch.
    # since we will use the same idstring
    # throughout we only need to save the
    # previous interval we used.
    self.db.last_ticker_interval = None
    self.db.last_hook_key = None

  def basetype_posthook_setup(self):
    # overriding this so we can do some post-init
    # after spawning, as BaseObject.at_first_save() applies _create_dict field values
    # *after* calling at_object_creation()
    super().basetype_posthook_setup()
    # TODO: what about level_health and level_mana? do mobs have a level?
    self.db.max_health = self.db.base_health + random.randint(0, self.db.random_health)
    self.db.health = self.db.max_health
    self.db.max_mana = self.db.base_mana
    self.db.mana = self.db.max_mana
    self.db.poisoned = False
    # call at_init() to add tickers and kickstart the mob
    self.at_init()

  def at_init(self):
    self.ndb.hiding = 0
    self.add_health_ticker()
    #self.add_mana_ticker()
    self.ndb.is_patrolling = self.db.patrolling
    self.ndb.is_attacking = False
    self.ndb.is_hunting = False    
    self.start_patrolling()

  def at_object_delete(self):
    # kill tickers
    self.start_idle()
    self.remove_health_ticker()

  def at_new_arrival(self, new_character):
    """This is triggered whenever a new character enters the room.

    This is called by the TutorialRoom the mob stands in and
    allows it to be aware of changes immediately without needing
    to poll for them all the time. For example, the mob can react
    right away, also when patrolling on a very slow ticker.
    """
    # the room actually already checked all we need, so
    # we know it is a valid target.
    if self.db.aggressive and not self.ndb.is_attacking:
      self.start_attacking()

  def gain_health(self, amount, damager=None, weapon_name=None):
    self.db.health = max(MIN_HEALTH, min(self.max_health, self.db.health + amount))
    # tell everyone else in the room our health
    self.location.msg_contents(health_msg(self.key, self.db.health), exclude=[self])
    if self.db.health <= 0:
      # die
      mob_death(self, damager)
    elif amount < 0 and not self.ndb.is_attacking:
      # we took damage and we're still alive - go aggro
      self.ndb.aggressive = True
      self.start_attacking()

  @property
  def level(self):
    return level_from_xp(self.db.xp)

  @property
  def is_dead(self):
    return self.db.health <= 0

  @property
  def max_health(self):
    return self.db.max_health

  @property
  def base_armor(self):
    return self.db.armor

  @property
  def deflect_armor(self):
    return 0

  @property
  def spell_armor(self):
    return self.db.spell_armor

  @property
  def spell_deflect_armor(self):
    return 0

  @property
  def attack_speed(self):
    return self.db.attack_speed  

  @property
  def move_speed(self):
    return self.db.move_speed  
  
  @property
  def heal_speed(self):
    return self.db.heal_speed  

  @property
  def base_damage(self):
    return self.db.base_damage

  @property
  def random_damage(self):
    return self.db.random_damage

  @property
  def is_poisoned(self):
    return self.db.poisoned

  @property
  def attack_name(self):
    return self.db.attack_name if self.db.attack_name else "claws"

  def _find_target(self, location):
    # TODO: handle death of our previous target
    # TODO: and not x.is_superuser ?
    characters = [x for x in location.contents 
      if x.is_typeclass("typeclasses.characters.Character") and not x.is_hiding]
    if characters:
      target = random.choice(characters)
      return target

  def _set_ticker(self, interval, hook_key, stop=False):
    """Set how often the given hook key should be "ticked".

    Args:
        interval (int): The number of seconds
            between ticks
        hook_key (str): The name of the method
            (on this mob) to call every interval
            seconds.
        stop (bool, optional): Just stop the
            last ticker without starting a new one.
            With this set, the interval and hook_key
            arguments are unused.

    In order to only have one ticker
    running at a time, we make sure to store the
    previous ticker subscription so that we can
    easily find and stop it before setting a
    new one. The tickerhandler is persistent so
    we need to remember this across reloads.
    """
    idstring = f"tick_state_{self.key}"  # this doesn't change
    last_interval = self.db.last_ticker_interval
    last_hook_key = self.db.last_hook_key
    if last_interval and last_hook_key:
      # we have a previous subscription, kill this first.
      try:
        TICKER_HANDLER.remove(interval=last_interval,
          callback=getattr(self, last_hook_key), idstring=idstring)
      except KeyError:
        pass
    self.db.last_ticker_interval = interval
    self.db.last_hook_key = hook_key
    if not stop:
      # set the new ticker
      TICKER_HANDLER.add(interval=interval,
        callback=getattr(self, hook_key), idstring=idstring)

  def _maybe_say_something(self):
    if random.random() < 0.01 and self.db.irregular_msgs:
      self.location.msg_contents(random.choice(self.db.irregular_msgs))

  def start_idle(self):
    """Starts just standing around. This will kill the ticker and do nothing more."""
    self._set_ticker(None, None, stop=True)

  def start_patrolling(self):
    """Start the patrolling state by registering us with the ticker-handler
      at a leasurely pace.
    """
    if not self.db.patrolling:
      self.start_idle()
      return
    self._set_ticker(self.db.patrolling_pace, "do_patrol")
    self.ndb.is_patrolling = True
    self.ndb.is_hunting = False
    self.ndb.is_attacking = False

  def start_hunting(self):
    """Start the hunting state."""
    if not self.db.hunting:
      self.start_patrolling()
      return
    self._set_ticker(self.db.hunting_pace, "do_hunt")
    self.ndb.is_patrolling = False
    self.ndb.is_hunting = True
    self.ndb.is_attacking = False

  def start_attacking(self):
    """Start the attacking state."""
    if not self.db.aggressive:
      self.start_hunting()
      return
    self._set_ticker(self.db.attacking_pace, "do_attack")
    self.ndb.is_patrolling = False
    self.ndb.is_hunting = False
    self.ndb.is_attacking = True

  def do_patrol(self, *args, **kwargs):
    """Called repeatedly during patrolling mode.  

    In this mode, the
    mob scans its surroundings and randomly chooses a viable exit.
    One should lock exits with the traverse:has_account() lock in
    order to block the mob from moving outside its area while
    allowing account-controlled characters to move normally.
    """
    #self._maybe_say_something()

    if self.db.aggressive:
      # first check if there are any targets in the room.
      target = self._find_target(self.location)
      if target:
        self.start_attacking()
        return

    if self.db.moves_between_rooms:
      # no target found, look for an exit.
      exits = [x for x in self.location.exits if x.access(self, "traverse")]
      if exits:
        # randomly pick an exit
        exit = random.choice(exits)
        # move there.
        self.move_to(exit.destination)
      else:
        # no exits! teleport to home to get away.
        self.move_to(self.home)

  def do_hunting(self, *args, **kwargs):
    """Called regularly when in hunting mode.

    In hunting mode the mob
    scans adjacent rooms for enemies and moves towards them to
    attack if possible.
    """
    #self._maybe_say_something()   

    if self.db.aggressive:
      # first check if there are any targets in the room.
      target = self._find_target(self.location)
      if target:
        self.start_attacking()
        return

    if self.db.moves_between_rooms:
      # no targets found, scan surrounding rooms
      exits = [x for x in self.location.exits if x.access(self, "traverse")]
      if exits:
        # scan the exits destination for targets
        for exit in exits:
          target = self._find_target(exit.destination)
          if target:
            # a target found. Move there.
            self.move_to(exit.destination)
            return
        # if we get to this point we lost our
        # prey. Resume patrolling.
        self.start_patrolling()
      else:
        # no exits! teleport to home to get away.
        self.move_to(self.home)

  def do_attack(self, *args, **kwargs):
    """Called regularly when in attacking mode. 

    In attacking mode
    the mob will bring its weapons to bear on any targets
    in the room.
    """
    #self._maybe_say_something()

    # first make sure we have a target
    target = self._find_target(self.location)
    if not target:
      # no target, start looking for one
      self.start_hunting()
      return
    resolve_mob_attack(self, target, self.attack_name)


class Mob(Object, TickerMixin):
  """Non-player monster aka mob aka Monster 'random'.

  Ticker code lifted from evennia.contrib.tutorial_world.mob.
  """  
  def at_object_creation(self):
    super().at_object_creation()
    # self.db.record_id
    # self.db.kind = MobKind.FIGHTER
    # self.db.min_level = 0
    # self.db.group = 0
    # self.db.size = 0
    # self.db.xp = 0
    # self.db.drop_gold = 0
    # self.db.drop_object_id = 0
    # self.db.base_health = 0
    # self.db.random_health = 0
    # self.db.level_health = 0
    # self.db.base_mana = 0
    # self.db.level_mana = 0
    # self.db.base_damage = 0
    # self.db.random_damage = 0
    # self.db.level_damage = 0
    # self.db.armor = 0
    # self.db.spell_armor = 0
    # self.db.move_speed = 0
    # self.db.attack_speed = 0
    # self.db.heal_speed = 0
    # self.db.weapon_id = 0
    # self.db.weapon_use = 0
    # self.db.level_weapon_use = 0
    # self.db.pursuit_chance = 0
    # self.db.spell_ids = []
    # self.db.sayings = []
    # self.db.attack_name = None
    # whether the mob moves between rooms
    self.db.moves_between_rooms = True
    # whether the mob immediately attacks targets in its room
    self.db.aggressive = True

  def basetype_posthook_setup(self):
    # overriding this so we can do some post-init
    # after spawning, as BaseObject.at_first_save() applies _create_dict field values
    # *after* calling at_object_creation()
    super().basetype_posthook_setup()
    # TODO: what about level_health and level_mana? do mobs have a level?
    self.db.max_health = self.db.base_health + random.randint(0, self.db.random_health)
    self.db.health = self.db.max_health
    self.db.max_mana = self.db.base_mana
    self.db.mana = self.db.max_mana
    self.db.poisoned = False
    # call at_init() to add tickers and kickstart the mob
    self.at_init()

  def at_init(self):
    logger.log_info(f"mob {self.key}#{self.id} at_init()")
    self.ndb.hiding = 0
    self.ndb.behavior = MobBehavior.PATROLLING
    self.add_to_global_tickers()

  def at_object_delete(self):
    self.remove_from_global_tickers()
    return True

  def add_to_global_tickers(self):
    GLOBAL_SCRIPTS.behavior_ticker.ndb.targets.add(self)
    GLOBAL_SCRIPTS.health_ticker.ndb.targets.add(self)

  def remove_from_global_tickers(self):
    GLOBAL_SCRIPTS.behavior_ticker.ndb.targets.remove(self)
    GLOBAL_SCRIPTS.health_ticker.ndb.targets.remove(self)

  def at_new_arrival(self, new_character):
    """This is triggered whenever a new character enters the room.

    This is called by the TutorialRoom the mob stands in and
    allows it to be aware of changes immediately without needing
    to poll for them all the time. For example, the mob can react
    right away, also when patrolling on a very slow ticker.
    """
    # the room actually already checked all we need, so
    # we know it is a valid target.
    if self.db.aggressive and self.ndb.behavior != MobBehavior.ATTACKING:
      #self.start_attacking()
      self.ndb.behavior = MobBehavior.ATTACKING

  def gain_health(self, amount, damager=None, weapon_name=None):
    self.db.health = max(MIN_HEALTH, min(self.max_health, self.db.health + amount))
    # tell everyone else in the room our health
    self.location.msg_contents(health_msg(self.key, self.db.health), exclude=[self])
    if self.db.health <= 0:
      # die
      mob_death(self, damager)
    elif amount < 0 and not self.ndb.is_attacking:
      # we took damage and we're still alive - go aggro
      self.ndb.aggressive = True
#      self.start_attacking()
      self.ndb.behavior = MobBehavior.ATTACKING

  @property
  def level(self):
    return level_from_xp(self.db.xp)

  @property
  def is_dead(self):
    return self.db.health <= 0

  @property
  def max_health(self):
    return self.db.max_health

  @property
  def base_armor(self):
    return self.db.armor

  @property
  def deflect_armor(self):
    return 0

  @property
  def spell_armor(self):
    return self.db.spell_armor

  @property
  def spell_deflect_armor(self):
    return 0

  @property
  def attack_speed(self):
    return self.db.attack_speed  

  @property
  def move_speed(self):
    return self.db.move_speed  
  
  @property
  def heal_speed(self):
    return self.db.heal_speed  

  @property
  def base_damage(self):
    return self.db.base_damage

  @property
  def random_damage(self):
    return self.db.random_damage

  @property
  def is_poisoned(self):
    return self.db.poisoned

  @property
  def attack_name(self):
    return self.db.attack_name if self.db.attack_name else "claws"

  def tick_behavior(self):
    logger.log_info(f"mob {self.key}#{self.id} is behavior {self.ndb.behavior.name}")
    if self.ndb.behavior == MobBehavior.IDLE:
      # do nothing
      return
    elif self.ndb.behavior == MobBehavior.PATROLLING:
      self.do_patrol()
    elif self.ndb.behavior == MobBehavior.HUNTING:
      self.do_hunting()
    elif self.ndb.behavior == MobBehavior.ATTACKING:
      self.do_attack()

  def _find_target(self, location):
    # TODO: handle death of our previous target
    # TODO: and not x.is_superuser ?
    characters = [x for x in location.contents 
      if x.is_typeclass("typeclasses.characters.Character") and not x.is_hiding]
    if characters:
      target = random.choice(characters)
      return target

  def _maybe_say_something(self):
    if random.random() < 0.01 and self.db.irregular_msgs:
      self.location.msg_contents(random.choice(self.db.irregular_msgs))

  def do_patrol(self, *args, **kwargs):
    """Called repeatedly during patrolling mode.  

    In this mode, the
    mob scans its surroundings and randomly chooses a viable exit.
    One should lock exits with the traverse:has_account() lock in
    order to block the mob from moving outside its area while
    allowing account-controlled characters to move normally.
    """
    #self._maybe_say_something()

    if self.db.aggressive:
      # first check if there are any targets in the room.
      target = self._find_target(self.location)
      if target:
        self.ndb.behavior = MobBehavior.ATTACKING
        return

    if self.db.moves_between_rooms:
      # no target found, look for an exit.
      exits = [x for x in self.location.exits if x.access(self, "traverse")]
      if exits:
        # randomly pick an exit
        exit = random.choice(exits)
        # move there.
        self.move_to(exit.destination)
      else:
        # no exits! teleport to home to get away.
        self.move_to(self.home)

  def do_hunting(self, *args, **kwargs):
    """Called regularly when in hunting mode.

    In hunting mode the mob
    scans adjacent rooms for enemies and moves towards them to
    attack if possible.
    """
    #self._maybe_say_something()   

    if self.db.aggressive:
      # first check if there are any targets in the room.
      target = self._find_target(self.location)
      if target:
        self.ndb.behavior = MobBehavior.ATTACKING
        return

    if self.db.moves_between_rooms:
      # no targets found, scan surrounding rooms
      exits = [x for x in self.location.exits if x.access(self, "traverse")]
      if exits:
        # scan the exits destination for targets
        for exit in exits:
          target = self._find_target(exit.destination)
          if target:
            # a target found. Move there.
            self.move_to(exit.destination)
            return
        # if we get to this point we lost our
        # prey. Resume patrolling.
        self.ndb.behavior = MobBehavior.PATROLLING
      else:
        # no exits! teleport to home to get away.
        self.move_to(self.home)

  def do_attack(self, *args, **kwargs):
    """Called regularly when in attacking mode. 

    In attacking mode
    the mob will bring its weapons to bear on any targets
    in the room.
    """
    #self._maybe_say_something()

    # first make sure we have a target
    target = self._find_target(self.location)
    if not target:
      # no target, start looking for one
      self.ndb.behavior = MobBehavior.HUNTING
      return
    resolve_mob_attack(self, target, self.attack_name)

