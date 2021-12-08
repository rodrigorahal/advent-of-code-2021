import fileinput
from collections import defaultdict
from pprint import pprint

SEGMENTS_BY_DISPLAY = {
    0: 6,
    1: 2,  # unique
    2: 5,
    3: 5,
    4: 4,  # unique
    5: 5,
    6: 6,
    7: 3,  # unique
    8: 7,  # unique
    9: 6,
}

PATTERN_BY_DISPLAY = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

WIRES = "abcdefg"


def get_patterns_by_n_segments(n_segments):
    displays = [
        display for display, size in SEGMENTS_BY_DISPLAY.items() if size == n_segments
    ]

    patterns = [set(PATTERN_BY_DISPLAY[display]) for display in displays]

    return patterns


def parse():
    def parse_line(line):
        reads, outputs = line.split(" | ")
        reads = reads.split()
        outputs = outputs.split()
        return (reads, outputs)

    return [parse_line(line) for line in fileinput.input()]


def count_uniques(notes):
    return sum(
        len(output) in {2, 4, 3, 7} for _, outputs in notes for output in outputs
    )


def get_candidates_by_wire(entry):
    candidates_by_wire_per_read = defaultdict(list)
    reads, _ = entry
    for read in sorted(reads, key=len):
        if len(read) in (2, 3, 4, 7):
            patterns = get_patterns_by_n_segments(len(read))
            assert len(patterns) == 1
            for wire in read:
                candidates_by_wire_per_read[wire].append(patterns[0])
        else:
            continue

    for wire in WIRES:
        candidates_by_wire_per_read[wire] = set.intersection(
            *candidates_by_wire_per_read[wire]
        )
    return candidates_by_wire_per_read


def get_wires_by_matching_candidates(candidates_by_wire):
    wires_by_matching_candidates = defaultdict(list)
    for wire, wire_candidates in candidates_by_wire.items():
        if len(wire_candidates) == 2:
            wires_by_matching_candidates["".join(wire_candidates)].append(wire)
    return wires_by_matching_candidates


def update_solved_wires(candidates_by_wire):
    solved_wires = []
    unsolved_wires = []
    for wire in WIRES:
        if len(candidates_by_wire[wire]) == 1:
            solved_wires.append(wire)
        else:
            unsolved_wires.append(wire)

    for solved_wire in solved_wires:
        for unsolved_wire in unsolved_wires:
            candidates_by_wire[unsolved_wire] -= candidates_by_wire[solved_wire]
    return candidates_by_wire


def update_matching_wires(candidates_by_wire):
    prev = 0
    wires_by_matching_candidates = get_wires_by_matching_candidates(candidates_by_wire)
    curr = len(wires_by_matching_candidates)

    while prev != curr:
        for (
            matching_candidates,
            wires_with_matching,
        ) in wires_by_matching_candidates.items():

            for wire in WIRES:
                if wire not in wires_with_matching and len(
                    candidates_by_wire[wire]
                ) > len(matching_candidates):
                    candidates_by_wire[wire] -= set(matching_candidates)

        prev = curr
        wires_by_matching_candidates = get_wires_by_matching_candidates(
            candidates_by_wire
        )
        curr = len(wires_by_matching_candidates)

    return candidates_by_wire


def update_wires_with_multiple_patterns(entry, candidates_by_wire):
    reads, _ = entry
    for reading in sorted(reads, key=len):
        if len(reading) in (2, 4, 3, 7):
            continue

        if len(reading) in (5, 6):
            possible_reading_patterns = get_possible_patterns_from_reading(
                reading, candidates_by_wire
            )
            if len(possible_reading_patterns) == 1:
                pattern = possible_reading_patterns[0]
                for wire in candidates_by_wire:
                    if wire in set(reading):
                        candidates_by_wire[wire] = candidates_by_wire[
                            wire
                        ].intersection(pattern)
                candidates_by_wire = update_solved_wires(candidates_by_wire)
    return candidates_by_wire


def get_possible_patterns_from_reading(read, candidates_by_wire):
    patterns = get_patterns_by_n_segments(len(read))
    impossible = set()
    wires_by_matching_candidates = get_wires_by_matching_candidates(candidates_by_wire)

    for pattern in patterns:
        for wire in read:
            if len(candidates_by_wire[wire]) == 1 and not pattern.intersection(
                candidates_by_wire[wire]
            ):
                impossible.add("".join(pattern))

        for (
            matching_candidates,
            wires_with_matching,
        ) in wires_by_matching_candidates.items():
            if set(wires_with_matching).intersection(set(read)) != set(
                wires_with_matching
            ):
                if set(matching_candidates).intersection(pattern) == set(
                    matching_candidates
                ):
                    impossible.add("".join(pattern))
    return [pattern for pattern in patterns if "".join(pattern) not in impossible]


def get_display(outputs, candidates):
    mapped = [map_output(output, candidates) for output in outputs]
    display = []
    for m in mapped:
        for i in range(10):
            p = PATTERN_BY_DISPLAY[i]
            if set(m) == set(p):
                display.append(str(i))
    return int("".join(display))


def map_output(output, candidates):
    mapped = []
    for wire in output:
        mapped.append(list(candidates[wire])[0])
    return "".join(mapped)


def solve(notes):
    displays = []
    for entry in notes:
        _, outputs = entry
        candidates = get_candidates_by_wire(entry)
        candidates = update_matching_wires(candidates)
        candidates = update_solved_wires(candidates)
        candidates = update_wires_with_multiple_patterns(entry, candidates)
        display = get_display(outputs, candidates)
        displays.append(display)
    return displays


def main():
    notes = parse()
    uniques = count_uniques(notes)
    print(f"Part 1: {uniques}")

    displays = solve(notes)
    print(f"Part 2: {sum(displays)}")


if __name__ == "__main__":
    main()
