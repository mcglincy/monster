r"""
Evennia settings file.

The available options are found in the default settings file found
here:

../../../evennia/evennia/settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

SERVERNAME = "Monster"
GAME_SLOGAN = "It's not a game, it's a lifestyle"
SSL_ENABLED = True
# DEFAULT_HOME = "#4"  # aka Void
START_LOCATION = "#4"  # aka Void

INSTALLED_APPS = INSTALLED_APPS + ["userdefined", ]
PROTOTYPE_MODULES = ["world.prototypes", "world.generated_mob_prototypes", "world.generated_object_prototypes"]

DATA_DIR = "/opt/monsterdata"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.getenv("TEST_DB_PATH", os.path.join(DATA_DIR, "monster.db3")),
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

DEFAULT_CHANNELS = [
     {
        "key": "Public",
        "aliases": ("pub"),
        "desc": "Global public messages",
        "locks": "control:perm(Admin);listen:all();send:all()",
    },
    {
        "key": "Admin",
        "aliases": ("adm"),
        "desc": "Global admin messages",
        "locks": "control:perm(Admin);listen:all();send:all()",
    },
]

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
