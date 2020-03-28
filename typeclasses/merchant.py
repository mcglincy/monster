from evennia.utils import evtable
from evennia.prototypes.spawner import spawn
from typeclasses.objects import Object


class Merchant(Object):
  def at_object_creation(self):
    super().at_object_creation()
    self.sticky = True
    spawn("axe")[0].location = self
    spawn("cudgel")[0].location = self
    spawn("dirk")[0].location = self
    spawn("iron_bar")[0].location = self
    spawn("meat_cleaver")[0].location = self
    spawn("short_sword")[0].location = self
    spawn("book_of_shadows")[0].location = self
    spawn("grand_grimoire")[0].location = self
    spawn("mabinogian")[0].location = self

  def return_appearance(self, looker, **kwargs):
    lines = []
    lines.append("")
    table = evtable.EvTable("Item", "Cost")
    for obj in self.contents:
      cost = obj.db.worth if obj.db.worth else 0
      table.add_row(obj.key, cost)
    return f"You see a merchant, hawking their wares:\n{table}"

  def at_object_receive(self, moved_obj, source_location, **kwargs):
    # only admins can give objects to merchant to go on sale
    is_admin = (source_location and source_location.account 
      and (source_location.account.check_permstring("Developer") or source_location.account.check_permstring("Admins")))
    if not is_admin:
      moved_obj.delete()
      if source_location and hasattr(source_location, "msg"):
        source_location.msg("Sweet, merchants love free stuff.")

