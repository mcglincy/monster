from evennia import TICKER_HANDLER

# A "tick" in old monster was 0.1 seconds.
# AllStats.Tick.TkMana := GetTicks + 350;
MANA_TICK_SECONDS = 35
MIN_MANA = 0


def add_mana_ticker(subject):
  id_string = f"tick_mana_{subject.key}"
  store_key = TICKER_HANDLER.add(MANA_TICK_SECONDS, tick_mana, id_string, False, subject)
  subject.db.mana_ticker_key = store_key


def remove_mana_ticker(subject):
  try:
    TICKER_HANDLER.remove(store_key=subject.db.mana_ticker_key)
  except KeyError:
    pass
  subject.db.mana_ticker_key = None


def tick_mana(subject):
  if subject.db.mana < subject.max_mana:
    # AllStats.Stats.Mana := AllStats.Stats.Mana + (AllStats.MyHold.MaxMana) DIV 2;
    # TODO: so in two ticks the subject will be fully mana-healed? is that correct?
    change = int(subject.max_mana / 2)
    subject.gain_mana(change)
    subject.msg("You feel magically energized.")