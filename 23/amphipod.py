from copy import deepcopy

ENERGY_TO_M0VE = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

AMPHI_ROOMS = {
    "A": ((1, 2), (2, 2), (3, 2), (4, 2)),
    "B": ((1, 4), (2, 4), (3, 4), (4, 4)),
    "C": ((1, 6), (2, 6), (3, 6), (4, 6)),
    "D": ((1, 8), (2, 8), (3, 8), (4, 8)),
}


CORRIDOR = [(0, col) for col in range(11)]
ROOMS = [
    # A
    (1, 2),
    (2, 2),
    (3, 2),
    (4, 2),
    # B
    (1, 4),
    (2, 4),
    (3, 4),
    (4, 4),
    # C
    (1, 6),
    (2, 6),
    (3, 6),
    (4, 6),
    # D
    (1, 8),
    (2, 8),
    (3, 8),
    (4, 8),
]
OPEN_SPACE = CORRIDOR + ROOMS


def pair_rooms(room):
    row, col = room
    return [(r, col) for r in range(1, 5) if r != row]


def distance(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    return abs(c2 - c1) + abs(r2 - r1)


def moves(grid, row, col):
    if (row, col) in ROOMS:
        return moves_from_room(grid, row, col)

    return moves_from_corridor(grid, row, col)


def moves_from_room(grid, row, col):
    amphipod = grid[row][col]
    is_in_target = (row, col) in AMPHI_ROOMS[amphipod]

    all_pairs_in_target = all(
        (pair_row, pair_col) in AMPHI_ROOMS.get(grid[pair_row][pair_col], set())
        for (pair_row, pair_col) in pair_rooms((row, col))
    )

    is_blocked = any(grid[r][col] != "." for r in range(1, row))

    if is_blocked:
        return []

    if is_in_target and all_pairs_in_target:
        return []

    return valid_corridor_positions(grid, row, col)


def valid_corridor_positions(grid, row, col):
    left = [c + 1 for c in range(0, col) if grid[0][c] != "."]
    start = max(left) if left else 0

    right = [c for c in range(col + 1, 11) if grid[0][c] != "."]
    end = min(right) if right else 11

    return [(0, c) for c in range(start, end) if c not in (2, 4, 6, 8)]


def moves_from_corridor(grid, row, col):
    amphipod = grid[row][col]
    return [
        room
        for room in AMPHI_ROOMS[amphipod]
        if can_move_to_room(grid, (row, col), room)
    ]


def can_move_to_room(grid, current, room):
    row, col = current
    amphipod = grid[row][col]
    room_row, room_col = room

    if col > room_col:
        for c in range(room_col, col):
            if grid[0][c] != ".":
                # Corridor blocked
                return False
    if col < room_col:
        for c in range(col + 1, room_col + 1):
            # Corridor blocked
            if grid[0][c] != ".":
                return False

    above_pairs_are_free = all(
        grid[pair_row][pair_col] == "."
        for pair_row, pair_col in pair_rooms(room)
        if pair_row < room_row
    )

    below_pairs_are_target = all(
        grid[pair_row][pair_col] == amphipod
        for pair_row, pair_col in pair_rooms(room)
        if pair_row > room_row
    )

    if (
        above_pairs_are_free
        and below_pairs_are_target
        and grid[room_row][room_col] == "."
    ):
        return True
    return False


def is_solved(grid):
    room_fillings = [grid[row][col] for row, col in ROOMS]
    return room_fillings == [
        "A",
        "A",
        "A",
        "A",
        "B",
        "B",
        "B",
        "B",
        "C",
        "C",
        "C",
        "C",
        "D",
        "D",
        "D",
        "D",
    ]


def search(initial_state):
    solutions = []
    new_states = [(initial_state, 0)]
    seen = {}
    min_score = float("+inf")

    while new_states:
        grid, score = new_states.pop()

        if hash(grid) in seen:
            if score >= seen[hash(grid)]:
                continue
        seen[hash(grid)] = score

        for row, col in OPEN_SPACE:
            if grid[row][col] != ".":
                # generate all next possible states
                amphipod = grid[row][col]
                for move_to_row, move_to_col in moves(grid, row, col):
                    new_grid = deepcopy(grid)
                    new_grid[row][col] = "."
                    new_grid[move_to_row][move_to_col] = amphipod
                    new_score = score + ENERGY_TO_M0VE[amphipod] * distance(
                        (row, col), (move_to_row, move_to_col)
                    )
                    if is_solved(new_grid):
                        solutions.append((new_grid, new_score))
                        min_score = min(min_score, new_score)
                    else:
                        if new_score < min_score:
                            new_states.append((new_grid, new_score))

    return solutions


def hash(state):
    s = ""
    for row in state:
        s += "".join(row)
    return s


def display(grid):
    for row in grid:
        print(row)


def main():

    GRID = [
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["#", "#", "D", "#", "A", "#", "D", "#", "C", "#", "#"],
        ["#", "#", "C", "#", "A", "#", "B", "#", "B", "#", "#"],
    ]
    # Once upon a time, this used to solve part 1
    # Not anymore, not anymore...
    # solutions = search(GRID)
    # print(f"Part 2: {min(score for _, score in solutions)}")

    GRID = [
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["#", "#", "D", "#", "A", "#", "D", "#", "C", "#", "#"],
        ["#", "#", "D", "#", "C", "#", "B", "#", "A", "#", "#"],
        ["#", "#", "D", "#", "B", "#", "A", "#", "C", "#", "#"],
        ["#", "#", "C", "#", "A", "#", "B", "#", "B", "#", "#"],
    ]

    solutions = search(GRID)
    print(f"Part 2: {min(score for _, score in solutions)}")


if __name__ == "__main__":
    main()
