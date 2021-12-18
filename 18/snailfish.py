import fileinput
import math
from copy import deepcopy


def parse():
    pairs = []
    for line in fileinput.input():
        pairs.append(eval(line.strip()))
    fileinput.close()
    return pairs


def set_in_pair_with_directions(root, directions, value):
    node = root
    for dir in directions[:-1]:
        node = node[dir]
    node[directions[-1]] = value


def get_inorder(root):
    regular_by_order = {}

    def inorder(pair, order=0, directions=None):
        if not directions:
            directions = []
        if isinstance(pair, int):
            regular_by_order[order] = (pair, directions)
            return order + 1, directions

        order, _ = inorder(pair[0], order, directions + [0])
        order, _ = inorder(pair[1], order, directions + [1])
        return order, directions

    pair = root
    inorder(pair)

    return regular_by_order


def traverse_explode(root):
    def recurse(pair, depth=0, order=0, has_exploded=False):
        if isinstance(pair, int):
            return order + 1, depth, has_exploded

        order, left_depth, has_exploded = recurse(
            pair[0], depth + 1, order, has_exploded
        )

        if left_depth == 5 and isinstance(pair, list):
            left, right = pair
            if isinstance(left, int) and isinstance(right, int) and not has_exploded:
                explode(root, left, right, order, regular_by_order)
                has_exploded = True

        order, right_depth, has_exploded = recurse(
            pair[1], depth + 1, order, has_exploded
        )

        return order, max(left_depth, right_depth), has_exploded

    regular_by_order = get_inorder(root)
    pair = root
    _, _, exploded = recurse(pair)
    return root, exploded


def traverse_split(root):
    def recurse(pair, has_splitted=False):
        if isinstance(pair, int):
            return has_splitted

        left_splitted = recurse(pair[0], has_splitted)

        if isinstance(pair[0], int) and pair[0] >= 10 and not has_splitted:
            pair[0] = [math.floor(pair[0] / 2), math.ceil(pair[0] / 2)]
            left_splitted = True

        right_splitted = recurse(pair[1], left_splitted)

        if isinstance(pair[1], int) and pair[1] >= 10 and not left_splitted:
            pair[1] = [math.floor(pair[1] / 2), math.ceil(pair[1] / 2)]
            right_splitted = True

        return left_splitted or right_splitted

    pair = root
    splitted = recurse(pair)
    return root, splitted


def explode(root, left, right, order, regular_by_order):
    if order > 1:
        leftmost, leftmost_directions = regular_by_order[order - 2]
        set_in_pair_with_directions(root, leftmost_directions, left + leftmost)

    if order < len(regular_by_order) - 1:
        rightmost, rightmost_directions = regular_by_order[order + 1]
        set_in_pair_with_directions(root, rightmost_directions, rightmost + right)
    _, exploded_directions = regular_by_order[order - 1]
    set_in_pair_with_directions(root, exploded_directions[:-1], 0)


def reduce(pair):
    pair, exploded = traverse_explode(pair)
    if exploded:
        return reduce(pair)

    pair, splitted = traverse_split(pair)
    if splitted:
        return reduce(pair)
    return pair


def sum_pairs(pairs):
    pair = pairs[0]
    for next_pair in pairs[1:]:
        pair = add_pairs(pair, next_pair)
        pair = reduce(pair)
    return pair


def add_pairs(a, b):
    return [a, b]


def magnitude(pair):
    left, right = pair
    left_magnitude = 3 * left if isinstance(left, int) else 3 * magnitude(left)
    right_magnitude = 2 * right if isinstance(right, int) else 2 * magnitude(right)
    return left_magnitude + right_magnitude


def simulate(pairs):
    magnitudes = []
    for i, x in enumerate(pairs):
        for j, y in enumerate(pairs):
            if i != j:
                magnitudes.append(magnitude(sum_pairs([deepcopy(x), deepcopy(y)])))
                magnitudes.append(magnitude(sum_pairs([deepcopy(y), deepcopy(x)])))
    return max(magnitudes)


def main():
    pairs = parse()
    pair = sum_pairs(pairs)
    print(f"Part 1: {magnitude(pair)}")

    pairs = parse()
    print(f"Part 2: {simulate(pairs)}")


if __name__ == "__main__":
    main()
