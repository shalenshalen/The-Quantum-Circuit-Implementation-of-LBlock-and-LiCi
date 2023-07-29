# LBLOCK

# from projectq import MainEngine
from projectq.cengines import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdag, Swap
from projectq.backends import CircuitDrawer, ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control


def MAJOR(eng, K, X, L, R):
    print('MAJOR...')

    for i in range(0, 32):
        R[i] = X[i]
        L[i] = X[i + 32]

    for round in range(0, 32, 2):

        L[28:32] = SBOX0(eng, L[28:32])
        L[24:28] = SBOX0(eng, L[24:28])
        L[20:24] = SBOX0(eng, L[20:24])
        L[16:20] = SBOX0(eng, L[16:20])
        L[12:16] = SBOX0(eng, L[12:16])
        L[8:12] = SBOX0(eng, L[8:12])
        L[4:8] = SBOX0(eng, L[4:8])
        L[0:4] = SBOX0(eng, L[0:4])
        CNOT32(eng, L, R)
        CNOT32(eng, K[0:32], R)

        R = S_plus_b_32(eng, R, 3)

        CNOT32(eng, R, L)
        CNOT32(eng, K[32:64], L)

        L = S_minus_a_32(eng, L, 7)

        if (round != 30):
            K = S_plus_b_128(eng, K, 13)
            K[0:4] = SBOX0(eng, K[0:4])
            K[4:8] = SBOX0(eng, K[4:8])
            AddConstant(eng, K, round)

            R[28:32] = SBOX0(eng, R[28:32])
            R[24:28] = SBOX0(eng, R[24:28])
            R[20:24] = SBOX0(eng, R[20:24])
            R[16:20] = SBOX0(eng, R[16:20])
            R[12:16] = SBOX0(eng, R[12:16])
            R[8:12] = SBOX0(eng, R[8:12])
            R[4:8] = SBOX0(eng, R[4:8])
            R[0:4] = SBOX0(eng, R[0:4])

            CNOT32(eng, R, L)
            CNOT32(eng, K[0:32], L)

            L = S_plus_b_32(eng, L, 3)

            CNOT32(eng, L, R)
            CNOT32(eng, K[32:64], R)

            R = S_minus_a_32(eng, R, 7)

            K = S_plus_b_128(eng, K, 13)
            K[0:4] = SBOX0(eng, K[0:4])
            K[4:8] = SBOX0(eng, K[4:8])
            AddConstant(eng, K, (round + 1))

        # Standard vector output test
        if (not resource_check):
            if (round == 30):
                print_state(eng, R)
                print_state(eng, L)


def AddConstant(eng, x, round):
    if (round & 1):
        X | x[59]
    if ((round >> 1) & 1):
        X | x[60]
    if ((round >> 2) & 1):
        X | x[61]
    if ((round >> 3) & 1):
        X | x[62]
    if ((round >> 4) & 1):
        X | x[63]


def SBOX0(eng, b):
    temp = []

    temp.append(b[3])
    temp.append(b[2])
    temp.append(b[1])
    temp.append(b[0])

    CNOT | (temp[0], temp[1])
    Toffoli_gate(eng, temp[2], temp[1], temp[0])
    Toffoli_gate(eng, temp[3], temp[2], temp[1])
    CNOT | (temp[0], temp[3])
    CNOT | (temp[2], temp[3])
    X | temp[1]
    CNOT | (temp[1], temp[2])
    Toffoli_gate(eng, temp[3], temp[1], temp[0])
    CNOT | (temp[3], temp[1])
    Toffoli_gate(eng, temp[3], temp[0], temp[1])

    new_b = []
    new_b.append(temp[2])
    new_b.append(temp[1])
    new_b.append(temp[0])
    new_b.append(temp[3])

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


def S_plus_b_128(eng, y, n):  # L-rotation

    new_y = []
    for i in range(128):
        new_y.append(y[(128 - n + i) % 128])

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
    K = eng.allocate_qureg(128)
    L = eng.allocate_qureg(32)
    R = eng.allocate_qureg(32)

    if (not resource_check):
        Round_constant_XOR(eng, X, 0x0000000000000000, 64)
        Round_constant_XOR(eng, K, 0x00000000000000000000000000000000, 128)
        #Round_constant_XOR(eng, X, 0x0000000000000000, 64)
        #Round_constant_XOR(eng, K, 0xffffffffffffffffffffffffffffffff, 128)
        print_input(eng, X, K)

    MAJOR(eng, K, X, L, R)


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
