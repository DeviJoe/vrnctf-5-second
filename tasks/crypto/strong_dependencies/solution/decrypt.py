import binascii
import random

import numpy as np
from pylfsr import LFSR
from tqdm import tqdm

pols = [
    [1, 2, 5, 6, 7, 9, 10, 11, 12, 13, 15],
    [1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 15],
    [1, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14]
]

states = []

N = 3
r = 16
size = 1 << r
length = 1000


def init_state():
    L = []
    for i in range(N):
        state = np.zeros(r)
        for j in range(r):
            state[j] = random.randint(0, 1)
        states.append(state.tolist())
        l = LFSR(fpoly=pols[i], initstate=state, verbose=False)
        L.append(l)
    return L


def get_next(l):
    v = [0] * 3
    for i in range(N):
        v[i] = l[i].next()
    return (v[0] * v[1]) ^ ((v[1] ^ 1) * v[2])


def get_seq(l):
    ans = [0] * length
    for i in range(length):
        ans[i] = get_next(l)

    return ans


def encode(l, st_bytes):
    res = []
    for sb in st_bytes:
        num = 0
        for i in range(8):
            f = get_next(l)
            if f == 1:
                num += 1 << i
        res.append(sb ^ num)
    return res


def init_lfsr(i, state):
    l = LFSR(fpoly=pols[i], initstate=state, verbose=False)
    return l


def get_values(l, n):
    res = []
    for i in range(n):
        res.append(l.next())

    return res


def create_state(s):
    ans = []
    for i in range(r):
        ans.append(s % 2)
        s = s >> 1
    return ans


# 0 0 0 0
# 0 1 0 0
# 0 0 1 1
# 0 1 1 0
# 1 0 0 0
# 1 1 0 1
# 1 0 1 1
# 1 1 1 1
#
# 1 - 6
# 2 - 4
# 3 - 6

def get_likelihood(seq, x, n):
    c = 0
    for i in range(n):
        c += ((-1) ** x[i]) * ((-1) ** seq[i])
    c = c / n
    return c


# https://github.com/MaryAlex/study-Siegenthaler-attack

def correlation_attack(flag, seq):
    n = length // 2
    ans = [[], [], []]
    for j in [0, 2]:
        for s in tqdm(range(1, size)):
            state = create_state(s)
            l = init_lfsr(j, state)
            x = get_values(l, n)
            c = get_likelihood(seq, x, n)
            if c >= 0.5:
                print(c)
                print(state)
                ans[j].append(state)

    print(len(ans[0]))
    print(len(ans[2]))

    for r0 in ans[0]:
        for r2 in ans[2]:
            l0 = init_lfsr(0, r0)
            l2 = init_lfsr(2, r2)

            v0 = get_values(l0, length)
            v2 = get_values(l2, length)

            for s in tqdm(range(1, size)):
                state = create_state(s)
                l1 = init_lfsr(1, state)
                n = length // 2
                v1 = get_values(l1, n)

                x = [(v0[i] * v1[i]) ^ ((v1[i] ^ 1) * v2[i]) for i in range(n)]
                c = get_likelihood(seq, x, n)
                if c > 0.9:
                    decode(flag, [r0, state, r2])


def decode(flag, current_states):
    b_st = bytes.fromhex(flag)
    l = []
    for i in range(N):
        l.append(init_lfsr(i, current_states[i]))
    _ = get_seq(l)
    res = encode(l, b_st)
    print("".join(map(chr, res)))


if __name__ == '__main__':
    res = 'accc717b776efcd050c3610b22ae35424132829654d47010b725f573519c224c3a2cb164b71c33'
    seq = '0,1,0,1,1,1,1,0,0,1,0,0,0,0,1,1,1,1,0,0,1,0,1,1,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,0,1,1,0,0,0,1,1,1,1,1,1,0,0,1,0,1,1,1,1,0,0,0,1,1,0,1,1,0,0,1,0,0,1,1,0,0,0,0,1,1,1,1,0,0,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,1,1,0,0,1,0,0,1,1,1,1,0,1,0,1,1,1,0,1,1,0,0,1,0,1,0,1,1,0,1,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,1,0,1,0,0,1,0,1,1,0,1,1,0,0,1,0,1,0,0,1,0,1,0,1,1,1,0,1,1,0,0,1,0,1,0,0,1,0,1,0,1,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,1,1,0,0,0,0,1,1,0,1,1,0,0,0,1,1,0,0,0,1,1,1,0,1,0,0,1,0,0,1,0,0,1,1,1,1,0,1,1,0,1,0,1,1,0,1,0,0,0,0,1,0,0,1,0,0,1,1,0,0,0,0,1,0,0,1,1,1,1,1,0,1,1,1,0,1,0,0,0,1,1,1,1,1,0,1,0,0,0,0,1,1,0,1,0,0,1,1,1,0,1,0,1,0,0,0,1,0,0,1,1,0,1,1,1,0,1,0,0,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,1,1,0,1,1,1,1,1,0,1,0,0,0,1,1,1,1,1,0,1,0,0,1,0,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,1,1,1,0,1,0,0,1,0,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,1,1,0,0,0,0,1,1,1,0,1,1,0,0,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,0,1,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,1,1,0,0,1,1,0,1,1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1,1,1,0,0,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,1,1,0,0,1,1,1,0,0,1,0,0,0,1,1,0,1,1,0,0,1,0,1,0,0,1,0,1,0,0,1,1,1,0,1,1,1,0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,1,0,1,0,0,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1,0,1,1,1,0,1,1,0,1,0,1,1,1,1,0,1,0,0,0,1,1,1,0,1,0,0,1,1,0,1,1,0,0,0,1,1,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1,1,1,1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,1,1,0,1,1,0,0,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,0,1,1,1,1,0,1,1,1,1,0,1,1,1,0,0,0,1,1,1,0,0,1,1,0,1,0,0,1,1,1,1,1,1,0,0,0,1,0,1,1,0,0,1,1,1,0,0,0,0,0,1,1,0,1,0,1,1,1,0,0,1,1,0,1,0,1,1,0,0,1,1,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,0,0,0,1,1,0,1,0,0,0,1,1,1,0,0,1,1,0,1,1,1,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,1,0,1,1,1,1,0,1,0,1,0,1,1,0,0,0,1,0,1,1,1,1,0,0,0,1,1,1,0,1,0,1,0,0,1,0,1,1,0,1,1,1,1,1,1,0,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,0,1,1,1,1'.split(
        ',')
    seq = list(map(int, seq))
    correlation_attack(res, seq)
