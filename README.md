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
* Map/Rooms
  * Imported all original Tai Tastigon rooms, room descriptions, and exits
  * Exit types
    * set or reset class
  * Exit descriptions
  * Exit messages: success, failure, "go in", "come out"
* Objects
  * Imported all original armor and weapons
  * Simple gold system
  * Wear/equipment slots
* Combat
  * Attack command
  * Damage-dependent attack messages for attacker, target, and observer (e.g., "Tutt creams your poor little body!!")
  * Rest / bleed commands
  * Weapon base damage / random damage
  * Character health and max health
  * Death at 0 health => go to the Void
  * XP for kills (based on level/xp comparison)
  * Weapon use percent
  * Claws  
* Command set
  * *.* for last action
  * *who* that shows everyone's room location
  * *sheet*
  * *brief*
* Commerce
  * Simple merchant in-room object
  * *buy* and *sell* commands


## What's not implemented yet

* Character
  * Various global player messages
    * E.g., "Welcome back, King Kickass.  Your last play was on 24-FEB-1991 at 3:35pm." "(Puzzeledfrog once again roams the land.)" "(Mummy has returned to sleep.)" "Puzzeledfrog has been slain by Giant Spider's Elf Slayer.""
* Map/Rooms
  * Start game in tutorial room(s)
  * Look at in-room subdescriptions
  * Trap door
  * Exit types
    * passworded
    * hidden
    * object keyed/forbidden
    * guardian
    * do-effect (gain/lose health, gold, xp)
  * Windows / window_descs?
* Combat
  * Freeze / attack delay
  * Weapon speed
  * Surprise attack
  * Punch
  * Get 50 gold upon death
  * Missiles and *throw* command
  * Bombs and *lob* command
* Commands
  * *name* command
  * *hide* / *search* / *reveal* commands
  * *use* command
  * *block* command
  * *steal* / *pickpocket* commands
  * Redirect *pose* to *express*
  * Atmosphere
  * Remove any Evennia commands we don't want
* Spells
  * Spell / ability system
  * *learn* command
  * thundering voice?
  * Spell effects
    * Same room, single target Damage / Heal / Freeze
    * Same room, multiple target Damage / Heal / Freeze
    * Missile Damage / Heal / Freeze
