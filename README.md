# Monster

*It's not a game, it's a lifestyle.*

This is a WIP port of University at Buffalo's circa-1990 VMS game [Monster](http://www.skrenta.com/monster/) to a modern MUD engine ([Evennia](https://github.com/evennia/evennia)).

The running game server is up at http://www.monstermud.com.

## What's implemented

* Character
  * Account login; each account has a character
* Map/Rooms
  * Imported all original Tai Tastigon rooms, room descriptions, and exits
* Objects
  * Imported all original armor and weapons
  * Simple gold system
* Combat
  * Attack command
  * Damage-dependent attack messages for attacker, target, and observer (e.g., "Tutt creams your poor little body!!")
  * Rest / bleed commands
  * Weapon base damage / random damage
  * Character health and max health
  * Death at 0 health => go to void (currently Limbo)
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
  * Classes
  * XP/level
  * Various global player messages
    * E.g., "Welcome back, King Kickass.  Your last play was on 24-FEB-1991 at 3:35pm." "(Puzzeledfrog once again roams the land.)" "(Mummy has returned to sleep.)" "Puzzeledfrog has been slain by Giant Spider's Elf Slayer.""
* Map/Rooms
  * Start game in tutorial room(s)
  * Look at in-room subdescriptions
  * Trap door
  * Windows / window_descs
  * Exit types
    * hidden
    * passworded
    * object keyed/forbidden
    * guardian
    * do-effect (gain/lose health, gold, xp; set or reset class)
* Combat
  * Freeze / attack delay
  * Weapon use percent
  * Per-level damage
  * Surprise attack
  * Claws
  * Punch
  * Weapon speed / freeze
  * Go to the Void upon death
  * Get 50 gold upon death
  * Missiles and *throw* command
  * Bombs and *lob* command
* Commands
  * Redirect *pose* to *express*
  * Atmosphere
  * *use* command
  * *block* command
  * remove any Evennia commands we don't want
  * *hide* / *search* / *reveal* commands
  * *steal* / *pickpocket* commands
* Spells
  * Spell / ability system
  * *learn* command
  * thundering voice?
  * Spell effects
    * Same room, single target Damage / Heal / Freeze
    * Same room, multiple target Damage / Heal / Freeze
    * Missile Damage / Heal / Freeze
