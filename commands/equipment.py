from commands.command import QueuedCommand
from gamerules.find import find_first
from gamerules.equipment_slot import EquipmentSlot


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