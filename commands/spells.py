from commands.command import QueuedCommand
from evennia.utils.evmenu import get_input
from gamerules.direction import Direction
from gamerules.distance_spell_behavior import DistanceSpellBehavior
from gamerules.find import find_first_unhidden
from gamerules.special_room_kind import SpecialRoomKind
from gamerules.spell_effect_kind import SpellEffectKind
from gamerules.spells import can_cast_spell, cast_spell


class CmdCast(QueuedCommand):
  key = "cast"
  aliases = ["cas"]
  help_category = "Monster"

  def check_preconditions(self):
    if self.caller.location.is_special_kind(SpecialRoomKind.NO_COMBAT):
      self.caller.msg("You cannot fight here.")
      return False    
    # TODO: figure out rules for spellbook vs. no spellbook    
    spellbook = self.caller.equipped_spellbook
    if not spellbook:
      self.caller.msg("No spellbook equipped!")
      return False
    spell_name = self.args.strip()
    self.spell = spellbook.find_spell(spell_name)
    if not self.spell:
      self.caller.msg(f"No spell found for {spell_name}!")
      return False
    return can_cast_spell(self.caller, self.spell)

  def input_prompt1(self):
    if self.spell.is_distance:
      return "Direction?"
    elif self.spell.should_prompt:
      return "At who?"
    else:
      return None

  def input_prompt2(self):
    distance_effect = self.spell.distance_effect
    if distance_effect:
      behavior = DistanceSpellBehavior(distance_effect.db_param_4)
      if behavior != DistanceSpellBehavior.DAMAGES_ENTIRE_PATH:
        return "Person to target?"
    return None

  def pre_freeze(self):
    return self.spell.casting_time / 200.0

  def post_freeze(self):
    return self.spell.casting_time / 200.0

  def inner_func(self):
    target = None
    direction = None
    distance_target_key = None
    if self.spell.is_distance:
      direction = Direction.from_string(self.input1)
      distance_target_key = self.input2
    elif self.spell.should_prompt:
      key = self.input1
      target = find_first_unhidden(self.caller.location, key)
      if not target:
        self.caller.msg(f"Could not find '{key}'.")      
      # we check for missing target later in cast_spell(),
      # so mana etc gets deducted properly

    cast_spell(self.caller, self.spell, target=target, 
      direction=direction, distance_target_key=distance_target_key)


class CmdLearn(QueuedCommand):
  key = "learn"
  aliases = ["lea", "lear"]
  help_category = "Monster"

  def inner_func(self):
    # TODO: support spellbooks/scrolls in room
    # for now, just look at equipped spellbook
    spellbook = self.caller.equipped_spellbook
    if not spellbook:
      self.caller.msg("No spellbook equipped!")
      return

    spells = sorted(spellbook.spells, key = lambda x: (x.min_level, x.key))
    table = self.styled_table("|wSpell Name", "Level", "Mana/Lvl", "Casting Time", "Effects")
    for spell in spells:
      if spell.group and spell.group != self.caller.character_class.group:
        continue
      effects = spell.spelleffect_set.all()
      effect_names = ",".join([e.nice_name() for e in effects])
      table.add_row(
        spell.key, 
        spell.min_level,
        f"{spell.mana}/{spell.level_mana}",
        spell.casting_time,
        effect_names,
      )
    self.msg(f"{table}")
