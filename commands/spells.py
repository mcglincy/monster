from commands.command import QueuedCommand
from evennia.utils.evmenu import get_input
from gamerules.combat import find_first_attackable
from gamerules.direction import Direction
from gamerules.distance_spell_behavior import DistanceSpellBehavior
from gamerules.special_room_kind import SpecialRoomKind
from gamerules.spell_effect_kind import SpellEffectKind
from gamerules.spells import can_cast_spell, do_cast, first_prompt, second_prompt


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
    return first_prompt(self.spell)

  def input_prompt2(self):
    return second_prompt(self.spell)

  def pre_freeze(self):
    return self.spell.casting_time / 200.0

  def post_freeze(self):
    return self.spell.casting_time / 200.0

  def inner_func(self):
    do_cast(self.caller, self.spell, self.input1, self.input2,
      deduct_mana=True)


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
    list_spells(self, spellbook)


def list_spells(cmd, spellbook):
  # TODO: this function only takes command so we can use cmd.styled_table
  spells = sorted(spellbook.spells, key = lambda x: (x.min_level, x.key))
  table = cmd.styled_table("|wSpell Name", "Level", "Mana/Lvl", "Casting Time", "Effects")
  for spell in spells:
    if spell.group and spell.group != cmd.caller.character_class.group:
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
  cmd.msg(f"{table}")
