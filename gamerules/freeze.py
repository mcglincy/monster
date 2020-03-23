import time
from evennia import create_script
from commands.command import do_next_queued_command


def freeze(target, duration):
  now = time.time()
  # TODO: do we want to make freeze additive?
  # i.e., see how much exiting (frozen_until - now) is remaining?
  # that would affect both frozen_util and the needed script duration
  # if frozen_until > now:
  #   frozen_until = frozen_until + duration
  #   unfreeze_delay = (frozen_util - now) + duration
  # else:
  #   frozen_until = now + duration
  #   unfreeze_delay = duration
  target.ndb.frozen_until = now + duration
  target.msg("You cannot move!")
  target.location.msg_contents(f"{target.key} is frozen.", exclude=[target])

  # remove any existing unfreeze script
  for script in target.scripts.all():
    if script.key == "unfreeze":
      script.stop()

  # add a new unfreeze
  create_script("typeclasses.scripts.DelayedUnfreeze", obj=target, interval=duration)


def unfreeze(target):
  # usually this will be called from the one-shot Unfreeze script,
  # so no need to clean up scripts
  if target.ndb.frozen_until:
    target.ndb.frozen_until = 0
    target.msg("You can move again.")
    target.location.msg_contents(f"{target.key} is moving again.", exclude=[target])
    # start next command, if any
    do_next_queued_command(target)
