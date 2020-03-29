from evennia import TICKER_HANDLER

# A "tick" in old monster was 0.1 seconds.
# Tick.TkHealth := GetTicks + 300;
HEALTH_TICK_SECONDS = 30
MIN_HEALTH = 0


def health_msg(subject, health):
  to_be = "is"
  to_have = "has"
  to_look = "looks"
  if subject.lower() == "you":
    to_be = "are"
    to_have = "have"
    to_look = "feel"
  if health >= 1700:
    return f"{subject} {to_be} in ultimate health."
  elif health > 1400:
    return f"{subject} {to_be} in incredible health."
  elif health > 1200:
    return f"{subject} {to_be} in extraordinary health."
  elif health > 1000:
    return f"{subject} {to_be} in tremendous health."
  elif health > 850:
    return f"{subject} {to_be} in superior condition."
  elif health > 700:
    return f"{subject} {to_be} in exceptional health."
  elif health > 500:
    return f"{subject} {to_be} in good health."
  elif health > 350:
    return f"{subject} {to_look} a little bit dazed."
  elif health > 200:
    return f"{subject} {to_have} some minor wounds."
  elif health > 100:
    return f"{subject} {to_be} suffering from some serious wounds."
  elif health > 50:
    return f"{subject} {to_be} in critical condition."
  elif health > 1:
    return f"{subject} {to_be} near death."
  else:
    return f"{subject} {to_be} dead."


def add_health_ticker(subject):
  id_string = f"tick_health_{subject.key}"
  TICKER_HANDLER.add(HEALTH_TICK_SECONDS, tick_health, id_string, False, subject)


def remove_health_ticker(subject):
  id_string = f"tick_health_{subject.key}"
  try:
    TICKER_HANDLER.remove(interval=HEALTH_TICK_SECONDS, callback=tick_health, idstring=id_string)
  except KeyError:
    pass


def tick_health(subject):
#  subject.location.msg_contents(f"tick {subject.key}")
  change = int((subject.max_health - subject.db.health) * (subject.heal_speed / 1000))
  change = max(change, 5)  
  if subject.is_poisoned:
    subject.gain_health(-change)
  elif subject.db.health < subject.max_health:
    # TODO: debugging msg
    subject.msg(f"You heal {change}.")
    subject.gain_health(change)
