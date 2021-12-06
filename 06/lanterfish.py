import fileinput
from collections import Counter


def parse():
    return [int(n) for n in fileinput.input().readline().split(",")]


def simulate_naive(lanterfish, days=80):
    for _ in range(1, days + 1):
        new_born = []
        for i, fish in enumerate(lanterfish):
            if fish == 0:
                new_born.append(8)
                lanterfish[i] = 6
            else:
                lanterfish[i] -= 1
        lanterfish.extend(new_born)
    return len(lanterfish)


def simulate_efficient(lanterfish, days=256):
    fish_by_cycle_day = {cycle_day: 0 for cycle_day in range(9)}
    for fish in lanterfish:
        fish_by_cycle_day[fish] += 1

    for _ in range(1, days + 1):
        parents = new_born = fish_by_cycle_day.get(0, 0)
        # advance each fish by one day in cycle
        for i in range(8):
            fish_by_cycle_day[i] = fish_by_cycle_day[i + 1]
        # add new born
        fish_by_cycle_day[8] = new_born
        # reset parents
        fish_by_cycle_day[6] += parents
    return sum(fish_by_cycle_day.values())


def main():
    lanterfish = parse()
    count = simulate_naive(lanterfish[:])
    print(f"Part 1: {count}")

    count = simulate_efficient(lanterfish[:])
    print(f"Part 2: {count}")


if __name__ == "__main__":
    main()
