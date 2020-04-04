import random
from gamerules.special_room_kind import SpecialRoomKind


MAX_HIDE = 15


def evennia_hide(obj):
  obj.locks.remove("view")
  # TODO: refactor permissions into an enum?
  obj.locks.add("view:perm(see_hidden)")


def evennia_unhide(obj):
  obj.locks.remove("view")
  obj.locks.add("view:all()")


def unhidden_objects(location):
  return [x for x in location.contents if not hasattr(x, "is_hiding") or not x.is_hiding]


def unhidden_object(location, key):
  unhidden = [
    x for x in location.contents if not hasattr(x, "is_hiding") or not x.is_hiding]
  for x in unhidden:
    if x.key.lower().startswith(key.lower()):
      return x
  return None


def unhidden_others(hider):
  unhidden = []
  for obj in hider.location.contents:
    if ((obj.is_typeclass("typeclasses.characters.Character")
        and obj != hider
        and not obj.is_hiding)
      or obj.is_typeclass("typeclasses.mobs.Mob", exact=False)
      or obj.is_typeclass("typeclasses.merchant.Merchant", exact=False)):
      unhidden.append(obj)
  return unhidden


def num_unhidden_others(hider):
  num = 0
  for obj in hider.location.contents:
    if ((obj.is_typeclass("typeclasses.characters.Character")
        and obj != hider
        and not obj.is_hiding)
      or obj.is_typeclass("typeclasses.mobs.Mob", exact=False)
      or obj.is_typeclass("typeclasses.merchant.Merchant", exact=False)):
      num = num + 1
  return num


def find_unhidden(searcher, key):
  unhidden = [
    x for x in searcher.location.contents if not hasattr(x, "is_hiding") or not x.is_hiding]
  for x in unhidden:
    if x.key.lower().startswith(key.lower()):
      return x
  searcher.msg(f"Could not find '{key}'.")
  return None


def hide_object(hider, obj):
  if (hider.location.is_special_kind(SpecialRoomKind.MARKET)
    and not hider.account.is_superuser):
    hider.msg("You can't hide that here.")
    return

  if unhidden_others(hider):
    hider.msg("You can't hide things when people are watching you.")
    return

  obj.db.hiding = 1
  evennia_hide(obj)
  hider.msg(f"You have hidden {obj.key}.")


def hide(hider):
  # TODO: freeze for 0.5 + hide delay

  # check for no-hide room
  room = hider.location
  if room.is_special_kind(SpecialRoomKind.NO_HIDE):
    hider.msg("There is no room to hide here.")
    return

  # check for hard-to-hide room
  if (room.is_special_kind(SpecialRoomKind.HARD_TO_HIDE)
    and random.randint(0, 100) > 20):
    hider.msg("You couldn't find a place to hide.")
    return

  # check for other non-hidden occupants
  if unhidden_others(hider):
    if hider.ndb.hiding > 0:
      hider.msg("You can't hide any better with people in the room.")
    else:
      hider.msg("You can't hide when people are watching you.")
    return

  if random.randint(0, 100) < 25:
    # hide fail
    if hider.ndb.hiding > 0:
      hider.msg("You could not find a better hiding place.")
    else:
      hider.msg("You could not find a good hiding place.")
    return

  # hide success! increase hiding amount, maybe

  # you can hide up to your level + 1
  if hider.ndb.hiding > hider.level:
    hider.msg("You're pretty well hidden now.  I don't think you could be any less visible.")
    return

  hider.ndb.hiding = hider.ndb.hiding + 1
  if hider.ndb.hiding > 1:
    hider.msg("You've managed to hide yourself a little better.")
  else:
    evennia_hide(hider)
    hider.msg("You've hidden yourself from view.")


def reveal(hider):
  if hider.ndb.hiding == 0:
    hider.msg("You were not hiding.")
    return
  hider.ndb.hiding = 0
  evennia_unhide(hider)
  hider.msg("You are no longer hiding.")
  hider.location.msg_contents(f"{hider.key} has stepped out of the shadows.", exclude=[hider])


def reveal_object(obj):
  obj.db.hiding = 0
  evennia_unhide(obj)


def search(searcher):
  searcher.location.msg_contents(
    f"{searcher.key} seems to be looking for something.", exclude=[searcher])
  rand = random.randint(0, 100)
  room = searcher.location
  found = False
  if rand < 20:
    found = reveal_objects(searcher)
  elif rand < 40:
    found = reveal_exits(searcher)
  else:
    found = reveal_people(searcher)

  if not found:
    searcher.msg("You haven't found anything.")
  #searcher.location.msg_contents(f"{searcher.key} appears to have found something.", exclude=[searcher])
  

def reveal_objects(searcher):
  for obj in searcher.location.contents:
    if obj.is_typeclass("typeclasses.objects.Object", exact=False) and obj.is_hiding:
      searcher.msg(f"You found {obj.name}.")
      reveal_object(obj)
      # only find one object at a time
      return True
  return False


def reveal_exits(searcher):
  # TODO
  return False


def reveal_people(searcher):
  # TODO: this logic is a bit wacko
  characters = [
    x for x in searcher.location.contents if x.is_typeclass("typeclasses.characters.Character")]
  for retry in range(0, 7):
    picked = random.choice(characters)
    if (picked != searcher and picked.is_hiding
      and random.randint(0, MAX_HIDE) > picked.ndb.hiding):
      picked.ndb.hiding = 0
      evennia_unhide(picked)
      searcher.msg(f"You've found {picked.key} hiding in the shadows!")
      picked.msg(f"You've been discovered by {searcher.key}!")
      searcher.location.msg_contents(
        f"{searcher.key} has found {picked.key} hiding in the shadows!", exclude=[searcher, picked])
      return True
  return False
