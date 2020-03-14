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
  db_caster_desc = models.CharField(blank=False, null=True, max_length=256)
  db_victim_desc = models.CharField(blank=False, null=True, max_length=256)
  db_alignment = models.PositiveSmallIntegerField(default=0, blank=0)
  db_failure_desc = models.CharField(blank=False, null=True, max_length=256)
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

  # Room    :INTEGER;       (* Where do I have to be to cast it *)
  # Command :String;  (* Command to execute *)
  # CommandPriv :BYTE_BOOL; (* Execute it with Privs? *)
 #   Extra1, Extra2, Extra3 : INTEGER;

  # room: 0,
  # command: ""
  # command_priv: false,
  # extra1: 0,
  # extra2: 0,
  # extra3: 0,


class SpellEffect(SharedMemoryModel):
  spell = models.ForeignKey(Spell, on_delete=models.CASCADE)  
  db_effect_kind = models.CharField(max_length=16, choices = [(k, k.value) for k in SpellEffectKind])
  db_affects_room = models.BooleanField(default=False)
  db_affects_caster = models.BooleanField(default=False)
  db_target_prompt = models.BooleanField(default=False)
  db_param_1 = models.SmallIntegerField(default=0, blank=0)
  db_param_2 = models.SmallIntegerField(default=0, blank=0)
  db_param_3 = models.SmallIntegerField(default=0, blank=0)
  db_param_4 = models.SmallIntegerField(default=0, blank=0)
  
  # db.push_direction
  # db.base_strength
  # db.level_strength
  # db.base_speed
  # db.level_speed
  # db.base_health
  # db.random_health
  # db.level_health
  # db.level_random_health
  # db.base_sleep
  # db.random_sleep
  # db.level_sleep
  # db.level_random_sleep
  # db.base_duration
  # db.random_duration
  # db.range
  # db.ranged_behavior
  # db.cure_or_poison