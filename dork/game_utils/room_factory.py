"""Generate rooms for a given maze"""

from random import randint
from operator import add
from dork.game_utils.item_factory import main as ItemFactory
from dork.game_utils.player_factory import main as PlayerFactory

def main(maze, rooms) -> tuple:
    """make rooms dictionaries and get adjacencies"""

    moves = {
        "north": (0, 1), "south": (0, -1),
        "east": (1, 0), "west": (-1, 0),
    }
    worldmap = {}
    players = {}

    def _make_rooms():
        i = 0
        for room in rooms:
            new_room = {
                "description": f"placeholder description {i}",
                "adjacent": {},
                "players": {},
                "items": {},
            }

            for _ in range(randint(1, 7)):
                new_item = ItemFactory()
                new_room["items"][new_item["name"]] = new_item

            for _ in range(randint(0, 2)):
                new_player = PlayerFactory(i, room)
                new_room["players"][new_player["name"]] = new_player
                players[new_player["name"]] = new_player

            worldmap[room] = new_room
            i += 1

        return _get_adj(worldmap, players)

    def _get_adj(worldmap, players):
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
                        room["adjacent"][direction] = position
                        searching = False

        return worldmap, players

    return _make_rooms()
