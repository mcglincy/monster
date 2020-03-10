
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
