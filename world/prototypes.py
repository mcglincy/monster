"""
Prototypes

A prototype is a simple way to create individualized instances of a
given `Typeclass`. For example, you might have a Sword typeclass that
implements everything a Sword would need to do. The only difference
between different individual Swords would be their key, description
and some Attributes. The Prototype system allows to create a range of
such Swords with only minor variations. Prototypes can also inherit
and combine together to form entire hierarchies (such as giving all
Sabres and all Broadswords some common properties). Note that bigger
variations, such as custom commands or functionality belong in a
hierarchy of typeclasses instead.

Example prototypes are read by the `@spawn` command but is also easily
available to use from code via `evennia.spawn` or `evennia.utils.spawner`.
Each prototype should be a dictionary. Use the same name as the
variable to refer to other prototypes.

Possible keywords are:
    prototype_parent - string pointing to parent prototype of this structure.
    key - string, the main object identifier.
    typeclass - string, if not set, will use `settings.BASE_OBJECT_TYPECLASS`.
    location - this should be a valid object or #dbref.
    home - valid object or #dbref.
    destination - only valid for exits (object or dbref).

    permissions - string or list of permission strings.
    locks - a lock-string.
    aliases - string or list of strings.

    ndb_<name> - value of a nattribute (the "ndb_" part is ignored).
    any other keywords are interpreted as Attributes and their values.

See the `@spawn` command and `evennia.utils.spawner` for more info.

"""

from gamerules.equipment_slot import EquipmentSlot

# from random import randint
#
# GOBLIN = {
# "key": "goblin grunt",
# "health": lambda: randint(20,30),
# "resists": ["cold", "poison"],
# "attacks": ["fists"],
# "weaknesses": ["fire", "light"]
# }
#
# GOBLIN_WIZARD = {
# "prototype_parent": "GOBLIN",
# "key": "goblin wizard",
# "spells": ["fire ball", "lighting bolt"]
# }
#
# GOBLIN_ARCHER = {
# "prototype_parent": "GOBLIN",
# "key": "goblin archer",
# "attacks": ["short bow"]
# }
#
# This is an example of a prototype without a prototype
# (nor key) of its own, so it should normally only be
# used as a mix-in, as in the example of the goblin
# archwizard below.
# ARCHWIZARD_MIXIN = {
# "attacks": ["archwizard staff"],
# "spells": ["greater fire ball", "greater lighting"]
# }
#
# GOBLIN_ARCHWIZARD = {
# "key": "goblin archwizard",
# "prototype_parent" : ("GOBLIN_WIZARD", "ARCHWIZARD_MIXIN")
# }

#
# Misc object prototypes
#

BAG_OF_GOLD = {
  'typeclass': 'typeclasses.objects.Gold',
  'key': 'gold',
  'amount': 50,
  'desc': 'A bag of 50 gold.'
}

GHOSTLY_MERCHANT = {
  'typeclass': 'typeclasses.merchant.Merchant',
  'key': 'Ghostly Merchant',
  'for_sale_keys': ['axe', 'claymoore_sword', 'cudgel', 'dirk', 
    'hatchet', 'short_sword'],
}

WEAPONSMITH = {
  'typeclass': 'typeclasses.merchant.Merchant',
  'key': 'Weaponsmith',
  # TODO: add back scimitar when it's nerfed
  'for_sale_keys': ['broadsword', 'longsword', 'mace', 'military_fork', 
    'pike', 'saxon_axe', 'spear', 'voulge', 'warhammer'],
}

ARMORER = {
  'typeclass': 'typeclasses.merchant.Merchant',
  'key': 'Armorer',
  'for_sale_keys': ['buckler', 'chain_mail_armor', 'conical_helm',
    'crested_helm', 'horned_helm', 'leather_jerkin', 'norman_kite_shield',
    'plumed_helm', 'ring_mail_armor', 'steel_breastplate', 'wooden_shield',
    'viking_round_shield'],
}

BOOKSELLER = {
  'typeclass': 'typeclasses.merchant.Merchant',
  'key': 'Bookseller',
  'for_sale_keys': ['book_of_shadows', 'druid_spellbook', 'elf_spellbook',
  'grand_grimoire', 'lich_spellbook', 'mabinogian', 'wizard_spellbook'],
}

CURIO_MERCHANT = {
  'typeclass': 'typeclasses.merchant.Merchant',
  'key': 'Curio Merchant',
  'for_sale_keys': ['amber_hemisphere', 'animal_pelt', 'arrowhead', 
    'chunk_of_amber', 'diamond', 
    'elf_skull', 'flat_stone', 'garnet', 'glass_bottle', 'golden_ring',
    'granite_stone', 'huge_pearl', 'ivory_carving', 'jade_figurine',
    'jeweled_scimitar', 'lead_bar', 'long_strand_of_hemp', 'marble', 
    'persian_carpet', 'porcelain_vase', 'rhinestone_ring', 'silver_mirror',
    'small_ruby', 'velvet_cloth', 'vial']  
}

DRUID_SPELLBOOK = {
  'key': "Druid Spellbook",
  'prototype_parent': 'base_spellbook',
  'prototype_tags': ['object'],
  'equipment_slot': EquipmentSlot.BACKPACK,
  'spell_keys': ['Animate Shrubbery', 'Bear Claws', 'Earth Hammer', 'Forest Fire',
    'Gripping Plants', 'Insect Cloud', 'Locust Plague', 'Morning Frost',
    'Pack of Wolves', 'Soul Harvester', 'Stinging Hornets', 'Tidal Wave', 'Tornado',
    'Tree Attack']
}

ELF_SPELLBOOK = {
  'key': "Elf Spellbook",
  'prototype_parent': 'base_spellbook',
  'prototype_tags': ['object'],
  'equipment_slot': EquipmentSlot.BACKPACK,
  # TODO: there is a dupe Heal/heal spell
  'spell_keys': ['Heal', 'Poison Thorn', 'Silver Dagger', 'Sleep', 'Willow Blast',
    'charm', 'chestnut hail'],
}

LICH_SPELLBOOK = {
  'key': "Lich Spellbook",
  'prototype_parent': 'base_spellbook',
  'prototype_tags': ['object'],
  'equipment_slot': EquipmentSlot.BACKPACK,
  # TODO: figure out Grave Rot vs grave rot 2
  'spell_keys': ['Dark Arrows', 'Finger of Death', 'Grave Rot', 'Hands of Fire',
    'Minor Hellfire', 'Solar Flare', 'Storm', 'Unholy Blast', 'ray of death'],
}

WIZARD_SPELLBOOK = {
  'key': "Wizard Spellbook",
  'prototype_parent': 'base_spellbook',
  'prototype_tags': ['object'],
  'equipment_slot': EquipmentSlot.BACKPACK,
  'spell_keys': ['Brain Hammer', 'Dragon fire', 'Fireball', 'Flame Spray', 'Hailstorm',
  'Magic Missile', 'Touch of Death', 'earthquake'],
}
