import fileinput
from itertools import pairwise, tee

def count(depths):
    return sum(1 for a, b in pairwise(depths) if b > a)

def count_with_window(windows):
    return sum(1 for a, b in pairwise(windows) if sum(b) > sum(a))

def triplewise(iterable):
    a, b, c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)

def parse():
    return [int(line) for line in fileinput.input()]

def main():
    depths = parse()
    print(f"Part 1: {count(depths)}")
    print(f"Part 2: {count_with_window(triplewise(depths))}")

if __name__ == "__main__":
    main()
