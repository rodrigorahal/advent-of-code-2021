import fileinput
from math import prod
from dataclasses import dataclass


@dataclass
class Packet:
    version: int
    type_id: int
    content: str
    endptr: int
    literal: int
    subpackets: list


def parse():
    return [line.strip() for line in fileinput.input()]


def convert(message):
    size = len(message)
    nbits = size * 4
    bits = bin(int(message, 16))[2:].zfill(nbits)
    return bits


def decode(bits):
    packet = decode_packet(bits, i=0)
    return packet


def decode_packet(bits, i):
    version = int(bits[i : i + 3], 2)
    i += 3

    type_id = int(bits[i : i + 3], 2)
    i += 3

    if type_id == 4:
        startptr = i
        digits = ""
        is_last = "1"
        while is_last == "1":
            is_last = bits[i]
            i += 1
            digits += bits[i : i + 4]
            i += 4
        packet = Packet(version, type_id, bits[startptr:i], i, int(digits, 2), [])

    else:
        length_type_id = bits[i]
        i += 1

        if length_type_id == "0":
            startptr = i
            total_length = int(bits[i : i + 15], 2)
            i += 15
            subpackets = []
            while i < startptr + total_length + 15:
                subpacket = decode_packet(bits, i)
                subpackets.append(subpacket)
                i = subpacket.endptr
            packet = Packet(version, type_id, bits[startptr:i], i, None, subpackets)

        elif length_type_id == "1":
            startptr = i
            n_subpackets = int(bits[i : i + 11], 2)
            i += 11
            subpackets = []
            for _ in range(n_subpackets):
                subpacket = decode_packet(bits, i)
                i = subpacket.endptr
                subpackets.append(subpacket)
            packet = Packet(version, type_id, bits[startptr:i], i, None, subpackets)

    return packet


def versions(packet: Packet):
    versions = 0
    stack = [packet]

    while stack:
        packet = stack.pop()
        versions += packet.version

        for subpacket in packet.subpackets:
            stack.append(subpacket)
    return versions


def eval(packet: Packet):
    if packet.type_id == 4:
        return packet.literal

    if packet.type_id == 0:
        return sum(eval(subpacket) for subpacket in packet.subpackets)
    if packet.type_id == 1:
        return prod(eval(subpacket) for subpacket in packet.subpackets)
    if packet.type_id == 2:
        return min(eval(subpacket) for subpacket in packet.subpackets)
    if packet.type_id == 3:
        return max(eval(subpacket) for subpacket in packet.subpackets)
    if packet.type_id == 5:
        return 1 if eval(packet.subpackets[0]) > eval(packet.subpackets[1]) else 0
    if packet.type_id == 6:
        return 1 if eval(packet.subpackets[0]) < eval(packet.subpackets[1]) else 0
    if packet.type_id == 7:
        return 1 if eval(packet.subpackets[0]) == eval(packet.subpackets[1]) else 0


def main():
    messages = parse()

    for message in messages:
        packet = decode(convert(message))
        print(f"Part 1: {versions(packet)}")
        print(f"Part 2: {eval(packet)}")


if __name__ == "__main__":
    main()
