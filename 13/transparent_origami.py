import fileinput
from collections import defaultdict
from pprint import pprint


def parse():
    paper = set()
    instructions = []
    file = fileinput.input()

    for line in file:
        if line == "\n":
            break

        y, x = line.strip().split(",")
        paper.add((int(x), int(y)))

    for line in file:
        _, _, along = line.strip().split(" ")
        dir, axis = along.split("=")
        instructions.append((dir, int(axis)))

    return paper, instructions


def fold(paper, instructions):
    for dir, axis in instructions:
        if dir == "x":
            paper = fold_left(paper, axis)
        if dir == "y":
            paper = fold_up(paper, axis)
    return paper


def fold_left(paper, axis):
    folded = set()
    for x, y in paper:
        if y > axis:
            ny = (y - axis) - 1
        if y < axis:
            ny = abs(y - axis) - 1
        folded.add((x, ny))
    return folded


def fold_up(paper, axis):
    folded = set()
    for x, y in paper:
        if x > axis:
            nx = 2 * axis - x
        if x < axis:
            nx = x
        folded.add((nx, y))
    return folded


def display_paper(paper):
    max_x = max(x for x, _ in paper)
    max_y = max(y for _, y in paper)

    for x in range(max_x + 1):
        chars = []
        for y in range(max_y + 1, -1, -1):
            if (x, y) not in paper:
                chars.append(".")
            else:
                chars.append("#")
        print(" ".join(chars))
    print()


def main():
    paper, instructions = parse()

    folded = fold(paper, instructions[:1])
    print(f"Part 1: {len(folded)}")

    print("Part 2:")
    folded = fold(paper, instructions)
    display_paper(folded)


if __name__ == "__main__":
    main()
