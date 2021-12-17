import fileinput


def parse():
    xt, yt = fileinput.input().readline().strip()[13:].split(", ")
    x0, x1 = map(int, xt[2:].split(".."))
    y0, y1 = map(int, yt[2:].split(".."))

    return (x0, x1), (y0, y1)


def simulate(target, vx, vy):
    x, y = 0, 0
    (xt0, xt1), (yt0, yt1) = target
    maxy = 0
    for _ in range(300):
        x += vx
        y += vy
        dx = -1 if vx > 0 else (1 if x < 0 else 0)
        vx += dx
        vy -= 1
        maxy = max(y, maxy)

        if xt0 <= x <= xt1 and yt0 <= y <= yt1:
            return True, maxy

        if vx == 0 and x < xt0:
            break
        if x > xt1 and y < yt1:
            break
    return False, None


def search(target, yrange):
    peaks = []
    hits = set()
    (xt0, xt1), (yt0, yt1) = target
    for vx in range(xt1 + 1):
        for vy in range(yt0 - 1, yrange):
            hits_target, maxy = simulate(target, vx, vy)
            if hits_target:
                peaks.append(maxy)
                hits.add((vx, vy))
    return max(peaks), hits


def main():
    xt, yt = parse()
    peak, hits = search(target=(xt, yt), yrange=300)
    print(f"Part 1: {peak}")
    print(f"Part 2: {len(hits)}")


if __name__ == "__main__":
    main()
