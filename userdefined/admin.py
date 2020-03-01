from django.contrib import admin
from userdefined.models import CharacterClass

class CharacterClassAdmin(admin.ModelAdmin):
  list_display = ["db_key"]
  ordering = ["db_key"]


admin.site.register(CharacterClass, CharacterClassAdmin)
#admin.site.register(CharacterClass)

