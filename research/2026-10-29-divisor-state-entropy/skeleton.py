"""A binary triangle skeleton inside the canonical divisor graph.

Run: python research/2026-10-29-divisor-state-entropy/skeleton.py
Python 3.10+, standard library, no RNG. r <= 4096; recurrence depth <=12
for the saved exact sequence. Displayed decimals are not used in proofs.
"""
from functools import lru_cache
from pathlib import Path
from math import exp, log
import json


def oddpart(n):
    assert n > 0
    return n//(n & -n)


def skeleton_graph(r):
    vertices = list(range(1,2*r,2))
    adjacent = [0]*r
    for i,n in enumerate(vertices[1:], 1):
        for p in (oddpart(n-1), oddpart(n+1)):
            assert p < n
            j = (p-1)//2
            adjacent[i] |= 1 << j
            adjacent[j] |= 1 << i
    return adjacent


def count_skeleton(r):
    if r == 1:
        return 2
    ceiling = 2*r-1

    def subtree(v, a, b):
        # Index 2*x_a+x_b; boundary state 11 is forbidden by the base edge.
        if v > ceiling:
            return (1,1,1,0)
        p, q = oddpart(v-1), oddpart(v+1)
        assert {p,q} == {a,b}
        left = subtree(2*v-1, v, p)
        right = subtree(2*v+1, v, q)
        out = []
        for xa,xb in ((0,0),(0,1),(1,0)):
            boundary = {a:xa,b:xb}
            total = 0
            for xv in (0,1):
                if xv and (xa or xb):
                    continue
                total += left[2*xv+boundary[p]]*right[2*xv+boundary[q]]
            out.append(total)
        return (*out,0)

    # Two triangle subtrees on the same root edge {1,3}.
    left = subtree(5, 3, 1)
    right = subtree(7, 3, 1)
    return sum(left[i]*right[i] for i in range(3))


def complete_sequence(hmax=12):
    a = b = 1
    result = [(a,b)]
    for _ in range(hmax):
        a,b = a*a+b*b, a*b
        result.append((a,b))
    return result


def decompose(r):
    """Perfect off-spine subtrees and at most one incomplete spine."""
    ceiling = 2*r-1
    heights = []
    partial = 0

    def size(v):
        total = 0
        low = high = v
        while low <= ceiling:
            total += (min(high,ceiling)-low)//2+1
            low,high = 2*low-1,2*high+1
        return total

    def visit(v):
        nonlocal partial
        m = size(v)
        if not m:
            return
        if (m+1) & m == 0:
            heights.append((m+1).bit_length()-1)
        else:
            partial += 1
            visit(2*v-1)
            visit(2*v+1)

    if r >= 2:
        visit(5)
        visit(7)
    return partial,heights


def main():
    seq = complete_sequence()
    rows = []
    for r in (1,2,3,4,8,14,16,32,64,128,256,512,1024,4096):
        value = count_skeleton(r)
        p,heights = decompose(r)
        row = {'r':r,'independent_sets':value,'partial_vertices':p,
               'complete_heights':heights}
        rows.append(row)
        print(f'r={r}: {str(value)[:64]}'
              f'{"..." if value.bit_length()>210 else ""}; p={p}, heights={heights}',
              flush=True)
    q = 1.0
    z = 0.0
    for h in range(40):
        z += 2**(-h-1)*log(1+q*q)
        q /= 1+q*q
    output = {'cases':rows,'complete_sequence':seq,'display_beta':exp(z)}
    Path(__file__).with_name('skeleton.json').write_text(
        json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'display beta={exp(z):.12f}')


if __name__ == '__main__':
    main()
