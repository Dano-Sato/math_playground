"""Exact self-checks; no RNG, Python 3.10+ standard library.

Run: python research/2026-10-29-divisor-state-entropy/verify.py
r=1..256 structural/decomposition checks; Boolean enumeration r<=16;
generic deletion counts r<=40; rational log certificate at h=12.
"""
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import json

from explore import CANONICAL, arithmetic_graph, odd_edge
from skeleton import (oddpart,skeleton_graph,count_skeleton,
                      complete_sequence,decompose)


def log_bounds(x, terms=16):
    """Positive rational x>=1; atanh expansion with geometric remainder."""
    x = Fraction(x)
    assert x >= 1
    w = (x-1)/(x+1)
    total = Fraction(0)
    power = w
    for k in range(terms):
        total += 2*power/(2*k+1)
        power *= w*w
    error = 2*power/((2*terms+1)*(1-w*w))
    return total,total+error


def integer_log_bounds(n):
    e = n.bit_length()-1
    lo2,hi2 = log_bounds(Fraction(2))
    lo,hi = log_bounds(Fraction(n,1 << e))
    return e*lo2+lo,e*hi2+hi


def main():
    seq = complete_sequence()
    a,b = seq[12]
    loglo,loghi = integer_log_bounds(a)
    lower = loglo/(1 << 12)
    upper = (loghi+Fraction(b*b,a*a))/(1 << 12)
    candidate_lo = Fraction(154168,100000)
    candidate_hi = Fraction(154171,100000)
    assert log_bounds(candidate_lo)[1] < lower
    assert upper < log_bounds(candidate_hi)[0]
    print('[A] rational certificate: 1.54168 < beta < 1.54171 PASS',flush=True)

    boolean_cases = deletion_cases = decomposition_cases = 0
    for r in range(1,257):
        graph = skeleton_graph(r)
        full = arithmetic_graph(list(range(1,2*r,2)))
        assert all(g & ~c == 0 for g,c in zip(graph,full))
        for i in range(2,r):
            n = 2*i+1
            parents = (oddpart(n-1),oddpart(n+1))
            u = max(parents)
            assert len(set(parents)) == 2
            j,k = ((x-1)//2 for x in parents)
            assert graph[j] & (1 << k)
            assert n in (2*u-1,2*u+1)
        value = count_skeleton(r)
        if r <= 16:
            brute = sum(1 for mask in range(1 << r)
                        if all(not (mask & (1 << i) and mask & graph[i])
                               for i in range(r)))
            assert brute == value
            boolean_cases += 1 << r
        if r <= 40:
            generic, _ = CANONICAL.count_independent(graph)
            assert generic == value
            deletion_cases += 1
        if r >= 2:
            p, heights = decompose(r)
            q = len(heights)
            assert p <= (r-1).bit_length()
            assert q <= p+2
            assert sum((1 << h)-1 for h in heights)+p+2 == r
            product = 1
            for h in heights:
                product *= seq[h][0]
            assert product <= value <= 3*(1 << p)*product
            decomposition_cases += 1
        # The lower interval uses c=2r and c=2r+1 separately.
        for c in (2*r,2*r+1):
            ceiling = c-1
            band = [o for o in range(1,c,2) if 5*o > 3*ceiling]
            expected = r-((3*ceiling//5+1)//2)
            assert len(band) == expected
            assert all(not odd_edge(x,y) for i,x in enumerate(band) for y in band[i+1:])
        # Test the claimed uniform upper and skeleton lower with rational bounds.
        assert value*candidate_hi.denominator**r <= 6*r*candidate_hi.numerator**r
        assert 64*r*r*value*candidate_lo.denominator**r >= candidate_lo.numerator**r
    print(f'[B] skeleton subgraph/parents/independent band: r=1..256 PASS',flush=True)
    print(f'[C] Boolean states {boolean_cases}; generic deletion {deletion_cases} cases PASS')
    print(f'[D] decomposition {decomposition_cases} cases; rational uniform bounds PASS')

    levels = 0
    for h in range(12):
        r = 1 << (h+1)
        a,b = seq[h]
        assert count_skeleton(r) == a*a+2*b*b
        levels += 1
    print(f'[E] complete-level formula {levels} cases, r<=4096 PASS')
    # Check previously computed canonical counts against the new skeleton bound.
    old = json.loads((CANONICAL.ROOT/'research/2026-10-29-divisor-canonical-antichain/counts.json')
                     .read_text(encoding='utf-8'))
    for row in old:
        c,r = row['c'],row['r']
        k = r-((3*(c-1)//5+1)//2)
        assert (1 << k) <= row['quotient_states'] <= count_skeleton(r)
    print('[F] five exact canonical counts lie in the new sandwich PASS')
    output = {'certificate':{'depth':12,'lower_base':str(candidate_lo),
                             'upper_base':str(candidate_hi),'terms':16},
              'graphs_checked':256,'boolean_states':boolean_cases,
              'deletion_cases':deletion_cases,'decomposition_cases':decomposition_cases,
              'complete_level_cases':levels,'canonical_counts_compared':len(old)}
    Path(__file__).with_name('verification.json').write_text(
        json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
