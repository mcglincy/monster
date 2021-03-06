from django.contrib import admin
from userdefined.models import CharacterClass, Spell, SpellEffect


class CharacterClassAdmin(admin.ModelAdmin):
  list_display = ["db_key", "db_group", "db_record_id"]
  ordering = ["db_key"]


class SpellEffectInline(admin.TabularInline):
  model = SpellEffect
  extra = 0


class SpellEffectAdmin(admin.ModelAdmin):
  list_display = ["db_key", "db_group", "db_class_id", "db_min_level"]
  ordering = ["db_key"]
  inlines = (SpellEffectInline, )


admin.site.register(CharacterClass, CharacterClassAdmin)
admin.site.register(Spell, SpellEffectAdmin)
admin.site.register(SpellEffect)
