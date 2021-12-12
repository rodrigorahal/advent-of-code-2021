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


def search_paths(graph, with_revisit=False):
    stack = [("start", ["start"], set(), False)]
    paths = []

    while stack:
        cave, path, visited, has_revisit = stack.pop()

        for adjacent in graph[cave]:
            if adjacent == "start":
                continue
            elif adjacent == "end":
                paths.append(path + ["end"])
                continue
            elif adjacent.isupper():
                stack.append((adjacent, path + [adjacent], visited, has_revisit))
            elif adjacent not in visited:
                stack.append(
                    (adjacent, path + [adjacent], {*visited, adjacent}, has_revisit)
                )
            elif with_revisit and not has_revisit:
                stack.append((adjacent, path + [adjacent], visited, True))
    return paths


def main():
    graph = parse()

    paths = search_paths(graph, with_revisit=False)
    print(f"Part 1: {len(paths)}")

    paths = search_paths(graph, with_revisit=True)
    print(f"Part 2: {len(paths)}")


if __name__ == "__main__":
    main()
