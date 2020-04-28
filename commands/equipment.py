from commands.command import QueuedCommand
from commands.spells import list_spells
from gamerules.combat import find_first_attackable
from gamerules.direction import Direction
from gamerules.find import find_first
from gamerules.equipment_slot import EquipmentSlot
from gamerules.object_kind import ObjectKind
from gamerules.spells import cast_spell, first_prompt, second_prompt
from userdefined.models import Spell


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

  def __init__(self, *args, **kwargs):
    super(CmdUse, self).__init__(*args, **kwargs)
    self.obj = None
    self.spell = None

  def check_preconditions(self):
    if not self.args:
      self.caller.msg("Usage: use <obj>")
      return False
    key = self.args.strip()
    obj = find_first(self.caller, key)
    if not obj:
      self.caller.msg(f"You're not carrying {key}.")
      return False
    if obj.db.object_kind is None:
      self.caller.msg("You can't use that.")
      return False
    if (obj.db.use_object_required 
      and not find_first(self.caller, obj.db.use_object_required)):
      self.caller.msg("It doesn't work for some reason.")
      return False
    if (obj.db.use_location_required 
      and self.caller.location.key != obj.db.use_location_required):
      self.caller.msg("It doesn't work for some reason.")
      return False
    if obj.db.spell_key:
      self.spell = Spell.objects.filter(db_key=obj.db.spell_key)[0]
    self.obj = obj
    return True

  def input_prompt1(self):
    if self.spell:
      return first_prompt(self.spell)
    return None

  def input_prompt2(self):
    if self.spell:
      return second_prompt(self.spell)
    return None

  def inner_func(self):
    if self.obj.db.object_kind == ObjectKind.BLAND:
      # silently do nothing
      pass
    elif self.spell:
      # covers SCROLL, WAND, and EQUIPMENT with a spell
      use_spell(self.caller, self.obj, self.spell, self.input1, self.input2)      
    elif self.obj.db.object_kind == ObjectKind.EQUIPMENT:
      use_equipment(self.caller, self.obj)
    elif self.obj.db.object_kind == ObjectKind.MISSILE_LAUNCHER:
      use_missile_launcher(self.caller, self.obj, input1, input2)
    elif self.obj.db.object_kind == ObjectKind.SPELLBOOK:
      # same as LEARN command
      list_spells(self, self.obj)
    elif self.obj.db.object_kind == ObjectKind.BANKING_MACHINE:
      use_banking_machine(self.caller, self.obj, input1, input2)
    else:
      self.caller.msg("That object is of an unknown type.")


def use_equipment(user, obj, input1, input2):
  if object.db.spell_key:
    # j/k, cast a spell
    use_spell(user, obj, input1, input2)
  elif object.db.teleport:
    room_id = f"room_{object.db.teleport}"
    rooms = search_object(destination)
    if rooms:
      # TODO: teleport msg? XPoof()
      # Writeln(s,' vanishes from the room in a cloud of blue smoke.'
      # 'In an explosion of golden light ',s,' poofs into the room.'
      user.move_to(rooms[0])
  elif object.db.crystal_radius:
    # TODO: afaict crystalradius was never implemented in the original code
    pass
  else:
    user.msg("How the heck do you expect to be able to use that?")
  pass


def use_spell(user, obj, spell, input1, input2):
  if obj.db.charges > 0:
    do_cast(user, spell, input1, input2)
    # TODO: do the actual cast
    obj.db.charges -= 1

  if obj.db.charges < 1:
    verb = ""
    if obj.is_typeclass("typeclasses.objects.Scroll"):
      verb = "crumbles"
    elif obj.is_typeclass("typeclasses.objects.Wand"):
      verb = "shatters"
    # TODO: are there non-scroll / non-wand spell objects we need to handle?
    user.msg(f"The {obj.name} {verb} in your hands.")
    user.location.msg_contents(
      f"The {obj.name} {verb} as {user.name} drains its remaining power.",
      exclude=user)
    obj.delete()


def use_missile_launcher(user, obj, input1, input2):
  user.msg("[not implemented yet]")


def use_banking_machine(user, obj, input1, input2):
  user.msg("[not implemented yet]")


def do_cast(user, spell, input1, input2):
  try:
    target = None
    direction = None
    distance_target_key = None
    if spell.is_distance:
      direction = Direction.from_string(input1)
      distance_target_key = input2
    elif spell.should_prompt:
      key = input1
      target = find_first_attackable(user.location, key)
      if not target:
        user.msg(f"Could not find '{key}'.")
    # spells cast from items don't deduct mana
    cast_spell(user, spell, target=target, 
      direction=direction, distance_target_key=distance_target_key)
  except Exception as e:
    user.msg(e)
