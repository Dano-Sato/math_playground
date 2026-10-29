"""Exact finite-graph exploration of lower-bound divisor-game outcome periods.

Python 3.10+, integers/Fractions, no randomness.
Run: python research/2026-10-29-divisor-period-growth/explore.py
Range c=2..512; each orbit capped at 20000 states. The seed is generated
from terminal dyadic shells, without assuming any unproved game pattern.
"""
from fractions import Fraction
import json
from pathlib import Path


class Model:
    def __init__(self, c, cap=20000):
        self.c = c
        self.J = (c-1).bit_length()
        self.H = 2*self.J
        self.odds = sorted(range(1, c, 2),
                           key=lambda o: Fraction(o, 1 << (o.bit_length()-1)))
        self.r = len(self.odds)
        ns = [o << (self.H-(o.bit_length()-1)) for o in self.odds]
        self.same = [[] for _ in ns]
        self.prev = [[] for _ in ns]
        self.same_masks = [0]*self.r
        self.prev_masks = [0]*self.r
        for i, n in enumerate(ns):
            for j, t in enumerate(ns):
                d = n-t
                if d > 0 and n % d == 0:
                    assert j < i
                    self.same[i].append((j, d))
                    self.same_masks[i] |= 1 << j
                d = n-t//2
                if d > 0 and n % d == 0:
                    self.prev[i].append((j, d))
                    self.prev_masks[i] |= 1 << j
            assert self.prev_masks[i] & (1 << i)
        # All positions of the shell h=J-1 are below 2*c, hence terminal.
        state = (1 << self.r)-1
        self.initial_states = [state]
        for h in range(self.J, self.H):
            state = self.early_step(state, h)
            self.initial_states.append(state)
        self.seed = state
        self.states = []
        seen = {}
        for _ in range(cap):
            if state in seen:
                self.mu = seen[state]
                self.period = len(self.states)-self.mu
                break
            seen[state] = len(self.states)
            self.states.append(state)
            state = self.step(state)
        else:
            raise RuntimeError(f'c={c}: orbit exceeded cap={cap}')
        self.alpha = Fraction(sum(s.bit_count() for s in self.states[self.mu:]),
                              self.period)

    def early_step(self, previous, height):
        threshold = self.c << (self.H-height)
        current = 0
        for i in range(self.r):
            blocked = any(d >= threshold and (current & (1 << j))
                          for j, d in self.same[i])
            if not blocked:
                blocked = any(d >= threshold and (previous & (1 << j))
                              for j, d in self.prev[i])
            if not blocked:
                current |= 1 << i
        return current

    def step(self, previous):
        current = 0
        for i in range(self.r):
            if not ((self.prev_masks[i] & previous)
                    or (self.same_masks[i] & current)):
                current |= 1 << i
        return current

    def row(self):
        return {'c': self.c, 'r': self.r, 'J': self.J,
                'mu': self.mu, 'period': self.period, 'alpha': str(self.alpha),
                'seed': self.seed}


def main():
    rows = []
    last_record = 0
    for c in range(2, 513):
        m = Model(c)
        rows.append(m.row())
        if m.period > last_record:
            last_record = m.period
            print(f'period record c={c}: mu={m.mu}, period={m.period}, alpha={m.alpha}',
                  flush=True)
        if c in (64, 128, 256, 512):
            print(f'checkpoint c={c}: mu={m.mu}, period={m.period}, alpha={m.alpha}',
                  flush=True)
    dest = Path(__file__).with_name('periods.json')
    dest.write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n',
                    encoding='utf-8')
    print('max preperiod:', max((r['mu'], r['c']) for r in rows))
    print('distinct periods:', sorted({r['period'] for r in rows}))
    print('Wrote periods.json (c=2..512)')


if __name__ == '__main__':
    main()
