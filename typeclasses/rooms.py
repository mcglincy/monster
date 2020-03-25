"""
Room

Rooms are simple containers that has no location of their own.

"""

from collections import defaultdict
from evennia import DefaultRoom
from evennia.utils.utils import list_to_string
from gamerules.special_room_kind import SpecialRoomKind


# TODO: move this somewhere (utils?)
def check_bit(num, offset):
  mask = 1 << offset
  return(num & mask)


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.record_id = None
        # see SpecialRoomKind for the various special kinds and bit positions
        self.db.special_kind_bitmask = 0
        self.db.trap_chance = 0
        self.db.trap_direction = None

    def special_kinds(self):
        return [x for x in SpecialRoomKind 
          if check_bit(self.special_kind_bitmask, x.value)]

    def is_special_kind(self, special_room_kind):
        return check_bit(self.special_kind_bitmask, special_room_kind.value)

    def return_appearance(self, looker, **kwargs):
        """
        This formats a description. It is the hook a 'look' command
        should call.

        Args:
            looker (Object): Object doing the looking.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        if not looker:
            return ""
        # get and identify all objects
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))
        exits, users, things = [], [], defaultdict(list)
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)
            elif con.has_account:
                users.append("|c%s|n" % key)
            else:
                # things can be pluralized
                things[key].append(con)
        # get description, build string
        string = "|c%s|n\n" % self.get_display_name(looker)

        if not kwargs.get('brief', False):
            desc = self.db.desc
            if desc:
                string += "%s\n" % desc
        if exits:
            string += "\n" + "\n".join(exits)
        if users or things:
            # handle pluralization of things (never pluralize users)
            thing_strings = []
            for key, itemlist in sorted(things.items()):
                nitem = len(itemlist)
                if nitem == 1:
                    key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
                else:
                    key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][
                        0
                    ]
                thing_strings.append(key)

            string += "\n|wYou see:|n " + list_to_string(users + thing_strings)

        return string
