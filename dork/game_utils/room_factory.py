"""Generate rooms for a given maze"""

from copy import deepcopy
from random import randint
from operator import add
from dork.game_utils.item_factory import main as ItemFactory
from dork.game_utils.player_factory import main as PlayerFactory


def main(maze, rooms) -> dict:
    """make rooms dictionary and get adjacencies"""

    moves = {
        "north": (0, 1), "south": (0, -1),
        "east": (1, 0), "west": (-1, 0),
    }
    worldmap = {}

    def _make_rooms():
        i = 0
        for room in rooms:
            new_room = {
                "name": f"room {i}",
                "description": f"room {i} description",
                "adjacent": {},
                "players": {},
                "items": {},
            }

            for _ in range(randint(1, 7)):
                new_item = ItemFactory()
                new_room["items"][new_item["name"]] = new_item

            for _ in range(randint(0, 2)):
                new_player = PlayerFactory(i, new_room["name"])
                new_room["players"][new_player["name"]] = new_player

            worldmap[room] = new_room
            i += 1

        return _get_adj()

    def _get_adj():
        for coord, room in worldmap.items():
            for direction in moves:
                searching = True
                position = coord
                while searching:
                    position = tuple(map(add, position, moves[direction]))
                    if maze[position] == 0:
                        room["adjacent"][direction] = None
                        searching = False
                    elif maze[position] == 2:
                        room["adjacent"][direction] = worldmap[position]["name"]
                        searching = False

        for coord, room in deepcopy(worldmap).items():
            worldmap[room.pop("name")] = worldmap.pop(coord)

        return worldmap
    return _make_rooms()
