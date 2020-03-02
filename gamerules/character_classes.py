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