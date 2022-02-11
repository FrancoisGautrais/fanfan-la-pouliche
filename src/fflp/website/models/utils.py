import random
CHARACTERS = "abcdefghijklmnopqrsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def get_id(l):
    return "".join([x for _ in range(l) for x in random.choice(CHARACTERS) ])
