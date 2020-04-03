from evennia import create_object

STARTING_GOLD_AMOUNT = 50

def give_starting_gold(character):
  gold = create_object("typeclasses.objects.Gold", key="gold")
  gold.add(STARTING_GOLD_AMOUNT)
  # use move_to() so we invoke StackableObject accumulation
  gold.move_to(character, quiet=True)
  character.msg(f"You now have {gold.db.amount} gold.")