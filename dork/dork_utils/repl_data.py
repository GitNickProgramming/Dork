from functools import partial
# from dork.dork_utils import map_generator as map_gen


__all__ = ["CMDS", "ARGS"]


CMDS = {
    "say": {
        "hello": _hello,
        "goodbye": _bye,
    },
    "help": {
        "hello": partial(_help, "hello"),
        "goodbye": partial(_help, "bye"),
        "move": partial(_help, "move")
    },
    "q": _gtfo,
    "n": partial(_move, "north"),
    "s": partial(_move, "south"),
    "e": partial(_move, "east"),
    "w": partial(_move, "west"),
    "north": partial(_move, "north"),
    "south": partial(_move, "south"),
    "east": partial(_move, "east"),
    "west": partial(_move, "west"),
    "go": _move,
    "move": _move,
    "walk": _move,
    "travel": _move,
    "run": _move,
    "load map": _load_map
}


# dict or maybe just list
ARGS = [
    "n", "s", "e", "w", "north", "south", "east", "west"
]


def _hello():
    return "hello, world!", False


def _bye():
    return "goodbye, world!", True


def _help():
    return "try typing 'say hello'", False


def _gtfo():
    return "rude!", True


def _move(cardinal):
    if len(cardinal) == 1:
        cardinal = {
            "n": "north",
            "s": "south",
            "e": "east",
            "w": "west"
        }[cardinal]
    return f"You moved to the {cardinal}", False


def _load_map(path):
    pass
    