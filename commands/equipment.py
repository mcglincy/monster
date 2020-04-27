from commands.command import QueuedCommand
from commands.spells import list_spells
from gamerules.find import find_first
from gamerules.equipment_slot import EquipmentSlot
from gamerules.object_kind import ObjectKind


class CmdEquip(QueuedCommand):
  key = "equip"
  aliases = ["equ", "equi", "wie", "wiel", "wield", "wea", "wear"]  
  help_category = "Monster"

  def inner_func(self):
    if not self.args:
      self.show_currently_equipped()
      return
    key = self.args.strip()
    obj = find_first(self.caller, key)
    if not obj:
      self.caller.msg(f"You're not carrying {key}.")
      return
    self.caller.equip(obj)

  def show_currently_equipped(self):
    if not self.caller.db.equipment:
      self.msg("Nothing equipped.")
      return
    table = self.styled_table("|wSlot", "Equipped Item")
    for slot in EquipmentSlot:
      if slot in self.caller.db.equipment and self.caller.db.equipment[slot] is not None:
        table.add_row(slot.name, self.caller.db.equipment[slot].key)
    self.msg(f"{table}")


class CmdUnequip(QueuedCommand):
  key = "unequip"
  aliases = ["une", "uneq", "unequ", "unequi"] 
  help_category = "Monster"

  def inner_func(self):
    if not self.args:
      self.caller.msg("Usage: unequip <obj>")
      return
    key = self.args.strip()
    obj = find_first(self.caller, key)
    if not obj:
      self.caller.msg(f"You're not carrying {key}.")
      return
    if obj.db.cursed:
      self.caller.msg(f"The {obj.key} is cursed.")
      return
    self.caller.unequip(obj)


class CmdUse(QueuedCommand):
  key = "use"
  help_category = "Monster"

  def inner_func(self):
    if not self.args:
      self.caller.msg("Usage: use <obj>")
      return
    key = self.args.strip()
    obj = find_first(self.caller, key)
    if not obj:
      self.caller.msg(f"You're not carrying {key}.")
      return
    if obj.db.object_kind is None:
      self.caller.msg("You can't use that.")
    elif obj.db.object_kind == ObjectKind.BLAND:
      # silently do nothing
      pass
    elif obj.db.object_kind == ObjectKind.EQUIPMENT:
      use_equipment(user, obj)
    elif obj.db.object_kind == ObjectKind.SCROLL:
      use_spell(user, obj)
    elif obj.db.object_kind == ObjectKind.WAND:
      use_spell(user, obj)
    elif obj.db.object_kind == ObjectKind.MISSILE_LAUNCHER:
      self.caller.msg("[not implemented yet]")
    elif obj.db.object_kind == ObjectKind.SPELLBOOK:
      # same as LEARN command
      list_spells(self, obj)
    elif obj.db.object_kind == ObjectKind.BANKING_MACHINE:
      self.caller.msg("[not implemented yet]")
    else:
      self.caller.msg("That object is of an unknown type.")
# "It doesn't work for some reason."


def use_equipment(user, obj):
  pass


def use_spell(user, obj):
  pass

