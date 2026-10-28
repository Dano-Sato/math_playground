"""Independent exact half-integer and moment checks; approximate root slopes."""

from decimal import Decimal, localcontext
from fractions import Fraction as Q
from math import factorial, isqrt, prod
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[2]


def vertices(a, steps):
    for mask in range(1 << len(steps)):
        active = [i for i in range(len(steps)) if mask & (1 << i)]
        yield (-1) ** len(active), a + sum((steps[i] for i in active), Q(0))


def exact_sqrt(x):
    numerator, denominator = isqrt(x.numerator), isqrt(x.denominator)
    if numerator**2 != x.numerator or denominator**2 != x.denominator:
        raise AssertionError(("not a rational square", x))
    return Q(numerator, denominator)


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, length - 1):
                yield (first,) + rest


def expanded_moment(a, steps, degree):
    answer = Q(0)
    for powers in compositions(degree, len(steps) + 1):
        term = Q(factorial(degree), prod(factorial(p) for p in powers)) * a**powers[0]
        for h, p in zip(steps, powers[1:]):
            term *= h**p / (p + 1)
        answer += term
    return answer


def main():
    module = runpy.run_path(str(ROOT / "research/2026-10-29-real-power-differences/verify.py"))
    exact_halves = 0
    for scale in (Q(1), Q(4, 9), Q(25, 4)):
        for basic_steps in ((), (Q(3),), (Q(15), Q(48))):
            a = scale
            steps = tuple(scale * h for h in basic_steps)
            for twice_s in range(-15, 16, 2):
                exact = sum((sign * exact_sqrt(x)**(-twice_s) for sign, x in vertices(a, steps)), Q(0))
                rising = prod((Q(twice_s, 2) + j for j in range(len(steps))), start=Q(1))
                if (exact > 0) - (exact < 0) != (rising > 0) - (rising < 0):
                    raise AssertionError(("exact half sign", a, steps, twice_s))
                exact_halves += 1
    print(f"PASS: {exact_halves} exact rational half-integer sign cases on square vertices.")

    moments = 0
    for a, steps in (
        (Q(2, 7), ()),
        (Q(2, 7), (Q(1, 11),)),
        (Q(2, 7), (Q(1, 11), Q(2, 5), Q(3, 2))),
    ):
        for degree in range(8):
            if expanded_moment(a, steps, degree) != module["cube_moment"](a, steps, degree):
                raise AssertionError(("independent moment", a, steps, degree))
            moments += 1
    print(f"PASS: {moments} independently expanded rational cube moments.")

    slopes = 0
    with localcontext() as context:
        context.prec = 100
        for a in (Q(2, 7), Q(5, 3)):
            for steps in ((Q(1, 11),), (Q(1), Q(3)), (Q(1, 11), Q(2, 5), Q(3, 2))):
                for k in range(len(steps)):
                    derivative = Decimal(0)
                    for sign, x in vertices(a, steps):
                        base = Decimal(x.numerator) / Decimal(x.denominator)
                        derivative -= sign * base**k * base.ln()
                    if (derivative > 0) - (derivative < 0) != (-1) ** k:
                        raise AssertionError(("approximate simple-root slope", a, steps, k))
                    slopes += 1
    print(f"OBSERVED: {slopes} root-derivative signs agree at 100 digits (not interval-certified).")
    print("No source or shared wiki files written.")


if __name__ == "__main__":
    main()
