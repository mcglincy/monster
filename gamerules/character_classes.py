import re
from gamerules.xp import set_xp
from userdefined.models import CharacterClass

def reset_character_class(target, record_id):
  set_character_class(target, record_id)
  set_xp(target, 0)


def set_character_class(target, record_id):
  try:
    # TODO make sure this is a valid class
    char_class = CharacterClass.objects.get(db_record_id=record_id)
    target.db.character_class_key = char_class.db_key
    # force re-cache
    _ = target.character_class
    if target.db.health > target.max_health:
      target.db.health = target.max_health
    if target.db.mana > target.max_mana:
      target.db.health = target.max_mana
    target.msg(f"You are now a {char_class.db_key}.")
  except Exception as err:
    target.msg(err)

# letters/spaces/hyphen/underscore, first 3 chars must be letters
VALID_NAME_REGEX = re.compile('^[a-zA-Z]{3}[a-zA-Z -_]{0,13}$')
FORBIDDEN_NAMES = ['dow', 'down', 'eas', 'east', 'nor', 'nort', 'north',
  'sou', 'sout', 'south', 'wes', 'west']

def is_valid_character_name(name):
  if not VALID_NAME_REGEX.match(name):
    return False
  # no cheater names
  if name.lower() in FORBIDDEN_NAMES:
    return False
  return True

