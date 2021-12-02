import fileinput


def steer(cmmds):
    x, z = 0, 0

    for dir, amt in cmmds:
        if dir == "forward":
            x += amt
        elif dir == "down":
            z += amt
        elif dir == "up":
            z -= amt
    return x, z


def steer_with_aim(cmmds):
    x, z, a = 0, 0, 0

    for dir, amt in cmmds:
        if dir == "down":
            a += amt
        elif dir == "up":
            a -= amt
        elif dir == "forward":
            x += amt
            z += a * amt
    return x, z


def parse():
    cmmds = []
    for line in fileinput.input():
        dir, amt = line.split()
        cmmds.append((dir, int(amt)))
    return cmmds


def main():
    cmmds = parse()
    x, z = steer(cmmds)
    print(f"Part 1: {x*z}")
    x, z = steer_with_aim(cmmds)
    print(f"Part 2: {x*z}")


if __name__ == "__main__":
    main()
