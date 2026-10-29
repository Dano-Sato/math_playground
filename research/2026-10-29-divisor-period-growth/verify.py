"""Verify improved bounds, seeds, and multistability certificates.

Run: python research/2026-10-29-divisor-period-growth/verify.py
Python 3.10+, standard library, exact integer arithmetic, no randomness.
Bounds/seed/3-adic matching checks: c=2..512, cap=20000 per orbit.
Independent direct outcome checks: six c values, n<=65536.
Independent-set counts: r=2,14,16,32; exhaustive comparison only r<=16.
"""
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
from explore import Model


def independent(mask, directed):
    return all(not (mask & (1 << i)) or not (mask & neighbors)
               for i, neighbors in enumerate(directed))


def matching(m):
    index = {o: i for i, o in enumerate(m.odds)}
    pairs = []
    used = set()
    for o in m.odds:
        q, v = o, 0
        while q % 3 == 0:
            q //= 3
            v += 1
        if v % 2:
            a, b = index[o//3], index[o]
            assert a not in used and b not in used
            assert (m.same_masks[a] & (1 << b)) or (m.same_masks[b] & (1 << a))
            used.update((a, b))
            pairs.append((a, b))
    return pairs


def count_independent(directed):
    adj = directed.copy()
    r = len(adj)
    for i, mask in enumerate(directed):
        for j in range(r):
            if mask & (1 << j):
                adj[j] |= 1 << i

    @lru_cache(None)
    def count(mask):
        if not mask:
            return 1
        v = max((i for i in range(r) if mask & (1 << i)),
                key=lambda i: (adj[i] & mask).bit_count())
        rest = mask & ~(1 << v)
        return count(rest)+count(rest & ~adj[v])

    return count((1 << r)-1), count.cache_info().currsize


def state_at(m, height):
    if height < m.H-1:
        return m.initial_states[height-(m.J-1)]
    t = height-(m.H-1)
    if t >= len(m.states):
        t = m.mu+(t-m.mu) % m.period
    return m.states[t]


def losing(m, n):
    k = (n & -n).bit_length()-1
    o = n >> k
    if k == 0:
        return True
    if o >= m.c:
        return False
    height = n.bit_length()-1
    if height < m.J-1:
        return True
    return bool(state_at(m, height) & (1 << m.odds.index(o)))


def direct_tables(limit):
    ds = [[] for _ in range(limit+1)]
    for d in range(1, limit//2+1):
        for n in range(2*d, limit+1, d):
            ds[n].append(d)
    return ds


def main():
    here = Path(__file__).resolve().parent
    previous = json.loads((here.parent/'2026-10-29-divisor-outcome-automaton'/
                           'report.json').read_text(encoding='utf-8'))
    old = {row['c']: row for row in previous}
    selected = (28, 29, 32, 33, 64, 65)
    keep = {}
    orbit_states = old_checks = pair_checks = 0
    rows = json.loads((here/'periods.json').read_text(encoding='utf-8'))
    assert len(rows) == 511
    for c in range(2, 513):
        m = Model(c)
        assert m.row() == rows[c-2]
        assert independent(m.seed, m.same_masks)
        assert all(independent(s, m.same_masks) for s in m.states)
        orbit_states += len(m.states)
        pairs = matching(m)
        bound = 3**len(pairs)*2**(m.r-2*len(pairs))
        assert m.mu+m.period <= bound <= 2**m.r
        assert m.alpha > 0
        if c in old:
            row = old[c]
            assert m.odds == row['odd_parts_in_bit_order']
            assert m.same_masks == row['same_masks']
            assert m.prev_masks == row['previous_masks']
            assert m.seed == row['states'][0]
            assert m.states == row['states']
            old_checks += 1
        if c in selected or c == 4:
            keep[c] = m
        if c % 2 == 0 and c < 512:
            other = Model(c+1)
            assert m.odds == other.odds
            assert m.same_masks == other.same_masks
            assert m.prev_masks == other.prev_masks
            pair_checks += 1
    print(f'[A] c=2..512: {orbit_states} orbit states and matching bounds PASS')
    print(f'[B] terminal-shell seeds vs previous direct seeds: {old_checks} PASS')
    print(f'[C] identical stationary maps for adjacent pairs: {pair_checks} PASS')

    exhaustive = 0
    independent_rows = []
    for c in (4, 28, 32, 64):
        m = keep[c]
        count, subproblems = count_independent(m.same_masks)
        assert m.mu+m.period <= count
        if m.r <= 16:
            brute = sum(independent(s, m.same_masks) for s in range(1 << m.r))
            assert count == brute
            exhaustive += 1 << m.r
        independent_rows.append({'c': c, 'r': m.r, 'independent_sets': count,
                                 'recurrence_subproblems': subproblems})
        print(f'[I] c={c}: I(A)={count}, raw={1 << m.r}, '
              f'recurrence subproblems={subproblems}')
    assert [row['independent_sets'] for row in independent_rows] == [3, 287, 858, 401846]
    print(f'[D] exhaustive independent-set masks: {exhaustive} PASS')

    ds = direct_tables(1 << 16)
    direct_count = 0
    for c in selected:
        m = keep[c]
        win = bytearray(len(ds))
        for n in range(1, len(ds)):
            win[n] = any(not win[n-d] for d in ds[n] if d >= c)
            assert losing(m, n) == (not win[n]), (c, n)
            direct_count += 1
    print(f'[E] direct outcome comparisons: {direct_count} PASS')

    assert (keep[64].period, keep[65].period) == (8, 6)
    assert (keep[64].alpha, keep[65].alpha) == (Fraction(19, 2), Fraction(10))
    assert (keep[32].alpha, keep[33].alpha) == (Fraction(11, 2), Fraction(5))
    for m in keep.values():
        cycle = m.states[m.mu:]
        assert all(m.step(s) == cycle[(i+1) % len(cycle)] for i, s in enumerate(cycle))
        assert len(set(cycle)) == m.period
    # Infinite witness follows from the certified cycle; finite phase checks here.
    for k in range(13, 1014):
        assert losing(keep[32], 1 << k) == (k % 2 == 1)
        assert not losing(keep[33], 1 << k)
    print('[F] periods 8/6, alpha decrease, and power-of-two witnesses PASS')

    certificate = {
        'independent_counts': independent_rows,
        'models': [{
            **m.row(), 'odd_parts_in_bit_order': m.odds,
            'same_masks': m.same_masks, 'previous_masks': m.prev_masks,
            'terminal_and_early_states': m.initial_states,
            'transient': m.states[:m.mu], 'cycle': m.states[m.mu:],
        } for _, m in sorted(keep.items())],
    }
    (here/'certificate.json').write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ALL CHECKS PASSED; wrote certificate.json')


if __name__ == '__main__':
    main()
