from evennia.server.sessionhandler import SESSIONS


def msg_global(message):
  """Send msg to all connected sessions."""
  # TODO: do we want to use public (or global) channel instead?
  if not message.startswith("|"):
    message = "|w" + message
  SESSIONS.announce_all(message)
