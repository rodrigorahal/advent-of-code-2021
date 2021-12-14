import fileinput
from collections import Counter, defaultdict
from itertools import pairwise
from pprint import pp, pprint


def parse():
    file = fileinput.input()
    template = list(next(file).strip())
    insert_by_pair_rules = {}
    next(file)
    for line in file:
        pair, insert = line.strip().split(" -> ")
        insert_by_pair_rules[pair] = insert
    return template, insert_by_pair_rules


def step_naive(polymer, insert_by_pair_rules):
    updated = polymer[:]

    i = j = 0
    while i < len(polymer) - 1:
        pair = polymer[i] + polymer[i + 1]
        if pair in insert_by_pair_rules:
            updated.insert(j + 1, insert_by_pair_rules[pair])
            j += 1
        i += 1
        j += 1
    return updated


def polymerize_naive(template, insert_by_pair_rules, steps=10):
    polymer = template[:]
    for _ in range(steps):
        polymer = step_naive(polymer, insert_by_pair_rules)
    return polymer


def step_with_pairs(pairs, insert_by_pair_rules, counter):
    previous_pairs = pairs
    current_pairs = defaultdict(int, {**pairs})

    for rule_pair, insert in insert_by_pair_rules.items():
        if rule_pair in previous_pairs:
            count = previous_pairs[rule_pair]

            current_pairs[rule_pair[0] + insert] += count
            current_pairs[insert + rule_pair[1]] += count
            current_pairs[rule_pair] -= count
            if current_pairs[rule_pair] == 0:
                del current_pairs[rule_pair]

            counter[insert] += count

    return current_pairs, counter


def polymerize_with_pairs(template, rules, steps=40):
    counter = Counter(template)
    pairs = Counter(template[i] + template[i + 1] for i in range(len(template) - 1))

    for _ in range(steps):
        pairs, counter = step_with_pairs(pairs, rules, counter)
    return pairs, counter


def main():
    template, insert_by_pair_rules = parse()
    polymer = polymerize_naive(template, insert_by_pair_rules, steps=10)
    counter = Counter(polymer)
    most_common_count = max(counter.items(), key=lambda c: c[1])[1]
    least_common_count = min(counter.items(), key=lambda c: c[1])[1]
    print(f"Part 1: {most_common_count- least_common_count}")

    pairs, counter = polymerize_with_pairs(template, insert_by_pair_rules, steps=40)
    most_common_count = max(counter.items(), key=lambda t: t[1])[1]
    least_common_count = min(counter.items(), key=lambda t: t[1])[1]
    print(f"Part 2: {most_common_count- least_common_count}")


if __name__ == "__main__":
    main()
