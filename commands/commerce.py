from commands.command import QueuedCommand
from evennia.objects.models import ObjectDB


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
    merchants = self.caller.location.search("merchant",
      candidates=self.caller.location.contents, typeclass="typeclasses.merchant.Merchant", quiet=True)
    if len(merchants) == 0 or merchants[0] is None:
      self.caller.msg("There is no merchant in this room.")
      return
    merchant = merchants[0]

    # does the merchant have that object for sale?
    objs = merchant.search(self.args.strip(), candidates=merchant.contents, quiet=True)
    if len(objs) == 0 or objs[0] is None:
      self.caller.msg("Merchant doesn't have that for sale.")
      return
    obj = objs[0]

    # does the buyer have enough gold?
    if self.caller.gold < obj.worth:
      self.caller.msg("You don't have enough gold.")
      return

    self.caller.gain_gold(-obj.worth)
    self.caller.msg(f"You buy a {obj.key} for {obj.worth} gold.")
    # copy the object directly into the caller
    ObjectDB.objects.copy_object(obj, new_key=obj.key, new_location=self.caller)


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
    obj = self.caller.search(self.args.strip(), candidates=self.caller.contents)
    if not obj:
      return

    # is there a merchant in the room?
    merchants = self.caller.location.search("merchant",
      candidates=self.caller.location.contents, typeclass="typeclasses.merchant.Merchant", quiet=True)
    if len(merchants) == 0 or merchants[0] is None:
      self.caller.msg("There is no merchant in this room.")
      return

    # is the object sellable?
    # TODO: for now allow selling 0-worth objects
    # if not obj.worth:
    #  self.caller.msg("You can't sell that.")
    #  return
    if obj.is_typeclass("typeclasses.objects.Gold"):
      self.caller.msg("You can't sell gold.")
      return

    self.caller.msg(f"You sell a {obj.key} for {obj.worth} gold.")
    self.caller.gain_gold(obj.worth)
    obj.delete()

