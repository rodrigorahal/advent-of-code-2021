import fileinput
from itertools import cycle, pairwise
from typing import Counter

DICE = cycle(range(1, 101))


def parse():
    file = fileinput.input()
    player_1 = int(file.readline().strip().split(": ")[1])
    player_2 = int(file.readline().strip().split(": ")[1])
    return player_1, player_2


def play(player_1, player_2):
    score_1 = score_2 = 0
    rolled = 0

    while score_1 < 1000 and score_2 < 1000:

        roll = sum((next(DICE), next(DICE), next(DICE)))
        rolled += 3
        player_1 = update_player(player_1, roll)
        score_1 += player_1
        if score_1 >= 1000:
            break

        roll = sum((next(DICE), next(DICE), next(DICE)))
        rolled += 3
        player_2 = update_player(player_2, roll)
        score_2 += player_2

    return sorted([score_1, score_2]), rolled


def update_player(player, roll):
    player += roll % 10
    if player > 10:
        return player % 10
    return player


def count_wins(p1, p2, s1, s2, cache):
    if (p1, p2, s1, s2) in cache:
        return cache[(p1, p2, s1, s2)]

    counts = (0, 0)
    for d1 in [1, 2, 3]:
        for d2 in [1, 2, 3]:
            for d3 in [1, 2, 3]:
                new_p1 = update_player(p1, d1 + d2 + d3)
                new_s1 = s1 + new_p1
                if new_s1 >= 21:
                    counts = counts[0] + 1, counts[1]
                    continue

                for d11 in [1, 2, 3]:
                    for d22 in [1, 2, 3]:
                        for d33 in [1, 2, 3]:
                            new_p2 = update_player(p2, d11 + d22 + d33)
                            new_s2 = s2 + new_p2

                            if new_s2 >= 21:
                                counts = counts[0], counts[1] + 1
                                continue

                            w1, w2 = count_wins(new_p1, new_p2, new_s1, new_s2, cache)
                            counts = counts[0] + w1, counts[1] + w2

    cache[(p1, p2, s1, s2)] = counts
    return cache[(p1, p2, s1, s2)]


def main():
    player_1, player_2 = parse()
    (loser, winner), rolled = play(player_1, player_2)
    print(f"Part 1: {loser * rolled}")

    w1, w2 = count_wins(player_1, player_2, 0, 0, {})
    print(f"Part 2: {max(w1, w2)}")


if __name__ == "__main__":
    main()
