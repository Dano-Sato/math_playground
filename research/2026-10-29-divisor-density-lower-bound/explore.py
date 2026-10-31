"""Coverage lower bounds for the divisor-game logarithmic coefficient.

Run: python research/2026-10-29-divisor-density-lower-bound/explore.py
Python 3.10+, standard library, exact integers/Fractions, no randomness.
Saved range c=2..512, each pre-existing model orbit capped at 20000.
This script changes no earlier research files.
"""
from fractions import Fraction
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    'period_model',ROOT/'research/2026-10-29-divisor-period-growth/explore.py')
PREVIOUS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREVIOUS)


def divisors(n):
    small,large = [],[]
    d = 1
    while d*d <= n:
        if n % d == 0:
            small.append(d)
            if d*d != n:
                large.append(n//d)
        d += 1
    return small+large[::-1]


def incoming_sources(o,R):
    """Odd parts of all predecessors of 2**k*o in (n,2n], stable k.

    One source per coordinate, including o itself (removing half).
    Sources <o come from odd q=s; sources >o from q=2**t*s.
    """
    result = []
    for s in divisors(o):
        u = s+1
        u //= u & -u
        result.append((o//s)*u)
        a = 2*o+o//s
        t = 1
        while a <= R:
            result.append(a)
            t += 1
            a = (1 << t)*o+o//s
    assert len(result) == len(set(result))
    assert all(a % 2 and 1 <= a <= R for a in result)
    return sorted(result)


def weights(m):
    R = 2*m.r-1
    result = []
    for j,o in enumerate(m.odds):
        incoming = incoming_sources(o,R)
        actual = [m.odds[i] for i in range(m.r)
                  if (m.same_masks[i] | m.prev_masks[i]) & (1 << j)]
        assert incoming == sorted(actual)
        assert all(not (a & b) for a,b in zip(m.same_masks,m.prev_masks))
        result.append(1+len(incoming))
    return result


def sieve_weights(r):
    """Same column weights without constructing a graph or a game orbit."""
    R = 2*r-1
    out = [1]*r
    for g in range(1,R+1,2):
        for o in range(g,R+1,2*g):
            q = (R-g)//o
            out[(o-1)//2] += 1+max(0,q.bit_length()-1)
    return out


def capacity_bound(w):
    """One-constraint fractional covering relaxation, f_i in [0,1/2].

    Fill the largest column capacities first. The fractional answer is an
    exact lower bound on total frequency, not an attainable game outcome.
    """
    needed = Fraction(len(w))
    mass = Fraction(0)
    for a in sorted(w,reverse=True):
        take = min(Fraction(1,2),needed/a)
        needed -= a*take
        mass += take
        if not needed:
            return mass
    raise AssertionError('Coverage capacity insufficient')


def main():
    rows = []
    maximum_checks = 0
    for c in range(2,513):
        m = PREVIOUS.Model(c)
        w = weights(m)
        sieve = sieve_weights(m.r)
        assert sorted(w) == sorted(sieve)
        cycle = m.states[m.mu:]
        counts = [sum(bool(s & (1 << j)) for s in cycle)
                  for j in range(m.r)]
        assert all(2*f <= m.period for f in counts)
        coverage = sum(a*b for a,b in zip(w,counts))
        assert m.r*m.period <= coverage
        simple = Fraction(m.r,max(w))
        moment = Fraction(2*m.r*m.r,sum(x*x for x in w))
        capacity = capacity_bound(w)
        assert simple <= capacity <= m.alpha <= Fraction(m.r,2)
        assert moment <= m.alpha
        rows.append({'c':c,'r':m.r,'period':m.period,'alpha':str(m.alpha),
                     'max_weight':max(w),'weight_square_sum':sum(x*x for x in w),
                     'maximum_bound':str(simple),'moment_bound':str(moment),
                     'capacity_bound':str(capacity),
                     'coverage_per_period':coverage})
        maximum_checks += len(cycle)
        if c in (2,4,16,32,64,128,256,512):
            print(f'c={c}: alpha={m.alpha}, max-bound={simple}, '
                  f'moment-bound={moment}, capacity={capacity}, '
                  f'max-w={max(w)}',flush=True)
    output = {'range':[2,512],'cases':rows,
              'periodic_states_checked':maximum_checks}
    Path(__file__).with_name('bounds.json').write_text(
        json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PASS: {len(rows)} models; {maximum_checks} periodic states',flush=True)
    large = []
    for r in (512,1024,4096,16384,32768):
        w = sieve_weights(r)
        bound = capacity_bound(w)
        large.append({'r':r,'max_weight':max(w),
                      'weight_square_sum':sum(x*x for x in w),
                      'capacity_bound':str(bound)})
        print(f'sieve r={r}: max-w={max(w)}, capacity={bound}',flush=True)
    Path(__file__).with_name('large-bounds.json').write_text(
        json.dumps(large,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
