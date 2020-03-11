import random
from gamerules.room_kind import RoomKind

def hide(hider):

  # TODO: freeze for 0.5 + hide delay

  # check for no-hide room
  room = hider.location
  if room.db.room_kind == RoomKind.NO_HIDE:
    hider.msg("There is no room to hide here.")
    return

  # check for hard-to-hide room
  if (room.db.room_kind == RoomKind.HARD_TO_HIDE
    and random.randint(0, 100) > 20):
    hider.msg("You couldn't find a place to hide.")
    return

  # check for other non-hidden occupants
  if num_unhidden_others(room, hider) > 0:
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
  if hider.ndb.hiding > hider.level():
    hider.msg("You're pretty well hidden now.  I don't think you could be any less visible.")
    return

  hider.ndb.hiding = hider.ndb.hiding + 1
  if hider.ndb.hiding > 1:
    hider.msg("You've managed to hide yourself a little better.")
  else:
    hider.msg("You've hidden yourself from view.")


def num_unhidden_others(room, hider):
  num = 0
  for obj in room.contents:
    if obj.is_typeclass("typeclasses.characters.Character") and obj != hider:
      num = num + 1
  return num


def reveal(hider):
  if hider.ndb.hiding == 0:
    hider.msg("You were not hiding.")
    return
  hider.ndb.hiding = 0
  hider.msg("You are no longer hiding.")
