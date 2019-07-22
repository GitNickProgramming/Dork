"""data for factories"""

from random import randint

DEFAULT_ROOMS = {"Entrance": "This is the beginning. Go explore!!!",
                 "End": "This is the end of the maze. Congrats on completing DORK!!!"}

ROOMS = {"Cave": "It's very dark in here...",
         "Dead forest": "Trees are all dead! ",
         "Cemetery": "This has gotta be the worst place in the maze!",
         "Valley": "Finally some green around here.",
         "Troll territory": "There's no one here right now... might be able to take some items",
         "Mansion": "All rooms in the mansion appear to be sealed shut, should exit before trouble arrives",
         "yes": "test",
         "no": "Another test",
         "idk": "Test!",
         "idc": "Test again",
         "idfk": "testing!",
         "idfc": "testsss",
         "idf": "testsss",
         "ic": "testsss",
         "c": "testsss",
         "i": "testsss",
         "id": "testsss",
         "f": "testsss",
         "fdsa": "testsss",
         "asdf": "testsss",
         "qwer": "testsss",
         "zxcv": "testsss",
         "mkop": "testsss",
         "idfccc": "testsss",
         "idfc": "testsss",
         "idfcfs": "testsss",
         "idffdsac": "testsss",
         "idfaac": "testsss",
         "idfrc": "testsss",
         "idfwc": "testsss"}

ITEMS = {
    "condition": {
        "filler": [
            "ruined",
            "damaged",
            "burnt",
            "waterlogged",
            "derelict",
            "dusty",
            "rusty",
            "cobwebbed",
            "chewed",
            "mended",
            "dirty",
            "moldy",
            "chipped"
        ],
        "jewelry": [
            "crude",
            "rusty",
            "worn",
            "flawed",
            "filthy",
            "dirty",
            "mended",
            "adequate",
            "fair",
            "fine",
            "polished",
            "untouched",
            "pristine",
            "ornate"
        ],
        "magic consumables": [
            "petty",
            "lesser",
            "common",
            "greater",
            "grand"
        ],
        "magic items": [
            "petty",
            "lesser",
            "common",
            "greater",
            "grand"
        ],
        "usable": [
            "damaged",
            "ruined",
            "fragile",
            "decrepit",
            "crude",
            "rusty",
            "worn",
            "filthy",
            "dirty",
            "old",
            "etched",
            "carved",
            "adequate",
            "fair",
            "fine",
            "pristine"
        ]
    },
    "material": {
        "armor": [
            "bone",
            "dragonscale",
            "hide",
            "iron",
            "steel",
            "leather",
            "plate",
            "mail"
        ],
        "jewelry": [
            "bone",
            "gold",
            "silver",
            "onyx",
            "obsidian",
            "amethyst",
            "emerald",
            "ruby",
            "jade",
            "turquoise",
            "ivory",
            "bronze",
            "copper",
            "meteorite",
            "adamantine"
        ],
        "magic items": [
            "bone",
            "gold",
            "silver",
            "onyx",
            "obsidian",
            "amethyst",
            "emerald",
            "ruby",
            "jade",
            "turquoise",
            "ivory",
            "bronze",
            "copper",
            "meteorite",
            "adamantine"
        ],
        "weapon": [
            "bone",
            "iron",
            "steel",
            "glass",
            "golden",
            "silver",
            "bronze",
            "meteorite",
            "adamantine"
        ]
    },
    "types": {
        "armor": [
            "bascinet",
            "helm",
            "hood",
            "gorget",
            "morion",
            "brigandine",
            "gambeson",
            "cuirass",
            "vest",
            "pauldrons",
            "spaulders",
            "vambrace",
            "cloak",
            "greaves",
            "gauntlets",
            "gloves"
        ],
        "filler": [
            "chains",
            "urn",
            "crate",
            "pottery",
            "chair",
            "stool",
            "pail",
            "beaker",
            "alembic",
            "cauldron",
            "bowl",
            "decanter",
            "bedroll",
            "blanket",
            "mortar",
            "pestle",
            "rope",
            "funnel",
            "cup",
            "pot",
            "cuffs",
            "rags",
            "parchment",
            "teeth",
            "bones",
            "dust",
            "book",
            "journal",
            "charcoal",
            "note",
            "incense",
            "lamp",
            "candle",
            "lantern",
            "torch"
        ],
        "jewelry": [
            "ring",
            "amulet",
            "circlet",
            "talisman"
        ],
        "magic consumables": [
            "potion",
            "philter",
            "scroll",
            "tome"
        ],
        "magic items": [
            "dust",
            "gem",
            "orb",
            "magestone",
            "shard",
            "horn"
        ],
        "weapon": [
            "longsword",
            "staff",
            "longbow",
            "recurve bow",
            "war hammer",
            "halberd",
            "spear",
            "battle axe",
            "glaive",
            "scythe",
            "shortsword",
            "blade",
            "falchion",
            "dagger",
            "mace",
            "crossbow",
            "scimitar",
            "club",
            "morning star"
        ]
    }
}

NAMES = {
    "abstract": [
        "of blooding",
        "of humiliation",
        "of hubris",
        "of the hunt",
        "of spite",
        "of death",
        "of life",
        "of regret",
        "of dread",
        "of sorrow",
        "of screams",
        "of lust",
        "of carving",
        "of surprise",
        "of confusion",
        "of frenzy",
        "of breaking",
        "of loathing",
        "of sickness",
        "of poisons",
        "of tragedy",
        "of souls",
        "of rotting",
        "of governing",
        "of ecstasy",
        "of torpor",
        "of truth",
        "of lies",
        "of victory",
        "of ambition",
        "of vengeance",
        "of somnolence",
        "of joy",
        "of the heretic",
        "of the prophet",
        "of corruption",
        "of erosion",
        "of jubilance",
        "of merit",
        "of witching",
        "of burdens",
        "of honor",
        "of repulsion",
        "of reckoning",
        "of mourning",
        "of grieving",
        "of judgement",
        "of battering",
        "of the night",
        "of the stars",
        "of the dawn",
        "of the dusk",
        "of the morning",
        "of hell",
        "of starlight",
        "of scorching",
        "of smite",
        "of waning",
        "of smiting",
        "of diffusion",
        "of mummification",
        "of crushing",
        "of extraction",
        "of valor",
        "of fear",
        "of firestorms",
        "of icestorms",
        "of ice",
        "of thunder",
        "of lightning",
        "of hatred",
        "of terror",
        "of ruin",
        "of ruining",
        "of fury",
        "of disgust",
        "of friendship",
        "of calming",
        "of shame",
        "of pity",
        "of envy",
        "of suffering",
        "of weeping",
        "of disdain",
        "of putrification",
        "of contempt",
        "of mediocrity",
        "of misery",
        "of thorns",
        "of light",
        "of dark",
        "of darkness",
        "of dawn",
        "of dusk",
        "of herecy",
        "of twilight",
        "of maleficence",
        "of brutality",
        "of savagery",
        "of malice",
        "of quickening",
        "of grace",
        "of disintegration",
        "of disintegrating",
        "of embalming",
        "of destruction",
        "of exsanguination"
    ],
    "adjectives": [
        "ghastly",
        "addictive",
        "gilded",
        "beautiful",
        "valorous",
        "ancient",
        "magnificent",
        "strange",
        "dreaded",
        "fearful",
        "splendid",
        "horrible",
        "luminous",
        "furious",
        "shameful",
        "friendly",
        "piteous",
        "weeping",
        "splendiferous",
        "loathsome",
        "blunderous",
        "magnetic",
        "electric",
        "burning",
        "brutal",
        "savage",
        "graceful",
        "volcanic",
        "uncanny",
        "spectral",
        "sinister",
        "ornate",
        "bloody",
        "ashen",
        "gleaming",
        "glittering",
        "eldritch",
        "eerie",
        "elegant",
        "exquisite",
        "munificent",
        "ineffable",
        "mirthful",
        "noxious",
        "nefarious",
        "repulsive",
        "freakish",
        "bewitched",
        "repugnant",
        "exotic",
        "burdensome",
        "vigilant",
        "bewildering",
        "chosen",
        "dazzling",
        "dusky",
        "putrid",
        "unpleasant",
        "bizarre",
        "frenzied",
        "stormy",
        "erosive",
        "vengeful",
        "somnolent",
        "opulent",
        "lustrous",
        "hideous",
        "insideous",
        "spiteful",
        "ugly",
        "thorny",
        "barbed",
        "ghoulish",
        "soulless",
        "corrupted",
        "envious",
        "grotesque",
        "weeping"
    ],
    "nonposessive": [
        "doom",
        "death",
        "hate",
        "fear",
        "soul",
        "sky",
        "mind",
        "god",
        "star",
        "shadow"
        "sun",
        "moon",
        "storm"
    ],
    "posessive": [
        "wolf",
        "troll",
        "goliath",
        "raven",
        "dragon",
        "crow",
        "widow",
        "wraith",
        "heart"
    ],
    "suffixes": [
        "sbane",
        "ripper",
        "eater",
        "stealer",
        "absorber",
        "shredder",
        "bruiser",
        "seer",
        "destroyer",
        "killer",
        "purger",
        "bearer",
        "corrupter",
        "preacher",
        "defier",
        "husher",
        "defiler",
        "dredger",
        "mutilator",
        "adder",
        "breaker",
        "scorcher",
        "maker",
        "bringer",
        "slayer"
    ]
}

SEQUENCE = {
    "jewelry": {
        "seq": [
            [ITEMS["condition"], ITEMS["material"], ""],
            [NAMES["adjectives"], ITEMS["material"], ""],
            [ITEMS["condition"], ITEMS["material"], "", NAMES["abstract"]],
            [NAMES["adjectives"], "", NAMES["abstract"]]
        ],
        "w": [15, 6, 3, 1]
    },
    "magic items": {
        "seq": [
            [ITEMS["condition"], ITEMS["material"], ""],
            [NAMES["adjectives"], ITEMS["material"], ""],
            [ITEMS["condition"], ITEMS["material"], "", NAMES["abstract"]],
            [NAMES["adjectives"], "", NAMES["abstract"]]
        ],
        "w": [15, 6, 3, 1]
    },
    "magic consumables": {
        "seq": [
            [ITEMS["condition"], "", NAMES["abstract"]],
            [NAMES["adjectives"], "", NAMES["abstract"]],
        ],
        "w": [3, 1]
    },
    "weapon": {
        "seq": [
            [ITEMS["condition"], ITEMS["material"], ""],
            [NAMES["adjectives"], ""],
            [ITEMS["condition"], ITEMS["material"], "", NAMES["abstract"]],
            [NAMES["adjectives"], "", NAMES["abstract"]],
            [NAMES["nonposessive"], NAMES["suffixes"]],
            [NAMES["posessive"], NAMES["suffixes"]],
        ],
        "w": [20, 15, 12, 10, 6, 5]
    },
    "armor": {
        "seq": [
            [ITEMS["condition"], ITEMS["material"], ""],
            [NAMES["adjectives"], ""],
            [ITEMS["condition"], ITEMS["material"], "", NAMES["abstract"]],
            [NAMES["adjectives"], "", NAMES["abstract"]],
        ],
        "w": [10, 6, 3, 1]
    },
    "filler": {
        "seq": [[ITEMS["condition"], ""]],
        "w": [1]
    }
}

MOVES = [
    [(0, 2), (0, 1)], [(0, -2), (0, -1)],
    [(2, 0), (1, 0)], [(-2, 0), (-1, 0)]
]


def rules(wall, path):
    """rules for neighbor checking during maze generation"""

    return [
        [wall, wall, wall, path],
        [wall, wall, path, wall],
        [wall, path, wall, wall],
        [path, wall, wall, wall],
        [path, path, path, wall],
        [path, path, wall, path],
        [path, wall, path, path],
        [wall, path, path, path],
        [path, path, path, path],
        [path, wall, path, wall],
        [path, wall, wall, path],
        [wall, path, path, wall],
        [wall, path, wall, path]
    ]


def stats(item_type):
    """item type-specific stats"""

    item_type = item_type.split()[0]

    attack = {
        "weapon": randint(10, 30),
        "magic": randint(15, 50),
        "legendary": randint(60, 120),
    }.get(item_type, 0)

    amount = {
        "magic": randint(3, 12)
    }.get(item_type, 0)

    strength = {
        "armor": randint(10, 30),
        "jewelry": randint(-1, 10),
        "magic": randint(5, 15),
    }.get(item_type, 0)

    weight = {
        "weapon": randint(5, 20),
        "armor": randint(15, 40),
        "filler": randint(5, 25),
        "legendary": randint(5, 15),
    }.get(item_type, 0)

    luck = {
        "jewelry": randint(-4, 4),
        "filler": randint(-10, 10),
        "legendary": randint(20, 80)
    }.get(item_type, randint(1, 15))

    equipable = {
        "filler": False
    }.get(item_type, True)

    return {
        "attack": attack,
        "amount": amount,
        "strength": strength,
        "weight": weight,
        "luck": luck,
        "equipable": equipable
    }
