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

random.seed('*********************************')


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


flag = '******'
if __name__ == '__main__':
    l = init_state()
    seq = get_seq(l)
    f = open("out.txt", "w")
    f.write(",".join(map(str, seq)) + "\n")
    st_bytes = str.encode(flag)
    res = encode(l, st_bytes)
    res = binascii.hexlify(bytearray(res)).decode()
    f.write(f"Encrypted: {res}")
    f.close()
