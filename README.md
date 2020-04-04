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
    * set or reset class, change xp, change health, change mana
  * Trapdoors
  * Special room kinds: no combat, no hide, hard to hide, object destroy, monster generator, monster lair
  * Special room magnitudes
* Objects
  * Imported all original objects (weapons, armor, etc)
  * Simple gold system
  * Wear/equipment slots
  * Drop-destroy
* Combat
  * Attack command
  * Damage-dependent attack messages for attacker, target, and observer (e.g., "Tutt creams your poor little body!!")
  * Rest w/ exit
  * Bleed (useful for debugging health)
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
* Command set
  * *.* for last action
  * *who* that shows everyone's room location
  * *sheet*
  * *brief*
  * *buy* / *sell*
  * *equip* / *unequip*
  * *name* 
  * *hide* / *reveal* / *search*
  * *shout* (easy replacement for thundering voice)
  * *express* (replaces Evennia *pose*)
  * Make some built-in Evennia commands queueable/blocking (look, say, whisper, get, drop, etc)  
  * Edit self-description (via Evennia *setdesc*)
* Commerce
  * Simple merchant in-room object
  * *buy* and *sell* commands
* Spells
  * Spell and SpellEffect schema
  * Character and class mana
  * Spellbooks w/ spells
  * *learn* command (list spells only)
  * *cast* command
    * At Who? target prompt
  * Spell effects: hurt, group hurt, heal, sleep (freeze), distance hurt
  * Direction/Target prompt for distance spells
  * Spell deflect and armor
* Randoms (aka mobs)
  * Mob class with prototypes from OG Monster randoms.json data
  * Simple mob AI: find target, attack, die, patrol/hunt
  * Mobs spawned by MONSTER_GENERATOR and MONSTER_LAIR rooms
  * Lair mobs stay in lair
  * drop gold and object


## What's not implemented yet

* Character
  * ...
* Map/Rooms
  * Room owners / customizations
    * (unclear if we need to bother replicating old monster custroom.pas, given Evennia's existing and extensive builder commands)
  * Special room kinds: market, treasure drop, heal
  * Move silent between rooms
  * Exit types
    * guardian
  * Exit effects
    * gold, alarmed, guardian, health less
  * Hidden/searchable exits
  * Look at in-room subdescriptions
  * Start game in tutorial room(s) (w/ room special/special effect)
  * Windows / window_descs?
* Objects
  * Hidden/searchable objects
  * Object damage
  * Cursed (no drop) objects
  * Enter amount of gold to drop
* Combat
  * Drop objects when hit
  * Punch
  * Missiles and *throw* command
  * Bombs and *lob* command
  * Poison
* Commands
  * Default attack / get / etc to picking the first thing for name dupes?
  * Remove any Evennia commands we don't want
  * hidesay
  * *use* command
  * *block* command
  * *steal* / *pickpocket* commands
  * Atmosphere
  * ctrl-c or some way to interrupt command queue
* Spells
  * Spell effects: cure/poison, push, strength/weak, speed/slow, invisible, see invisible, announce, command, detect magic, find person, locate
* Randoms (aka mobs)
  * pursuit chance / pursuit behavior
  * sayings
  * cast spells
  * figure out if extra1/extra2 fields contain actually-useful data


  