import fileinput
from collections import defaultdict
from os import major


def is_horizontal(a, b):
    _, y1 = a
    _, y2 = b
    return y1 == y2


def is_vertical(a, b):
    x1, _ = a
    x2, _ = b
    return x1 == x2


def draw_map(lines, with_diagonals=False):
    map = {}
    for line in lines:
        a, b = line
        x1, y1 = a
        x2, y2 = b

        if is_horizontal(*line):
            y = y1

            start, end = min(x1, x2), max(x1, x2)
            for x in range(start, end + 1):
                map[(x, y)] = map.get((x, y), 0) + 1

        elif is_vertical(*line):
            x = x1

            start, end = min(y1, y2), max(y1, y2)
            for y in range(start, end + 1):
                map[(x, y)] = map.get((x, y), 0) + 1

        else:
            if not with_diagonals:
                continue

            x_slope = 1 if x1 < x2 else -1
            y_slope = 1 if y1 < y2 else -1

            start, end = min(x1, x2), max(x1, x2)

            x, y = x1, y1

            for _ in range(start, end + 1):
                map[(x, y)] = map.get((x, y), 0) + 1
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


def get_ends(lines):
    valid = [line for line in lines if is_horizontal(*line) or is_vertical(*line)]
    xs = [max(a[0], b[0]) for a, b in valid]
    ys = [max(a[1], b[1]) for a, b in valid]
    return max(xs), max(ys)


def plot_map(map, ends):
    max_x, max_y = ends

    print()
    for y in range(max_y + 1):
        row = [
            str(map.get((x, y))) if map.get((x, y)) else "." for x in range(max_x + 1)
        ]
        print("".join(row))
    print()


def count_overlaps(map, ends):
    max_x, max_y = ends

    count = 0
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if map.get((x, y), 0) >= 2:
                count += 1
    return count


def main():
    lines = parse()
    max_x, max_y = get_ends(lines)
    map = draw_map(lines)
    overlaps = count_overlaps(map, (max_x, max_y))
    print(f"Part 1: {overlaps}")

    map_with_diagonals = draw_map(lines, with_diagonals=True)
    overlaps = count_overlaps(map_with_diagonals, (max_x, max_y))
    print(f"Part 2: {overlaps}")


if __name__ == "__main__":
    main()
