import fileinput
from collections import defaultdict


def is_horizontal(a, b):
    _, y1 = a
    _, y2 = b
    return y1 == y2


def is_vertical(a, b):
    x1, _ = a
    x2, _ = b
    return x1 == x2


def draw_map(lines, with_diagonals=False):
    map = defaultdict(int)

    for line in lines:
        if not with_diagonals and not is_vertical(*line) and not is_horizontal(*line):
            continue

        a, b = line
        x1, y1 = a
        x2, y2 = b

        dx = x2 - x1
        dy = y2 - y1

        x_slope = 1 if dx > 0 else (-1 if dx < 0 else 0)
        y_slope = 1 if dy > 0 else (-1 if dy < 0 else 0)

        x, y = x1, y1
        for _ in range(max(abs(dx), abs(dy)) + 1):
            map[(x, y)] += 1
            x += x_slope
            y += y_slope
    return map


def parse():
    lines = []
    for line in fileinput.input():
        a, b = line.split(" -> ")
        x1, y1 = a.split(",")
        x2, y2 = b.split(",")
        lines.append(((int(x1), int(y1)), (int(x2), int(y2))))
    return lines


def get_ends(map):
    return max(x for x, _ in map), max(y for _, y in map)


def plot_map(map):
    max_x, max_y = get_ends(map)

    print()
    for y in range(max_y + 1):
        row = [str(map[(x, y)]) if map[(x, y)] else "." for x in range(max_x + 1)]
        print("".join(row))
    print()


def count_overlaps(map):
    return sum(1 for count in map.values() if count >= 2)


def main():
    lines = parse()
    map = draw_map(lines)
    overlaps = count_overlaps(map)
    print(f"Part 1: {overlaps}")

    map_with_diagonals = draw_map(lines, with_diagonals=True)
    overlaps = count_overlaps(map_with_diagonals)
    print(f"Part 2: {overlaps}")


if __name__ == "__main__":
    main()
