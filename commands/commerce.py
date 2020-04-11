from commands.command import QueuedCommand
from evennia.objects.models import ObjectDB
from gamerules.find import find_first


def find_merchant(location):
  for obj in location.contents:
    if obj.is_typeclass("typeclasses.merchant.Merchant", exact=False):
      return obj
  return None


class CmdBuy(QueuedCommand):
  key = "buy"
  aliases = []
  locks = "cmd:all()"
  help_category = "Monster"

  def check_preconditions(self):
    if not self.args:
      self.caller.msg("Usage: buy <item>")
      return False

  def inner_func(self):
    # is there a merchant in the room?
    merchant = find_merchant(self.caller.location)
    if not merchant:
      self.caller.msg("There is no merchant in this room.")
      return

    # does the merchant have that object for sale?
    key = self.args.strip()
    obj = find_first(merchant, key)
    if not obj:
      self.caller.msg("Merchant doesn't have that for sale.")
      return

    # does the buyer have enough gold?
    if self.caller.gold < obj.worth:
      self.caller.msg("You don't have enough gold.")
      return

    # buy it!
    self.caller.gain_gold(-obj.worth)
    # copy the object directly into the caller
    ObjectDB.objects.copy_object(obj, new_key=obj.key, new_location=self.caller)
    self.caller.msg(f"You buy a {obj.key} for {obj.worth} gold.")


class CmdSell(QueuedCommand):
  key = "sell"
  aliases = ["sel"]
  locks = "cmd:all()"
  help_category = "Monster"

  def check_preconditions(self):
    if not self.args:
      self.caller.msg("Usage: sell <item>")
      return False

  def inner_func(self):
    key = self.args.strip()
    obj = find_first(self.caller, key)
    if not obj:
      self.caller.msg(f"You aren't carrying {key}.")      
      return

    # is there a merchant in the room?
    merchant = find_merchant(self.caller.location)
    if not merchant:
      self.caller.msg("There is no merchant in this room.")
      return

    # is the object sellable?
    # TODO: for now allow selling 0-worth objects
    # if not obj.worth:
    #  self.caller.msg("You can't sell that.")
    #  return
    if obj.db.cursed:
      self.caller.msg(f"The {obj.key} is cursed.")
      return   
    if obj.is_typeclass("typeclasses.objects.Gold"):
      self.caller.msg("You can't sell gold.")
      return

    sell_price = int(obj.worth / 2)
    self.caller.msg(f"You sell a {obj.key} for {sell_price} gold.")
    self.caller.gain_gold(sell_price)
    # TODO: do we want to call obj.at_drop()?
    obj.delete()

