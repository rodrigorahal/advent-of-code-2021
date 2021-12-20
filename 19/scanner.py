from collections import deque
from itertools import combinations
from typing import Deque, List


class Scanner:
    def __init__(self, id=None):
        self.id = id
        self.positions = set()
        self.overlaps_with = []

    @property
    def pair_distances(self) -> set:
        return {
            manhanttan_distance(p1, p2) for p1, p2 in combinations(self.positions, 2)
        }

    @property
    def pair_distances_by_position(self) -> dict:
        return {
            p: set([manhanttan_distance(p, p1) for p1 in self.positions])
            for p in self.positions
        }


def rotate(position, axis, angle):
    SIN_COS_BY_ANGLE = {0: (0, 1), 90: (1, 0), 180: (0, -1), 270: (-1, 0)}
    x, y, z = position

    sin, cos = SIN_COS_BY_ANGLE[angle]
    if axis == "x":
        return (x, y * cos - z * sin, y * sin + z * cos)
    if axis == "y":
        return (x * cos + z * sin, y, -x * sin + z * cos)
    if axis == "z":
        return (x * cos - y * sin, x * sin + y * cos, z)


def rotate_around(position, axis):
    for angle in [0, 90, 180, 270]:
        yield rotate(position, axis, angle)


def generate_rotations(position):
    # facing x
    # rotate around x
    yield from rotate_around(position, "x")

    # facing negative x
    # rotate around x
    yield from rotate_around(rotate(position, "y", 180), "x")

    # facing z
    # rotate around z
    yield from rotate_around(rotate(position, "y", 90), "z")

    # facing negative z
    # rotate around z
    yield from rotate_around(rotate(position, "y", 270), "z")

    # facing y
    # rotate around y
    yield from rotate_around(rotate(position, "z", 90), "y")

    # facing negative y
    # rotate around y
    yield from rotate_around(rotate(position, "z", 270), "y")


def manhanttan_distance(p1, p2):
    (x1, y1, z1), (x2, y2, z2) = p1, p2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def parse(filename):
    scanners = []
    with open(filename) as f:
        blocks = f.read().split("\n\n")
        for block in blocks:
            scanner = Scanner()
            for line in block.split("\n"):
                if line.strip().startswith("---"):
                    _, id = line.strip("---").strip().split(" ")
                    scanner.id = int(id)
                else:
                    (x, y, z) = map(int, line.strip().split(","))
                    scanner.positions.add((x, y, z))
            scanners.append(scanner)
    return scanners


def match(scanners: List[Scanner]):
    for a, b in combinations(scanners, 2):
        if (
            len(a.pair_distances.intersection(b.pair_distances)) >= 66
        ):  # 66 equals the size of combinations(12, 2)
            # we found an overlap
            a.overlaps_with.append(b)
            b.overlaps_with.append(a)


def get_matching_positions(scanner_a: Scanner, scanner_b: Scanner):
    matching_positions = []
    for p1, d1 in scanner_a.pair_distances_by_position.items():
        for p2, d2 in scanner_b.pair_distances_by_position.items():
            if len(d1.intersection(d2)) >= 11:
                matching_positions.append((p1, p2))
    return matching_positions


def find_rotation(matching_positions):
    a1, b1 = matching_positions[0]
    a2, b2 = matching_positions[1]
    for rotation_idx, (br1, br2) in enumerate(
        zip(list(generate_rotations(b1)), list(generate_rotations(b2)))
    ):
        xref, yref, zref = a1[0] - br1[0], a1[1] - br1[1], a1[2] - br1[2]
        if (a2[0], a2[1], a2[2]) == (xref + br2[0], yref + br2[1], zref + br2[2]):
            # found!
            return rotation_idx, (xref, yref, zref)
    return False


def normalize(scanners: List[Scanner]):
    merged_scanner = Scanner("merged")
    merged_scanner.positions = scanners[0].positions

    locations = [(0, 0, 0)]

    queue: Deque[Scanner] = deque([scanners[0].overlaps_with[0]])
    seen = set([0])

    while queue:
        scanner = queue.popleft()
        seen.add(scanner.id)

        matching_positions = get_matching_positions(merged_scanner, scanner)

        rotation_idx, (xref, yref, zref) = find_rotation(matching_positions)

        rotated = [list(generate_rotations(p))[rotation_idx] for p in scanner.positions]
        transformed = [(xr + xref, yr + yref, zr + zref) for (xr, yr, zr) in rotated]
        merged_scanner.positions.update(transformed)

        locations.append((xref, yref, zref))

        for overlap in scanner.overlaps_with:
            if overlap.id not in seen:
                queue.append(overlap)

    return merged_scanner, locations


def main():
    scanners: List[Scanner] = parse("19/input.txt")
    match(scanners)
    merged, locations = normalize(scanners)
    print(f"Part 1: {len(merged.positions)}")
    print(
        f"Part 2: {max(manhanttan_distance(a,b) for a, b in combinations(locations,2))}"
    )


if __name__ == "__main__":
    main()
