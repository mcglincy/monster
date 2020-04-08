import random
from evennia import create_object
from evennia.prototypes import prototypes as protlib, spawner
from gamerules.combat import apply_armor, attack_bystander_msg, attack_target_msg
from gamerules.special_room_kind import SpecialRoomKind
from gamerules.xp import calculate_kill_xp, set_xp, gain_xp




def resolve_mob_attack(mob, target, attack_name="claws"):
  if target.is_dead:
    # already dead
    return

  # TODO: add hiding
  is_surprise = False
  damage = mob_attack_damage(mob, is_surprise)

  # attack message for target
  target.msg(attack_target_msg(mob.name, attack_name, damage))

  # attack message for room bystanders
  location_msg = attack_bystander_msg(mob.name, target.name, attack_name, damage)
  mob.location.msg_contents(location_msg, exclude=[mob, target])

  # apply armor to reduce damage
  damage = apply_armor(target, damage)

  # target takes the damage
  target.gain_health(-damage, damager=mob, weapon_name=attack_name)


def mob_attack_damage(mob, is_surprise=False):
  rand_multiplier = .7 if is_surprise else random.random()
  # TODO: consider mob.level_damage?
  dmg = mob.base_damage + random.randint(0, mob.random_damage)
  if is_surprise:
    dmg = dmg + int(dmg * mob.shadow_damage_percent / 100)
  return dmg  


def mob_death(mob, killer=None):
  if killer:
    killer.msg(f"You killed {mob.key}!")
    xp = calculate_kill_xp(killer.db.xp, mob.db.xp)
    gain_xp(killer, xp)

  if mob.db.drop_gold:
    gold = create_object("typeclasses.objects.Gold", key="gold")
    gold.add(mob.db.drop_gold)
    # use move_to() so we invoke StackableObject accumulation
    gold.move_to(mob.location, quiet=True)
    mob.location.msg_contents(f"{mob.key} drops {mob.db.drop_gold} gold.")

  if mob.db.drop_object_id:
    tags = ["object", f"record_id_{mob.db.drop_object_id}"]
    prototypes = protlib.search_prototype(tags=tags)
    if prototypes:
      obj = spawner.spawn(prototypes[0]["prototype_key"])[0]
      obj.location = mob.location
      mob.location.msg_contents(f"{mob.key} drops {obj.name}.")

  mob.location.msg_contents(
    f"{mob.key} disappears in a cloud of greasy black smoke.", exclude=[mob])
  mob.location = None
  mob.delete()


def generate_mob(location, level):
  tags = [f"min_level_{x}" for x in range(level+1)]
  mob_prototypes = protlib.search_prototype(tags=tags)
  if not mob_prototypes:
    # no valid prototypes found
    return
  proto_choice = random.choice(mob_prototypes)
  mob = spawner.spawn(proto_choice['prototype_key'])[0]
  mob.location = location
  location.msg_contents(f"A {mob.key} appears!")


def has_players_or_mobs(location):
  for obj in location.contents:
    if obj.is_typeclass("typeclasses.characters.Character") or obj.is_typeclass("typeclasses.mobs.Mob"):
      return True
  return False


def maybe_spawn_mob_in_lair(location):
  if not location.is_special_kind(SpecialRoomKind.MONSTER_LAIR):
    # not a lair
    return

  if has_players_or_mobs(location):
    # only spawn a new mob in a room devoid of players or mobs
    return

  mob_id = location.magnitude(SpecialRoomKind.MONSTER_LAIR)
  record_id_tag = f"record_id_{mob_id}"
  mob_prototypes = protlib.search_prototype(tags=[record_id_tag])
  if not mob_prototypes:
    return
  proto_choice = mob_prototypes[0]
  mob = spawner.spawn(proto_choice['prototype_key'])[0]
  # stay in the lair
  mob.location = location
  mob.db.moves_between_rooms = False
