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
    # TODO: support various equipment slots
    if obj.is_typeclass("typeclasses.objects.Armor"):
      self.caller.db.equipped_armor = obj
      self.caller.msg(f"You wear the {obj.key}.")
    elif obj.is_typeclass("typeclasses.objects.Weapon"):
      self.caller.db.equipped_weapon = obj
      self.caller.msg(f"You wield the {obj.key}.")


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
    # TODO: support various equipment slots
    if obj == self.caller.db.equipped_armor:
      self.caller.db.equipped_armor = None
      self.caller.msg(f"You remove the {obj.key}.")
    elif obj == self.caller.db.equipped_weapon:
      self.caller.db.equipped_weapon = None
      self.caller.msg(f"You sheath the {obj.key}.")
    else:
      self.caller.msg("Not currently equipped.")
