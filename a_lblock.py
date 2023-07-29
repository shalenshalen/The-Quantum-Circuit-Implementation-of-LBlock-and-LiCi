# LBLOCK

# from projectq import MainEngine
from projectq.cengines import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdag, Swap
from projectq.backends import CircuitDrawer, ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control


def MAJOR(eng, K, X, L, R, k):
    print('MAJOR...')

    for i in range(0, 32):
        R[i] = X[i]
        L[i] = X[i + 32]

    for round in range(0, 32, 2):

        if (round != 0):
            K = S_plus_b_80(eng, K, 29)
            K[76:80] = SBOX9(eng, K[76:80])
            K[72:76] = SBOX8(eng, K[72:76])
            AddConstant(eng, K, round)

        k = K[48:80]
        CNOT32(eng, k, L)
        L[28:32] = SBOX7(eng, L[28:32])
        L[24:28] = SBOX6(eng, L[24:28])
        L[20:24] = SBOX5(eng, L[20:24])
        L[16:20] = SBOX4(eng, L[16:20])
        L[12:16] = SBOX3(eng, L[12:16])
        L[8:12] = SBOX2(eng, L[8:12])
        L[4:8] = SBOX1(eng, L[4:8])
        L[0:4] = SBOX0(eng, L[0:4])

        L = Permutation(eng, L)

        R = S_plus_b_32(eng, R, 8)

        CNOT32(eng, L, R)

        L[20:24] = SBOX7R(eng, L[20:24])
        L[28:32] = SBOX6R(eng, L[28:32])
        L[16:20] = SBOX5R(eng, L[16:20])
        L[24:28] = SBOX4R(eng, L[24:28])
        L[4:8] = SBOX3R(eng, L[4:8])
        L[12:16] = SBOX2R(eng, L[12:16])
        L[0:4] = SBOX1R(eng, L[0:4])
        L[8:12] = SBOX0R(eng, L[8:12])

        L = PermutationR(eng, L)

        CNOT32(eng, k, L)

        K = S_plus_b_80(eng, K, 29)
        K[76:80] = SBOX9(eng, K[76:80])
        K[72:76] = SBOX8(eng, K[72:76])
        AddConstant(eng, K, (round + 1))

        k = K[48:80]

        CNOT32(eng, k, R)
        R[28:32] = SBOX7(eng, R[28:32])
        R[24:28] = SBOX6(eng, R[24:28])
        R[20:24] = SBOX5(eng, R[20:24])
        R[16:20] = SBOX4(eng, R[16:20])
        R[12:16] = SBOX3(eng, R[12:16])
        R[8:12] = SBOX2(eng, R[8:12])
        R[4:8] = SBOX1(eng, R[4:8])
        R[0:4] = SBOX0(eng, R[0:4])

        R = Permutation(eng, R)

        L = S_plus_b_32(eng, L, 8)

        CNOT32(eng, R, L)

        R[20:24] = SBOX7R(eng, R[20:24])
        R[28:32] = SBOX6R(eng, R[28:32])
        R[16:20] = SBOX5R(eng, R[16:20])
        R[24:28] = SBOX4R(eng, R[24:28])
        R[4:8] = SBOX3R(eng, R[4:8])
        R[12:16] = SBOX2R(eng, R[12:16])
        R[0:4] = SBOX1R(eng, R[0:4])
        R[8:12] = SBOX0R(eng, R[8:12])

        R = PermutationR(eng, R)

        CNOT32(eng, k, R)

        # Standard vector output test
        if (not resource_check):
            if (round == 30):
                print_state(eng, R)
                print_state(eng, L)


def Permutation(eng, x):
    index = [4, 5, 6, 7, 12, 13, 14, 15, 0, 1, 2, 3, 8, 9, 10, 11, 20, 21, 22, 23, 28, 29, 30, 31, 16, 17, 18, 19, 24,
             25, 26, 27]

    new_x = []
    for i in range(32):
        new_x.append(x[index[i]])

    return new_x


def PermutationR(eng, x):
    index = [8, 9, 10, 11, 0, 1, 2, 3, 12, 13, 14, 15, 4, 5, 6, 7, 24, 25, 26, 27, 16, 17, 18, 19, 28, 29, 30, 31, 20,
             21, 22, 23]

    new_x = []
    for i in range(32):
        new_x.append(x[index[i]])

    return new_x


def AddConstant(eng, x, round):
    if (round & 1):
        X | x[46]
    if ((round >> 1) & 1):
        X | x[47]
    if ((round >> 2) & 1):
        X | x[48]
    if ((round >> 3) & 1):
        X | x[49]
    if ((round >> 4) & 1):
        X | x[50]


def SBOX0(eng, b):
    temp = []
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])
    temp.append(b[3])

    CNOT | (temp[3], temp[2])
    X | temp[3]
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[3])
    CNOT | (temp[2], temp[1])
    X | temp[2]
    Toffoli_gate(eng, temp[1], temp[0], temp[2])
    Toffoli_gate(eng, temp[3], temp[2], temp[0])

    new_b = []
    new_b.append(temp[1])
    new_b.append(temp[2])
    new_b.append(temp[0])
    new_b.append(temp[3])

    return new_b


def SBOX0R(eng, b):
    temp = []
    temp.append(b[3])
    temp.append(b[2])
    temp.append(b[0])
    temp.append(b[1])

    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[3])
    X | temp[3]
    CNOT | (temp[3], temp[2])
    Toffoli_gate(eng, temp[3], temp[2], temp[0])
    Toffoli_gate(eng, temp[1], temp[0], temp[2])
    X | temp[0]
    CNOT | (temp[0], temp[3])

    new_b = []
    new_b.append(temp[3])
    new_b.append(temp[2])
    new_b.append(temp[1])
    new_b.append(temp[0])

    return new_b


def SBOX1(eng, b):
    temp = []
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])
    temp.append(b[3])

    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    CNOT | (temp[0], temp[1])
    CNOT | (temp[1], temp[3])
    CNOT | (temp[2], temp[3])
    X | temp[0]
    Toffoli_gate(eng, temp[3], temp[1], temp[2])
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[0])

    new_b = []
    new_b.append(temp[1])
    new_b.append(temp[3])
    new_b.append(temp[0])
    new_b.append(temp[2])

    return new_b


def SBOX1R(eng, b):
    temp = []
    temp.append(b[2])
    temp.append(b[3])
    temp.append(b[1])
    temp.append(b[0])

    Toffoli_gate(eng, temp[3], temp[1], temp[0])
    Toffoli_gate(eng, temp[2], temp[0], temp[3])
    Toffoli_gate(eng, temp[3], temp[2], temp[1])
    X | temp[0]
    CNOT | (temp[1], temp[2])
    CNOT | (temp[3], temp[2])
    CNOT | (temp[0], temp[3])
    Toffoli_gate(eng, temp[2], temp[0], temp[3])

    new_b = []
    new_b.append(temp[1])
    new_b.append(temp[3])
    new_b.append(temp[0])
    new_b.append(temp[2])

    return new_b


def SBOX2(eng, b):
    temp = []
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])
    temp.append(b[3])

    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    CNOT | (temp[0], temp[1])
    CNOT | (temp[1], temp[3])
    CNOT | (temp[2], temp[3])
    X | temp[0]
    Toffoli_gate(eng, temp[3], temp[1], temp[2])
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[0])

    new_b = []
    new_b.append(temp[0])
    new_b.append(temp[3])
    new_b.append(temp[2])
    new_b.append(temp[1])

    return new_b


def SBOX2R(eng, b):
    temp = []
    temp.append(b[3])
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])

    Toffoli_gate(eng, temp[1], temp[0], temp[3])
    Toffoli_gate(eng, temp[3], temp[2], temp[0])
    Toffoli_gate(eng, temp[2], temp[0], temp[1])
    X | temp[3]
    CNOT | (temp[0], temp[2])
    CNOT | (temp[3], temp[0])
    CNOT | (temp[1], temp[2])
    Toffoli_gate(eng, temp[3], temp[2], temp[0])

    new_b = []
    new_b.append(temp[1])
    new_b.append(temp[0])
    new_b.append(temp[3])
    new_b.append(temp[2])

    return new_b


def SBOX3(eng, b):
    temp = []
    temp.append(b[0])
    temp.append(b[3])
    temp.append(b[1])
    temp.append(b[2])

    Toffoli_gate(eng, temp[3], temp[1], temp[2])
    CNOT | (temp[0], temp[1])
    X | temp[3]
    CNOT | (temp[3], temp[2])
    CNOT | (temp[2], temp[0])
    Toffoli_gate(eng, temp[1], temp[0], temp[2])
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[3])

    new_b = []
    new_b.append(temp[0])
    new_b.append(temp[2])
    new_b.append(temp[1])
    new_b.append(temp[3])

    return new_b


def SBOX3R(eng, b):
    temp = []
    temp.append(b[3])
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])

    Toffoli_gate(eng, temp[2], temp[1], temp[0])
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[3], temp[1], temp[2])
    CNOT | (temp[2], temp[3])
    CNOT | (temp[0], temp[2])
    X | temp[0]
    CNOT | (temp[3], temp[1])
    Toffoli_gate(eng, temp[1], temp[0], temp[2])

    new_b = []
    new_b.append(temp[3])
    new_b.append(temp[2])
    new_b.append(temp[0])
    new_b.append(temp[1])

    return new_b


def SBOX4(eng, b):
    temp = []
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])
    temp.append(b[3])

    CNOT | (temp[3], temp[2])
    X | temp[3]
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[3])
    CNOT | (temp[2], temp[1])
    X | temp[2]
    Toffoli_gate(eng, temp[1], temp[0], temp[2])
    Toffoli_gate(eng, temp[3], temp[2], temp[0])

    new_b = []
    new_b.append(temp[1])
    new_b.append(temp[0])
    new_b.append(temp[3])
    new_b.append(temp[2])

    return new_b


def SBOX4R(eng, b):
    temp = []
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])
    temp.append(b[3])

    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[3])
    X | temp[3]
    CNOT | (temp[3], temp[2])
    Toffoli_gate(eng, temp[3], temp[2], temp[0])
    Toffoli_gate(eng, temp[1], temp[0], temp[2])
    X | temp[0]
    CNOT | (temp[0], temp[3])

    new_b = []
    new_b.append(temp[3])
    new_b.append(temp[2])
    new_b.append(temp[1])
    new_b.append(temp[0])

    return new_b


def SBOX5(eng, b):
    temp = []
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])
    temp.append(b[3])

    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    CNOT | (temp[0], temp[1])
    CNOT | (temp[1], temp[3])
    CNOT | (temp[2], temp[3])
    X | temp[0]
    Toffoli_gate(eng, temp[3], temp[1], temp[2])
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[0])

    new_b = []
    new_b.append(temp[3])
    new_b.append(temp[0])
    new_b.append(temp[1])
    new_b.append(temp[2])

    return new_b


def SBOX5R(eng, b):
    temp = []
    temp.append(b[3])
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])

    Toffoli_gate(eng, temp[1], temp[0], temp[2])
    Toffoli_gate(eng, temp[3], temp[2], temp[1])
    Toffoli_gate(eng, temp[3], temp[1], temp[0])
    X | temp[2]
    CNOT | (temp[0], temp[3])
    CNOT | (temp[1], temp[3])
    CNOT | (temp[2], temp[1])
    Toffoli_gate(eng, temp[3], temp[2], temp[1])

    new_b = []
    new_b.append(temp[0])
    new_b.append(temp[1])
    new_b.append(temp[2])
    new_b.append(temp[3])

    return new_b


def SBOX6(eng, b):
    temp = []
    temp.append(b[0])
    temp.append(b[3])
    temp.append(b[1])
    temp.append(b[2])

    Toffoli_gate(eng, temp[3], temp[1], temp[2])
    CNOT | (temp[0], temp[1])
    X | temp[3]
    CNOT | (temp[3], temp[2])
    CNOT | (temp[2], temp[0])
    Toffoli_gate(eng, temp[1], temp[0], temp[2])
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[3])

    new_b = []
    new_b.append(temp[1])
    new_b.append(temp[0])
    new_b.append(temp[3])
    new_b.append(temp[2])

    return new_b


def SBOX6R(eng, b):
    temp = []

    temp.append(b[2])
    temp.append(b[3])
    temp.append(b[1])
    temp.append(b[0])

    Toffoli_gate(eng, temp[3], temp[1], temp[0])
    Toffoli_gate(eng, temp[2], temp[0], temp[3])
    Toffoli_gate(eng, temp[3], temp[2], temp[1])
    CNOT | (temp[1], temp[2])
    CNOT | (temp[2], temp[3])
    CNOT | (temp[0], temp[1])
    X | temp[0]
    Toffoli_gate(eng, temp[3], temp[0], temp[1])

    new_b = []
    new_b.append(temp[2])
    new_b.append(temp[1])
    new_b.append(temp[0])
    new_b.append(temp[3])

    return new_b


def SBOX7(eng, b):
    temp = []
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])
    temp.append(b[3])

    CNOT | (temp[3], temp[2])
    X | temp[3]
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[3])
    CNOT | (temp[2], temp[1])
    X | temp[2]
    Toffoli_gate(eng, temp[1], temp[0], temp[2])
    Toffoli_gate(eng, temp[3], temp[2], temp[0])

    new_b = []
    new_b.append(temp[2])
    new_b.append(temp[1])
    new_b.append(temp[0])
    new_b.append(temp[3])

    return new_b


def SBOX7R(eng, b):
    temp = []

    temp.append(b[3])
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])

    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[3])
    X | temp[3]
    CNOT | (temp[3], temp[2])
    Toffoli_gate(eng, temp[3], temp[2], temp[0])
    Toffoli_gate(eng, temp[1], temp[0], temp[2])
    X | temp[0]
    CNOT | (temp[0], temp[3])

    new_b = []
    new_b.append(temp[3])
    new_b.append(temp[2])
    new_b.append(temp[1])
    new_b.append(temp[0])

    return new_b


def SBOX8(eng, b):
    temp = []

    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])
    temp.append(b[3])

    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    CNOT | (temp[0], temp[1])
    CNOT | (temp[1], temp[3])
    CNOT | (temp[2], temp[3])
    X | temp[0]
    Toffoli_gate(eng, temp[3], temp[1], temp[2])
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[0])

    new_b = []
    new_b.append(temp[1])
    new_b.append(temp[3])
    new_b.append(temp[2])
    new_b.append(temp[0])

    return new_b


def SBOX9(eng, b):
    temp = []

    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])
    temp.append(b[3])

    CNOT | (temp[3], temp[2])
    X | temp[3]
    Toffoli_gate(eng, temp[3], temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[3])
    CNOT | (temp[2], temp[1])
    X | temp[2]
    Toffoli_gate(eng, temp[1], temp[0], temp[2])
    Toffoli_gate(eng, temp[3], temp[2], temp[0])

    new_b = []
    new_b.append(temp[3])
    new_b.append(temp[0])
    new_b.append(temp[1])
    new_b.append(temp[2])

    return new_b


def CNOT32(eng, a, b):
    for i in range(32):
        CNOT | (a[i], b[i])


def S_minus_a_32(eng, x, n):  # R-rotation

    new_x = []
    for i in range(32):
        new_x.append(x[(i + n) % 32])

    return new_x


def S_minus_a_80(eng, x, n):  # R-rotation

    new_x = []
    for i in range(80):
        new_x.append(x[(i + n) % 80])

    return new_x


def S_plus_b_32(eng, y, n):  # L-rotation

    new_y = []
    for i in range(32):
        new_y.append(y[(32 - n + i) % 32])

    return new_y


def S_plus_b_80(eng, y, n):  # L-rotation

    new_y = []
    for i in range(80):
        new_y.append(y[(80 - n + i) % 80])

    return new_y


def num2array(eng, din, bit_width):
    bin_obj = bin(int(din))[2:]
    bin_str = bin_obj.rjust(bit_width, '0')
    o_arr = []
    for ii in range(len(bin_str)):
        o_arr.append(int(bin_str[len(bin_str) - ii - 1]))
    return o_arr


def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if (rc >> i & 1):
            X | k[i]


def print_state(eng, b):
    All(Measure) | b
    print('Ciphertext : 0x', end='')
    print_hex(eng, b)
    print('\n')


def print_input(eng, b, k):
    All(Measure) | b
    All(Measure) | k
    print('Plaintext : 0x', end='')
    print_hex(eng, b)
    print('\nKey : 0x', end='')
    print_hex(eng, k)
    print('\n')


def print_hex(eng, qubits):
    for i in reversed(range(int(len(qubits) / 4))):
        temp = 0
        temp = temp + int(qubits[4 * i + 3]) * 8
        temp = temp + int(qubits[4 * i + 2]) * 4
        temp = temp + int(qubits[4 * i + 1]) * 2
        temp = temp + int(qubits[4 * i])

        temp = hex(temp)
        y = temp.replace("0x", "")
        print(y, end='')


def Toffoli_gate(eng, a, b, c):
    if (resource_check):
        Tdag | a
        Tdag | b
        H | c
        CNOT | (c, a)
        T | a
        CNOT | (b, c)
        CNOT | (b, a)
        T | c
        Tdag | a
        CNOT | (b, c)
        CNOT | (c, a)
        T | a
        Tdag | c
        CNOT | (b, a)
        H | c
    else:
        Toffoli | (a, b, c)


def Run(eng):
    X = eng.allocate_qureg(64)
    K = eng.allocate_qureg(80)
    L = eng.allocate_qureg(32)
    R = eng.allocate_qureg(32)
    k = eng.allocate_qureg(32)

    if (not resource_check):
        # Round_constant_XOR(eng, X, 0x0123456789abcdef, 64)
        # Round_constant_XOR(eng, K, 0x0123456789abcdeffedc, 80)
        Round_constant_XOR(eng, X, 0x0000000000000000, 64)
        Round_constant_XOR(eng, K, 0x00000000000000000000, 80)
        print_input(eng, X, K)

    MAJOR(eng, K, X, L, R, k)


global resource_check
print('Generate Ciphertext...')
Simulate = ClassicalSimulator()
eng = MainEngine(Simulate)
resource_check = 0
Run(eng)

print('Estimate cost...')
Resource = ResourceCounter()
eng = MainEngine(backend=Resource)
resource_check = 1
Run(eng)
print(Resource)
print('\n')
eng.flush()
