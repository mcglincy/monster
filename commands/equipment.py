from commands.command import Command
from typeclasses.equipment_slot import EquipmentSlot


class CmdEquip(Command):
  key = "equip"
  aliases = ["equ", "equi", "wie", "wiel", "wield", "wea", "wear"]  
  help_category = "Monster"

  def func(self):
    if not self.args:
      self.show_currently_equipped()
      return
    obj = self.caller.search(self.args.strip(), candidates=self.caller.contents)
    if not obj:
      return
    self.caller.equip(obj)

  def show_currently_equipped(self):
    if not self.caller.db.equipment:
      self.msg("Nothing equipped.")
      return
    table = self.styled_table("|wSlot", "Equipped Item")
    for slot in EquipmentSlot:
      if slot in self.caller.db.equipment:
        table.add_row(slot.name, self.caller.db.equipment[slot].key)
    self.msg(f"{table}")


class CmdUnequip(Command):
  key = "unequip"
  aliases = ["une", "uneq", "unequ", "unequi"] 
  help_category = "Monster"

  def func(self):
    if not self.args:
      self.caller.msg("Usage: unequip <obj>")
      return
    obj = self.caller.search(self.args.strip(), candidates=self.caller.contents)
    if not obj:
      return
    self.caller.unequip(obj)