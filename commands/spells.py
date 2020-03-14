from commands.command import Command
from gamerules.spell_effect_kind import SpellEffectKind


class CmdCast(Command):
  key = "cast"
  aliases = ["cas"]
  help_category = "Monster"

  def func(self):
    self.not_implemented_yet()


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

    spells = sorted(spellbook.spells(), key = lambda x: (x.min_level, x.key))
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
