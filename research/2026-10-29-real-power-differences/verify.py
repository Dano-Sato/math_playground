"""Exact polynomial checks and non-certified high-precision half-integer checks."""

from decimal import Decimal, localcontext
from fractions import Fraction
from math import comb, prod
from pathlib import Path
import platform


STEP_SETS = [
    (), (Fraction(1),), (Fraction(1, 2),),
    (Fraction(1), Fraction(2)), (Fraction(1, 3), Fraction(2, 3)),
    (Fraction(1),) * 3, (Fraction(1, 2), Fraction(3, 2), Fraction(2)),
    tuple(map(Fraction, (1, 2, 3, 4))),
    tuple(Fraction(1, j) for j in (5, 4, 3, 2, 1)),
]
BASES = [Fraction(1, 3), Fraction(1), Fraction(5, 2)]


def vertices(a, steps):
    values = [(1, a)]
    for h in steps:
        values += [(-sign, x + h) for sign, x in values]
    return values


def exact_sum(a, steps, s):
    return sum((sign * x**(-s) for sign, x in vertices(a, steps)), Fraction(0))


def cube_moment(a, steps, degree):
    moments = [a**p for p in range(degree + 1)]
    for h in steps:
        moments = [
            sum((comb(p, q) * moments[p - q] * h**q / (q + 1) for q in range(p + 1)), Fraction(0))
            for p in range(degree + 1)
        ]
    return moments[degree]


def sign_of(value):
    return (value > 0) - (value < 0)


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def half_sum(a, steps, twice_s, precision):
    with localcontext() as context:
        context.prec = precision
        terms = []
        for sign, x in vertices(a, steps):
            base = Decimal(x.numerator) / Decimal(x.denominator)
            terms.append(sign * base.sqrt() ** (-twice_s))
        return sum(terms, Decimal(0))


def main():
    polynomial = positive = fractional = 0
    half_exponents = (-11, -9, -7, -5, -3, -1, 1, 3, 5)
    for steps in STEP_SETS:
        n = len(steps)
        for a in BASES:
            for m in range(10):
                actual = exact_sum(a, steps, -m)
                rising = prod((-m + j for j in range(n)), start=Fraction(1))
                expected = Fraction(0) if m < n else rising * prod(steps, start=Fraction(1)) * cube_moment(a, steps, m - n)
                require(actual == expected, ("cube identity", a, steps, m))
                polynomial += 1
            for s in range(1, 6):
                require(exact_sum(a, steps, s) > 0, ("positive exponent", a, steps, s))
                positive += 1
            for twice_s in half_exponents:
                rising = prod((Fraction(twice_s, 2) + j for j in range(n)), start=Fraction(1))
                predicted = sign_of(rising)
                for precision in (80, 120):
                    observed = half_sum(a, steps, twice_s, precision)
                    require(sign_of(observed) == predicted, ("half-integer sign", a, steps, twice_s, precision))
                fractional += 1

    require(Fraction(1) - 2 * Fraction(2) + Fraction(4) == 1, "unequal-node counterexample")
    status = [
        f"PASS: {polynomial} exact polynomial cube-integral identities (s=0,-1,...,-9).",
        f"PASS: {positive} exact positive-integer exponent sign checks (s=1..5).",
        f"PASS: {fractional} half-integer configurations checked at both 80 and 120 digits.",
        "PASS: 1 unequal-node counterexample.",
    ]
    lines = [
        "# 계산 기록: 실수 지수와 비균등 차분", "", "[연구 노트](note.md)", "",
        "- 연구일: 2026-10-29", f"- 실행 환경: Python {platform.python_version()} ({platform.system()})",
        "- 난수 없음. 정수 지수는 Fraction, 반정수 지수는 Decimal.sqrt 사용.", "",
        "```powershell", "python research/2026-10-29-real-power-differences/verify.py", "```", "",
        "```text", *status, "```", "",
        "## 입력 범위", "", "a = 1/3, 1, 5/2. 간격 목록은 다음 9개다.", "",
        "```text", *(str(tuple(map(str, steps))) for steps in STEP_SETS), "```", "",
        "반정수 s = -11/2, -9/2, -7/2, -5/2, -3/2, -1/2, 1/2, 3/2, 5/2.", "",
        "정수 지수 405개 설정은 정확한 검산이다. 반정수 243개 설정은 각기 두 정밀도에서 확인한 수치 관찰이다.",
        "80자리와 120자리 계산은 구간 산술 인증을 대신하지 않는다. 일반적인 부호와 영점은 노트에서 증명했다.", "",
    ]
    Path(__file__).with_name("results.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(status))
    print("WROTE: results.md (exact and approximate evidence separated).")


if __name__ == "__main__":
    main()
