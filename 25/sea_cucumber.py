import fileinput
from copy import deepcopy


def parse():
    grid = {}
    for r, line in enumerate(fileinput.input()):
        for c, char in enumerate(line.strip()):
            if char != ".":
                grid[(r, c)] = char
    height = max(r for r, _ in grid)
    width = max(c for r, _ in grid)
    return grid, (height, width)


def display(grid, size):
    height, width = size
    for row in range(0, height + 1):
        print(" ".join([grid.get((row, col), ".") for col in range(0, width + 1)]))


def run(grid, size):
    steps = 0
    while True:
        new_grid, moves = step(grid, size)
        steps += 1
        if not moves:
            return steps
        grid = new_grid


def step(grid, size):
    height, width = size
    new_grid = deepcopy(grid)
    moves = 0

    for row in range(0, height + 1):
        for col in range(0, width + 1):
            if grid.get((row, col)) == ">":
                if move_east(new_grid, grid, size, row, col):
                    moves += 1

    grid = deepcopy(new_grid)

    for row in range(0, height + 1):
        for col in range(0, width + 1):
            if grid.get((row, col)) == "v":
                if move_south(new_grid, grid, size, row, col):
                    moves += 1

    return new_grid, moves


def move_east(grid, prev_grid, size, row, col):
    height, width = size
    east = col + 1 if col + 1 <= width else 0
    if not prev_grid.get((row, east)):
        del grid[(row, col)]
        grid[(row, east)] = ">"
        return True
    return False


def move_south(grid, prev_grid, size, row, col):
    height, width = size
    south = row + 1 if row + 1 <= height else 0
    if not prev_grid.get((south, col)):
        del grid[(row, col)]
        grid[(south, col)] = "v"
        return True
    return False


def main():
    grid, size = parse()

    steps = run(grid, size)
    print(f"Part 1: {steps}")


if __name__ == "__main__":
    main()
