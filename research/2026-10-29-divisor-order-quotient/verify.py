"""Verify the order/closure quotient and a complete cycle classification.

Run: python research/2026-10-29-divisor-order-quotient/verify.py
Python 3.10+, standard library, exact integers/Fractions, no randomness.
Structural checks: c=2..512. Complete graph checks: c=4,28,32,64.
Uses a different independent-set generator and Kahn pruning for cycle checks.
"""
from collections import Counter, deque
from fractions import Fraction
import json
from pathlib import Path
from explore import Model, closure, response


def independent_masks(earlier):
    """Deletion recurrence; different from the sequential inclusion generator."""
    r = len(earlier)
    adjacent = earlier.copy()
    for i, mask in enumerate(earlier):
        for j in range(r):
            if mask & (1 << j):
                adjacent[j] |= 1 << i

    def visit(remaining, chosen):
        if not remaining:
            yield chosen
            return
        v = remaining.bit_length()-1
        rest = remaining & ~(1 << v)
        yield from visit(rest, chosen)
        yield from visit(rest & ~adjacent[v], chosen | (1 << v))
    yield from visit((1 << r)-1, 0)


def canonical(cycle):
    j = cycle.index(min(cycle))
    return cycle[j:]+cycle[:j]


def graph_analysis(successors):
    """Strip transient vertices by indegree, then enumerate the remaining cycles."""
    indegree = dict.fromkeys(successors, 0)
    for target in successors.values():
        assert target in successors
        indegree[target] += 1
    queue = deque(s for s, degree in indegree.items() if degree == 0)
    removed = []
    while queue:
        s = queue.popleft()
        removed.append(s)
        target = successors[s]
        indegree[target] -= 1
        if indegree[target] == 0:
            queue.append(target)
    cyclic = {s for s, degree in indegree.items() if degree}
    cycles = []
    distance = {}
    period = {}
    while cyclic:
        start = min(cyclic)
        cycle = [start]
        s = successors[start]
        while s != start:
            cycle.append(s)
            s = successors[s]
        for s in cycle:
            cyclic.remove(s)
            distance[s] = 0
            period[s] = len(cycle)
        cycles.append(cycle)
    for s in reversed(removed):
        target = successors[s]
        distance[s] = distance[target]+1
        period[s] = period[target]
    return sorted(cycles, key=lambda seq: (len(seq), seq)), distance, period


def projected_orbit(m):
    seen, sequence = {}, []
    z = closure(m, m.seed)
    while z not in seen:
        seen[z] = len(sequence)
        sequence.append(z)
        z = closure(m, response(m, z))
        assert len(sequence) <= len(m.states)+1
    nu = seen[z]
    period = len(sequence)-nu
    alpha = Fraction(sum(response(m, v).bit_count() for v in sequence[nu:]), period)
    assert period == m.period
    assert nu <= m.mu <= nu+1
    assert alpha == m.alpha


def structural_checks():
    chains = samples = 0
    for c in range(2, 513):
        m = Model(c)
        heights = [1]*m.r
        for i in reversed(range(m.r)):
            row = m.prev_masks[i]
            assert row & (1 << i)
            assert row >> i << i == row
            joined = 0
            for j in range(i, m.r):
                if row & (1 << j):
                    joined |= m.prev_masks[j]
                    if j > i:
                        heights[i] = max(heights[i], heights[j]+1)
            assert joined == row
        expected_height = 1 if c <= 3 else 2 if c <= 135 else 3
        assert max(heights) == expected_height
        if max(heights) == 3:
            chains += 1
        for x in (0, (1 << m.r)-1, m.seed, 1, 1 << (m.r-1)):
            z = closure(m, x)
            assert x | z == z
            assert closure(m, z) == z
            assert response(m, z) == m.step(x)
            samples += 1
        projected_orbit(m)
    print(f'[A] exact order heights and transitivity: 511 maps PASS '
          f'({chains} have height 3)')
    print(f'[B] closure/factorization samples: {samples} PASS; '
          'actual-game quotient orbits: 511 PASS')


def main():
    structural_checks()
    here = Path(__file__).resolve().parent
    rows = json.loads((here/'quotients.json').read_text(encoding='utf-8'))
    summaries = []
    full_boolean_count = all_independent = 0
    for row in rows:
        m = Model(row['c'])
        original = {}
        quotient_set = set()
        for x in independent_masks(m.same_masks):
            original[x] = m.step(x)
            z = closure(m, x)
            assert closure(m, z) == z
            assert response(m, z) == original[x]
            quotient_set.add(z)
        assert len(original) == row['independent_sets']
        assert len(quotient_set) == row['quotient_states']
        all_independent += len(original)
        compressed = {z: closure(m, response(m, z)) for z in quotient_set}
        fcycles, fdist, fperiod = graph_analysis(original)
        tcycles, tdist, _ = graph_analysis(compressed)
        assert tcycles == row['cycles']
        assert max(tdist.values()) == row['max_quotient_transient']
        lifted = sorted((canonical([response(m,z) for z in cy]) for cy in tcycles),
                        key=lambda seq: (len(seq), seq))
        assert lifted == fcycles
        for x in original:
            assert tdist[closure(m,x)] <= fdist[x] <= tdist[closure(m,x)]+1
        if m.r <= 16:
            full = {x: m.step(x) for x in range(1 << m.r)}
            full_cycles, _, _ = graph_analysis(full)
            assert full_cycles == fcycles
            full_boolean_count += len(full)
        summary = {
            'c': m.c,
            'original_periodic_points': sum(map(len, fcycles)),
            'original_cycles': dict(sorted(Counter(map(len, fcycles)).items())),
            'max_original_transient_on_independent_sets': max(fdist.values()),
            'max_original_transient_plus_period': max(fdist[x]+fperiod[x] for x in fdist),
            'max_quotient_transient': max(tdist.values()),
        }
        witness = max(fdist, key=lambda x: fdist[x]+fperiod[x])
        summary['max_sum_witness'] = {
            'state': witness, 'transient': fdist[witness], 'period': fperiod[witness]}
        summaries.append(summary)
        print(f"[C] c={m.c}: cycles={summary['original_cycles']}, "
              f"max_mu={summary['max_original_transient_on_independent_sets']}, "
              f"max(mu+period)={summary['max_original_transient_plus_period']} PASS")
    assert [s['original_cycles'] for s in summaries] == [
        {3: 1}, {2: 6}, {2: 14}, {2: 68, 6: 6, 8: 1}]
    print(f'[D] independently generated independent-set states: {all_independent} PASS')
    print(f'[E] complete Boolean-state comparison (r<=16): {full_boolean_count} PASS')
    (here/'verification.json').write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ALL CHECKS PASSED; wrote verification.json')


if __name__ == '__main__':
    main()
