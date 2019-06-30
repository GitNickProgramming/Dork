# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""
# from pprint import pprint
import dork.game_utils.world_maker as world_maker


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
        self.name = str()
        self.description = str()
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
        self.name = str()
        self.location = Room()
        self.equipped = list()

    def make(self, player):
        """Make a player
        """
        self.name = player["name"]
        self.equipped.append(player["equipped"])

        if player["inventory"] is not None:
            inventory = player["inventory"]
            for item in inventory:
                new_item = Item()
                new_item.make(inventory[item])
                self.items[new_item.name] = new_item

    def set_location(self, location):
        """Set player's location
        """
        self.location.players.remove(self.name)
        self.location = location
        self.location.players.append(self.name)

    def get_location(self):
        """Get Player's location
        """
        return self.location


class Room(Holder):
    """A room on the map
    """

    def __init__(self):
        super().__init__()
        self.name = str()
        self.description = str()
        self.adjacent = dict()
        self.players = list()
        self.clues = dict()

    def make(self, room, players):
        """Make a room
        """
        self.name = room["name"]
        self.description = room["description"]
        self.adjacent = room["adjacent"]

        if room["clues"] is not None:
            clues = room["clues"]
            for clue in clues:
                trigger = clues[clue]["trigger"]
                event = clues[clue]["event"]
                self.clues[trigger] = event

        if room["players"] is not None:
            for player in room["players"]:
                self.players.append(player)

            for player in players:
                if players[player].name in self.players:
                    players[player].location = self

        if room["items"] is not None:
            items = room["items"]
            for item in items:
                new_item = Item()
                new_item.make(items[item])
                self.items[new_item.name] = new_item


class Worldmap:
    """A map relating the rooms connectivity
        as well as the players/items within
    """

    def __init__(self):
        self.rooms = dict()
        self.players = dict()


class Game:
    """A container for holding a game state
    """

    def __init__(self):
        self.worldmap = Worldmap()
        self.players = dict()
        self.hero = Player()

    def build(self):
        """Make a new game
        """
        player_name = input("What's your name, stranger? ")
        data = world_maker.load_game(player_name)
        self._build_players(players=data["players"])
        self._build_world(rooms=data["rooms"])
        self._build_hero(hero=player_name)

    def _build_players(self, players):
        for player in players:
            new_player = Player()
            new_player.make(players[player])
            self.players[new_player.name] = new_player

    def _build_world(self, rooms):
        self.worldmap.players = self.players
        for room in rooms:
            new_room = Room()
            new_room.make(rooms[room], self.players)
            self.worldmap.rooms[new_room.name] = new_room

    def _build_hero(self, hero):
        self.hero = self.players.get(
            hero, self.players.get("new_player")
        )
        if "new_player" in self.players.keys():
            self.players[hero] = self.players.pop("new_player")
            self.hero.location.players.remove("new_player")
            self.hero.location.players.append(hero)
        self.hero.name = hero

    def _gtfo(self):
        return f"Thanks for playing DORK, {self.hero.name}!", True

    def _move(self, cardinal):
        hero = self.hero
        location = hero.get_location()
        adjacent_room = location.adjacent.get(cardinal, None)

        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            hero.set_location(self.worldmap.rooms[adjacent_room])
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

    def _start_over(self, new_or_load):
        if self._confirm():
            self.build()
            out = new_or_load
        else:
            out = "Guess you changed your mind!"

        return out, False

    def _save_game(self):
        return world_maker.save_game(self), False

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

    # def _take(self, item="all"):
    #     # Item defaults to "all", and adds all items in room to inventory
    #     return "You took the thing. You took it well.", False

    # def _drop_item(self, item):
    #     return "Oops, you dropped something!", False

    # def _use_item(self, item):
    #     return "You used the thing! It's super effective!", False
