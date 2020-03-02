from django.db import models

# Create your models here.
from evennia.utils.idmapper.models import SharedMemoryModel


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
  # fields to add later, maybe:
  # How well can it control its actions
  # control = models.PositiveSmallIntegerField(default=0, blank=0)
  # my_void = models.CharField(blank=False, null=True, max_length=32)
  # shadow_damage_percent = models.PositiveSmallIntegerField(default=0, blank=0)