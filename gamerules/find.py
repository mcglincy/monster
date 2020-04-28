

def keymatch(obj, key):
  return obj.key.lower().startswith(key.lower())


def is_hidden(obj):
  return hasattr(obj, "is_hiding") and obj.is_hiding


def find_first(container, key):
  for obj in container.contents:
    if keymatch(obj, key):
      return obj
  return None


def find_first_unhidden(container, key):
  for obj in container.contents:
    if keymatch(obj, key) and not is_hidden(obj):
      return obj
  return None


def find_all_unhidden(container, key=None):
  if key:
    return [x for x in container.contents if keymatch(x, key) and not is_hidden(x)]
  else:
    return [x for x in container.contents if not is_hidden(x)]


def find_exit(location, direction):
  if direction is not None and direction != Direction.INVALID:
    for x in location.contents:
      if (x.is_typeclass("typeclasses.exits.Exit", exact=False) 
        and x.key.lower() == direction.name.lower()):
        return x
  return None