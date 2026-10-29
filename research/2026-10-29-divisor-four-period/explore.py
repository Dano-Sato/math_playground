"""Conditional exploration: assumes g(2**k * o)=k when o>87.

This script discovers a candidate, not a proof. Standard Python 3.10; no RNG.
Run: python research/2026-10-29-divisor-four-period/explore.py
"""
from functools import lru_cache
import json
from pathlib import Path
import sys

sys.setrecursionlimit(10000)
M = 87
C = 4


@lru_cache(None)
def divisors(o):
    return tuple(e for e in range(1, o + 1, 2) if o % e == 0)


def split(n):
    k = (n & -n).bit_length() - 1
    return k, n >> k


def options(k, o):
    for j in range(k + 1):
        for e in divisors(o):
            if (1 << j) * e < C or (j, e) == (k, o):
                continue
            if j < k:
                yield j, (o << (k - j)) - e
            else:
                t, r = split(o // e - 1)
                yield k + t, e * r


def mex(values):
    v = 0
    while v in values:
        v += 1
    return v


def conditional(k, o):
    if o > M:
        return k
    return inside(k, o)


@lru_cache(None)
def inside(k, o):
    return mex({conditional(j, q) for j, q in options(k, o)})


def main():
    for o in range(1, M + 1, 2):
        vs = [conditional(k, o) for k in range(181)]
        fit = None
        for p in range(1, 31):
            for start in range(0, 100):
                patterns = []
                for r in range(p):
                    vals = [(k, vs[k]) for k in range(start, len(vs)) if k % p == r]
                    if len(vals) < 3:
                        break
                    if len({v-k for k,v in vals}) == 1:
                        patterns.append(('s', vals[0][1]-vals[0][0]))
                    elif len({v for k,v in vals}) == 1:
                        patterns.append(('c', vals[0][1]))
                    else:
                        break
                if len(patterns) == p:
                    fit = (p, start, patterns)
                    break
            if fit:
                break
        if fit != (1, 0, [('s', 0)]):
            print(o, fit, 'first:', vs[:25])
    print(inside.cache_info())
    if '--write-candidate' in sys.argv:
        data = {'c': C, 'M': M, 'K0': 28, 'period': 3, 'columns': {}}
        for o in range(1, M + 1, 2):
            pattern = []
            for r in range(3):
                vals = [(k, conditional(k, o)) for k in range(28, 181) if k % 3 == r]
                shifts = {v-k for k, v in vals}
                consts = {v for k, v in vals}
                if len(shifts) == 1:
                    pattern.append(['shift', shifts.pop()])
                else:
                    assert len(consts) == 1, (o, r)
                    pattern.append(['const', consts.pop()])
            data['columns'][str(o)] = {
                'initial': [conditional(k, o) for k in range(28)],
                'pattern': pattern,
            }
        dest = Path(__file__).with_name('candidate.json')
        dest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('Wrote candidate.json; requires independent finite-certificate checks.')


if __name__ == '__main__':
    main()
