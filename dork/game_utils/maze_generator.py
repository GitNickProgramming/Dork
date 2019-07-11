"""Random maze generator
"""
from random import shuffle
from random import choice
import matplotlib.pyplot as plt
from numpy import zeros as npz


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


def main(debug=False):
    """Generate a maze with 'rooms' on intersections, corners, and dead-ends.

    Keyword Arguments:

            debug {bool}: toggles whether the maze is drawn or not

    Returns:

            maze {list of list of int}:
                a numpy integer matrix

            rooms {list of tuple}:
                a {list} of room coordinates as {tuple}
    """

    x_dims = choice([10, 12, 14, 18])
    y_dims = 148//x_dims
    maze, rooms = _generate_maze((x_dims, y_dims))
    if debug:
        _draw_maze(maze)
    return maze, rooms


def _generate_maze(dims):
    x, y = dims
    m = npz((x+1, y+1), dtype=int)
    grid = [(i, j) for i in range(1, x+1, 2) for j in range(1, y+1, 2)]
    visited = [choice(grid)]
    vis = visited[0]
    grid.remove(vis)

    while grid:
        n = len(visited)
        nsew = []
        for i in range(4):
            probe = tuple(sum(x) for x in zip(_MOVES[i][0], vis))
            link = tuple(sum(x) for x in zip(_MOVES[i][1], vis))
            nsew.append([probe, link])
        shuffle(nsew)
        for prb_lnk in nsew:
            probe, link = prb_lnk
            if probe in grid:
                m[probe], m[link] = 1, 1
                grid.remove(probe)
                visited.extend(prb_lnk)
                break
        if n == len(visited):
            vis = visited[max(visited.index(vis)-1, 1)]
        else:
            vis = visited[-1]
    return _get_rooms(m, visited)


def _get_rooms(m, visited):
    rooms = []
    m[visited[0]], m[visited[-2]] = 2, 2
    for coord in visited:
        i, j = coord
        neighbors = [m[i-1, j], m[i+1, j], m[i, j-1], m[i, j+1]]
        if neighbors in _RULES:
            rooms.append(coord)
            m[coord] = 2
    return m, rooms


def _draw_maze(m):
    _, fig_axes = plt.subplots(figsize=(10, 10))
    fig_axes.set_aspect(1.0)
    plt.xticks([])
    plt.yticks([])
    plt.pcolormesh(m, cmap=plt.cm.get_cmap("tab20b"))
    # plt.show()
