"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from random import randint
from evennia import DefaultCharacter, search_object
from evennia.commands import cmdhandler
from commands.combat import target_msg
from typeclasses.health import health_msg


def level_from_xp(xp):
  return int(xp / 1000)


# [GLOBAL]
# PROCEDURE DieChangeExperience(Th : INTEGER; My : INTEGER; VAR Stat : StatType);
# VAR
#   Mylevel, R : INTEGER;
# BEGIN
#   Th := Th DIV 1000;  (* making it the level, not the exp *)
#   Mylevel := My DIV 1000;
#   IF (Mylevel = 0) OR (Mylevel < Th) THEN
#   BEGIN
#     IF (((TH/2) + 1.5 - Mylevel) > 0) THEN
#       R := Round(1000*((Th/2) + 1.5 - Mylevel))
#     ELSE R := Round(1000*(1/(Mylevel+(Mylevel-th))));
#   END
#   ELSE
#   BEGIN
#     IF (Mylevel >= Th) AND (Mylevel < 10) AND ((Mylevel - Th) < 3)THEN
#       R := Round(1000*(1/(Mylevel+(Mylevel-Th))))
#    ELSE
#      R := 0;
#    END;
#    ChangeExp(R, Stat.Log, Stat.Experience);
# END;
def kill_xp(killer_xp, victim_xp):
  killer_level = level_from_xp(killer_xp)
  victim_level = level_from_xp(victim_xp)
  levels_above = killer_level - victim_level
  amt = 0
  if killer_level == 0 or killer_level < victim_level:
    multiplier = (victim_level / 2) + 1.5 - killer_level
    if multiplier < 0:
      multiplier = 1 / (killer_level + levels_above)
    amt = int(round(1000 * multiplier))
  elif killer_level >= victim_level and killer_level < 10 and levels_above < 3:
    amt = int(round(1000 * (1 / (killer_level + levels_above))))
  return amt


class Character(DefaultCharacter):
  """
  The Character defaults to reimplementing some of base Object's hook methods with the
  following functionality:

  at_basetype_setup - always assigns the DefaultCmdSet to this object type
                (important!)sets locks so character cannot be picked up
                and its commands only be called by itself, not anyone else.
                (to change things, use at_object_creation() instead).
  at_after_move(source_location) - Launches the "look" command after every move.
  at_post_unpuppet(account) -  when Account disconnects from the Character, we
                store the current location in the pre_logout_location Attribute and
                move it to a None-location so the "unpuppeted" character
                object does not need to stay on grid. Echoes "Account has disconnected"
                to the room.
  at_pre_puppet - Just before Account re-connects, retrieves the character's
                pre_logout_location Attribute and move it back on the grid.
  at_post_puppet - Echoes "AccountName has entered the game" to the room.

  """
  def at_object_creation(self):
    """Called at initial creation."""
    super().at_object_creation()
    self.set_field_defaults()

  def set_field_defaults(self):
    """Set various field defaults in an idempotent way."""
    # TODO: figure health etc from level and class
    if self.db.max_health is None:
      self.db.max_health = 1000
    if self.db.health is None:
      self.db.health = 1000
    if self.db.brief_descriptions is None:
      self.db.brief_descriptions = False      
    # TODO: support various equipment slots
    # checking None to set None is pointless
    if not self.db.equipped_weapon:
      self.db.equipped_weapon = None
    if not self.db.equipped_armor:
      self.db.equipped_armor = None
    if self.db.gold_in_bank is None:
      self.db.gold_in_bank = 0
    if self.db.xp is None:
      self.db.xp = 1000

  def execute_cmd(self, raw_string, session=None, **kwargs):
    """Support execute_cmd(), like account and object."""
    return cmdhandler.cmdhandler(
        self, raw_string, callertype="account", session=session, **kwargs
    )

  def at_after_move(self, source_location, **kwargs):
    # override to apply our brief descriptions setting
    if self.location.access(self, "view"):
      self.msg(self.at_look(self.location, brief=self.db.brief_descriptions))

  def at_object_leave(self, obj, target_location):
    # called when an object leaves this object in any fashion
    super().at_object_leave(obj, target_location)
    # unequip if equipped
    if obj == self.db.equipped_armor:
      self.db.equipped_armor = None
    elif obj == self.db.equipped_weapon:
      self.db.equipped_weapon = None

  def at_weapon_hit(self, attacker, weapon, damage):
    self.msg(target_msg(attacker.key, weapon.key, damage))
    # TODO: apply armor
    armor = self.db.equipped_armor
    if armor:
      if armor.db.deflect_armor > 0 and randint(0, 100) < armor.db.deflect_armor:
        self.msg("The attack is deflected by your armor.")
        attacker.msg(f"Your weapon is deflected by {self.key}'s armor.")
        damage = int(damage / 2)
      if armor.db.base_armor > 0:
        self.msg("The attack is partially blocked by your armor.")
        attacker.msg(f"Your weapon is partially blocked by {self.key}'s armor.")
        damage = int(damage * ((100 - armor.db.base_armor) / 100))
    self.at_damage(damage, causer=attacker)

  def at_damage(self, damage, causer=None):
    self.db.health = max(self.db.health - damage, 0)
    self.msg(f"You take {damage} damage.")
    self.msg(health_msg("You", self.db.health))
    self.location.msg_contents(health_msg(self.key, self.db.health), exclude=[self])
    if self.db.health <= 0:
      self.die(causer)

  def at_heal(self, amount):
    self.db.health = min(self.db.health + amount, self.db.max_health)
    self.msg(health_msg("You", self.db.health))
    self.location.msg_contents(health_msg(self.key, self.db.health), exclude=[self])

  def carried_gold_amount(self):
    gold = self.search("gold",
      candidates=self.contents, typeclass="typeclasses.objects.Gold", quiet=True)
    if len(gold) > 0:
      return gold[0].db.amount
    return 0

  def at_kill(self, deceased):
    self.msg(f"You killed {deceased.key}!")
    xp = kill_xp(self.db.xp, deceased.db.xp)
    self.at_gain_xp(xp)

  def die(self, causer=None):
    # drop everything we're holding
    for obj in self.contents:
      if obj.db.worth:
        # only drop things with value
        # TODO: possible destroy chance?
        self.execute_cmd(f"drop {obj.key}")
      else:
        # nuke worthless objects
        obj.delete()

    the_void = search_object("Void")[0]
    if the_void:
      self.move_to(the_void)

    if causer and hasattr(causer, "at_kill"):
      causer.at_kill(self)

    self.db.health = 200
    self.at_set_xp(int(self.db.xp / 2))

  def level(self):
    return level_from_xp(self.db.xp)

  def classname(self):
    # TODO: pull from character class
    return "Peasant"

  def at_gain_xp(self, xp):
    new_xp = max(1000, self.db.xp + xp)
    self.at_set_xp(new_xp)

  def at_set_xp(self, new_xp):
    old_level = self.level()
    self.db.xp = new_xp
    new_level = self.level()
    if old_level != new_level:
      self.msg(f"You are now level {new_level}.")

