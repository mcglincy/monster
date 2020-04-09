from django.db import models
from evennia.utils.idmapper.models import SharedMemoryModel
from gamerules.spell_effect_kind import SpellEffectKind


class CharacterClass(SharedMemoryModel):
  # original pascal record id / index
  db_record_id = models.PositiveSmallIntegerField(db_index=True)
  # human readable key (name)
  db_key = models.CharField(max_length=32, db_index=True, unique=True)
  # name to display on the who command table
  db_who_name = models.CharField(blank=False, null=False, max_length=16)
  db_group = models.PositiveSmallIntegerField(default=0, blank=0)
  db_size = models.PositiveSmallIntegerField(default=0, blank=0)
  db_alignment = models.PositiveSmallIntegerField(default=0, blank=0)
  db_move_speed = models.PositiveSmallIntegerField(default=0, blank=0)
  db_attack_speed = models.PositiveSmallIntegerField(default=0, blank=0)
  db_heal_speed = models.PositiveSmallIntegerField(default=0, blank=0)  
  db_hide_delay = models.PositiveSmallIntegerField(default=0, blank=0)
  db_base_health = models.PositiveSmallIntegerField(default=0, blank=0)
  db_level_health = models.PositiveSmallIntegerField(default=0, blank=0)
  db_base_mana = models.PositiveSmallIntegerField(default=0, blank=0)
  db_level_mana = models.PositiveSmallIntegerField(default=0, blank=0)
  db_base_weapon_use = models.PositiveSmallIntegerField(default=0, blank=0)
  db_level_weapon_use = models.PositiveSmallIntegerField(default=0, blank=0)
  db_base_claw_damage = models.PositiveSmallIntegerField(default=0, blank=0)
  db_level_claw_damage = models.PositiveSmallIntegerField(default=0, blank=0)
  db_random_claw_damage = models.PositiveSmallIntegerField(default=0, blank=0)
  db_base_steal = models.PositiveSmallIntegerField(default=0, blank=0)
  db_level_steal = models.PositiveSmallIntegerField(default=0, blank=0)
  db_base_move_silent = models.PositiveSmallIntegerField(default=0, blank=0)
  db_level_move_silent = models.PositiveSmallIntegerField(default=0, blank=0)
  db_armor = models.PositiveSmallIntegerField(default=0, blank=0)
  db_spell_armor = models.PositiveSmallIntegerField(default=0, blank=0)
  db_hear_noise = models.PositiveSmallIntegerField(default=0, blank=0)
  db_poison_chance = models.PositiveSmallIntegerField(default=0, blank=0)
  # shadow damager percent can also be negative
  db_shadow_damage_percent = models.SmallIntegerField(default=0, blank=0)
  # fields to add later, maybe:
  # How well can it control its actions
  # control = models.PositiveSmallIntegerField(default=0, blank=0)
  # my_void = models.CharField(blank=False, null=True, max_length=32)


class Spell(SharedMemoryModel):
  # original pascal record id / index
  db_record_id = models.PositiveSmallIntegerField(db_index=True)
  # human readable key (name)
  db_key = models.CharField(max_length=32, db_index=True, unique=True)
  db_mana = models.PositiveSmallIntegerField(default=0, blank=0)
  db_level_mana = models.PositiveSmallIntegerField(default=0, blank=0)
  db_caster_desc = models.CharField(blank=True, null=True, max_length=256)
  db_victim_desc = models.CharField(blank=True, null=True, max_length=256)
  db_room_desc = models.CharField(blank=True, null=True, max_length=256)
  db_alignment = models.PositiveSmallIntegerField(default=66, blank=66)
  db_failure_desc = models.CharField(blank=True, null=True, max_length=256)
  db_min_level = models.PositiveSmallIntegerField(default=0, blank=0)
  db_class_id = models.PositiveSmallIntegerField(default=0, blank=0)
  db_group = models.PositiveSmallIntegerField(default=0, blank=0)
  db_room = models.PositiveSmallIntegerField(default=0, blank=0)
  db_failure_chance = models.PositiveSmallIntegerField(default=0, blank=0)
  db_casting_time = models.PositiveSmallIntegerField(default=0, blank=0)
  # object key/name
  db_object_required = models.CharField(blank=False, null=True, max_length=32)
  db_object_consumed = models.BooleanField(default=False)
  db_silent = models.BooleanField(default=False)
  db_reveals = models.BooleanField(default=False)
  db_memorize = models.BooleanField(default=False)
  db_command = models.CharField(blank=True, null=True, max_length=32)
  db_command_priv = models.BooleanField(default=False)

  # Room    :INTEGER;       (* Where do I have to be to cast it *)
  # Extra1, Extra2, Extra3 : INTEGER;

  @property
  def effects(self):
    return self.spelleffect_set.all()

  @property
  def should_prompt(self):
    for effect in self.effects:
      if effect.target_prompt:
        return True
    return False

  @property
  def affects_room(self):
    for effect in self.effects:
      if effect.affects_room:
        return True
    return False

  @property
  def is_distance(self):
    return self.distance_effect is not None

  @property
  def distance_effect(self):
    # TODO: this assumes that a special can only have one distance effect
    for effect in self.effects:
      if effect.effect_kind == SpellEffectKind.DISTANCE_HURT:
        return effect
    return None


class SpellEffect(SharedMemoryModel):
  spell = models.ForeignKey(Spell, on_delete=models.CASCADE)  
  db_effect_kind = models.SmallIntegerField(default=0, blank=0, choices = [(k.value, k.name) for k in SpellEffectKind])
  db_affects_room = models.BooleanField(default=False)
  db_affects_caster = models.BooleanField(default=False)
  db_target_prompt = models.BooleanField(default=False)
  db_param_1 = models.SmallIntegerField(default=0, blank=0)
  db_param_2 = models.SmallIntegerField(default=0, blank=0)
  db_param_3 = models.SmallIntegerField(default=0, blank=0)
  db_param_4 = models.SmallIntegerField(default=0, blank=0)
  
  def nice_name(self):
    effect_name = SpellEffectKind(self.db_effect_kind).name
    if self.db_affects_room:
      effect_name = "GROUP_" + effect_name
    return effect_name.replace("_", " ").lower()
