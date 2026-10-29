"""Exact closure quotient of the dyadic divisor-game outcome map.

Python 3.10+, standard library, integer arithmetic, no randomness.
Run: python research/2026-10-29-divisor-order-quotient/explore.py
Complete independent-set enumeration for c=4,28,32,64 (r<=32).
Imports the already-proved arithmetic map without changing older files.
"""
import importlib.util
from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    'period_growth', ROOT/'research/2026-10-29-divisor-period-growth/explore.py')
PREVIOUS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREVIOUS)
Model = PREVIOUS.Model


def closure(m, state):
    return sum(1 << i for i, mask in enumerate(m.prev_masks) if mask & state)


def response(m, blocked):
    current = 0
    for i, mask in enumerate(m.same_masks):
        if not ((blocked & (1 << i)) or (mask & current)):
            current |= 1 << i
    return current


def independent_sets(m):
    def visit(i, state):
        if i == m.r:
            yield state
            return
        yield from visit(i+1, state)
        if not (m.same_masks[i] & state):
            yield from visit(i+1, state | (1 << i))
    yield from visit(0, 0)


def cycles_of(successors):
    """All cycles, computed once per vertex of a finite functional graph."""
    finished = set()
    cycles = []
    for start in successors:
        if start in finished:
            continue
        path = []
        positions = {}
        state = start
        while state not in finished and state not in positions:
            positions[state] = len(path)
            path.append(state)
            state = successors[state]
        if state in positions:
            cycle = path[positions[state]:]
            # Rotate for deterministic output.
            j = cycle.index(min(cycle))
            cycles.append(cycle[j:]+cycle[:j])
        finished.update(path)
    return sorted(cycles, key=lambda seq: (len(seq), seq))


def image_sizes(successors):
    current = set(successors)
    sizes = [len(current)]
    while True:
        following = {successors[z] for z in current}
        if following == current:
            return sizes
        sizes.append(len(following))
        current = following


def main():
    rows = []
    for c in (4, 28, 32, 64):
        m = Model(c)
        # B is a reflexive upper-triangular relation; rows are successor sets.
        for i, row in enumerate(m.prev_masks):
            assert row & (1 << i)
            assert row >> i << i == row
            joined = 0
            for j in range(m.r):
                if row & (1 << j):
                    joined |= m.prev_masks[j]
            assert joined == row
        quotient = set()
        count = 0
        for state in independent_sets(m):
            z = closure(m, state)
            assert closure(m, z) == z
            assert response(m, z) == m.step(state)
            quotient.add(z)
            count += 1
        transitions = {z: closure(m, response(m, z)) for z in quotient}
        assert set(transitions.values()) <= quotient
        cycles = cycles_of(transitions)
        sizes = image_sizes(transitions)
        periods = {}
        averages = {}
        for cycle in cycles:
            periods[len(cycle)] = periods.get(len(cycle), 0)+1
            alpha = Fraction(sum(response(m,z).bit_count() for z in cycle), len(cycle))
            key = f'{len(cycle)}:{alpha}'
            averages[key] = averages.get(key, 0)+1
        row = {
            'c': c, 'r': m.r, 'independent_sets': count,
            'quotient_states': len(quotient),
            'image_states': len(set(transitions.values())),
            'all_cycle_period_counts': periods,
            'cycle_weight_counts': averages,
            'image_sizes': sizes,
            'max_quotient_transient': len(sizes)-1,
            'odd_parts_in_bit_order': m.odds,
            'same_masks': m.same_masks, 'previous_masks': m.prev_masks,
            'cycles': cycles,
        }
        rows.append(row)
        print(f'c={c}: independent={count}, quotient={len(quotient)}, '
              f'image={row["image_states"]}, cycles={periods}', flush=True)
        print(f'  image sizes={sizes}; max quotient transient={len(sizes)-1}', flush=True)
    dest = Path(__file__).with_name('quotients.json')
    dest.write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Wrote quotients.json')


if __name__ == '__main__':
    main()
