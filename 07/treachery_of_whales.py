import fileinput


def parse():
    return [int(p) for p in fileinput.input().readline().split(",")]


def get_cost_to_align(positions, target):
    return sum(abs(position - target) for position in positions)


def get_variable_cost_to_align(positions, target):
    sorted_positions_by_dist_to_target = sorted(
        positions, key=lambda position: abs(position - target)
    )

    cost = 0
    for position in sorted_positions_by_dist_to_target:
        diff = abs(position - target)
        cost += (diff + 1) * diff // 2
    return cost


def search(positions, get_cost_fn=get_cost_to_align):
    return min(get_cost_fn(positions, target) for target in search_range(positions))


def search_range(positions):
    return range(min(positions), max(positions) + 1)


def main():
    positions = parse()
    min_cost = search(positions)
    print(f"Part 1: {min_cost}")

    min_cost = search(positions, get_cost_fn=get_variable_cost_to_align)
    print(f"Part 2: {min_cost}")


if __name__ == "__main__":
    main()
