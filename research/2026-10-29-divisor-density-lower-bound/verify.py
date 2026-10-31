"""Exact checks for the arithmetic coverage theorem.

Run: python research/2026-10-29-divisor-density-lower-bound/verify.py
Python 3.10+, standard library, no RNG.
Direct reverse moves r<=64; all Boolean states r<=12;
all 96 previously certified cycles for c=4,28,32,64;
divisor inequalities n<=4096; graph-free sieves r<=32768.
"""
from explore import (ROOT,PREVIOUS,divisors,incoming_sources,
                     weights,sieve_weights,capacity_bound)
from fractions import Fraction
from math import comb
from pathlib import Path
import json


def cycles_of(m):
    successor = [m.step(x) for x in range(1 << m.r)]
    finished = set()
    cycles = []
    for start in range(len(successor)):
        if start in finished:
            continue
        path,seen = [],{}
        x = start
        while x not in seen and x not in finished:
            seen[x] = len(path)
            path.append(x)
            x = successor[x]
        if x in seen:
            cycles.append(path[seen[x]:])
        finished.update(path)
    return cycles


def check_cycle(m,cycle,w):
    length = len(cycle)
    assert all(m.step(cycle[i]) == cycle[(i+1)%length] for i in range(length))
    counts = [sum(bool(s & (1 << j)) for s in cycle) for j in range(m.r)]
    assert all(2*f <= length for f in counts)
    assert m.r*length <= sum(a*b for a,b in zip(w,counts))
    alpha = Fraction(sum(counts),length)
    moment = Fraction(2*m.r*m.r,sum(a*a for a in w))
    assert moment <= capacity_bound(w) <= alpha <= Fraction(m.r,2)


def response(m,z):
    y = 0
    for i,mask in enumerate(m.same_masks):
        if not ((z & (1 << i)) or (mask & y)):
            y |= 1 << i
    return y


def main():
    reverse_checks = 0
    for r in range(1,65):
        R = 2*r-1
        for o in range(1,R+1,2):
            # At this exponent all possible reverse-move types are present.
            n = o << (R.bit_length()+2)
            direct = []
            for a in range(1,R+1,2):
                exponent = (n//a).bit_length()
                source = a << exponent
                assert n < source <= 2*n
                if source % (source-n) == 0:
                    direct.append(a)
            assert direct == incoming_sources(o,R)
            reverse_checks += 1
    print(f'[A] {reverse_checks} direct reverse-move columns PASS',flush=True)

    state_count = cycle_count = 0
    for r in range(1,13):
        m = PREVIOUS.Model(2*r)
        w = weights(m)
        for cycle in cycles_of(m):
            check_cycle(m,cycle,w)
            cycle_count += 1
        state_count += 1 << r
    print(f'[B] {state_count} Boolean states; {cycle_count} complete cycles PASS',
          flush=True)

    old = json.loads((ROOT/'research/2026-10-29-divisor-order-quotient/quotients.json')
                     .read_text(encoding='utf-8'))
    saved_cycles = saved_states = 0
    for row in old:
        m = PREVIOUS.Model(row['c'])
        assert m.odds == row['odd_parts_in_bit_order']
        assert m.same_masks == row['same_masks']
        assert m.prev_masks == row['previous_masks']
        w = weights(m)
        for zcycle in row['cycles']:
            cycle = [response(m,z) for z in zcycle]
            assert len(set(cycle)) == len(cycle)
            check_cycle(m,cycle,w)
            saved_cycles += 1
            saved_states += len(cycle)
    print(f'[C] {saved_cycles} saved cycles; {saved_states} states PASS',flush=True)

    # Independent prime factor count checks tau(n)^2 <= d_4(n).
    for n in range(1,4097):
        value = n
        d4 = 1
        p = 2
        while p*p <= value:
            e = 0
            while value % p == 0:
                value //= p
                e += 1
            d4 *= comb(e+3,3)
            p += 1
        if value > 1:
            d4 *= 4
        assert len(divisors(n))**2 <= d4
    harmonic = Fraction(0)
    tau_square_sum = 0
    for n in range(1,129):
        harmonic += Fraction(1,n)
        tau_square_sum += len(divisors(n))**2
        assert tau_square_sum <= n*harmonic**3
    for M in range(33):
        finite = sum((Fraction((j+1)**2,1 << j) for j in range(M+1)),Fraction(0))
        assert finite == 12-Fraction(M*M+6*M+11,1 << M)
    print('[D] divisor moment n<=4096; harmonic 128; geometric 33 PASS',flush=True)

    large = json.loads(Path(__file__).with_name('large-bounds.json')
                       .read_text(encoding='utf-8'))
    for row in large:
        r = row['r']
        w = sieve_weights(r)
        assert max(w) == row['max_weight']
        assert sum(a*a for a in w) == row['weight_square_sum']
        assert capacity_bound(w) == Fraction(row['capacity_bound'])
        assert Fraction(2*r*r,sum(a*a for a in w)) <= capacity_bound(w)
    print(f'[E] {len(large)} graph-free sieve bounds r<=32768 PASS',flush=True)
    data = {'direct_reverse_columns':reverse_checks,
            'complete_boolean_states':state_count,'complete_cycles':cycle_count,
            'saved_cycles':saved_cycles,'saved_cycle_states':saved_states,
            'divisor_cases':4096,'harmonic_cases':128,'geometric_cases':33,
            'large_sieve_cases':len(large)}
    Path(__file__).with_name('verification.json').write_text(
        json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
