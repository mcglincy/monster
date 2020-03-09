import re
from gamerules.xp import set_xp
from userdefined.models import CharacterClass

def reset_character_class(target, record_id):
  set_character_class(target, record_id)
  set_xp(target, 0)


def set_character_class(target, record_id):
  # make sure this is a valid class
  try:
    char_class = CharacterClass.objects.get(db_record_id=record_id)
    target.db.character_class_key = char_class.db_key
    # force re-cache
    target.character_class()
    target.msg(f"You are now a {char_class.db_key}.")
  except:
    # Show error somewhere?
    target.msg(f"Could not set character class {record_id}.")
    return


VALID_NAME_REGEX = re.compile('^[a-zA-z]{3,16}$')
FORBIDDEN_NAMES = ['dow', 'down', 'eas', 'east', 'nor', 'nort', 'north',
  'sou', 'sout', 'south', 'wes', 'west']

def is_valid_character_name(name):
  # letters only, 3-16 chars in length
  if not VALID_NAME_REGEX.match(name):
    return False
  # no cheater names
  if name.lower() in FORBIDDEN_NAMES:
    return False
  return True

