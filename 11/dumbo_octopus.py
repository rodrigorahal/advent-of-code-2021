import fileinput
from pprint import pprint


def parse():
    grid = []
    for line in fileinput.input():
        grid.append([int(n) for n in line.strip()])
    return grid


def get_adjacent(grid, row, col):
    height = len(grid)
    width = len(grid[0])

    adjacent = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if not (dr == dc == 0) and 0 <= row + dr < height and 0 <= col + dc < width:
                adjacent.append((row + dr, col + dc))
    return adjacent


def step_flashes(grid):
    to_flash = set()
    flashed = set()

    for row, energy_levels in enumerate(grid):
        for col, _ in enumerate(energy_levels):
            grid[row][col] += 1
            if grid[row][col] > 9:
                to_flash.add((row, col))

    while to_flash:
        row, col = to_flash.pop()
        flashed.add((row, col))
        for row_adj, col_adj in get_adjacent(grid, row, col):
            if (row_adj, col_adj) not in flashed and (row_adj, col_adj) not in to_flash:
                grid[row_adj][col_adj] += 1
                if grid[row_adj][col_adj] > 9:
                    to_flash.add((row_adj, col_adj))

    for row, col in flashed:
        grid[row][col] = 0

    return len(flashed)


def simulate(grid, steps=100):
    grid = [row[:] for row in grid]
    return sum(step_flashes(grid) for _ in range(steps))


def simulate_until_simultaneous_flash(grid, steps=100):
    grid = [row[:] for row in grid]
    size = len(grid) * len(grid[0])

    for i in range(1, steps):
        if step_flashes(grid) == size:
            return i
    return -1


def main():
    grid = parse()

    flashes = simulate(grid, steps=100)
    print(f"Part 1: {flashes}")

    step = simulate_until_simultaneous_flash(grid, steps=300)
    print(f"Part 2: {step}")


if __name__ == "__main__":
    main()
