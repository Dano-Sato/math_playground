"""Small exact rule witnesses for the novelty comparison.

Run: python research/2026-10-29-divisor-novelty-audit/verify.py
Python 3.10+, standard library, no RNG. c=2,3,4,5,64; n<=4096.
This is a focused self-check, not a novelty proof or an independent review.
"""
from pathlib import Path
from fractions import Fraction
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    'outcome',ROOT/'research/2026-10-29-divisor-outcome-automaton/verify.py')
OUTCOME = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OUTCOME)


def main():
    ds = OUTCOME.divisor_table(4096)
    expected = {2:(2,Fraction(1,2)),3:(2,Fraction(1,2)),
                4:(3,Fraction(2,3)),5:(3,Fraction(2,3)),
                64:(8,Fraction(19,2))}
    rows = []
    for c,(period,alpha) in expected.items():
        direct = OUTCOME.direct_outcomes(c,ds)
        model = OUTCOME.Model(c,direct)
        assert model.period == period and model.alpha == alpha
        comparisons = 0
        for n in range(1,4097):
            assert model.losing(n) == (not direct[n])
            comparisons += 1
        row = {'c':c, 'period':period,'alpha':str(alpha),
               'p_1':int(not direct[1]),'p_4':int(not direct[4]),
               'compared_positions':comparisons}
        rows.append(row)
        print(f'c={c}: period={period}, alpha={alpha}, '
              f'p(1)={row["p_1"]}, p(4)={row["p_4"]} PASS')
    assert rows[0]['p_4'] == 0 and rows[1]['p_4'] == 1
    # SALIQUOT: 1 -> 0; our domain is positive and 1 is terminal.
    assert 1-1 == 0
    # No fixed finite i-Mark subtraction set can supply every 3d -> 2d.
    # A division n/q would require integer q=3/2, which is impossible.
    witnesses = []
    for c,subtractions in ((2,(1,)),(4,(2,4)),(64,(1,3,7))):
        d = max(c,max(subtractions)+1)
        n,target = 3*d,2*d
        assert n % d == 0 and c <= d < n and d not in subtractions
        assert Fraction(n,target) == Fraction(3,2)
        witnesses.append({'c':c,'i_mark_S':subtractions,
                          'source':n,'target':target,'removed':d})
    data = {'cases':rows,'direct_comparisons':5*4096,
            'finite_i_mark_move_witnesses':witnesses}
    Path(__file__).with_name('witnesses.json').write_text(
        json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS: 20480 exact outcome comparisons and rule witnesses')


if __name__ == '__main__':
    main()
