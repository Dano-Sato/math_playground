"""Check a finite induction certificate for ALL positive n, for c=4.

Python 3.10+, standard library, integer arithmetic, no randomness.
Run: python research/2026-10-29-divisor-four-period/verify.py
The candidate is input, not an assumption: all mex equations are certified
by finite base checks, symbolic tails, and exhaustive boundary shapes.
An independent n-based sieve checks n <= 2**18 as a regression check.
See note.md for the mathematical reduction behind these finite checks.
"""
import json
from math import isqrt
from pathlib import Path

DATA = json.loads(Path(__file__).with_name('candidate.json').read_text(encoding='utf-8'))
C, M, K0, P = (DATA[key] for key in ('c', 'M', 'K0', 'period'))
W = 7
KSTAR = 40


def split(n):
    assert n > 0
    k = (n & -n).bit_length() - 1
    return k, n >> k


def divisors(o):
    return [e for e in range(1, o + 1, 2) if o % e == 0]


def mex(values):
    v = 0
    while v in values:
        v += 1
    return v


def pattern(o, residue):
    return DATA['columns'][str(o)]['pattern'][residue]


def G(k, o):
    assert k >= 0 and o > 0 and o % 2 == 1
    if o > M:
        return k
    if k < K0:
        return DATA['columns'][str(o)]['initial'][k]
    kind, a = pattern(o, k % P)
    return k + a if kind == 'shift' else a


def options(k, o):
    for j in range(k + 1):
        for e in divisors(o):
            if (1 << j) * e < C or (j, e) == (k, o):
                continue
            if j < k:
                yield j, (o << (k-j)) - e
            else:
                t, r = split(o // e - 1)
                yield k+t, e*r


def symbolic_target(delta, q, residue):
    # Target exponent is k+delta and k % P = residue.
    if q > M:
        return 'shift', delta
    kind, a = pattern(q, (residue + delta) % P)
    return (kind, delta+a) if kind == 'shift' else (kind, a)


def check_base():
    count = 0
    for o in range(1, M+1, 2):
        for k in range(KSTAR):
            assert G(k, o) == mex({G(j, q) for j, q in options(k, o)}), (k, o)
            count += 1
    print(f'[A] finite mex equations: {count} PASS')


def check_tail():
    assert (1 << W)-1 > M
    assert KSTAR-W+1 >= K0
    assert KSTAR-W >= 2
    count = 0
    for o in range(1, M+1, 2):
        for residue in range(P):
            # Low options give [2,k-W], plus exactly these low values.
            small = set(range(0 if o >= 5 else 1 if o == 3 else 2, 2))
            shifts = set()
            top = []
            for h in range(1, W):
                for e in divisors(o):
                    top.append(symbolic_target(-h, (o << h)-e, residue))
            for e in divisors(o):
                if e < o:
                    t, r = split(o // e - 1)
                    top.append(symbolic_target(t, e*r, residue))
            for kind, a in top:
                if kind == 'const':
                    assert 0 <= a <= 1
                    small.add(a)
                else:
                    assert KSTAR+a > 1
                    shifts.add(a)
            kind, a = pattern(o, residue)
            if kind == 'const':
                assert 0 <= a <= 1
                assert all(b in small for b in range(a))
                assert a not in small
            else:
                assert a > -W
                assert {0, 1} <= small
                assert all(b in shifts for b in range(-W+1, a))
                assert a not in shifts
            count += 1
    print(f'[B] symbolic tail classes: {count} PASS (k >= {KSTAR})')


def check_large_odd():
    transient = negative = constant = 0
    for q in range(1, M+1, 2):
        for e in divisors(q):
            for s in range(1, K0):
                k = G(s, q)
                # Equality G(k+t,q)=k forces this unique k and t=s-k.
                if k < s and (1 << k)*e >= C:
                    t = s-k
                    assert e+(q << t) <= M, ('transient', s, q, e, k)
                    transient += 1
            for residue in range(P):
                kind, a = pattern(q, residue)
                if kind == 'shift' and a < 0:
                    assert e+(q << (-a)) <= M, ('tail shift', q, e, residue)
                    negative += 1
                elif kind == 'const':
                    assert (1 << a)*e < C, ('tail constant', q, e, residue)
                    constant += 1
    print(f'[C] large-odd boundary: {transient} transient, '
          f'{negative} negative-shift, {constant} constant cases PASS')


def check_sieve():
    # Uses d | n and n-d directly, without the (k,o) option generator.
    limit = 1 << 18
    seen = [0]*(limit+1)
    exceptional_max = 0
    for n in range(1, limit+1):
        mask = seen[n]
        v = 0
        while mask & (1 << v):
            v += 1
        k, o = split(n)
        assert v == G(k, o), ('sieve', n, v, G(k, o))
        if v != k:
            exceptional_max = max(exceptional_max, o)
        # n is a successor of n+d exactly when d | n and d >= C.
        for d in range(1, isqrt(n)+1):
            if n % d:
                continue
            for e in ({d, n//d}):
                if e >= C and n+e <= limit:
                    seen[n+e] |= 1 << v
    assert exceptional_max == M
    assert G(11, 87) == 13
    print(f'[D] direct n-based sieve: {limit} values PASS; '
          f'max exceptional odd part={exceptional_max}')
    print('[E] sharpness witness: g(178176)=g(2^11 * 87)=13 != 11 PASS')


def check_losing_positions():
    count = 0
    for o in range(1, M+1, 2):
        for k in range(K0+P):
            losing = k == 0 or (o == 1 and k == 2) or (o in (1, 3) and k % 3 == 1)
            assert (G(k, o) == 0) == losing, (k, o)
            count += 1
        for residue in range(P):
            kind, a = pattern(o, residue)
            if kind == 'shift':
                first = K0 + (residue-K0) % P
                assert first+a > 0
    print(f'[F] losing-position formula: {count} initial/phase checks PASS')


def main():
    assert (C, M, K0, P) == (4, 87, 28, 3)
    assert set(DATA['columns']) == {str(o) for o in range(1, M+1, 2)}
    for o in range(1, M+1, 2):
        col = DATA['columns'][str(o)]
        assert len(col['initial']) == K0 and len(col['pattern']) == P
        assert all(isinstance(v, int) and v >= 0 for v in col['initial'])
        for residue, (kind, a) in enumerate(col['pattern']):
            assert kind in ('shift', 'const') and isinstance(a, int)
            first = K0 + (residue-K0) % P
            assert a >= 0 if kind == 'const' else first+a >= 0
    check_base()
    check_tail()
    check_large_odd()
    check_sieve()
    check_losing_positions()
    print('ALL CHECKS PASSED')


if __name__ == '__main__':
    main()
