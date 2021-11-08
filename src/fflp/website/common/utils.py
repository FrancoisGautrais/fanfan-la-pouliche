import random


def arg(obj, key, default=None, empty = True):
    if key in obj:
        return obj[key]
    else:
        if not empty:
            raise ValueError("Erreur le paramètre '%s' est introuvable" % key)
        else:
            return default

CHARACTERS="abcdefghijklmnopqrstuvwxyz012345689"
def random_name(length=16):
    return "".join([random.choice(CHARACTERS)])