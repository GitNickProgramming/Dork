"""Load an existing gameworld or begin anew"""


from copy import deepcopy
from random import choices, choice, randint, shuffle, randrange
from operator import add
import matplotlib.pyplot as plt
from numpy import full as npf
import dork.game_utils.factory_data as factory_data
# pylint: disable=protected-access


class ItemFactory:
    """Generates a random named item with randomized stats"""

    items = factory_data.ITEMS
    names = factory_data.NAMES
    sequence = factory_data.SEQUENCE

    types = items["types"]
    condition = items["condition"]
    material = items["material"]

    posessive = names["posessive"]
    nonposessive = names["nonposessive"]
    suffixes = names["suffixes"]
    abstract = names["abstract"]
    adjectives = names["adjectives"]

    @staticmethod
    def build(weights=None):
        """generate a random item"""

        weights = {
            "player": [8, 0, 0, 7, 5, 10]
        }.get(weights, [8, 35, 3, 7, 5, 10])

        item_type = choice(choices(
            population=list(ItemFactory.types.keys()),
            weights=weights,
            k=len(list(ItemFactory.types.keys()))
        ))

        item_name = choice(choices(
            population=ItemFactory.types[item_type],
            k=len(ItemFactory.types[item_type])
        ))

        return ItemFactory._forge(item_name, item_type)

    @staticmethod
    def _generate(stats, item_name, item_type):
        return {
            "name": item_name,
            "type": item_type,
            "description": "",
            "stats": stats
        }

    @staticmethod
    def _stats(item_name, item_type):
        stats = factory_data.stats(item_type.split()[0])
        return ItemFactory._generate(stats, item_name, item_type)

    @staticmethod
    def _forge(item_name, item_type):
        new_name = []
        build = ItemFactory.sequence[item_type]

        seq = choice(choices(
            population=build["seq"],
            weights=build["w"],
            k=len(build["seq"])
        ))

        for lists in seq:
            if isinstance(lists, dict):
                this_list = lists.get(
                    item_type, lists.get("usable", ['']))
            elif lists:
                this_list = lists
            else:
                this_list = ['']

            this_word = choice(choices(
                population=this_list,
                k=len(this_list)
            ))

            if this_word:
                if this_word in ItemFactory.suffixes:
                    new_name[-1] += this_word
                    item_type = f"legendary {item_name}"
                else:
                    new_name.append(this_word)
            else:
                new_name.append(item_name)

        item_name = " ".join(new_name)
        return ItemFactory._stats(item_name, item_type)


class PlayerFactory:
    """Generate players for a room"""

    @staticmethod
    def build(i, room):
        """Make a player, give them items"""

        new_player = {
            "name": f"player {i}",
            "description": f"player {i} description",
            "location": room["name"],
            "inventory": {},
            "equipped": []
        }

        for _ in range(randint(1, 3)):
            new_item = ItemFactory.build("player")
            new_player["inventory"][new_item.pop("name")] = new_item

        for key, val in new_player["inventory"].items():
            if val["stats"]["equipable"]:
                new_player["equipped"].append(key)

        return new_player


class RoomFactory:
    """Generate rooms for a given maze"""

    #  N, S and E, W are backwards because numpy uses column-order
    moves = {
        "north": (1, 0), "south": (-1, 0),
        "east": (0, 1), "west": (0, -1),
    }

    @staticmethod
    def build(maze, rooms):
        """build a room"""

        RoomFactory.maze = maze
        RoomFactory.rooms = rooms
        RoomFactory.worldmap = {}
        return RoomFactory._make_rooms()

    @staticmethod
    def _make_rooms():

        list_of_keys = factory_data.ROOMS
        shuffle(list_of_keys)
        list_of_adjtvs = factory_data.NAMES["adjectives"]
        shuffle(list_of_adjtvs)
        list_of_abstract = factory_data.NAMES["abstract"]
        shuffle(list_of_abstract)

        i = 0

        for room in RoomFactory.rooms:
            if i == 0:
                x, y = room
                new_room = {
                    "number": f"room 0",
                    "name": f"Entrance",
                    "description": factory_data.DEFAULT_ROOMS["Entrance"],
                    "coordinates": [x, y],
                    "adjacent": {},
                    "players": {},
                    "inventory": {},
                }
            elif i < len(RoomFactory.rooms) - 1:
                rand = list_of_keys[i]
                x, y = room
                new_room = {
                    "number": f"room {i}",
                    "name": rand,
                    "description": "The " + list_of_adjtvs[i] + rand +
                                   list_of_abstract[i],
                    "coordinates": [x, y],
                    "adjacent": {},
                    "players": {},
                    "inventory": {},
                }
            else:
                x, y = room
                new_room = {
                    "number": f"room "+str(len(RoomFactory.rooms)),
                    "name": f"End",
                    "description": factory_data.DEFAULT_ROOMS["End"],
                    "coordinates": [x, y],
                    "adjacent": {},
                    "players": {},
                    "inventory": {},
                }

            for _ in range(randint(1, 7)):
                new_item = ItemFactory.build()
                new_room["inventory"][new_item.pop("name")] = new_item

            for _ in range(randint(0, 2)):
                new_player = PlayerFactory.build(i, new_room)
                new_room["players"][new_player.pop("name")] = new_player

            RoomFactory.worldmap[room] = new_room
            i += 1

        return RoomFactory._get_adj()

    @staticmethod
    def _get_adj():
        for coord, room in RoomFactory.worldmap.items():
            for direction in RoomFactory.moves:
                searching = True
                position = coord
                while searching:
                    position = tuple(
                        map(add, position, RoomFactory.moves[direction]))
                    if RoomFactory.maze[position] == MazeFactory.wall_color:
                        room["adjacent"][direction] = None
                        searching = False
                    elif RoomFactory.maze[position] in \
                            [MazeFactory.room_color, MazeFactory.player_color]:
                        room["adjacent"][direction] = \
                            RoomFactory.worldmap[position]["number"]
                        searching = False

        for coord, room in deepcopy(RoomFactory.worldmap).items():
            new_room = RoomFactory.worldmap.pop(coord)
            RoomFactory.worldmap[new_room.pop("number")] = new_room

        RoomFactory._get_adj_description(RoomFactory.worldmap)
        RoomFactory._get_room_inv_description(RoomFactory.worldmap)

        return RoomFactory.worldmap

    @staticmethod
    def _get_room_inv_description(worldmap):
        for rooms in worldmap:
            inv_list = worldmap[rooms]["inventory"]
            num = len(inv_list)
            if num > 2:
                rand_ind = randrange(4)
                first_desc = worldmap[rooms]["description"] + "\n"
                desc = factory_data.ROOM_INV_DESCRIPTIONS["1"][rand_ind]
                worldmap[rooms]["description"] = first_desc+desc
            elif num == 1:
                first_desc = worldmap[rooms]["description"] + "\n"
                desc = factory_data.ROOM_INV_DESCRIPTIONS["2"]
                worldmap[rooms]["description"] = first_desc+desc
        return 0

    @staticmethod
    def _get_adj_description(worldmap):
        for rooms in worldmap:
            desc = ""
            adj_list = list()
            adj_possibilities = {"north", "east", "south", "west"}
            for pos in adj_possibilities:
                if worldmap[rooms]["adjacent"][pos] is not None:
                    adj_list.append(pos)

            adj_string = ""
            for adj in adj_list:
                if adj_list[0] == adj:
                    adj_string += " "+adj
                else:
                    adj_string += ", "+adj
            adj_string += "..."

            if((len(adj_list) == 1)
               and rooms != "room 0" and rooms != "room "+str(len(RoomFactory.rooms))):
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["1"]
            elif len(adj_list) == 2:
                rand_ind = randrange(8)
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["2"][rand_ind] \
                    + adj_string
            elif len(adj_list) == 3:
                rand_ind = randrange(5)
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["3"][rand_ind] \
                    + adj_string
            first_desc = worldmap[rooms]["description"] + "\n"
            worldmap[rooms]["description"] = first_desc+desc

        return 0


class MazeFactory:
    """Generate a maze with rooms on intersections, corners, and dead-ends"""

    wall_color, path_color, room_color, player_color = (-2, 2, 1, 0)
    moves = factory_data.MOVES
    rules = factory_data.rules(wall_color, path_color)

    @staticmethod
    def draw(maze):
        """display the maze"""

        plt.figure(figsize=(len(maze[0])//2, len(maze)//2))
        plt.pcolormesh(maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.ion()
        plt.show()

    @staticmethod
    def update(maze):
        """update the maze display"""

        plt.pcolormesh(maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.draw()

    # pylint: disable=R0914
    @staticmethod
    def build():
        """generate a maze"""

        x = choice([10, 12, 14, 18])
        y = 148//x

        maze = npf((x+1, y+1), MazeFactory.wall_color)
        grid = [(i, j) for i in range(1, x+1, 2) for j in range(1, y+1, 2)]
        path = [choice(grid)]
        rooms = []
        position = path[0]
        grid.remove(position)

        while grid:
            n = len(path)
            nsew = []
            for move in MazeFactory.moves:
                nsew.append([
                    tuple(map(add, move[0], position)),
                    tuple(map(add, move[1], position))
                ])
            shuffle(nsew)
            for probe in nsew:
                if probe[0] in grid:
                    maze[probe[0]] = MazeFactory.path_color
                    maze[probe[1]] = MazeFactory.path_color
                    grid.remove(probe[0])
                    path.extend(probe)
                    break
            if n == len(path):
                position = path[max(path.index(position)-1, 1)]
            else:
                position = path[-1]

        for coord in path:
            i, j = coord
            neighbors = [
                maze[i-1, j],
                maze[i+1, j],
                maze[i, j-1],
                maze[i, j+1]
            ]
            if neighbors in MazeFactory.rules:
                rooms.append(coord)
                maze[coord] = MazeFactory.room_color
            maze[rooms[0]] = MazeFactory.player_color

        return {
            "maze": maze.tolist(),
            "rooms": RoomFactory.build(maze, rooms)
        }
