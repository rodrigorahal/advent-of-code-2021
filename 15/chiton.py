import fileinput
from collections import deque, defaultdict
import time
import heapq
from pprint import pp, pprint


def parse():
    grid = []
    for line in fileinput.input():
        grid.append([int(x) for x in line.strip()])
    return grid


def get_adjacent(grid, row, col):
    H, W = len(grid), len(grid[0])

    adjacents = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if abs(dr) != abs(dc) and (0 <= row + dr < H) and (0 <= col + dc < W):
                adjacents.append((row + dr, col + dc))
    return adjacents


def dijkstra(grid, source=(0, 0)):
    risk_to_source = defaultdict(lambda: float("inf"))
    risk_to_source[source] = 0

    queue = []
    heapq.heappush(queue, (risk_to_source[source], source))

    while queue:
        _, curr = heapq.heappop(queue)
        row, col = curr

        for adj in get_adjacent(grid, row, col):
            row_a, col_a = adj
            if risk_to_source[adj] > risk_to_source[curr] + grid[row_a][col_a]:
                risk_to_source[adj] = risk_to_source[curr] + grid[row_a][col_a]
                heapq.heappush(queue, (risk_to_source[adj], adj))
    return risk_to_source


def propagate(tile):
    H, W = len(tile), len(tile[0])
    map = [[None] * W * 5 for i in range(H)]
    for row, risks in enumerate(tile):
        for col, risk in enumerate(risks):
            map[row][col] = risk
            for j in range(1, 5):
                map[row][col + j * W] = propagate_risk(map[row][col + (j - 1) * W])
    for i in range(4):
        for row in range(H):
            new_row = [propagate_risk(map[row + i * H][col]) for col in range(5 * W)]
            map.append(new_row)
    return map


def propagate_risk(risk):
    return risk + 1 if risk + 1 <= 9 else 1


def main():
    tile = parse()

    target = len(tile) - 1, len(tile[0]) - 1
    risk_to_source = dijkstra(tile)
    print(f"Part 1: {risk_to_source[target]}")

    map = propagate(tile)
    target = len(map) - 1, len(map[0]) - 1
    risk_to_source = dijkstra(map)
    print(f"Part 2: {risk_to_source[target]}")


if __name__ == "__main__":
    main()
