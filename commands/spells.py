from commands.command import Command
from gamerules.hiding import find_unhidden
from gamerules.spell_effect_kind import SpellEffectKind
from gamerules.spells import can_cast_spell, cast_spell


class CmdCast(Command):
  key = "cast"
  aliases = ["cas"]
  help_category = "Monster"

  def func(self):
    # TODO: figure out rules for spellbook vs. no spellbook    
    spellbook = self.caller.equipped_spellbook
    if not spellbook:
      self.caller.msg("No spellbook equipped!")
      return

    # TODO: figure out prompting etc
    words = self.args.strip().split(" ")
    spell_name = words[0]
    spell = spellbook.find_spell(spell_name)
    if not spell:
      self.caller.msg(f"No spell found for {spell_name}!")
      return

    # TODO: need to figure out how to mix prompts and error-check-returns
    # maybe prompt for target
    # target = None
    # if spell.should_prompt:
    #   target_name = yield("At who?")
    #   self.msg("you said " + target_name)
    #   target = find_unhidden(self.caller, target_name)
    #   if not target:
    #    yield -1
    target = None
    if spell.should_prompt:
      if len(words) < 2:
        self.caller.msg(f"This spell needs a target! Usage: cast <spell> <target>")
        return
      target_name = words[1]
      target = find_unhidden(self.caller, target_name)
      if not target:
        return
      # TODO: make sure we want this not-me check... e.g., for healing spells?
      if target == self.caller:
        self.caller.msg("You can't target yourself!")
        return  

    cast_spell(self.caller, spell, target)


class CmdLearn(Command):
  key = "learn"
  aliases = ["lea", "lear"]
  help_category = "Monster"

  def func(self):
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
