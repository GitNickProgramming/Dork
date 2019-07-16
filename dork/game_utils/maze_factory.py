"""Maze generator that returns an integer matrix representation
of the maze, and a list of room coordinate tuples."""

from operator import add
from random import choice, shuffle
from numpy import zeros as npzeros
from dork.game_utils.room_factory import main as RoomFactory


__all__ = ["main"]


_MOVES = [
    [(0, 2), (0, 1)], [(0, -2), (0, -1)],
    [(-2, 0), (-1, 0)], [(2, 0), (1, 0)]
]


_RULES = [
    [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0],
    [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1],
    [1, 1, 1, 1], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0],
    [0, 1, 0, 1]
]


def main() -> dict:
    """Generates the maze"""

    x = choice([10, 12, 14, 18])
    y = 148//x
    rng_x = range(1, x+1, 2)
    rng_y = range(1, y+1, 2)

    maze = npzeros((x+1, y+1), dtype=int)
    grid = [(i, j) for i in rng_x for j in rng_y]
    path = [choice(grid)]
    rooms = []

    def _prb_lnk(coord):
        nsew = []
        for move in _MOVES:
            prb = tuple(map(add, move[0], coord))
            lnk = tuple(map(add, move[1], coord))
            nsew.append([prb, lnk])
        return nsew

    def _neighbors(maze, coord):
        i, j = coord
        return [
            maze[(i-1, j)],
            maze[(i+1, j)],
            maze[(i, j-1)],
            maze[(i, j+1)],
        ]

    def _walk(maze, coord):
        prb, lnk = coord
        maze[prb] = 1
        maze[lnk] = 1

    def _worldmap(maze, rooms, players) -> dict:
        return {
            "maze": maze,
            "rooms": rooms,
            "players": players,
        }

    def _get_rooms(maze, path, rooms) -> _worldmap:
        for coord in path:
            if _neighbors(maze, coord) in _RULES:
                rooms.append(coord)
                maze[coord] = 2
        maze[path[0]] = 2
        maze[path[-2]] = 2

        rooms, players = RoomFactory(maze, rooms)
        maze = maze.tolist()

        return _worldmap(maze, rooms, players)

    def _generate(maze, grid, path, rooms) -> _get_rooms:
        k = path[0]
        grid.remove(k)
        while grid:
            n = len(path)
            nsew = _prb_lnk(k)
            shuffle(nsew)
            for prb_lnk in nsew:
                probe, _ = prb_lnk
                if probe in grid:
                    _walk(maze, prb_lnk)
                    grid.remove(probe)
                    path.extend(prb_lnk)
                    break
            if n == len(path):
                k = path[max(path.index(k)-1, 1)]
            else:
                k = path[-1]

        return _get_rooms(maze, path, rooms)

    return _generate(maze, grid, path, rooms)
