from collections import Counter
from commands.command import QueuedCommand
from evennia.prototypes import prototypes as protlib, spawner



def find_attr_value(prototype, attr_name):
  for attr in prototype["attrs"]:
    (name, value, _, _) = attr
    if name == attr_name:
      return value
  return None


def has_components(caller, components):
  # components is a list of keys; turn that into a count
  component_counts = Counter(components)
  for key in component_counts.keys():
    objs = [x for x in caller.contents if x.key == key]
    if len(objs) < component_counts[key]:
      return False
  return True


def consume_first(caller, key):
  for obj in caller.contents:
    # delete first found only
    if obj.key == key:
      caller.msg(f"Consuming {obj.key}.")
      obj.delete()
      return


def consume_components(caller, components):
  for key in components:
    consume_first(caller, key)


class CmdMake(QueuedCommand):
  key = "make"
  aliases = ["mak"]
  help_category = "Monster"

  def inner_func(self):
    if not self.args:
      self.caller.msg("Make what?")
      return
    prototypes = protlib.search_prototype(key=self.args.strip())
    if not prototypes:
      self.caller.msg("No such object.")
      return
    prototype = prototypes[0]
    components = find_attr_value(prototype, "components")
    if not components:
      self.caller.msg("You can't make that.")
      return
    if not has_components(self.caller, components):
      self.caller.msg("You don't have all the components.")
      return
    consume_components(self.caller, components)
    obj = spawner.spawn(prototype['prototype_key'])[0]
    obj.location = self.caller
    self.caller.msg(f"You created {prototype['key']}.")

