import fileinput


def power_rates(report):
    gamma = []
    epislon = []

    entry_size = len(report[0])

    for i in range(entry_size):
        position_bit = "".join(num[i] for num in report)
        sum = position_bit.count("1")

        if sum >= len(report) / 2:
            gamma.append("1")
            epislon.append("0")
        else:
            gamma.append("0")
            epislon.append("1")
    return "".join(gamma), "".join(epislon)


def life_rates(report):
    return filter_rates(report, power_rate=0), filter_rates(report, power_rate=1)


def filter_rates(report, power_rate):
    to_filter = [n for n in report]

    entry_size = len(report[0])

    for i in range(entry_size):
        rate = power_rates(to_filter)[power_rate]
        to_filter = [n for n in to_filter if n[i] == rate[i]]
        if len(to_filter) == 1:
            return to_filter[0]


def parse():
    return [line.strip() for line in fileinput.input()]


def main():
    report = parse()
    gamma, epislon = power_rates(report)
    print(f"Part 1: { int(gamma, 2) * int(epislon, 2) }")
    ox, co = life_rates(report)
    print(f"Part 2: { int(ox, 2) * int(co, 2) } ")


if __name__ == "__main__":
    main()
