"""Random maze generator
"""
from random import shuffle
from random import choice
import matplotlib.pyplot as plt
from numpy import zeros as npz


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
    x_dims = [6, 8, 10]
    y_dims = [10, 12, 14]
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

    dims = (choice(x_dims), choice(y_dims))
    maze, rooms = _generate_maze(dims, moves, rules)
    print(f"maze is {maze.shape[0]-1}x{maze.shape[1]-1} and has {len(rooms)} rooms")
    if debug:
        _draw_maze(maze)
    return maze, rooms


def _generate_maze(dims, moves, rules):
    x, y = dims
    m = npz((x+1, y+1), dtype=int)
    grid = [(a, b) for a in range(1, x+1, 2) for b in range(1, y+1, 2)]
    visited = [choice(grid)]
    k = visited[0]
    grid.remove(k)

    while grid:
        n = len(visited)
        nsew = []
        for i in range(4):
            probe = tuple(sum(x) for x in zip(moves[i][0], k))
            link = tuple(sum(x) for x in zip(moves[i][1], k))
            nsew.append([probe, link])
        shuffle(nsew)
        for a in nsew:
            probe, link = a
            if probe in grid:
                m[probe], m[link] = 1, 1
                grid.remove(probe)
                visited.extend(a)
                break
        if n == len(visited):
            k = visited[max(visited.index(k)-1, 1)]
        else:
            k = visited[-1]
    return _get_rooms(m, visited, rules)


def _get_rooms(m, visited, rules):
    rooms = []
    m[visited[0]], m[visited[-2]] = 2, 2
    for coord in visited:
        i, j = coord
        neighbors = [m[i-1, j], m[i+1, j], m[i, j-1], m[i, j+1]]
        if neighbors in rules:
            rooms.append(coord)
            m[coord] = 2
    return m, rooms


def _draw_maze(m):
    _, m_ax = plt.subplots(figsize=(10, 10))
    m_ax.set_aspect(1.0)
    plt.xticks([])
    plt.yticks([])
    plt.pcolormesh(m, cmap=plt.cm.get_cmap("tab20b"))
    plt.show()


# if __name__ == "__main__":
#     m, n = main(debug=True)
#     for r in m:
#         print(r)
