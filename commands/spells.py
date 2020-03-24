from commands.command import QueuedCommand
from evennia.utils.evmenu import get_input
from gamerules.distance_spell_behavior import DistanceSpellBehavior
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
  target = None

  def check_preconditions(self):
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

  def input_prompt(self):
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
    distance_target_name = None
    if self.spell.is_distance:
      direction = self.input.lower()
      if direction not in ["n", "north", "s", "south", "e", "east", 
        "w", "west", "u", "up", "d", "down"]:
        self.caller("Not a valid direction.")
        return
      distance_target_name = self.input2
    elif self.spell.should_prompt:
      target = find_unhidden(self.caller, self.input)
      # we check for missing target later in cast_spell(),
      # so mana etc gets deducted properly

    cast_spell(self.caller, self.spell, target=target, 
      direction=direction, distance_target_name=distance_target_name)


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
