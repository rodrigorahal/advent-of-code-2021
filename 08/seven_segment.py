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

    for wire in "abcdefg":
        candidates_by_wire_per_read[wire] = set.intersection(
            *candidates_by_wire_per_read[wire]
        )
    return candidates_by_wire_per_read


def get_matching(candidates):
    matching = defaultdict(list)
    for wire, cs in candidates.items():
        if len(cs) == 2:
            matching["".join(cs)].append(wire)
    return matching


def clean(candidates):
    for wire, cs in candidates.items():
        if len(cs) == 1:
            for w in "abcdefg":
                if w != wire:
                    candidates[w] -= cs
    return candidates


def step(candidates):
    prev_len = 0
    matching = defaultdict(list)
    for wire, cs in candidates.items():
        if len(cs) == 2:
            matching["".join(cs)].append(wire)
    curr_len = len(matching)

    while prev_len != curr_len:
        for k, v in matching.items():
            if len(v) == 1:
                continue

            for wire in "abcdefg":
                if wire not in v and len(candidates[wire]) > len(k):
                    candidates[wire] -= set(k)
        prev_len = curr_len
        for wire, cs in candidates.items():
            if len(cs) == 2:
                matching["".join(cs)].append(wire)
        curr_len = len(matching)

    for wire, cs in candidates.items():
        if len(cs) == 1:
            for w in "abcdefg":
                if w != wire:
                    candidates[w] -= cs

    return candidates


def longs(entry, candidates):
    reads, _ = entry
    for read in sorted(reads, key=len):
        if len(read) in (2, 4, 3, 7):
            continue

        if len(read) == 5 or len(read) == 6:
            cs = get_possible_candidates_from_multiple(read, candidates)
            if len(cs) == 1:
                pattern = cs[0]
                for wire in candidates:
                    if wire in set(read):
                        candidates[wire] = candidates[wire].intersection(pattern)
                        candidates = clean(candidates)

    return candidates


def get_possible_candidates_from_multiple(read, candidates):
    patterns = get_patterns_by_n_segments(len(read))
    impossible = set()
    matching = get_matching(candidates)

    for pattern in patterns:
        for wire in read:
            if len(candidates[wire]) == 1 and not pattern.intersection(
                candidates[wire]
            ):
                impossible.add("".join(pattern))

        for cs, wires in matching.items():
            if (wires[0] in set(read) and wires[1] not in set(read)) or (
                wires[0] not in set(read) and wires[1] in set(read)
            ):
                if set(cs).intersection(pattern) == set(cs):
                    impossible.add("".join(pattern))
    return [p for p in patterns if "".join(p) not in impossible]


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
        candidates = get_candidates_by_wire(entry)
        candidates = step(candidates)
        candidates = longs(entry, candidates)
        display = get_display(entry[1], candidates)
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
