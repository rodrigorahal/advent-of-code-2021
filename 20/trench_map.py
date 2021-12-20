import fileinput
from pprint import pprint


def parse():
    f = fileinput.input()
    enhancement = f.readline().strip()
    f.readline()
    image = {}
    for row, line in enumerate(f):
        for col, pixel in enumerate(line.strip()):
            image[(row, col)] = pixel
    return enhancement, image


def enhanced_area(row, col):
    return [(row + r, col + c) for r in [-1, 0, 1] for c in [-1, 0, 1]]


def enhance(image, enhancement, default="."):
    output = {}
    for row in range(-50, 150):
        for col in range(-50, 150):
            binary_pixels = [
                image.get((r, w), default) for r, w in enhanced_area(row, col)
            ]
            binary_index = "".join(["1" if p == "#" else "0" for p in binary_pixels])
            pixel = enhancement[int(binary_index, 2)]
            output[(row, col)] = pixel
    return output


def process(image, enhancement, times=50):
    def default_pixel(i, flips):
        if not flips:
            return "."
        return "." if i % 2 == 0 else "#"

    flips = enhancement[0] == "#"
    for i in range(times):
        output = enhance(image, enhancement, default=default_pixel(i, flips))
        image = output
    return output


def main():
    enhancement, image = parse()
    output = process(image, enhancement, times=2)
    lit = sum(v == "#" for v in output.values())
    print(f"Part 1: {lit}")
    output = process(image, enhancement, times=50)
    lit = sum(v == "#" for v in output.values())
    print(f"Part 2: {lit}")


if __name__ == "__main__":
    main()
