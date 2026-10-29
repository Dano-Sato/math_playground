"""Count closure-quotient states via canonical antichains, not enumeration.

Run: python research/2026-10-29-divisor-canonical-antichain/explore.py
Python 3.10+, standard library, exact integers, no RNG.
Counts c=4,28,32,64,128, with at most 200000 memoized subproblems per c.
The clique bound is computed for c=2..512.
"""
import importlib.util
import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    'growth', ROOT/'research/2026-10-29-divisor-period-growth/explore.py')
GROWTH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GROWTH)
Model = GROWTH.Model


def union_graph(m):
    adjacent = [0]*m.r
    for i in range(m.r):
        mask = (m.same_masks[i] | m.prev_masks[i]) & ~(1 << i)
        adjacent[i] |= mask
        for j in range(m.r):
            if mask & (1 << j):
                adjacent[j] |= 1 << i
    return adjacent


def odd_edge(a, b):
    """Exact arithmetic adjacency, independent of the dyadic normalization."""
    g = gcd(a, b)
    small, large = sorted((a//g, b//g))
    if small == large:
        return False
    for neighbor in (large-1, large+1):
        if neighbor % small == 0:
            q = neighbor//small
            if q >= 2 and q & (q-1) == 0:
                return True
    return False


def arithmetic_graph(odds):
    return [sum(1 << j for j, b in enumerate(odds) if odd_edge(a, b))
            for a in odds]


def maxima(m, state):
    return sum(1 << i for i in range(m.r)
               if state & (1 << i)
               and not (state & (m.prev_masks[i] & ~(1 << i))))


def six_block_bound(c):
    blocks = {}
    for o in range(1, c, 2):
        a = b = 0
        work = o
        while work % 3 == 0:
            work //= 3
            a += 1
        while work % 5 == 0:
            work //= 5
            b += 1
        u = o//(3**(a % 3)*5**(b % 2))
        blocks.setdefault(u, []).append(o)
    factors = (1, 3, 5, 9, 15, 45)
    independent_counts = (1, 2, 3, 4, 5, 6, 8)
    sizes = [0]*7
    bound = 1
    for u, block in blocks.items():
        assert sorted(block) == [u*t for t in factors if u*t < c]
        sizes[len(block)] += 1
        bound *= independent_counts[len(block)]
    return blocks, sizes[1:], bound


def count_independent(adjacent, cap=200000):
    memo = {}

    def count(mask):
        if not mask:
            return 1
        if mask in memo:
            return memo[mask]
        if len(memo) >= cap:
            raise RuntimeError(f'independent-set subproblem cap {cap} reached')
        # Factor out isolated vertices before branching.
        isolated = 0
        work = mask
        while work:
            bit = work & -work
            work ^= bit
            i = bit.bit_length()-1
            if not (adjacent[i] & mask):
                isolated |= bit
        if isolated:
            value = (1 << isolated.bit_count())*count(mask & ~isolated)
        else:
            vertices = [i for i in range(len(adjacent)) if mask & (1 << i)]
            v = max(vertices, key=lambda i: (adjacent[i] & mask).bit_count())
            rest = mask & ~(1 << v)
            value = count(rest)+count(rest & ~adjacent[v])
        memo[mask] = value
        return value

    return count((1 << len(adjacent))-1), len(memo)


def even_valuations_base(o):
    a = b = 0
    work = o
    while work % 3 == 0:
        work //= 3
        a += 1
    while work % 5 == 0:
        work //= 5
        b += 1
    return o // (3 if a % 2 else 1) // (5 if b % 2 else 1)


def clique_blocks(c):
    blocks = {}
    for o in range(1, c, 2):
        blocks.setdefault(even_valuations_base(o), []).append(o)
    assert all(set(block) == {u*t for t in (1,3,5,15) if u*t < c}
               for u, block in blocks.items())
    counts = [0]*5
    bound = 1
    for block in blocks.values():
        counts[len(block)] += 1
        bound *= len(block)+1
    return blocks, counts[1:], bound


def main():
    rows = []
    for c in (4, 28, 32, 64, 128):
        m = Model(c)
        graph = union_graph(m)
        count, work = count_independent(graph)
        blocks, sizes, bound = clique_blocks(c)
        _, six_sizes, six_bound = six_block_bound(c)
        assert graph == arithmetic_graph(m.odds)
        row = {'c': c, 'r': m.r, 'quotient_states': count,
               'counting_subproblems': work, 'clique_size_counts': sizes,
               'clique_bound': bound, 'six_block_size_counts': six_sizes,
               'six_block_bound': six_bound,
               'odd_parts_in_bit_order': m.odds,
               'union_masks': graph}
        rows.append(row)
        assert count <= six_bound <= bound
        print(f'c={c}: |Z|={count}, subproblems={work}, '
              f'six-block counts={six_sizes}, bound={six_bound}', flush=True)
    dest = Path(__file__).with_name('counts.json')
    dest.write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Wrote counts.json')


if __name__ == '__main__':
    main()
