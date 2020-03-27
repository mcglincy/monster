
from evennia.server.sessionhandler import SESSIONS
from commands.command import QueuedCommand


class CmdSay(QueuedCommand):
  """Speak as your character

  Usage:
    say <message>
  """
  key = "say"
  aliases = ['"', "'"]
  locks = "cmd:all()"
  help_category = "Monster"

  def inner_func(self):
    caller = self.caller

    if not self.args:
        caller.msg("Say what?")
        return

    speech = self.args

    # Calling the at_before_say hook on the character
    speech = caller.at_before_say(speech)

    # If speech is empty, stop here
    if not speech:
        return

    # Call the at_after_say hook on the character
    caller.at_say(speech, msg_self=True)


class CmdShout(QueuedCommand):
  key = "shout"
  aliases = ["sho", "shou"]  
  help_category = "Monster"

  def check_preconditions(self):
    if not self.args:
      self.caller.msg("Usage: shout <message>")
      return False

  def inner_func(self):
    message = f"{self.caller.key} shouts, \"{self.args.strip()}\""
    SESSIONS.announce_all(message)


class CmdWhisper(QueuedCommand):
  """Speak privately as your character to another

  Usage:
    whisper <character> = <message>
    whisper <char1>, <char2> = <message>

  Talk privately to one or more characters in your current location, without
  others in the room being informed.
  """
  key = "whisper"
  aliases = ["whi", "whis", "whisp", "whispe"]
  locks = "cmd:all()"
  help_category = "Monster"

  def inner_func(self):
    caller = self.caller

    # TODO: convert to monster syntax and nix the =
    if not self.lhs or not self.rhs:
      caller.msg("Usage: whisper <character> = <message>")
      return

    receivers = [recv.strip() for recv in self.lhs.split(",")]

    receivers = [caller.search(receiver) for receiver in set(receivers)]
    receivers = [recv for recv in receivers if recv]

    speech = self.rhs
    # If the speech is empty, abort the command
    if not speech or not receivers:
      return

    # Call a hook to change the speech before whispering
    speech = caller.at_before_say(speech, whisper=True, receivers=receivers)

    # no need for self-message if we are whispering to ourselves (for some reason)
    msg_self = None if caller in receivers else True
    caller.at_say(speech, msg_self=msg_self, receivers=receivers, whisper=True)


