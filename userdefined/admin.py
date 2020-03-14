from django.contrib import admin
from userdefined.models import CharacterClass, Spell

class KeyAdmin(admin.ModelAdmin):
  list_display = ["db_key"]
  ordering = ["db_key"]


admin.site.register(CharacterClass, KeyAdmin)
admin.site.register(Spell, KeyAdmin)


