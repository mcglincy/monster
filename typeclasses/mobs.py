import random
from gamerules.combat import mob_death
from gamerules.health import health_msg, MIN_HEALTH
from gamerules.mob_kind import MobKind
from typeclasses.objects import Object


class Mob(Object):
  def at_object_creation(self):
    super().at_object_creation()
    # self.db.record_id
    # self.db.kind = MobKind.FIGHTER
    # self.db.min_level = 0
    # self.db.group = 0
    # self.db.size = 0
    # self.db.xp = 0
    # self.db.drop_gold = 0
    # self.db.drop_object_id = 0
    # self.db.base_health = 0
    # self.db.random_health = 0
    # self.db.level_health = 0
    # self.db.base_mana = 0
    # self.db.level_mana = 0
    # self.db.base_damage = 0
    # self.db.random_damage = 0
    # self.db.level_damage = 0
    # self.db.armor = 0
    # self.db.spell_armor = 0
    # self.db.move_speed = 0
    # self.db.attack_speed = 0
    # self.db.heal_speed = 0
    # self.db.weapon_id = 0
    # self.db.weapon_use = 0
    # self.db.level_weapon_use = 0
    # self.db.pursuit_chance = 0
    # self.db.spell_ids = []
    # self.db.sayings = []

  def basetype_posthook_setup(self):
    # overriding this so we can do some post-init
    # after spawning, as BaseObject.at_first_save() applies _create_dict field values
    # *after* calling at_object_creation()
    super().basetype_posthook_setup()
    # TODO: what about level_health and level_mana? do mobs have a level?
    self.db.max_health = self.db.base_health + random.randint(0, self.db.random_health)
    self.db.health = self.db.max_health
    self.db.max_mana = self.db.base_mana
    self.db.mana = self.db.max_mana

  def gain_health(self, amount, damager=None, weapon_name=None):
    self.db.health = max(MIN_HEALTH, min(self.db.max_health, self.db.health + amount))
    if self.db.health <= 0:
      mob_death(self, damager)
    else:
      # tell everyone else in the room our health
      self.location.msg_contents(health_msg(self.key, self.db.health), exclude=[self])

  @property
  def base_armor(self):
    return self.db.armor

  @property
  def deflect_armor(self):
    return 0

  @property
  def spell_armor(self):
    return self.db.spell_armor

  @property
  def spell_deflect_armor(self):
    return 0
  

