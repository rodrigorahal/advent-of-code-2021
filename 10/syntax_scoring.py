import fileinput


OPEN = ["(", "[", "{", "<"]

CLOSE = [")", "]", "}", ">"]

OPEN_BY_CLOSE = dict(zip(CLOSE, OPEN))

CLOSE_BY_OPEN = dict(zip(OPEN, CLOSE))

CORRUPTED_SCORE_BY_CLOSE = dict(zip(CLOSE, [3, 57, 1197, 25137]))

INCOMPLETE_SCORE_BY_CLOSE = dict(zip(CLOSE, [1, 2, 3, 4]))


def parse():
    return [line.strip() for line in fileinput.input()]


def corrupted_score(lines):
    score = 0
    for line in lines:
        status, char = validate(line)
        if status == "corrupted":
            score += CORRUPTED_SCORE_BY_CLOSE[char]
    return score


def incomplete_scores(lines):
    scores = []
    for line in lines:
        status, open = validate(line)
        if status == "incomplete":
            score = 0
            for char in reversed(open):
                close = CLOSE_BY_OPEN[char]
                score = score * 5 + INCOMPLETE_SCORE_BY_CLOSE[close]
            scores.append(score)

    return scores


def validate(line):
    open = []
    close = []
    for char in line:

        if char in OPEN:
            open.append(char)

        elif char in CLOSE:
            open_char = open.pop()
            if open_char != OPEN_BY_CLOSE[char]:
                return "corrupted", char

    if len(open) != 0 or len(close) != 0:
        return "incomplete", open

    return "complete", None


def main():
    lines = parse()
    score = corrupted_score(lines)
    print(f"Part 1: {score}")

    scores = incomplete_scores(lines)
    print(f"Part 2: {sorted(scores)[len(scores)//2]}")


if __name__ == "__main__":
    main()
