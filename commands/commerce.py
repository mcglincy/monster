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
      candidates=self.caller.location.contents, typeclass="typeclasses.objects.Merchant", quiet=True)
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

    worth = obj.db.worth if obj.db.worth else 0
    # TODO: does buyer have enough gold?

    # TODO: take buyer gold
    # seller.take_gold(worth)
    self.caller.msg(f"You buy a {obj.key} for {worth} gold.")
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
      candidates=self.caller.location.contents, typeclass="typeclasses.objects.Merchant", quiet=True)
    if len(merchants) == 0 or merchants[0] is None:
      self.caller.msg("There is no merchant in this room.")
      return

    # check object type to make sure it's sellable
    #if not obj.db.worth:
    #  self.caller.msg("You can't sell that.")
    #  return
    if obj.key == "gold":
      self.caller.msg("You can't sell gold.")
      return

    worth = obj.db.worth if obj.db.worth else 0
    self.caller.msg(f"You sell a {obj.key} for {worth} gold.")

    # TODO: give seller gold
    # seller.give_gold(worth)

    obj.delete()

