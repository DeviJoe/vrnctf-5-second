import numpy as np
from pylfsr import LFSR


def brute_solve(st):
    size = 1 << 6
    state = np.zeros(size)
    state[0] = 1
    for p1 in range(2, (1 << 5) + 1):
        for p2 in range(2, (1 << 5) + 1):
            if p1 == p2:
                p2 += 1
            fpoly = [p1, p2]
            L = LFSR(fpoly=fpoly, initstate=state, verbose=False)
            b_st = bytes.fromhex(st)
            res = []
            ok = True
            for sb in b_st:
                l_out = L.runKCycle(8)
                num = 0
                for i, ls in enumerate(l_out):
                    if ls == 1:
                        num += 1 << i
                ch = sb ^ num
                if ch < 20 or ch > 128:
                    ok = False
                res.append(ch)
            if ok:
                print("".join(map(chr, res)))


if __name__ == '__main__':
    res = '76726e6374667be26535645d6c33662569535762f2167455dd73b674b43d536d'
    brute_solve(res)
