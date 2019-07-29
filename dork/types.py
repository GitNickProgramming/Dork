"""Base types for the Dork game"""
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import os
from random import randrange
from copy import deepcopy
from inspect import getfullargspec as argspec
import yaml
import dork.game_utils.factory_data as factory_data
from dork.game_utils.world_builder import MazeFactory
# pylint: disable=protected-access


class Grandparent:
    """common parent of holder, adjacent, and coord"""


class Holder(Grandparent):
    """A holder/container of items"""

    def __init__(self):
        super().__init__()
        self.inventory = dict

    def get_items(self, caller, data, verbose):
        """Print all inventory items

        Displays all items held by self<player instance> or not. Verbose
        print displays more information about inventory.

        Args:
            out (str): Inventory
            verbose (str): Displays detailed inventory

        returns:
            verbose (str): Returns a formated/detailed inventory of player.

        """

        if self.inventory:
            out = f"\n{caller} inventory:"
        else:
            out = f"There's nothing here."

        for name, item in data["inventory"].items():
            out += "\n    " + name
            if verbose:
                out += Game._verbose_print(item)
        return out


class Stats:
    """stats for items"""

    def __init__(self):
        self.data = dict
        self.attack = int
        self.strength = int
        self.weight = int
        self.luck = int
        self.equipable = bool


class Item(Stats):
    """An obtainable/usable item"""

    def __init__(self):
        super().__init__()
        self.data = dict
        self.name = str
        self.description = str
        self.type = str
        self.usable = NotUsable

    def make(self, item):
        """Make an item

        Creates the name, description, and type of item in game world

        Args:
            name (str): Generates a random item name
            description (str): Generates a random item description
            type (str): Generates a definition what type of item is generated
            usable(str): Is the item usable or not

        returns:
            name (str): returns the item name
            description (str): returns item description
            type (str): returns the type of item
            usable (str): returns the usability of item

        """
        self.name = item.get("name", "")
        self.description = item.get("description", "")
        self.type = item.get("type", "filler")
        if not isinstance(self.type, str) or self.type is None:
            self.usable = NotUsable
        elif len(self.type) > 1:
            self.set_usable(self.type)
        else:
            self.usable = NotUsable

    def set_usable(self, new_use):
        """method that sets usable on runtime

        This method changes the use behavior,
        provide usable class as argument

        Defines whether an item's type is usable or not

        Args:
            new_use (dict): checks if item's type is usable or not

        returns:
            nothing

        """
        uses = {"filler": NotUsable,
                "weapon": Attackable,
                "key": Openable,
                "gold": Payable,
                "magic items": Statable,
                "jewelry": Statable,
                "armor": Statable,
                "magic consumables": Statable}
        if new_use is None or new_use not in uses:
            self.usable = NotUsable
        else:
            self.usable = uses[new_use]

    def use(self, target, name):
        """Strategy pattern call

        This method is called by items to be used

        Calls its own behavior class called a Usable

        Args:
            target (Player): passes Player as target to be used on
            name (str): passed as name of item used

        returns:
            blurb (str): returns output for repl from specific usage

        """
        return self.usable.use(target, name)


class Usable(ABC):
    """Abstract class of use behavior in items use method"""

    @staticmethod
    @abstractmethod
    def use(target, name):
        """Strategy pattern inspired by refactoring.guru"""

        """use method defaults to doing nothing

        This method is the parent method inherited by
         all behavior classes' uses

        Args:
            target (Player): passes Player as target to
            be used on children
            name (str): passed as name of item used in children

        returns:
            nothing"""


class Attackable(Usable):
    """Any object that can be swung will say it was swung"""

    @staticmethod
    def use(target, name):
        """Swing use method

        Concrete use call for weapons"""
        """This method is called by weapons to be attack.
        Changes state of target player by calling
        the target's damage method.

        Args:
            target (Player): passes Player as target to attack
            name (str): passed as name of item used

        returns:
            blurb (str): returns that player swings weapon at target

        """
        target.damage()
        return "You swing the " + name + " at " + target.name


class NotUsable(Usable):
    """Any object that cannot be used"""

    @staticmethod
    def use(target, name):

        """Useless use method

        This method is called by filler items to be used

        Concrete unusable item class use method

        Args:
            target (Player): passes Player as target to be used on
            name (str): passed as name of item used

        returns:
            blurb (str): returns "You find no use of this item"

        """

        return "You find no use of this item"


class Openable(Usable):
    """Object opening behavior class"""


    @staticmethod
    def use(target, name):
        """Opens object targeted if possible

        This method is called by key items to be used


        Args:
            target (Player): passes Player as target to be used on
            name (str): passed as name of item used

        returns:
            blurbs (str): returns item has been inserted

        """
        return "You insert the " + name + " into " + target.name


class Payable(Usable):
    """Any object that can be used as gold"""

    @staticmethod
    def use(target, name):
        """Gold use method
        This method is called by gold items to be used


        Args:
            target (Player): passes Player as target to be used on
            name (str): passed as name of item used

        returns:
            blurb (str): returns that you pay with item

        """
        return "You use the " + name + " to pay " + target.name


class Statable(Usable):
    """Any object that can change stats"""

    @staticmethod
    def use(target, name):
        """Stat change use method

        This method is called by items to be used

        Args:
            target (Player): passes Player as target to be used on
            name (str): passed as name of item used

        returns:
            blurb (str): states that item took effect

        """
        return "The " + name + " takes effect on " + target.name


class Adjacent(Grandparent):
    """adjacency object for rooms"""

    def __init__(self):
        super().__init__()
        self.north = str
        self.south = str
        self.east = str
        self.west = str


class Coord(Grandparent):
    """coordinate object for rooms"""

    def __init__(self):
        super().__init__()
        self.x = int
        self.y = int


class Player(Holder):
    """A player or npc in the game"""
    states = {"damage": {"Calm": "Hostile", "Hostile": "Dead", "Dead": "Dead"},
              "talk": {"Calm": "Calm", "Hostile": "Calm", "Dead": "Dead"}}
    blurbs = {"Calm": {"talk": "Hello", "damage": "Ouch..Your gonna get it!"},
              "Hostile": {"talk": "I guess you are ok...I'll calm down",
                          "damage": "UGH\nYou dealt a death blow"},
              "Dead": {"talk": "That person is dead...blab away",
                       "damage": """You monster,
                        stop hitting that dead person!"""}}
    instances = []

    def __init__(self):
        super().__init__()
        self.data = dict
        self.name = str
        self.description = str
        self.location = Room
        self.equipped = list
        self.state = "Calm"

    def _new_instance(self):
        self.instances.append(self)

    def move(self, cardinal, maze):
        """walk this way

        Moves the player from one location to another in the game/maze

        Args:
            Out (str): describes where the player is located

        returns:
            out (str): returns if the player can move to next location

        """

        adjacent_room = getattr(self.location, cardinal)

        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            adjacent_room.data["players"][self.name] = \
                self.location.data["players"].pop(self.name)

            adjacent_room.players[self.name] = \
                self.location.players.pop(self.name)

            maze[self.location.x][self.location.y] = MazeFactory.room_color
            self.location = adjacent_room
            maze[self.location.x][self.location.y] = MazeFactory.player_color

            out = "You have entered " + self.location.description
            MazeFactory.update(maze)
        return out

    def next_state(self, action):
        """simpler state change method"""
        """This method updates players state based on name of method called

        Args:
            uses (str): passed as name action or method used on player

        returns:
            nothing

        """
        self.state = self.states[action][self.state]

    def talk(self):
        """Talk method called by players"""

        """This method is called by user to produce
        a text blurb based on player's state

        Args:
            None

        returns:
            uses (str): returns applicable blurb

        """
        out = (self.blurbs[self.state]["talk"])
        self.next_state("talk")
        return out

    def damage(self):
        """damage method called by items to inflict
        damage on players"""

        """This method is by items and changes the
        state of the callee player and returns blurb associated.

        Args:
            None

        returns:
            uses (str): returns blurb from hitting player

        """
        out = (self.blurbs[self.state]["damage"])
        self.next_state("damage")
        return out


class Room(Adjacent, Coord, Holder):
    """A room on the worldmap"""
    # pylint: disable=too-many-instance-attributes

    instances = []

    def __init__(self):
        super().__init__()
        self.name = str
        self.data = dict
        self.description = str
        self.players = dict

    def _new_instance(self):
        self.instances.append(self)


class Game:
    """An instance of Dork"""

    verbose = False
    dataaa = {}

    def __init__(self):
        self.data = {}
        self.maze = []
        self.rooms = {}
        self.hero = Player()
        self.points = 10

    def __call__(self, cmd, arg):
        do_func = getattr(self, cmd)
        func_args = argspec(do_func).args
        if arg:
            if not func_args or ("self" in func_args and len(func_args) == 1):
                out = self._repl_error("This command takes no arguments")
            else:
                out = do_func(arg)
        else:
            out = do_func()
        return out

    def _toggle_verbose(self) -> (str, bool):
        self.verbose = not self.verbose
        out = {
            True: "verbose inventory: ON",
            False: "verbose inventory: OFF"
        }[self.verbose]
        return out, False

    def _gtfo(self):
        return f"Thanks for playing DORK, {self.hero.name}!", True

    def _draw_maze(self):
        MazeFactory.draw(self.maze)
        return "\b", False

    def _move(self, cardinal):
        return self.hero.move(cardinal, self.maze), False

    def _points(self, user_input):
        if '_repl_error' in user_input:
            self.points = 0
        elif '_get_points' in user_input:
            pass
        else:
            self.points += 1
        return self.points

    def _get_points(self):
        point = self.points
        if point == 0:
            return f"Booooooo! you suck.\nYou have {point} points.", False
        return f"you have: {point}", False

    def _examine(self):
        return self.hero.location.get_items(
            caller=self.hero.location.name,
            data=self.hero.location.data,
            verbose=self.verbose
        ), False

    def _inventory(self):
        return self.hero.get_items(
            caller=self.hero,
            data=self.hero.data,
            verbose=self.verbose), False

    def _look(self):
        return self.hero.location.description, False

    def _save_game(self):
        self._get_state()
        Gamebuilder.save_game(self.hero.name, self.data)
        return "game saved successfully!", False

    # item_name defaults to None, so we take all items in room
    def _take_item(self, item_name=None):
        out = ""
        hero = self.hero
        room = hero.location
        if not item_name:
            room_copy = deepcopy(room.inventory)
            for item in room_copy:
                this_item = room.inventory.pop(item)
                this_data = room.data["inventory"].pop(item)
                hero.inventory[item] = this_item
                hero.data["inventory"][item] = this_data
                out += f"You took {item}\n"
        elif item_name in room.inventory:
            this_item = room.inventory.pop(item_name)
            this_data = room.data["inventory"].pop(item_name)
            hero.inventory[item_name] = this_item
            hero.data["inventory"][item_name] = this_data
            out += f"You took {item_name}. You took it well."
        else:
            out = f"There is no {item_name} here."

        self._update_room_inv_description(room)
        return out, False

    def _drop_item(self, item_name=None):
        out = ""
        hero = self.hero
        room = hero.location
        if not item_name:
            player_copy = deepcopy(hero.inventory)
            for item in player_copy:
                this_item = hero.inventory.pop(item)
                this_data = hero.data["inventory"].pop(item)
                room.inventory[item] = this_item
                room.data["inventory"][item] = this_data
                out += f"You dropped {item}\n"
        elif item_name in hero.inventory:
            this_item = hero.inventory.pop(item_name)
            this_data = hero.data["inventory"].pop(item_name)
            room.inventory[item_name] = this_item
            room.data["inventory"][item_name] = this_data
            out += f"You dropped {item_name}. How clumsy."
        else:
            out = f"There is no {item_name} in your inventory."

        self._update_room_inv_description(room)
        return out, False

    def _use_item(self, item="Nothing"):
        if item in self.hero.inventory.keys():
            target = input("What do you want to use it on? ")
            if target in self.hero.location.players:
                target_obj = self.hero.location.players[target]
                return self.hero.inventory[item].use(target_obj, item), False
            return "Invalid target", False
        return "You don't have that item...", False

    def _start_over(self):
        if self._confirm():
            out = "new game"
        else:
            out = "Guess you changed your mind!"
        return out, False

    def _get_state(self):
        for name, room in self.rooms.items():
            self.data["rooms"][name] = room.data

    def _talk(self, target="nobody"):
        if target in self.hero.location.players:
            npc = self.hero.location.players.get(target, "")
            return npc.talk(), False
        return "Who are you talking to?", False

    @staticmethod
    def _update_room_inv_description(location):
        inv_list = location.inventory
        num = len(inv_list)
        description = location.description.splitlines()
        des = location.description
        if num > 1:
            rand_ind = randrange(4)
            des = description[0] + "\n" + description[1] + "\n" \
                + factory_data.ROOM_INV_DESCRIPTIONS["1"][rand_ind]
        if num == 1:
            des = description[0] + "\n" + description[1] \
                + "\n" + factory_data.ROOM_INV_DESCRIPTIONS["2"]
        elif num == 0:
            des = description[0] + "\n" + description[1] \
                + "\n" + factory_data.ROOM_INV_DESCRIPTIONS["3"]
        location.description = des
        return 0

    @staticmethod
    def _verbose_print(data, calls=2):
        out = ""
        spc = "    "
        for key, val in data.items():
            if isinstance(val, dict):
                out += "\n" + spc*calls + \
                    f"{key}:{Game._verbose_print(val, calls+1)}"
            elif val not in (0, ''):
                out += "\n" + spc*calls + f"{key}: {val}"
        return out

    @staticmethod
    def _confirm():
        print("\n!!!WARNING!!! You will lose unsaved data!\n")
        conf = False
        while True:
            conf = str.casefold(
                input("Would you like to proceed? Y/N: ")
            )
            conf = {
                "y": True,
                "n": False
            }.get(conf, None)
            if conf is None:
                print("That is not a valid response!")
            else:
                break
        return conf

    @staticmethod
    def _repl_error(arg):
        return f"{arg}", False

    @staticmethod
    def _zork():
        return "holy *%&#@!!! a wild zork appeared!", False


class Gamebuilder:
    """Build an instance of Game"""

    @staticmethod
    def build(player_name):
        """Instantiate a game of Dork from dictionary

        Creates an instance of a game from a dictionary of game data

        Args:
            data (dict): Saves the state of the game, player, and items
            game (): Class instance of the game

        returns:
            data (dict): returns the state of the current game
            game (): returns the updated location, player, and items

        """

        data = Gamebuilder.load_game(player_name)

        if not data:
            data = MazeFactory.build()

            hero_data = {
                "name": player_name,
                "description": "the hero of dork!",
                "location": "Entrance",
                "inventory": {},
                "equipped": []
            }

            data["rooms"]["room 0"]["players"][player_name] = hero_data

        game = Gamebuilder._instantiate(Game, **data)
        setattr(game, "maze", data["maze"])
        setattr(
            game, "rooms", Gamebuilder._make_rooms(
                deepcopy(data["rooms"])
            )
        )

        Gamebuilder._place_players(game)
        Gamebuilder._make_paths(game)

        Gamebuilder._get_adj_description(game)
        Gamebuilder._get_room_inv_description(game)

        for player in Player.instances:
            if player.name == player_name:
                hero = player

        game.hero = hero
        game.maze[hero.location.x][hero.location.y] = MazeFactory.player_color
        return game

    @staticmethod
    def _make_rooms(rooms):

        factories = {
            "adjacent": Gamebuilder._make_adjacent,
            "inventory": Gamebuilder._make_item,
            "players": Gamebuilder._make_player,
            "stats": Gamebuilder._make_stats,
        }

        for name, room in rooms.items():
            new_room = Gamebuilder._instantiate(Room, **room)
            for field, data in room.items():
                if field == "adjacent":
                    Gamebuilder._make_adjacent(new_room, data)
                elif field == "coordinates":
                    Gamebuilder._make_coord(new_room, data)
                elif isinstance(data, dict):
                    room_field = getattr(new_room, field)
                    for sub in data:
                        room_field[sub] = factories[field](data[sub])
                else:
                    setattr(new_room, field, data)
            rooms[name] = new_room
            new_room._new_instance()

        return rooms

    @staticmethod
    def _make_player(player):
        new_player = Gamebuilder._instantiate(Player, **player)
        for field, data in player.items():
            if isinstance(data, dict):
                inventory = getattr(new_player, field)
                for sub in data:
                    inventory[sub] = Gamebuilder._make_item(data)
            else:
                setattr(new_player, field, data)
        new_player._new_instance()
        return new_player

    @staticmethod
    def _make_item(item):
        new_item = Gamebuilder._instantiate(Item, **item)
        for field, data in item.items():
            if field == "stats":
                Gamebuilder._make_stats(new_item, data)
            if field == "type":
                new_item.set_usable(item["type"])
            else:
                setattr(new_item, field, data)
        return new_item

    @staticmethod
    def _make_adjacent(room, adjacent):
        for key, val in adjacent.items():
            setattr(room, key, val)

    @staticmethod
    def _make_coord(room, coord):
        setattr(room, "x", coord[0])
        setattr(room, "y", coord[1])

    @staticmethod
    def _make_stats(item, stats):
        for key, val in stats.items():
            setattr(item, key, val)

    @staticmethod
    def _place_players(game):
        for _, room in game.rooms.items():
            for _, player in room.players.items():
                player.location = room

    @staticmethod
    def _make_paths(game):
        adj = ["north", "south", "east", "west"]
        for _, room in game.rooms.items():
            for direction, room_name in vars(room).items():
                if room_name and direction in adj:
                    setattr(room, direction, game.rooms[room_name])

    @staticmethod
    def _get_room_inv_description(worldmapp):
        worldmap = worldmapp.rooms
        worldmap_length = len(worldmap)
        iterator = 0
        for rooms in worldmap:
            if iterator != worldmap_length - 1:
                inv_list = worldmap[rooms].inventory
                num = len(inv_list)
                if num >= 2:
                    rand_ind = randrange(4)
                    first_desc = worldmap[rooms].description + "\n"
                    desc = factory_data.ROOM_INV_DESCRIPTIONS["1"][rand_ind]
                    worldmap[rooms].description = first_desc+desc
                elif num == 1:
                    first_desc = worldmap[rooms].description + "\n"
                    desc = factory_data.ROOM_INV_DESCRIPTIONS["2"]
                    worldmap[rooms].description = first_desc+desc
            iterator += 1
        return 0

    @staticmethod
    def _get_adj_description(worldmapp):

        worldmap = worldmapp.rooms

        for rooms in worldmap:
            desc = ""
            adj_list = list()
            adj_possibilities = {"north", "east", "south", "west"}
            for pos in adj_possibilities:
                if worldmap[rooms].data["adjacent"][pos] is not None:
                    adj_list.append(pos)

            adj_string = ""
            for adj in adj_list:
                if adj_list[0] == adj:
                    adj_string += " "+adj
                else:
                    adj_string += ", "+adj
            adj_string += "..."

            if((len(adj_list) == 1)
               and rooms != "room 0" and rooms != "room "+str(len(worldmap))):
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["1"]
            elif len(adj_list) == 2:
                rand_ind = randrange(8)
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["2"][rand_ind] \
                    + adj_string
            elif len(adj_list) == 3:
                rand_ind = randrange(5)
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["3"][rand_ind] \
                    + adj_string
            first_desc = worldmap[rooms].description + "\n"
            worldmap[rooms].description = first_desc+desc

        return 0

    @staticmethod
    def _instantiate(clz, **data):
        """return an object of type clz with attributes given by data"""

        new_obj = clz()
        setattr(new_obj, "data", data)
        for key, val in deepcopy(data).items():
            setattr(new_obj, key, val)
        return new_obj

    @staticmethod
    def load_game(player):
        """Load the save file associated with player

        Loads a saved yaml file based on what the user named their player

        Args:
            data (dict): dictionary of the game state from yaml file

        returns:
            data (dict): returns the game state based upon the player's name

        """

        save_files = []
        with os.scandir("./dork/saves") as saves:
            for entry in saves:
                save_files.append(entry.name.strip(".yml"))
        if player in save_files:
            file_path = f"./dork/saves/{player}.yml"
            with open(file_path) as file:
                data = yaml.safe_load(file.read())
        else:
            data = dict()
        return data

    @staticmethod
    def save_game(player, data):
        """Save a game instance to a yaml file if it exists, else create one

        Gets data on game state from saved yaml file

        Args:
            data (dict): dictionary of game state
            player (str): string of the player's name

        returns:
            data (dict): returns the dictionary state of the game from yaml
            player (str): returns the yaml file depending on the player's name

        """

        data = {
            "rooms": data["rooms"],
            "maze": data["maze"],
        }

        file_name = f"./dork/saves/{player}.yml"
        with open(file_name, "w") as save_file:
            yaml.safe_dump(
                data, save_file,
                indent=4, width=80,
            )

        return f"Your game was successfully saved as {player}.yml!"
