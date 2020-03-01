from gamerules.xp import set_xp
from userdefined.models import CharacterClass


def reset_character_class(target, character_class_key):
  set_character_class(target, character_class_key)
  set_xp(target, 0)


def set_character_class(target, character_class_key):
  # make sure this is a valid class
  try:
    char_class = CharacterClass.objects.get(db_key=self.db.character_class_key)
  except:
    # Show error somewhere?
    target.msg(f"There is no character class {character_class_key}.")
    return
  target.db.character_class_name = exit_effect_value
  # force re-cache
  target.character_class()
  target.msg(f"You are now a {character_class_key}.")


