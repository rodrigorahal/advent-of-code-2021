import fileinput
from math import prod


def parse():
    return [line.strip() for line in fileinput.input()]


def covert(message):
    size = len(message)
    nbits = size * 4
    bits = bin(int(message, 16))[2:].zfill(nbits)
    return bits


def decode_packet(bits, i, versions):
    value = None

    version = int(bits[i : i + 3], 2)
    i += 3

    type_id = int(bits[i : i + 3], 2)
    i += 3

    if type_id == 4:
        digits = ""
        is_last = "1"
        while is_last == "1":
            is_last = bits[i]
            i += 1
            digits += bits[i : i + 4]
            i += 4
        value = int(digits, 2)

    else:
        length_type_id = bits[i]
        i += 1

        if length_type_id == "0":  # total length
            total_length = int(bits[i : i + 15], 2)
            i += 15
            start = i
            values = []
            while i < start + total_length:
                versions, i, subvalue = decode_packet(bits, i, versions)
                values.append(subvalue)

        elif length_type_id == "1":  # num of sub-packets
            nsubpacktes = int(bits[i : i + 11], 2)
            i += 11
            n = 0
            values = []
            while n < nsubpacktes:
                versions, i, subvalue = decode_packet(bits, i, versions)
                values.append(subvalue)
                n += 1

        if type_id == 0:
            value = sum(values)
        elif type_id == 1:
            value = prod(values)
        elif type_id == 2:
            value = min(values)
        elif type_id == 3:
            value = max(values)
        elif type_id == 5:
            value = 1 if values[0] > values[1] else 0
        elif type_id == 6:
            value = 1 if values[0] < values[1] else 0
        elif type_id == 7:
            value = 1 if values[0] == values[1] else 0

    return versions + version, i, value


def decode(bits):
    versions, _, value = decode_packet(bits, i=0, versions=0)
    return versions, value


def main():
    messages = parse()

    for message in messages:
        versions, value = decode(covert(message))
        print(f"versions: {versions}")
        print(f"value: {value}")


if __name__ == "__main__":
    main()
