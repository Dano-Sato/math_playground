"""Self-check with independent constructions, exact integers, no RNG.

Run: python research/2026-10-29-divisor-canonical-antichain/verify.py
Python 3.10+, standard library. c=2..512 structural checks; exhaustive c<=32
Boolean tests at c=4,28,32 and independent-set comparison at c=64.
No complete enumeration at c=128 is claimed.
"""
import importlib.util
import json
from collections import Counter
from functools import lru_cache
from math import log
from pathlib import Path

from explore import (Model, ROOT, arithmetic_graph, count_independent, maxima,
                     odd_edge, six_block_bound, union_graph)

SPEC = importlib.util.spec_from_file_location(
    'quotient', ROOT/'research/2026-10-29-divisor-order-quotient/explore.py')
QUOTIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUOTIENT)
closure, response = QUOTIENT.closure, QUOTIENT.response


def independent(mask, graph):
    return all(not (graph[i] & mask) for i in range(len(graph))
               if mask & (1 << i))


def enumerate_independent(graph, mask=None):
    if mask is None:
        mask = (1 << len(graph))-1
    if not mask:
        yield 0
        return
    bit = mask & -mask
    i = bit.bit_length()-1
    rest = mask ^ bit
    yield from enumerate_independent(graph, rest)
    for state in enumerate_independent(graph, rest & ~graph[i]):
        yield state | bit


def alternate_count(graph):
    """Different pivot plus connected-component splitting for c=128."""
    visited = 0
    @lru_cache(None)
    def solve(mask):
        nonlocal visited
        visited += 1
        if visited > 200000:
            raise RuntimeError('alternate counting cap 200000 reached')
        if not mask:
            return 1
        start = mask & -mask
        reached = 0
        work = start
        while work:
            bit = work & -work
            work ^= bit
            if reached & bit:
                continue
            reached |= bit
            work |= graph[bit.bit_length()-1] & mask & ~reached
        if reached != mask:
            return solve(reached)*solve(mask ^ reached)
        # Largest-index tie break differs from the main counter's first pivot.
        i = max((j for j in range(len(graph)) if mask & (1 << j)),
                key=lambda j: ((graph[j] & mask).bit_count(), j))
        rest = mask & ~(1 << i)
        return solve(rest)+solve(rest & ~graph[i])
    value = solve((1 << len(graph))-1)
    return value, solve.cache_info().currsize


def literal_union_graph(m):
    h = m.H
    n = [o << (h-(o.bit_length()-1)) for o in m.odds]
    graph = [0]*m.r
    for i in range(m.r):
        for j in range(m.r):
            if i == j:
                continue
            for target in (n[j], n[j]//2):
                d = n[i]-target
                if m.c <= d < n[i] and n[i] % d == 0:
                    graph[i] |= 1 << j
                    graph[j] |= 1 << i
    return graph


def base_count(t):
    # Count w coprime to 30 by residue classes, then sum 27^a 25^b.
    def coprime30(x):
        return 8*(x//30)+sum(1 for a in (1,7,11,13,17,19,23,29) if a <= x % 30)
    total = 0
    p = 1
    while p <= t:
        q = p
        while q <= t:
            total += coprime30(t//q)
            q *= 25
        p *= 27
    return total


def main():
    edge_pairs = structural_samples = base_cases = 0
    for c in range(2, 513):
        m = Model(c)
        graph = union_graph(m)
        assert graph == arithmetic_graph(m.odds) == literal_union_graph(m)
        edge_pairs += m.r*(m.r-1)//2
        blocks, sizes, bound = six_block_bound(c)
        r0 = c-1
        thresholds = (1,3,5,9,15,45)
        counts = [base_count(r0//s) for s in thresholds]+[0]
        assert sizes == [counts[j]-counts[j+1] for j in range(6)]
        base_cases += 6
        for u, block in blocks.items():
            g = arithmetic_graph(block)
            value, _ = count_independent(g)
            assert value == (1,2,3,4,5,6,8)[len(block)]
        for x in (0, (1 << m.r)-1, m.seed,
                  sum(1 << i for i in range(0, m.r, 2))):
            s = maxima(m, x)
            assert maxima(m, closure(m, x)) == s
            assert closure(m, s) == closure(m, x)
            assert maxima(m, s) == s
            assert m.step(s) == m.step(x)
            assert maxima(m, m.step(x)) == maxima(m, m.step(s))
            structural_samples += 1
    print(f'[A] arithmetic/direct-move graph equality: 511 maps, {edge_pairs} pairs PASS')
    print(f'[B] maxima projection: {structural_samples} samples PASS; '
          f'six-block count formulas: {base_cases} cases PASS')

    summaries = []
    total_original = total_canonical = full_cube = 0
    old_rows = json.loads((ROOT/'research/2026-10-29-divisor-order-quotient/quotients.json')
                          .read_text(encoding='utf-8'))
    for c in (4,28,32,64):
        m = Model(c)
        graph = union_graph(m)
        original = list(QUOTIENT.independent_sets(m))
        images = {closure(m, x) for x in original}
        representatives = list(enumerate_independent(graph))
        represented = {closure(m, s) for s in representatives}
        assert len(representatives) == len(set(representatives)) == len(images)
        assert images == represented
        fibers = Counter(maxima(m, x) for x in original)
        fiber_cache = {}
        for s in representatives:
            assert maxima(m, closure(m, s)) == s
            assert independent(maxima(m, m.step(s)), graph)
            # Optional fiber formula: choose an A-independent subset below S,
            # excluding S and all its A-neighbors.
            lower = closure(m, s) & ~s
            a_neighbors = 0
            for i in range(m.r):
                if s & (1 << i):
                    a_neighbors |= m.same_masks[i]
                    a_neighbors |= sum(1 << j for j in range(m.r)
                                       if m.same_masks[j] & (1 << i))
            remaining = lower & ~a_neighbors
            if remaining not in fiber_cache:
                # The lower sets are tiny here: direct submask enumeration,
                # separate from the recursive counting algorithm.
                num = 0
                sub = remaining
                while True:
                    if not any(sub & (1 << i) and sub & m.same_masks[i]
                               for i in range(m.r)):
                        num += 1
                    if sub == 0:
                        break
                    sub = (sub-1) & remaining
                fiber_cache[remaining] = num
            assert fibers[s] == fiber_cache[remaining]
        assert sum(fibers.values()) == len(original)
        successors = {s: maxima(m, m.step(s)) for s in representatives}
        cycles = QUOTIENT.cycles_of(successors)
        periods = dict(sorted(Counter(map(len, cycles)).items()))
        old = next(row for row in old_rows if row['c'] == c)
        assert periods == {int(k): v for k,v in old['all_cycle_period_counts'].items()}
        assert len(images) == old['quotient_states']
        if m.r <= 16:
            for x in range(1 << m.r):
                assert maxima(m, closure(m, x)) == maxima(m, x)
                assert m.step(maxima(m, x)) == m.step(x)
            full_cube += 1 << m.r
        total_original += len(original)
        total_canonical += len(representatives)
        print(f'[C] c={c}: originals {len(original)}, representatives {len(representatives)}, '
              f'cycles {periods}, every fiber formula PASS', flush=True)
        summaries.append({'c':c, 'original_states':len(original),
                          'canonical_states':len(representatives),
                          'cycles':periods, 'distinct_fiber_subproblems':len(fiber_cache),
                          'max_fiber_size':max(fibers.values())})
    print(f'[D] originals {total_original}, canonical {total_canonical}, '
          f'full cube {full_cube} PASS')
    m = Model(128)
    value, subproblems = alternate_count(arithmetic_graph(m.odds))
    saved = json.loads(Path(__file__).with_name('counts.json').read_text(encoding='utf-8'))[-1]
    assert value == saved['quotient_states'] == 36489348992
    print(f'[E] c=128 alternate counting {value}, subproblems {subproblems} PASS')
    beta = (43*log(2)+8*log(3)+2*log(5))/78
    print(f'[F] six-block exponential base (display only): {__import__("math").exp(beta):.9f}')
    output = {'graphs_checked':511, 'graph_pairs_checked':edge_pairs,
              'projection_samples':structural_samples, 'block_count_checks':base_cases,
              'full_boolean_checks':full_cube, 'cases':summaries,
              'c128_alternate_subproblems':subproblems,
              'display_only_beta':__import__('math').exp(beta)}
    Path(__file__).with_name('verification.json').write_text(
        json.dumps(output, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
