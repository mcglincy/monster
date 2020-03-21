from commands.command import QueuedCommand
from evennia.utils.evmenu import get_input
from gamerules.hiding import find_unhidden
from gamerules.spell_effect_kind import SpellEffectKind
from gamerules.spells import can_cast_spell, cast_spell


def _target_callback(caller, prompt, target_name):
  target = find_unhidden(caller, target_name)
  if not target:
    return

  # TODO: make sure we want this not-me check... e.g., for healing spells?
  # if target == caller:
  #   caller.msg("You can't target yourself!")
  #   return

  if caller.ndb.active_spell:
    cast_spell(caller, caller.ndb.active_spell, target)


class CmdCast(QueuedCommand):
  key = "cast"
  aliases = ["cas"]
  help_category = "Monster"

  def check_preconditions(self):
    # TODO: figure out rules for spellbook vs. no spellbook    
    spellbook = self.caller.equipped_spellbook
    if not spellbook:
      self.caller.msg("No spellbook equipped!")
      return False
    spell_name = self.args.strip()
    spell = spellbook.find_spell(spell_name)
    if not spell:
      self.caller.msg(f"No spell found for {spell_name}!")
      return False
    return can_cast_spell(self.caller, spell)

  def inner_func(self):
    spellbook = self.caller.equipped_spellbook
    spell_name = self.args.strip()
    spell = spellbook.find_spell(spell_name)
    if spell.should_prompt:
      # stash the spell on the caster, for use from the callback
      self.caller.ndb.active_spell = spell
      get_input(self.caller, "At who?", _target_callback)
    else:
      cast_spell(self.caller, spell, target=None)


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
