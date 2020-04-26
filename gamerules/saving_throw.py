

def make_saving_throw(target, save_name):
  # TODO: original monster save % is MyExperience DIV 1000, aka 1% per level...
  # but that code also checks if >80, which would never happen. WTF?
  # Maybe it was supposed to be 10% per level? or max 8%?
  chance_to_save = target.level
  if random.randint(0, 100) <= chance_to_save:
    target.msg(f"You resisted the {save_name}.")
    target.location.msg_contents(
      f"{target.ket} resisted the {save_name}.", exclude=[target])
    return True
  return False
