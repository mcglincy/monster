"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds
from commands.character import CmdName, CmdSheet
from commands.combat import CmdAttack, CmdBleed, CmdRest
from commands.commerce import CmdBuy, CmdSell
from commands.debug import CmdClear
from commands.equipment import CmdEquip, CmdUnequip
from commands.general import CmdDrop, CmdExpress, CmdGet, CmdInventory, CmdLook
from commands.hiding import CmdHide, CmdReveal, CmdSearch
from commands.misc import CmdBrief, CmdDot, CmdWho
from commands.spells import CmdCast, CmdLearn
from commands.talk import CmdSay, CmdShout, CmdWhisper


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(CmdAttack())
        self.add(CmdBleed())
        self.add(CmdBuy())
        self.add(CmdBrief())
        self.add(CmdCast())
        self.add(CmdClear())
        self.add(CmdDot())
        self.remove(default_cmds.CmdDrop())
        self.add(CmdDrop())
        self.add(CmdEquip())
        self.add(CmdExpress())        
        self.remove(default_cmds.CmdGet())
        self.add(CmdGet())
        self.remove(default_cmds.CmdGive())
        self.remove(default_cmds.CmdHome())        
        self.add(CmdHide())
        self.remove(default_cmds.CmdInventory())
        self.add(CmdInventory())
        self.add(CmdLearn())
        self.remove(default_cmds.CmdLook())
        self.add(CmdLook())
        self.remove(default_cmds.CmdName())
        self.add(CmdName())
        self.remove(default_cmds.CmdNick())
        self.remove(default_cmds.CmdPose())
        self.add(CmdRest())
        self.add(CmdReveal())
        self.remove(default_cmds.CmdSay())
        self.add(CmdSay())
        self.add(CmdSheet())
        self.add(CmdShout())
        self.add(CmdSearch())
        self.add(CmdSell())
        self.add(CmdUnequip())
        self.remove(default_cmds.CmdWhisper())
        self.add(CmdWhisper())
        self.remove(default_cmds.CmdWho())
        self.add(CmdWho())

        # add back the original name command as 'rename'
        rename = default_cmds.CmdName(key="rename", aliases="")
        self.add(rename)


class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.remove(default_cmds.CmdCharCreate())
        self.remove(default_cmds.CmdCharDelete())
        self.remove(default_cmds.CmdIC())
        self.remove(default_cmds.CmdNick())
        self.remove(default_cmds.CmdOOC())


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """

    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
