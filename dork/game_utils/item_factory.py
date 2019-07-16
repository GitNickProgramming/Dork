"""Generates a random item"""

from random import choices, choice, randint
import yaml

__all__ = ["main"]


def _load():
    print("loading data...")
    file_path = f"./dork/game_utils/item_word_bank.yml"
    with open(file_path) as file:
        data = yaml.safe_load(file.read())
    return data["items"], data["names"]


_ITEMS, _NAMES = _load()


_TYPES = _ITEMS["types"]
_CONDITION = _ITEMS["condition"]
_MATERIAL = _ITEMS["material"]


_POSESSIVE = _NAMES["posessive"]
_NONPOSESSIVE = _NAMES["nonposessive"]
_SUFFIXES = _NAMES["suffixes"]
_ABSTRACT = _NAMES["abstract"]
_ADJECTIVES = _NAMES["adjectives"]


_SEQUENCE = {
    "jewelry": {
        "seq": [
            [_CONDITION, _MATERIAL, ""],
            [_ADJECTIVES, _MATERIAL, ""],
            [_CONDITION, _MATERIAL, "", _ABSTRACT],
            [_ADJECTIVES, "", _ABSTRACT]
        ],
        "w": [15, 6, 3, 1]
    },
    "magic items": {
        "seq": [
            [_CONDITION, _MATERIAL, ""],
            [_ADJECTIVES, _MATERIAL, ""],
            [_CONDITION, _MATERIAL, "", _ABSTRACT],
            [_ADJECTIVES, "", _ABSTRACT]
        ],
        "w": [15, 6, 3, 1]
    },
    "magic consumables": {
        "seq": [
            [_CONDITION, "", _ABSTRACT],
            [_ADJECTIVES, "", _ABSTRACT],
        ],
        "w": [3, 1]
    },
    "weapon": {
        "seq": [
            [_CONDITION, _MATERIAL, ""],
            [_ADJECTIVES, ""],
            [_CONDITION, _MATERIAL, "", _ABSTRACT],
            [_ADJECTIVES, "", _ABSTRACT],
            [_NONPOSESSIVE, _SUFFIXES],
            [_POSESSIVE, _SUFFIXES],
        ],
        "w": [20, 15, 12, 10, 6, 5]
    },
    "armor": {
        "seq": [
            [_CONDITION, _MATERIAL, ""],
            [_ADJECTIVES, ""],
            [_CONDITION, _MATERIAL, "", _ABSTRACT],
            [_ADJECTIVES, "", _ABSTRACT],
        ],
        "w": [10, 6, 3, 1]
    },
    "filler": {
        "seq": [[_CONDITION, ""]],
        "w": [1]
    }
}


def main() -> dict:
    """Generate a random item dictionary"""

    item_type = choice(choices(
        population=list(_TYPES.keys()),
        weights=[10, 8, 3, 7, 5, 35],
        k=len(list(_TYPES.keys()))
    ))
    item_name = choice(choices(
        population=_TYPES[item_type],
        k=len(_TYPES[item_type])
    ))
    return _generate(item_name, item_type)


def _forge(item_name, item_type, unique_type, stats) -> dict:
    return {
        "name": item_name,
        "type": item_type,
        "description": unique_type,
        "stats": stats
    }


def _stats(item_name, item_type, unique_type) -> _forge:
    stats = {
        "weapon": {
            "attack": randint(10, 30),
            "weight": randint(5, 20),
            "luck": randint(-10, 10),
            "equippable": True,
        },
        "armor": {
            "strength": randint(10, 30),
            "weight": randint(15, 40),
            "luck": randint(-10, 10),
            "equippable": True,
        },
        "magic": {
            "attack": randint(15, 50),
            "amount": randint(5, 15),
            "luck": randint(-10, 10),
            "equippable": True,
        },
        "jewelry": {
            "strength": randint(-2, 10),
            "attack": randint(-2, 10),
            "luck": randint(-4, 4),
            "equippable": True,
        },
        "filler": {
            "weight": randint(5, 50),
            "luck": randint(-10, 10),
            "equippable": False,
        },
        "legendary": {
            "attack": randint(60, 120),
            "weight": randint(5, 15),
            "luck": randint(20, 80),
            "equippable": True,
        }
    }[item_type.split()[0]]

    return _forge(item_name, item_type, unique_type, stats)


def _generate(item_name, item_type) -> _stats:
    new_name = []
    unique_type = ""
    build = _SEQUENCE[item_type]

    seq = choice(choices(
        population=build["seq"],
        weights=build["w"],
        k=len(build["seq"])
    ))

    for lists in seq:
        if isinstance(lists, dict):
            this_list = lists.get(item_type, lists.get("usable", ['']))
        elif lists:
            this_list = lists
        else:
            this_list = ['']

        this_word = choice(choices(
            population=this_list,
            k=len(this_list)
        ))

        if this_word:
            if this_word in _SUFFIXES:
                new_name[-1] += this_word
                unique_type = item_name
                item_type = "legendary"
            else:
                new_name.append(this_word)
        else:
            new_name.append(item_name)

    item_name = " ".join(new_name)
    return _stats(item_name, item_type, unique_type)
