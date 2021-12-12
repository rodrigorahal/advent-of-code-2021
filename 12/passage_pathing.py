import fileinput
from collections import defaultdict, Counter
from pprint import pprint


def parse():
    graph = defaultdict(list)
    for line in fileinput.input():
        v, u = line.strip().split("-")
        graph[v].append(u)
        graph[u].append(v)
    return graph


def search_paths(graph):
    stack = [("start", ["start"])]
    paths = []

    while stack:
        cave, path = stack.pop()

        for adjacent in graph[cave]:
            if adjacent == "end":
                paths.append(path + ["end"])
            elif adjacent.isupper() or (adjacent.islower() and adjacent not in path):
                stack.append((adjacent, path + [adjacent]))
    return paths


def search_paths_with_revisit(graph):
    stack = [("start", ["start"], {})]
    paths = []

    while stack:
        cave, path, counter = stack.pop()

        for adjacent in graph[cave]:
            if adjacent == "start":
                continue
            elif adjacent == "end":
                paths.append(path + ["end"])
                continue
            elif adjacent.isupper():
                stack.append((adjacent, path + [adjacent], {**counter}))
            elif not counter.get(adjacent) or all(
                count < 2 for count in counter.values()
            ):
                stack.append(
                    (
                        adjacent,
                        path + [adjacent],
                        {**counter, adjacent: counter.get(adjacent, 0) + 1},
                    )
                )
    return paths


def main():
    graph = parse()

    paths = search_paths(graph)
    print(f"Part 1: {len(paths)}")

    paths = search_paths_with_revisit(graph)
    print(f"Part 2: {len(paths)}")


if __name__ == "__main__":
    main()
