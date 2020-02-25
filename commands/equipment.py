from commands.command import Command


class CmdEquip(Command):
  key = "equip"
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
    self.caller.msg(f"You wield the {obj.key}.")


class CmdUnequip(Command):
  key = "unequip"
  help_category = "Monster"

  def func(self):
    obj = self.caller.search(self.args.strip(), candidates=self.caller.contents)
    if not obj:
      return

    if not obj == self.caller.db.equipped_weapon:
      self.caller.msg("Not current equipped.")
      return

    self.caller.db.equipped_weapon = None
    self.caller.msg("OK, unequipped.")
