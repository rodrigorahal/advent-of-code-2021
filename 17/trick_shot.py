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
        if y > maxy:
            maxy = y

        if xt0 <= x <= xt1 and yt0 <= y <= yt1:
            return True, maxy

        if vx == 0 and x < xt0:
            break
        if x > xt1 and y < yt1:
            break
    return False, None


def search(target, vrange=50):
    peaks = []
    hits = set()
    for vx in range(-vrange, vrange):
        for vy in range(-vrange, vrange):
            hits_target, maxy = simulate(target, vx, vy)
            if hits_target:
                peaks.append(maxy)
                hits.add((vx, vy))
    return max(peaks), hits


def main():
    xt, yt = parse()
    peak, vlcts = search(target=(xt, yt), vrange=300)
    print(f"Part 1: {peak}")
    print(f"Part 2: {len(vlcts)}")


if __name__ == "__main__":
    main()
