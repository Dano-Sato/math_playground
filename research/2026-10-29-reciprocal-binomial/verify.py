"""Exact checks for note.md; also record a bounded float cancellation experiment."""

from fractions import Fraction
from math import comb, factorial, fsum
from pathlib import Path
import platform


def direct(n, r, a):
    return sum(
        ((-1) ** j * comb(n, j) / (a + j) ** r for j in range(n + 1)),
        Fraction(0),
    )


def positive_coefficients(n, max_degree, a):
    h = [Fraction(1)] + [Fraction(0)] * max_degree
    b = 1 / a
    for j in range(n + 1):
        x = 1 / (a + j)
        if j:
            b *= Fraction(j) / (a + j)
        for k in range(1, max_degree + 1):
            h[k] += x * h[k - 1]
    return b, h


def power_sum_coefficients(n, max_degree, a):
    powers = [Fraction(0)] + [
        sum((1 / (a + j) ** ell for j in range(n + 1)), Fraction(0))
        for ell in range(1, max_degree + 1)
    ]
    h = [Fraction(1)]
    for k in range(1, max_degree + 1):
        h.append(sum((powers[ell] * h[k - ell] for ell in range(1, k + 1)), Fraction(0)) / k)
    return h


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def main():
    parameters = [Fraction(1, 5), Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(5)]
    identities = coefficients = bounds = recurrences = 0
    for n in range(13):
        for a in parameters:
            b, h = positive_coefficients(n, 7, a)
            independent_h = power_sum_coefficients(n, 7, a)
            total = sum((1 / (a + j) for j in range(n + 1)), Fraction(0))
            for r in range(1, 9):
                k = r - 1
                actual = direct(n, r, a)
                require(actual == b * h[k] and actual > 0, ("identity", n, r, a))
                identities += 1
                require(h[k] == independent_h[k], ("coefficients", n, k, a))
                coefficients += 1
                lower = b * total**k / factorial(k)
                upper = b / factorial(k)
                for i in range(k):
                    upper *= total + Fraction(i) / a
                require(lower <= actual <= upper, ("bounds", n, r, a))
                bounds += 1
                if n:
                    require(actual == direct(n - 1, r, a) - direct(n - 1, r, a + 1), ("Pascal", n, r, a))
                    recurrences += 1

    require(direct(1, 2, Fraction(1)) > direct(1, 1, Fraction(1)), "r increase example")
    require(direct(1, 2, Fraction(2)) < direct(1, 1, Fraction(2)), "r decrease example")
    require(direct(1, 1, Fraction(-1, 2)) == -4, "negative a counterexample")

    rows = []
    for n in (10, 30, 50, 80):
        exact = direct(n, 1, Fraction(1))
        require(exact == Fraction(1, n + 1), ("stress exact", n))
        naive = sum((-1) ** j * comb(n, j) / (1 + j) for j in range(n + 1))
        compensated = fsum((-1) ** j * comb(n, j) / (1 + j) for j in range(n + 1))
        positive = 1.0
        for j in range(1, n + 1):
            positive *= j / (1 + j)
        rows.append(f"| {n} | {exact} | {naive!r} | {compensated!r} | {positive!r} |")

    status = [
        f"PASS: {identities} exact alternating-sum identities and positivity checks.",
        f"PASS: {coefficients} independent power-sum coefficient checks.",
        f"PASS: {bounds} exact lower/upper bound checks.",
        f"PASS: {recurrences} Pascal recurrence checks.",
        "PASS: 3 counterexample checks and 4 exact stress cases.",
    ]
    report = "\n".join([
        "# 계산 기록: 교대 이항합", "", "[연구 노트](note.md)", "",
        "- 연구일: 2026-10-29", f"- 실행 환경: Python {platform.python_version()} ({platform.system()})",
        "- 산술: 핵심 검산은 Fraction을 이용한 정확한 유리수 계산. 난수 없음.", "",
        "```powershell", "python research/2026-10-29-reciprocal-binomial/verify.py", "```", "",
        "```text", *status, "```", "",
        "범위: n=0..12, r=1..8, a=1/5,1/2,1,3/2,2,5. 점화식은 n=1..12.", "",
        "## 부동소수점 상쇄 실험", "", "a=r=1. 아래 실수 출력은 환경에 따라 달라질 수 있다.", "",
        "| n | 정확한 값 | 단순 합산 | math.fsum | 양수 곱 점화식 |",
        "| --- | --- | --- | --- | --- |", *rows, "",
        "유한 검산은 일반 증명을 대신하지 않는다. 미분 및 점근식은 노트의 증명으로 다룬다.", "",
    ])
    Path(__file__).with_name("results.md").write_text(report, encoding="utf-8")
    print("\n".join(status))
    print("WROTE: results.md (exact checks and floating-point observations).")


if __name__ == "__main__":
    main()
