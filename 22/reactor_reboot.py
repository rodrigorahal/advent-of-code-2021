import fileinput
from collections import Counter
from itertools import combinations


def parse():
    steps = []
    for line in fileinput.input():
        power, range = line.strip().split(" ")
        range = range.split(",")
        x = tuple(map(int, range[0][2:].split("..")))
        y = tuple(map(int, range[1][2:].split("..")))
        z = tuple(map(int, range[2][2:].split("..")))
        steps.append((power, (x, y, z)))
    return steps


def evolve(steps):
    state = set()
    for step in steps:
        power, ((xlo, xhi), (ylo, yhi), (zlo, zhi)) = step

        if not -50 <= xlo <= 50 and not -50 <= xhi <= 50:
            continue
        if not -50 <= ylo <= 50 and not -50 <= yhi <= 50:
            continue
        if not -50 <= zlo <= 50 and not -50 <= zhi <= 50:
            continue

        for x in range(xlo, xhi + 1):
            for y in range(ylo, yhi + 1):
                for z in range(zlo, zhi + 1):
                    if power == "on":
                        state.add((x, y, z))
                    elif power == "off":
                        state.discard((x, y, z))
    return state


def intersection(c1, c2):
    (x1lo, x1hi), (y1lo, y1hi), (z1lo, z1hi) = c1
    (x2lo, x2hi), (y2lo, y2hi), (z2lo, z2hi) = c2

    xilo = max(x1lo, x2lo)
    xihi = min(x1hi, x2hi)

    yilo = max(y1lo, y2lo)
    yihi = min(y1hi, y2hi)

    zilo = max(z1lo, z2lo)
    zihi = min(z1hi, z2hi)

    return (xilo <= xihi and yilo <= yihi and zilo <= zihi), (
        (xilo, xihi),
        (yilo, yihi),
        (zilo, zihi),
    )


def volume(cube):
    (xlo, xhi), (ylo, yhi), (zlo, zhi) = cube
    return (xhi + 1 - xlo) * (yhi + 1 - ylo) * (zhi + 1 - zlo)


# historical purposes
def disjoints(c1, c2):
    power_c1, ((x1lo, x1hi), (y1lo, y1hi), (z1lo, z1hi)) = c1
    power_c2, ((x2lo, x2hi), (y2lo, y2hi), (z2lo, z2hi)) = c2

    _, ci = intersection(c1, c2)

    ((xilo, xihi), (yilo, yihi), (zilo, zihi)) = ci

    minx = min(x1lo, x2lo)
    maxx = max(x1hi, x2hi)

    miny = min(y1lo, y2lo)
    maxy = max(y1hi, y2hi)

    minz = min(z1lo, z2lo)
    maxz = max(z1hi, z2hi)

    for i, (xlo, xhi) in enumerate([(minx, xilo), (xilo, xihi), (xihi, maxx)]):
        for j, (ylo, yhi) in enumerate([(miny, yilo), (yilo, yihi), (yihi, maxy)]):
            if (i, j) in [(0, 2), (2, 0)]:
                continue
            for k, (zlo, zhi) in enumerate([(minz, zilo), (zilo, zihi), (zihi, maxz)]):
                if (i, j, k) in [
                    (0, 0, 2),
                    (0, 1, 2),
                    (1, 0, 2),
                    (1, 2, 0),
                    (2, 1, 0),
                    (2, 2, 0),
                ]:
                    continue
                if power_c2 == "off" and (i, j, k) == (1, 1, 1):
                    continue
                yield "on", ((xlo, xhi), (ylo, yhi), (zlo, zhi))


# historical purposes
def merge(cubes, current):
    new_cubes = []
    for i, cube in enumerate(cubes):
        intersect, icube = intersection(cube, current)
        if not intersect:
            new_cubes.append(cube)
        if intersect:
            djs = disjoints(cube, current)
            if i == len(cubes) - 1:
                new_cubes.extend(djs)
            for dc in disjoints(cube, current):
                new_cubes.extend(merge(cubes[i + 1 :], dc))
    return new_cubes


def solve(steps):
    _, cube0 = steps[0]
    cubes = Counter([cube0])
    for power, cube in steps[1:]:
        for current_on, count in cubes.copy().items():
            intersects, intersect = intersection(current_on, cube)
            if intersects:
                cubes[intersect] += -count
        if power == "on":
            cubes[cube] += 1
    return sum(count * volume(cube) for cube, count in cubes.items())


def main():
    steps = parse()

    state = evolve(steps)
    print(f"Part 1: {len(state)}")

    c1 = ((10, 12), (10, 12), (10, 12))
    c2 = ((11, 13), (11, 13), (11, 13))
    c3 = ((9, 11), (9, 11), (9, 11))

    _, c = intersection(c1, c2)
    # print(f"v1: {volume(c1)} v2: {volume(c2)} vi: {volume(c)}")

    _, c13 = intersection(c1, c3)
    # print(f"v13 {volume(c13)}")
    _, c23 = intersection(c2, c3)
    # print(f"v23 {volume(c23)}")
    _, ci3 = intersection(c3, c)
    # print(f"i23 {volume(ci3)}")

    # print(volume(c1) + volume(c2) - volume(c) - volume(c13) - volume(c23) + volume(ci3))

    print(f"Part 2: {solve(steps)}")


if __name__ == "__main__":
    main()
