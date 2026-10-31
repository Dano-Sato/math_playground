"""Bound the entropy of the divisor-game canonical state space.

Run: python research/2026-10-29-divisor-state-entropy/explore.py
Python 3.10+, standard library. No RNG. Exact graph/counts/exponents.
Nine fixed finite block configurations; 200000 subproblems per configuration.
Floating logarithms are display only; verify.py certifies the chosen bound.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import gcd, exp, log
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    'canonical', ROOT/'research/2026-10-29-divisor-canonical-antichain/explore.py')
CANONICAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CANONICAL)
odd_edge = CANONICAL.odd_edge
arithmetic_graph = CANONICAL.arithmetic_graph


def factors(config):
    result = [1]
    for p, k in config:
        result = [a*p**e for a in result for e in range(k)]
    return sorted(result)


def prefix_counts(vertices, cap=200000):
    adjacent = arithmetic_graph(vertices)
    visited = 0

    @lru_cache(None)
    def count(mask):
        nonlocal visited
        visited += 1
        if visited > cap:
            raise RuntimeError(f'cap {cap} reached')
        if not mask:
            return 1
        # Split at the connected component of the first vertex.
        reached = 0
        work = mask & -mask
        while work:
            bit = work & -work
            work ^= bit
            if reached & bit:
                continue
            reached |= bit
            work |= adjacent[bit.bit_length()-1] & mask & ~reached
        if reached != mask:
            return count(reached)*count(mask ^ reached)
        v = max((i for i in range(len(vertices)) if mask & (1 << i)),
                key=lambda i: ((adjacent[i] & mask).bit_count(), i))
        rest = mask & ~(1 << v)
        return count(rest)+count(rest & ~adjacent[v])

    values = [count((1 << j)-1) for j in range(1, len(vertices)+1)]
    return values, visited


def exponents(config, vertices):
    rho = Fraction(1, 2)
    for p, k in config:
        rho *= Fraction(p-1, p)/ (1-Fraction(1, p**k))
    inverses = [Fraction(1, m) for m in vertices]+[Fraction(0)]
    weights = [2*rho*(inverses[j]-inverses[j+1]) for j in range(len(vertices))]
    return rho, weights


def block_bound(c, config, vertices, counts):
    groups = {}
    for o in range(1, c, 2):
        u = o
        for p, k in config:
            val = 0
            work = o
            while work % p == 0:
                work //= p
                val += 1
            u //= p**(val % k)
        groups.setdefault(u, []).append(o)
    bound = 1
    for u, block in groups.items():
        assert sorted(block) == [u*m for m in vertices if u*m < c]
        bound *= counts[len(block)-1]
    return bound, groups


CONFIGS = [
    ((3,3),(5,2)),
    ((3,3),(5,2),(7,2)),
    ((3,4),(5,3),(7,2)),
    ((3,5),(5,3),(7,2)),
    ((3,6),(5,4),(7,2)),
    ((3,4),(5,3),(7,2),(11,2)),
    ((3,4),(5,3),(7,2),(11,2),(13,2)),
    ((3,5),(5,3),(7,2),(11,2)),
    ((3,6),(5,4),(7,3)),
]


def main():
    rows = []
    for config in CONFIGS:
        vertices = factors(config)
        try:
            counts, visited = prefix_counts(vertices)
        except RuntimeError as exc:
            row = {'config':config, 'vertices':vertices, 'status':str(exc)}
            rows.append(row)
            print(f'{config}: {exc}', flush=True)
            continue
        rho, weights = exponents(config, vertices)
        log_beta = sum(float(w)*log(b) for w,b in zip(weights, counts))
        row = {'config':config, 'vertices':vertices, 'status':'complete',
               'prefix_counts':counts, 'subproblems':visited,
               'density':str(rho), 'exponents':[str(x) for x in weights],
               'display_beta':exp(log_beta)}
        rows.append(row)
        print(f'{config}: {len(vertices)} vertices, {visited} subproblems, '
              f'beta={exp(log_beta):.12f}', flush=True)
    Path(__file__).with_name('blocks.json').write_text(
        json.dumps(rows, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
