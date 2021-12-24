import fileinput
from itertools import product


def parse():
    program = []
    for line in fileinput.input():
        instruction = line.strip().split()
        cmd, vars = instruction[0], instruction[1:]
        vars = [cast_to_int(var) for var in vars]
        program.append((cmd, vars))
    return program


def cast_to_int(var):
    try:
        return int(var)
    except:
        return var


def run(program, inputs):
    inputs = inputs[:]
    mem = {"x": 0, "y": 0, "z": 0, "w": 0}
    for cmd, vars in program:

        if cmd == "inp":
            var = vars[0]
            if not inputs:
                return mem
            mem[var] = inputs.pop(0)

        elif cmd == "add":
            a, b = vars
            if isinstance(b, int):
                mem[a] += b
            else:
                mem[a] += mem[b]

        elif cmd == "mul":
            a, b = vars
            if isinstance(b, int):
                mem[a] *= b
            else:
                mem[a] *= mem[b]

        elif cmd == "div":
            a, b = vars
            if isinstance(b, int):
                mem[a] //= b
            else:
                mem[a] //= mem[b]

        elif cmd == "mod":
            a, b = vars
            if isinstance(b, int):
                mem[a] %= b
            else:
                mem[a] %= mem[b]

        elif cmd == "eql":
            a, b = vars
            if isinstance(b, int):
                mem[a] = 1 if mem[a] == b else 0
            else:
                mem[a] = 1 if mem[a] == mem[b] else 0
    return mem


def model_numbers():
    return product(range(9, 0, -1), repeat=14)


def search(program):
    # Yeah, you wish...
    for model_number in product(range(9, 0, -1), repeat=14):
        mem = run(program, list(model_number))
        if mem["z"] == 0:
            return model_number


def z1(W):
    return W[0] + 12


def z2(W):
    return z1(W) * 26 + W[1] + 7


def z3(W):
    return z2(W) * 26 + W[2] + 8


def z4(W):
    return z3(W) * 26 + W[3] + 8


def z5(W):
    return z4(W) * 26 + W[4] + 15


def z6(W):
    if (z5(W) % 26) - 16 == W[5]:
        return z5(W) // 26
    return (z5(W) // 26) * 26 + W[5] + 12


def z7(W):
    return z6(W) * 26 + W[6] + 8


def decompiled(mem, w, X, Y, Z):
    z_prev = mem["z"]

    x = z_prev
    x = x % 26 + X
    z = z_prev // Z
    y = 25
    if x == w:
        y = 0
    y += 1
    z = z * y
    y = w + Y
    if x == w:
        y = 0
    z = z + y

    return z


# Until this far we've come...
# Following is manually solving the input
# by noticing the constraints to bring z down to zero.

# Varying parameters on the input
PARAMETERS = [
    (1, 10, 12),  # PUSH w1 + 12
    (1, 12, 7),  # PUSH  w2 + 7
    (1, 10, 8),  # PUSH w3 + 8
    (1, 12, 8),  # PUSH w4 +8
    (1, 11, 15),  # PUSH w5 + 15
    (26, -16, 12),  # POP w6 - 16
    (1, 10, 8),  # PUSH w7 + 8
    (26, -11, 13),  # POP w8 - 11
    (26, -13, 3),  # POP w9 - 13
    (1, 13, 13),  # PUSH w10 + 13
    (26, -8, 3),  # POP w11 - 8
    (26, -1, 9),  # POP w12 - 1
    (26, -4, 4),  # POP w13 - 4
    (26, -14, 13),  # POP w14 - 14
]

# For z to be brought down to zero, the instructions with div z 26
# must follow the x == w path
# therefore z-prev % 26 - Y must equal current-w
# for example for the digit number 6:
# z5 % 26 - 16 must equal w6
# z5 % 26 being w5 + 15
# this gives us: w5 + 15 - 16 = w6
# we can do this for every pop/push pair:

"""
w5  + 15 - 16 = w6
w7  + 8  - 11 = w8
w4  + 8  - 13 = w9
w10 + 13 - 8  = w11
w3  + 8  - 1  = w12
w2  + 7  - 4  = w13
w1  + 12 - 14 = w14
"""

"""
To find largest: maximize left-most digits
w1  = 9  -> w14 = 7
w2  = 6  -> w13 = 9
w3  = 2  -> w12 = 9
w4  = 9  -> w9  = 4
w5  = 9  -> w6  = 8
w7  = 9  -> w8  = 6
w10 = 4 ->  w11 = 9

To find smallest: minimize left-most digits
w1  = 3 -> w14  = 1
w2  = 1 -> w13  = 4
w3  = 1 -> w12  = 8
w4  = 6 -> w9   = 1
w5  = 2 -> w6   = 1
w7  = 4 -> w8   = 1
w10 = 1 -> w11  = 6 
"""


def main():
    program = parse()

    largest = [9, 6, 2, 9, 9, 8, 9, 6, 4, 4, 9, 9, 9, 7]
    mem = run(program, largest)
    assert mem["z"] == 0
    print(f"Part 1: {''.join(map(str, largest))}")

    smallest = [3, 1, 1, 6, 2, 1, 4, 1, 1, 1, 6, 8, 4, 1]
    mem = run(program, smallest)
    assert mem["z"] == 0
    print(f"Part 2: {''.join(map(str, smallest))}")


if __name__ == "__main__":
    main()
