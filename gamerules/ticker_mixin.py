import random
from evennia import TICKER_HANDLER
from gamerules.mobs import generate_mob


# A "tick" in old monster was 0.1 seconds.
# Tick.TkHealth := GetTicks + 300;
HEALTH_TICK_SECONDS = 30
# AllStats.Tick.TkMana := GetTicks + 350;
MANA_TICK_SECONDS = 35
# AllStats.Tick.TkRandMove := AllStats.Tick.TkRandMove + 100;
MOB_GENERATOR_TICK_SECONDS = 10
TRAPDOOR_TICK_SECONDS = 1


class TickerMixin:
  """Various ticker callbacks.

  Ticker "add" functions are idempotent, and will simply replace any
  existing ticker at that (interval, callback).
  """

  def add_health_ticker(self):
    TICKER_HANDLER.add(HEALTH_TICK_SECONDS, self.tick_health)

  def remove_health_ticker(self):
    TICKER_HANDLER.remove(HEALTH_TICK_SECONDS, self.tick_health)

  def add_mana_ticker(self):
    TICKER_HANDLER.add(MANA_TICK_SECONDS, self.tick_mana)

  def remove_mana_ticker(self):
    TICKER_HANDLER.remove(MANA_TICK_SECONDS, self.tick_mana)

  def add_mob_generator_ticker(self):
    TICKER_HANDLER.add(MOB_GENERATOR_TICK_SECONDS, self.tick_mob_generator)

  def remove_mob_generator_ticker(self):
    TICKER_HANDLER.remove(MOB_GENERATOR_TICK_SECONDS, self.tick_mob_generator)

  def add_trapdoor_ticker(self):
    TICKER_HANDLER.add(TRAPDOOR_TICK_SECONDS, self.tick_trapdoor)

  def remove_trapdoor_ticker(self):
    TICKER_HANDLER.remove(TRAPDOOR_TICK_SECONDS, self.tick_trapdoor)

  def tick_health(self):
  #  self.location.msg_contents(f"tick {self.key}")
    if not self.db or not self.location:
      return
    change = int((self.max_health - self.db.health) * (self.heal_speed / 1000))
    change = max(change, 5)  
    if self.is_poisoned:
      self.gain_health(-change)
    elif self.db.health < self.max_health:
      # TODO: debugging msg
      self.msg(f"You heal {change}.")
      self.gain_health(change)

  def tick_mana(self):
    if not self.db or not self.location:
      return
    if self.db.mana < self.max_mana:
      # AllStats.Stats.Mana := AllStats.Stats.Mana + (AllStats.MyHold.MaxMana) DIV 2;
      # TODO: so in two ticks the self will be fully mana-healed? is that correct?
      change = int(self.max_mana / 2)
      self.gain_mana(change)
      self.msg("You feel magically energized.")

  def tick_mob_generator(self):
    if not self.db or not self.location:
      return
    if self.location.is_special_kind(SpecialRoomKind.NO_COMBAT):
      # never spawn mobs in a no-combat room
      return
    if self.location.is_special_kind(SpecialRoomKind.MONSTER_GENERATOR):
      spawn_chance = self.location.magnitude(SpecialRoomKind.MONSTER_GENERATOR)
    else:
      # default is a 1% chance
      spawn_chance = 1
    if random.randint(0, 100) < spawn_chance:
      # yay, let's make a monster
      generate_mob(self.location, self.level)

  def tick_trapdoor(self):
    if not self.db or not self.location:
      return
    if not self.location.db.trap_chance or not self.location.db.trap_direction:
      # no trapdoor here
      return
    # find the trapdoor exit
    exits = self.location.search(
      self.location.db.trap_direction, typeclass="typeclasses.exits.Exit", quiet=True)
    if not exits:
      return
    if random.randint(0, 100) < self.location.db.trap_chance:
      # away we go!
      exits[0].at_traverse(self, exits[0].destination)  
