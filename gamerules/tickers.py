import random
from enum import Enum
from evennia import TICKER_HANDLER
from gamerules.mobs import generate_mob
from gamerules.special_room_kind import SpecialRoomKind


# A "tick" in old monster was 0.1 seconds.
# Tick.TkHealth := GetTicks + 300;
HEALTH_TICK_SECONDS = 30
# AllStats.Tick.TkMana := GetTicks + 350;
MANA_TICK_SECONDS = 35
# AllStats.Tick.TkRandMove := AllStats.Tick.TkRandMove + 100;
MOB_GENERATOR_TICK_SECONDS = 10
TRAPDOOR_TICK_SECONDS = 1


class TickerKind(Enum):
  HEALTH = 1
  MANA = 2
  MOB_GENERATOR = 3
  TRAPDOOR = 4


def add_health_ticker(subject):
  subject.add_ticker(TickerKind.HEALTH, HEALTH_TICK_SECONDS, tick_health)


def add_mana_ticker(subject):
  subject.add_ticker(TickerKind.MANA, MANA_TICK_SECONDS, tick_mana)


def add_mob_generator_ticker(subject):
  subject.add_ticker(TickerKind.MOB_GENERATOR, MOB_GENERATOR_TICK_SECONDS, tick_mob_generator)


def add_trapdoor_ticker(subject):
  subject.add_ticker(TickerKind.TRAPDOOR, TRAPDOOR_TICK_SECONDS, tick_trapdoor)


def tick_health(subject):
  if subject is None or subject.db is None:
    return
#  subject.location.msg_contents(f"tick {subject.key}")
  change = int((subject.max_health - subject.db.health) * (subject.heal_speed / 1000))
  change = max(change, 5)  
  if subject.is_poisoned:
    subject.gain_health(-change)
  elif subject.db.health < subject.max_health:
    # TODO: debugging msg
    subject.msg(f"You heal {change}.")
    subject.gain_health(change)


def tick_mana(subject):
  if subject is None or subject.db is None:
    return
  if subject.db.mana < subject.max_mana:
    # AllStats.Stats.Mana := AllStats.Stats.Mana + (AllStats.MyHold.MaxMana) DIV 2;
    # TODO: so in two ticks the subject will be fully mana-healed? is that correct?
    change = int(subject.max_mana / 2)
    subject.gain_mana(change)
    subject.msg("You feel magically energized.")


def tick_mob_generator(subject):
  if subject is None or subject.db is None or subject.location is None:
    return
  if subject.location.is_special_kind(SpecialRoomKind.NO_COMBAT):
    # never spawn in a no-combat room
    return
  if subject.location.is_special_kind(SpecialRoomKind.MONSTER_GENERATOR):
    spawn_chance = subject.location.magnitude(SpecialRoomKind.MONSTER_GENERATOR)
  else:
    # always a 1% chance
    spawn_chance = 1
  if random.randint(0, 100) < spawn_chance:
    # yay, let's make a monster
    generate_mob(subject.location, subject.level)


def tick_trapdoor(subject):
  if subject is None or subject.db is None or subject.location is None:
    return
  if not subject.location.db.trap_chance or not subject.location.db.trap_direction:
    # no trapdoor here
    return
  # find the trapdoor exit
  exits = subject.location.search(
    subject.location.db.trap_direction, typeclass="typeclasses.exits.Exit", quiet=True)
  if not exits:
    return
  if random.randint(0, 100) < subject.location.db.trap_chance:
    # away they go!
    exits[0].at_traverse(subject, exits[0].destination)  
