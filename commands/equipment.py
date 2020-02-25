from commands.command import Command


class CmdEquip(Command):
  key = "equip"
  aliases = ["equ", "equi", "wie", "wiel", "wield", "wea", "wear"]  
  help_category = "Monster"

  def func(self):
    if not self.args:
      self.caller.msg("Usage: equip <obj>")
      return
    obj = self.caller.search(self.args.strip(), candidates=self.caller.contents)
    if not obj:
      return
    # TODO: support armor and slots
    if not obj.is_typeclass("typeclasses.objects.Weapon"):
      self.caller.msg("That's not a weapon!")
      return
    self.caller.db.equipped_weapon = obj 
    self.caller.msg(f"You equip the {obj.key}.")


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

    if not obj == self.caller.db.equipped_weapon:
      self.caller.msg("Not currently equipped.")
      return

    self.caller.db.equipped_weapon = None
    self.caller.msg(f"You unequip the {obj.key}.")
