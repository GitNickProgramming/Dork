# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""
from random import shuffle
from random import choice
from operator import add
import matplotlib.pyplot as plt
# import dork.game_utils.world_loader as world_loader


__all__ = ["Game"]


class Holder:
    """A holder/container of items
    """

    def __init__(self):
        self.items = dict()


class Item:
    """A obtainable/holdable item
    """

    def __init__(self):
        self.name = None
        self.description = None
        self.stats = dict()

    def make(self, item):
        """Make an item
        """
        self.name = item["name"]
        self.description = item["description"]
        self.stats = item["stats"]


class Player(Holder):
    """A player or NPC in the game
    """

    def __init__(self):
        super().__init__()
        self.name = None
        self.location = Room("")
        self.equipped = None

    def make(self, player):
        """Make a player
        """
        self.name = player["name"]
        self.equipped = player["equipped"]
        inventory = player["inventory"]
        for item in inventory:
            if item is not None:
                new_item = Item()
                new_item.make(inventory[item])
                self.items[new_item.name] = new_item

    def set_location(self, location):
        """Set player's location
        """
        self.location = location

    def get_location(self):
        """Get Player's location
        """
        return self.location


class Room(Holder):
    """A room on the worldmap
    """

    def __init__(self, desc):
        super().__init__()
        self.description = desc
        self.players = list()
        self.adjacent = dict()
        self.clues = dict()


class Worldmap:
    """A worldmap containing rooms, and the underlying maze
    """

    def __init__(self):
        self.worldmap = dict()
        self.maze = Maze()
        self._make_rooms()
        self._get_adj()

    def _make_rooms(self):
        i = 0
        rooms = self.maze.rooms
        for room in rooms:
            self.worldmap[room] = Room(f"dummy description {i}")
            i += 1

    def _get_adj(self):
        moves = {
            "north": (0, 1), "south": (0, -1), "east": (1, 0), "west": (-1, 0)
        }

        rooms = self.maze.rooms
        for room in rooms:
            this_room = self.worldmap[room]
            for direction in moves:
                position = room
                while True:
                    position = tuple(map(add, position, moves[direction]))
                    if self.maze(position) == 0:
                        this_room.adjacent[direction] = None
                        break
                    elif self.maze(position) == 2:
                        this_room.adjacent[direction] = self.worldmap[position]
                        break


class Game(Worldmap):
    """A container for holding a game state
    """

    def __init__(self):
        super().__init__()
        self.hero = Player()

    def __call__(self, cmd, arg):
        return getattr(self, cmd)(arg) if arg else getattr(self, cmd)()

    def build(self):
        """Make a new game
        """
        player_name = input("What's your name, stranger? ")
        self.hero.name = player_name

    def _gtfo(self):
        return f"Thanks for playing DORK, {self.hero.name}!", True

    def _move(self, cardinal):
        location = self.hero.get_location()
        adjacent_room = location.adjacent.get(cardinal, None)
        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            self.hero.set_location(self.worldmap[adjacent_room])
            print(f"You have entered {self.hero.location.name}")
            out = self.hero.location.description
        return out, False

    def _inventory(self):
        items = self.hero.items
        item_count = 0
        out = "Inventory:\n"
        for item in items:
            if item is not None:
                out += "\n" + " "*4 + items[item].name
                item_count += 1
        if item_count == 0:
            out = " "*4 + "You ain't got shit, son!"
        return out, False

    def _look(self):
        return self.hero.location.description, False

    def _start_over(self, load_or_save):
        if self._confirm():
            self.build()
            out = load_or_save
        else:
            out = "Guess you changed your mind!"
        return out, False

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
    def _zork():
        return "Oh shit, you found an easter egg!", False

    @staticmethod
    def _repl_error(arg):
        return f"{arg}", False


class Maze:
    """Generate a maze with 'rooms' on intersections, corners, and dead-ends.
    """

    moves = [
        [(0, 2), (0, 1)], [(0, -2), (0, -1)],
        [(-2, 0), (-1, 0)], [(2, 0), (1, 0)]
    ]

    rules = [
        [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0],
        [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1],
        [1, 1, 1, 1], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0],
        [0, 1, 0, 1]
    ]

    def __init__(self):
        self.rebuild()

    def __call__(self, *args):
        x, y, *val = args
        if val:
            self._maze[x][y] = val.pop()
        return self._maze[x][y]

    def rebuild(self):
        """Generate a new maze
        """
        x = choice([10, 12, 14, 18])
        y = 148//x
        rng_x = range(1, x+1, 2)
        rng_y = range(1, y+1, 2)

        self.rooms = []
        self._maze = [[0 for j in range(y+1)] for i in range(x+1)]
        self._grid = [(i, j) for i in rng_x for j in rng_y]
        self._path = [choice(self._grid)]
        self._generate()

    def reroom(self, obj):
        """Reassign maze rooms as obj
        """
        for room in self.rooms:
            self(*room, obj)

    def draw(self):
        """Show an image of the generated maze
        """
        _, axes = plt.subplots(figsize=(10, 10))
        axes.set_aspect(1.0)
        plt.xticks([])
        plt.yticks([])
        plt.pcolormesh(self._maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.show()

    def _generate(self):
        k = self._path[0]
        self._grid.remove(k)
        while self._grid:
            n = len(self._path)
            nsew = self._prb_lnk(k)
            shuffle(nsew)
            for prb_lnk in nsew:
                probe, _ = prb_lnk
                if probe in self._grid:
                    self._walk(prb_lnk)
                    self._grid.remove(probe)
                    self._path.extend(prb_lnk)
                    break
            if n == len(self._path):
                k = self._path[max(self._path.index(k)-1, 1)]
            else:
                k = self._path[-1]
        self._get_rooms()

    def _get_rooms(self):
        for coord in self._path:
            if self._neighbors(coord) in self.rules:
                self.rooms.append(coord)
                self(*coord, 2)
        self(*self._path[0], 2)
        self(*self._path[-2], 2)

    # def _set_rooms(self, obj):
    #     for room in self.rooms:
    #         self(*room, obj)

    def _prb_lnk(self, coord):
        nsew = []
        for move in self.moves:
            prb = tuple(map(add, move[0], coord))
            lnk = tuple(map(add, move[1], coord))
            nsew.append([prb, lnk])
        return nsew

    def _neighbors(self, coord):
        i, j = coord
        return [self(i-1, j), self(i+1, j), self(i, j-1), self(i, j+1)]

    def _walk(self, coords):
        prb, lnk = coords
        self(*prb, 1)
        self(*lnk, 1)
