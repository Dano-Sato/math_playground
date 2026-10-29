"""Finite-state outcome theorem for every integer lower bound c >= 2.

Run: python research/2026-10-29-divisor-outcome-automaton/verify.py
Python 3.10+, standard library, exact integers/Fractions, no randomness.
Default bounded calculation: 2 <= c <= 64, direct n <= 2**16,
at most 100000 states per c, and large exponent checks at k=1000.
The mathematical theorem is in note.md; a bounded computation is not its proof.
"""
from fractions import Fraction
import json
from pathlib import Path


def split(n):
    k = (n & -n).bit_length() - 1
    return k, n >> k


def divisor_table(limit):
    """All proper divisors, generated independently of dyadic coordinates."""
    table = [[] for _ in range(limit+1)]
    for d in range(1, limit//2+1):
        for n in range(2*d, limit+1, d):
            table[n].append(d)
    return table


def direct_outcomes(c, ds):
    win = bytearray(len(ds))
    for n in range(1, len(ds)):
        win[n] = any(not win[n-d] for d in ds[n] if d >= c)
    return win


class Model:
    def __init__(self, c, direct):
        assert c >= 2
        self.c = c
        self.J = (c-1).bit_length()  # ceil(log2(c))
        self.L = (c-1).bit_length()-1
        self.H = self.J+self.L+1
        assert self.H == 2*self.J
        self.odds = sorted(range(1, c, 2),
                           key=lambda o: Fraction(o, 1 << (o.bit_length()-1)))
        self.index = {o: i for i, o in enumerate(self.odds)}
        self.r = len(self.odds)
        assert self.r == c//2
        self.same = [0]*self.r
        self.previous = [0]*self.r
        self.direct = direct
        # At height H both candidate shell heights have integral even entries,
        # and every positive difference is >= 2**J >= c.
        for i, o in enumerate(self.odds):
            source = self.position(self.H, o)
            for delay in (0, 1):
                for j, q in enumerate(self.odds):
                    target = self.position(self.H-delay, q)
                    d = source-target
                    if d > 0:
                        assert d >= c
                    if d > 0 and source % d == 0:
                        assert target >= source//2
                        if delay == 0:
                            assert j < i
                            self.same[i] |= 1 << j
                        else:
                            self.previous[i] |= 1 << j
            assert self.previous[i] & (1 << i)  # removing half the pile
        seed = 0
        for i, o in enumerate(self.odds):
            n = self.position(self.H-1, o)
            assert n < len(direct)
            if not direct[n]:
                seed |= 1 << i
        self.seed = seed
        self.small_even_count = sum(not direct[n]
                                    for n in range(2, 1 << (self.H-1), 2))
        self.states = []
        seen = {}
        state = seed
        for _ in range(100000):
            if state in seen:
                self.mu = seen[state]
                self.period = len(self.states)-self.mu
                break
            seen[state] = len(self.states)
            self.states.append(state)
            state = self.step(state)
        else:
            raise RuntimeError(f'c={c}: computation cap reached; no period claimed')
        assert len(self.states) <= 1 << self.r
        assert self.mu+self.period == len(self.states)
        self.alpha = Fraction(sum(s.bit_count() for s in self.states[self.mu:]),
                              self.period)

    @staticmethod
    def position(height, o):
        exponent = height-(o.bit_length()-1)
        assert exponent >= 0
        return o << exponent

    def step(self, previous):
        current = 0
        for i in range(self.r):
            if not ((self.previous[i] & previous) or (self.same[i] & current)):
                current |= 1 << i
        return current

    def state_at(self, height):
        t = height-(self.H-1)
        assert t >= 0
        if t >= len(self.states):
            t = self.mu+(t-self.mu) % self.period
        return self.states[t]

    def losing(self, n):
        k, o = split(n)
        if k == 0:
            return True
        if o >= self.c:
            return False
        height = n.bit_length()-1
        if height < self.H-1:
            return not self.direct[n]
        return bool(self.state_at(height) & (1 << self.index[o]))

    def weight_sum(self, length):
        """Sum the losing counts of the first length stable shells."""
        weights = [s.bit_count() for s in self.states]
        if length <= self.mu:
            return sum(weights[:length])
        cycles, tail = divmod(length-self.mu, self.period)
        return (sum(weights[:self.mu])
                + cycles*sum(weights[self.mu:])
                + sum(weights[self.mu:self.mu+tail]))

    def count_losing(self, limit):
        if limit < (1 << (self.H-1)):
            return sum(not self.direct[n] for n in range(1, limit+1))
        height = limit.bit_length()-1
        extra = self.small_even_count+self.weight_sum(height-(self.H-1))
        mask = self.state_at(height)
        extra += sum(bool(mask & (1 << i)) and self.position(height, o) <= limit
                     for i, o in enumerate(self.odds))
        return (limit+1)//2+extra

    def check_edges(self, height):
        """Regenerate all legal successors from actual integer divisors."""
        edges = 0
        for i, o in enumerate(self.odds):
            n = self.position(height, o)
            actual_same = actual_previous = 0
            for j in range(height-(o.bit_length()-1)+1):
                for e in range(1, o+1, 2):
                    if o % e:
                        continue
                    d = e << j
                    if not (self.c <= d < n):
                        continue
                    target = n-d
                    _, q = split(target)
                    if q >= self.c:
                        continue
                    th = target.bit_length()-1
                    assert height-th in (0, 1)
                    bit = 1 << self.index[q]
                    if th == height:
                        actual_same |= bit
                    else:
                        actual_previous |= bit
                    edges += 1
            assert actual_same == self.same[i], (self.c, height, o, 'same')
            assert actual_previous == self.previous[i], (self.c, height, o, 'prev')
        return edges

    def report(self):
        return {'c': self.c, 'r': self.r, 'H': self.H,
                'mu': self.mu, 'period': self.period, 'alpha': str(self.alpha),
                'odd_parts_in_bit_order': self.odds,
                'same_masks': self.same, 'previous_masks': self.previous,
                'states': self.states}


def main():
    limit = 1 << 16
    ds = divisor_table(limit)
    reports = []
    count = edge_count = high_count = counting_checks = 0
    for c in range(2, 65):
        win = direct_outcomes(c, ds)
        m = Model(c, win)
        prefix = [0]*len(win)
        for n in range(1, limit+1):
            assert m.losing(n) == (not win[n]), (c, n)
            prefix[n] = prefix[n-1]+(not win[n])
            count += 1
        for n in sorted({0, 1, 2, 3, c-1, c, c+1, (1 << m.H)-1,
                         (1 << m.H), 32767, 32768, 65535, 65536}):
            assert m.count_losing(n) == prefix[n], ('count', c, n)
            counting_checks += 1
        for h in (m.H, m.H+1, m.H+7, 1000):
            edge_count += m.check_edges(h)
        for o in m.odds:
            n = o << 1000
            assert m.losing(n) == m.losing(n << m.period)
            high_count += 1
        if c == 4:
            for k in range(1001):
                for o in (1, 3, 5, 87, 89):
                    expected = k == 0 or (o == 1 and k == 2) or (
                        o in (1, 3) and k % 3 == 1)
                    assert m.losing(o << k) == expected, (k, o)
            assert m.count_losing(1 << 1000)-(1 << 999) == 668
        reports.append(m.report())
        if c <= 16 or c in (32, 64):
            print(f'c={c}: r={m.r}, H={m.H}, mu={m.mu}, '
                  f'period={m.period}, alpha={m.alpha}')
    dest = Path(__file__).with_name('report.json')
    dest.write_text(json.dumps(reports, ensure_ascii=False, indent=2)+'\n',
                    encoding='utf-8')
    print(f'[A] direct outcome comparisons: {count} PASS')
    print(f'[B] regenerated small-odd successor edges: {edge_count} PASS')
    print(f'[C] exponent-1000 periodicity checks: {high_count} PASS')
    print('[D] c=4 hand formula: 5005 checks PASS')
    print(f'[D2] exact counting comparisons: {counting_checks} PASS; '
          'c=4, N=2^1000 has 668 even losing positions')
    largest = max(reports, key=lambda row: row['period'])
    print(f"[E] largest observed period: {largest['period']} at c={largest['c']}")
    print('ALL CHECKS PASSED; wrote report.json')


if __name__ == '__main__':
    main()
