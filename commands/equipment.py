from commands.command import Command
from typeclasses.equipment_slot import EquipmentSlot


class CmdEquip(Command):
  key = "equip"
  aliases = ["equ", "equi", "wie", "wiel", "wield", "wea", "wear"]  
  help_category = "Monster"

  def func(self):
    if not self.args:
      # TODO: show equipped?      
      # self.caller.msg("Usage: equip <obj>")
      self.show_currently_equipped()
      return
    obj = self.caller.search(self.args.strip(), candidates=self.caller.contents)
    if not obj:
      return
    self.caller.msg(obj)
    # if obj.is_typeclass("typeclasses.objects.Equipment"):
    if obj.db.equipment_slot:
      # TODO: show what slot it's equipped to?
      self.caller.msg(f"You equip the {obj.key}.")
      self.caller.db.equipment[obj.db.equipment_slot] = obj

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
    if obj.db.equipment_slot in self.caller.db.equipment:
      del self.caller.db.equipment[obj.db.equipment_slot]
      self.caller.msg(f"You unequip the {obj.key}.")
    else:
      self.caller.msg("Not currently equipped.")
