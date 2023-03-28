import random

import numpy as np
from pylfsr import LFSR
import binascii


def init_state():
    size = 1 << 6
    state = np.zeros(size)
    p1 = random.randint(2, 1 << 5)
    p2 = random.randint(2, 1 << 5)
    if p1 == p2:
        p2 += 1
    state[0] = 1
    fpoly = [p1, p2]
    L = LFSR(fpoly=fpoly, initstate=state, verbose=False)
    L.info()
    return L


def encode(L, st):
    st_bytes = str.encode(st)
    res = []
    for sb in st_bytes:
        l_out = L.runKCycle(8)
        num = 0
        for i, ls in enumerate(l_out):
            if ls == 1:
                num += 1 << i
        res.append(sb ^ num)
    res = binascii.hexlify(bytearray(res))
    return res


flag = '**********'
if __name__ == '__main__':
    l = init_state()
    res = encode(l, flag)
    print(res.decode())  # 76726e6374667be26535645d6c33662569535762f2167455dd73b674b43d536d
