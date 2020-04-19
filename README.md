# Monster

*It's not a game, it's a lifestyle.*

This is a WIP port of University at Buffalo's circa-1990 VMS game [Monster](http://www.skrenta.com/monster/) to a modern MUD engine ([Evennia](https://github.com/evennia/evennia)).

The running game server is up at http://www.monstermud.com.

## What's implemented

* Character
  * Account login; each account has a character
  * XP/level
  * Per-level stat increases 
  * Classes
  * Freeze/delays, queued commands
  * Move speed
  * Recover health and mana over time
  * Various global player messages w/ highlighting
    * E.g., "(Puzzeledfrog once again roams the land.)" "(Mummy has returned to sleep.)" "Puzzeledfrog has been slain by Giant Spider's Elf Slayer.""
  * Get 50 starting gold at creation and upon rebirth in Void    
* Map/Rooms
  * Imported all original Tai Tastigon rooms, room descriptions, and exits
  * Exit descriptions
  * Exit messages: success, failure, "go in", "come out"
  * Exit types
    * passworded/alias-required, hidden, object required/forbidden/hidden-without
  * Exit effects
    * set or reset class, change xp, change health, change mana, change gold, alarmed
  * Trapdoors
  * Special room kinds: no combat, no hide, hard to hide, object destroy, monster generator, monster lair, heal
  * Special room magnitudes
  * Hidden/searchable exits
  * MagicObj / secondary description
  * LOOK-able room details
* Objects
  * Imported all original objects (weapons, armor, etc)
  * Simple gold system
  * Wear/equipment slots
  * Drop-destroy
  * Hidden/searchable
  * Cursed (no drop)  
* Combat
  * Attack command
  * Damage-dependent attack messages for attacker, target, and observer (e.g., "Tutt creams your poor little body!!")
  * Rest w/ exit
  * Weapon base damage / random damage
  * Character health and max health
  * Death at 0 health => go to the Void
  * Armor
  * XP for kills (based on level/xp comparison)
  * Weapon use percent
  * Claws
  * Surprise attack
  * Freeze
  * Weapon speed  
  * Poison
  * Punch
* Command set
  * *.* for last action
  * *who* that shows everyone's room location
  * *sheet*
  * *brief*
  * *buy* / *sell*
  * *equip* / *unequip*
  * *name* 
  * *hide* / *reveal* / *search*, and "unidentified voice" for hidesay
  * *shout* (easy replacement for thundering voice)
  * *express* (replaces Evennia *pose*)
  * *make* command  
  * *show* (details) command
  * Make some built-in Evennia commands queueable/blocking (look, say, whisper, get, drop, etc)
  * Edit self-description (via Evennia *setdesc*)
  * Remove any Evennia commands we don't want
  * Target-needing commands picking the first match, to better deal with name dupes
* Commerce
  * Simple merchant in-room object that works with buy/sell
  * Weapon, armor, and spellbook merchants spawned at sensible rooms around the realm
* Spells
  * Spell and SpellEffect schema
  * Character and class mana
  * Spellbooks w/ spells
  * *learn* command (list spells only)
  * *cast* command
    * At Who? target prompt
  * Spell effects: hurt, group hurt, heal, sleep (freeze), distance hurt, cure/poison
  * Direction/Target prompt for distance spells
  * Spell deflect and armor
* Randoms (aka mobs)
  * Mob class with prototypes from OG Monster randoms.json data
  * Simple mob AI: find target, attack, die, patrol/hunt
  * Mobs spawned by MONSTER_GENERATOR and MONSTER_LAIR rooms
  * Lair mobs stay in lair
  * drop gold and object


## What's not implemented yet

* Map/Rooms
  * Move silent between rooms
  * Exit types
    * guardian
  * Exit effects
    * guardian, health less
  * Windows / window_descs (e.g., Improbable Structure <=> Forbidden Library)
  * Use NamePrint (Preposition for room name printing) / PrintParticle [sic]
  * Object drop destination
* Objects
  * Object damage
  * Enter amount of gold to drop
* Combat
  * Drop objects when hit
  * Missiles and *throw* command
  * Bombs and *lob* command
* Commands
  * *use* command
  * *block* command
  * *steal* / *pickpocket* commands
  * Atmosphere
  * ctrl-c or some way to interrupt command queue
  * Command help text
* Spells
  * Spell effects: push, strength/weak, speed/slow, invisible, see invisible, detect magic, find person, locate
* Randoms (aka mobs)
  * search for hidden character
  * sayings
  * pursuit chance / pursuit behavior
  * smarter lair behavior
 

## What probably won't get implemented (yet)

* Map/Rooms
  * Room special/special effect
    * afaict used only to overload commands in tutorial rooms?
  * Starting game tutorial rooms
    * Nice to have
  * Room owners / customizations
    * (unclear if we need to bother replicating old monster custroom.pas, given Evennia's existing toolset
  * Special room kinds: market (we have merchant objects instead), random group, random level, treasure drop (no rooms seem to use these SpcRoom values)
* Spells
  * Spell effects: announce (we have *shout* command instead of thundering voice), command (better implemented as a new effect in code?)
* Randoms (aka mobs)
  * cast spells and other combat behaviors

