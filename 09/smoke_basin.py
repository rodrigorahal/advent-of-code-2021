import fileinput
from pprint import pprint
from math import prod


def get_adjacent(row, col, width, height):
    return [
        (row + dr, col + dc)
        for dr in range(-1, 2)
        for dc in range(-1, 2)
        if (
            abs(dr) != abs(dc)
            and row + dr >= 0
            and row + dr < height
            and col + dc >= 0
            and col + dc < width
        )
    ]


def is_low_point(grid, row, col):
    width = len(grid[0])
    height = len(grid)

    return all(
        grid[row][col] < grid[row_adj][col_adj]
        for row_adj, col_adj in get_adjacent(row, col, width, height)
    )


def search_low_points(grid):
    return [
        (row, col, height)
        for row, heights in enumerate(grid)
        for col, height in enumerate(heights)
        if is_low_point(grid, row, col)
    ]


def dfs(grid, row, col):
    width = len(grid[0])
    height = len(grid)

    basin = []
    seen = {(row, col)}
    stack = [(row, col)]
    while stack:
        row, col = stack.pop()
        seen.add((row, col))
        basin.append((row, col))

        for row_adj, col_adj in get_adjacent(row, col, width, height):
            if grid[row_adj][col_adj] != 9 and (row_adj, col_adj) not in seen:
                seen.add((row_adj, col_adj))
                stack.append((row_adj, col_adj))
    return basin


def search_basins(grid, low_points):
    return [dfs(grid, row, col) for row, col, _ in low_points]


def parse():
    grid = []
    for line in fileinput.input():
        grid.append([int(n) for n in line.strip()])
    return grid


def main():
    grid = parse()
    low_points = search_low_points(grid)
    print(f"Part 1: {sum(h+1 for _,_,h in low_points)}")

    basins = search_basins(grid, low_points)
    largest = sorted(basins, key=len)[-3:]
    print(f"Part 2: {prod(len(basin) for basin in largest)}")


if __name__ == "__main__":
    main()
