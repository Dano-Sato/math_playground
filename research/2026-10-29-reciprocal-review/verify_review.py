"""Read-only independent checks for the reciprocal-binomial research note."""

from fractions import Fraction as Q
from itertools import combinations_with_replacement
from math import comb, factorial, prod
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[2]


def direct(n, r, a):
    return sum((Q((-1) ** j * comb(n, j), 1) / (a + j) ** r for j in range(n + 1)), Q(0))


def main():
    original = runpy.run_path(str(ROOT / "research/2026-10-29-reciprocal-binomial/verify.py"))
    cases = 0
    for n in (0, 1, 2, 5, 13, 20):
        for a in (Q(1, 101), Q(2, 3), Q(7, 5), Q(17)):
            b, h = original["positive_coefficients"](n, 10, a)
            powers = original["power_sum_coefficients"](n, 10, a)
            total = sum((1 / (a + j) for j in range(n + 1)), Q(0))
            for k in range(11):
                value = direct(n, k + 1, a)
                lower = b * total**k / factorial(k)
                upper = b / factorial(k) * prod((total + Q(i) / a for i in range(k)), start=Q(1))
                if not (value == b * h[k] and h[k] == powers[k] and lower <= value <= upper):
                    raise AssertionError(("identity or bounds", n, k, a))
                if not (value > direct(n + 1, k + 1, a) > 0 and value > direct(n, k + 1, a + Q(1, 7)) > 0):
                    raise AssertionError(("monotonicity", n, k, a))
                cases += 1
    print(f"PASS: {cases} additional rational cases; identities, bounds, n/a monotonicity.")

    enumerations = 0
    for n in range(5):
        for a in (Q(1, 101), Q(2, 3), Q(7, 5), Q(17)):
            b, h = original["positive_coefficients"](n, 5, a)
            for k in range(6):
                enumerated = sum(
                    (prod((1 / (a + j) for j in indices), start=Q(1))
                     for indices in combinations_with_replacement(range(n + 1), k)),
                    Q(0),
                )
                if enumerated != h[k] or direct(n, k + 1, a) != b * enumerated:
                    raise AssertionError(("independent enumeration", n, k, a))
                enumerations += 1
    print(f"PASS: {enumerations} independent weak-index coefficient enumerations.")

    for k in range(11):
        b, h = original["positive_coefficients"](0, k, Q(2, 3))
        if h[k] != Q(3, 2)**k or b * h[k] != Q(3, 2)**(k + 1):
            raise AssertionError(("n=0 edge", k))
    print("PASS: 11 n=0 coefficient edge cases.")
    print("No source or shared wiki files written.")


if __name__ == "__main__":
    main()
