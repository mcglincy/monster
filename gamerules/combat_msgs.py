

def attack_attacker_msg(target_name, weapon_name, damage):
  add_s = "" if weapon_name == "claws" else "s"
  if damage > 500:
    return f"You vaporize {target_name}'s putrid body. [{damage}]"
  elif damage > 400:
    return f"You attack {target_name} with blinding speed and power!!! [{damage}]"
  elif damage > 300:
    return f"You deliver an almost deadly blow to {target_name} with your {weapon_name}!! [{damage}]"
  elif damage > 200:
    return f"Your {weapon_name} cream{add_s} {target_name}'s poor little body!! [{damage}]"
  elif damage > 150:
    return f"Your {weapon_name} hit{add_s} {target_name} very hard! [{damage}]"
  elif damage > 100:
    return f"Your {weapon_name} hit{add_s} {target_name} hard! [{damage}]"
  elif damage > 50:
    return f"You hit {target_name}, good. [{damage}]"
  elif damage > 0:
    return f"{target_name} is grazed by your {weapon_name}."
  else:
    return f"You miss {target_name} with your {weapon_name}."


def attack_target_msg(attacker_name, weapon_name, damage):
  add_s = "" if weapon_name == "claws" else "s"  
  if damage > 500:
    return f"{attacker_name} vaporizes you! [{damage}]"
  elif damage > 400:
    return f"{attacker_name} attacks you with blinding speed and power, ARRRG!! [{damage}]"
  elif damage > 300:
    return f"{attacker_name}'s {weapon_name} nearly split{add_s} you in two!!! [{damage}]"
  elif damage > 200:
    return f"{attacker_name}'s {weapon_name} cream{add_s} your poor little body!! [{damage}]"
  elif damage > 150:
    return f"{attacker_name}'s {weapon_name} hit{add_s} you very hard! [{damage}]"
  elif damage > 100:
    return f"{attacker_name}'s {weapon_name} hit{add_s} you hard! [{damage}]"
  elif damage > 50:
    return f"{attacker_name}'s {weapon_name} hit{add_s} you, good. [{damage}]"
  elif damage > 0:
    return f"You are grazed by {attacker_name}'s {weapon_name}. [{damage}]"
  else:
    return f"{attacker_name} missed you with a {weapon_name}. [{damage}]"


def attack_bystander_msg(attacker_name, target_name, weapon_name, damage):
  add_s = "" if weapon_name == "claws" else "s"  
  if damage > 500:
    return f"{attacker_name} vaporizes {target_name}'s putrid body."
  elif damage > 400:
    return f"{attacker_name} attacks {target_name} with blinding speed and power!!!"
  elif damage > 300:
    return f"{attacker_name}'s {weapon_name} nearly split{add_s} {target_name} in two!!!"
  elif damage > 200:
    return f"{attacker_name}'s {weapon_name} cream{add_s} {target_name}'s poor little body!!"
  elif damage > 150:
    return f"{attacker_name}'s {weapon_name} hit{add_s} {target_name} very hard!"
  elif damage > 100:
    return f"{attacker_name}'s {weapon_name} hit{add_s} {target_name} with incredible force!"
  elif damage > 50:
    return f"{attacker_name} hits {target_name}, good."
  elif damage > 0:
    return f"{target_name} is grazed by {attacker_name}'s {weapon_name}."
  else:
    return f"{attacker_name} misses {target_name} with their {weapon_name}."


PUNCH_ATTACKER_MSGS = [
  "You deliver a quick jab to %s's jaw.",
  "You swing at %s and miss.",
  "A quick punch, but it only grazes %s.",
  "%s doubles over after your jab to the stomach.",
  "Your punch lands square on %s's face!",
  "You nail %s right upside the head, dizzying them for a moment.",
  "A good swing, but it misses %s by a mile!",
  "Your punch is blocked by %s.",
  "Your roundhouse blow sends %s reeling.",
  "You land a solid uppercut on %s's chin.",
  "%s fends off your blow.",
  "%s ducks and avoids your punch.",
  "You thump %s in the ribs.",
  "You catch %s's face on your elbow.",
  "You knock the wind out of %s with a punch to the chest.",
]

def punch_attacker_msg(target_name, num):
  if num < len(PUNCH_ATTACKER_MSGS):
    return PUNCH_ATTACKER_MSGS[num] % target_name
  return "Your senses dull as adrenaline rushes through your body... you desperately attack!"


PUNCH_TARGET_MSGS = [
  "%s delivers a quick jab to your jaw!",
  "%s swings at you but misses.",
  "%s's fist grazes you.",
  "You double over after %s lands a mean jab to your stomach.",
  "You see stars as %s bashes you in the face.",
  "You only feel the breeze as %s swings wildly.",
  "%s's swing misses you by a yard.",
  "With lightning reflexes you block %s's punch",
  "%s's blow sends you reeling.",
  "Your head snaps back from %s's uppercut!",
  "You parry %s's attack.",
  "You duck in time to avoid %s's punch.",
  "%s thumps you hard in the ribs.",
  "Your vision blurs as %s elbows you in the head.",
  "%s knocks the wind out of you with a punch to the chest.",
]


def punch_target_msg(attacker_name, num):
  if num < len(PUNCH_TARGET_MSGS):
    return PUNCH_TARGET_MSGS[num] % attacker_name
  return "%s screams, then in a blinding motion attacks you." % attacker_name


def punch_bystander_msg(attacker_name, target_name, num):
  if num == 1:
    "%s jabs %s in the jaw." % (attacker_name, target_name)
  elif num == 2:
    "%s throws a wild punch at the air." % attacker_name
  elif num == 3:
    "%s fist barely grazes %s." % (attacker_name, target_name)
  elif num == 4:
    "%s doubles over in pain with %s's punch" % (target_name, attacker_name)
  elif num == 5:
    "%s bashes %s in the face." % (attacker_name, target_name)
  elif num == 6:
    "%s takes a wild swing at %s and misses." % (attacker_name, target_name)
  elif num == 7:
    "%s swings at %s and misses by a yard." % (attacker_name, target_name)
  elif num == 8:
    "%s punch is blocked by %s's quick reflexes." % (attacker_name, target_name)
  elif num == 9:
    "%s is sent reeling from a punch by %s." % (target_name, attacker_name)
  elif num == 10:
    "%s lands an uppercut on %s's head." % (attacker_name, target_name)
  elif num == 11:
    "%s parrys %s's attack." % (target_name, attacker_name)
  elif num == 12:
    "%s ducks to avoid %s's punch." % (target_name, attacker_name)
  elif num == 13:
    "%s thumps %s hard in the ribs." % (attacker_name, target_name)
  elif num == 14:
    "%s elbow connects with %s's head." % (attacker_name, target_name)
  elif num == 15:
    "%s knocks the wind out of %s." % (attacker_name, target_name)
  else:
    "%s screams, then in a blurred motion attacks %s." % (attacker_name, target_name)
