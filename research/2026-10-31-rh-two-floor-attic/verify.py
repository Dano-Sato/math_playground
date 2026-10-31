"""Exact checks for the two Hankel towers and their finite-stage obstruction.

Run from repository root:
    python research/2026-10-31-rh-two-floor-attic/verify.py
Python >= 3.10, standard library only. No random numbers or floating point.
Search: N=0..6; T=2**e, e=1..20. Failure to find T raises an error.
This checks model functions, not numerical zeros of the Riemann xi function.
"""

from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import platform
import sys


def mul(a, b):
    c = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def moments_from_coefficients(coeffs, count):
    assert coeffs[0] == 1
    a = list(coeffs) + [Q(0)] * max(0, count + 1 - len(coeffs))
    m = []
    for n in range(count):
        m.append(-(n + 1) * a[n + 1]
                 - sum((a[j] * m[n - j] for j in range(1, n + 1)), Q(0)))
    return m


def hankel(m, n, shift=0):
    return [[m[i + j + shift] for j in range(n + 1)] for i in range(n + 1)]


def positive_definite(a):
    # Exact symmetric elimination: every Schur pivot must be strictly positive.
    a = [list(row) for row in a]
    for k in range(len(a)):
        pivot = a[k][k]
        if pivot <= 0:
            return False
        for i in range(k + 1, len(a)):
            for j in range(i, len(a)):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return True


def determinant(a):
    a = [list(row) for row in a]
    value = Q(1)
    for k in range(len(a)):
        pivot_row = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot_row is None:
            return Q(0)
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            value = -value
        pivot = a[k][k]
        value *= pivot
        for i in range(k + 1, len(a)):
            factor = a[i][k] / pivot
            for j in range(k + 1, len(a)):
                a[i][j] -= factor * a[k][j]
            a[i][k] = Q(0)
    return value


def perturbed_polynomial(n, t, count):
    # F0(z) = product_{j=1}^{n+1}(1-z/j).
    base = [Q(1)]
    for j in range(1, n + 2):
        base = mul(base, [Q(1), -Q(1, j)])
    delta = Q(1, 4)
    denom = (t * t + delta * delta) ** 2
    real_part = (t * t - delta * delta) / denom
    absolute_square = 1 / denom
    # a = (T+i/4)^(-2); factor=(1-az)(1-conj(a)z).
    coeffs = mul(base, [Q(1), -2 * real_part, absolute_square])
    pair_sums = [Q(2), 2 * real_part]
    for k in range(2, count + 1):
        pair_sums.append(2 * real_part * pair_sums[-1]
                         - absolute_square * pair_sums[-2])
    root_moments = [sum((Q(1, j) ** (k + 1) for j in range(1, n + 2)), Q(0))
                    + pair_sums[k + 1] for k in range(count)]
    assert moments_from_coefficients(coeffs, count) == root_moments
    return root_moments


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    lines = ["# 정확 유리수 검산 결과", "",
             f"- 환경: Python {platform.python_version()}, 표준 라이브러리",
             "- 난수·부동소수점 없음. 리만 영점의 수치 검증은 수행하지 않음.",
             "- 실행: `python research/2026-10-31-rh-two-floor-attic/verify.py`", ""]

    # sinc(sqrt(z))**2 * (3+cos(4*sqrt(z)))/4.
    order = 4
    sinc = [Q((-1) ** k, factorial(2 * k + 1)) for k in range(order + 1)]
    cosine_mix = [Q(1)] + [Q((-1) ** k * 4 ** (2 * k), 4 * factorial(2 * k))
                                for k in range(1, order + 1)]
    toy_coeffs = mul(mul(sinc, sinc), cosine_mix)[:order + 1]
    toy_moments = moments_from_coefficients(toy_coeffs, order)
    assert toy_coeffs[:3] == [Q(1), -Q(7, 3), Q(152, 45)]
    assert toy_moments[:2] == [Q(7, 3), -Q(59, 45)]
    lines += ["## 양의 Fourier 밀도 모형", "",
              f"- a0,a1,a2 = {', '.join(map(str, toy_coeffs[:3]))}",
              f"- m0 = {toy_moments[0]}; m1 = {toy_moments[1]} < 0: PASS", "",
              "## 유한 단계 통과 뒤 실패하는 다항식", "",
              "각 N에서 T=2^e(e=1..20)를 순서대로 탐색한다. δ=1/4.",
              "두 N단계 행렬의 양의 정부호와 두 (N+2)단계 행렬식의 음수를 정확히 확인한다.", "",
              "| N | 선택한 T | N단계 두 행렬 | (N+2)단계 두 행렬식 |",
              "| --- | --- | --- | --- |"]
    coefficient_comparisons = 0
    for n in range(7):
        count = 2 * (n + 2) + 2
        for exponent in range(1, 21):
            t = 2 ** exponent
            m = perturbed_polynomial(n, t, count)
            coefficient_comparisons += count
            if all(positive_definite(hankel(m, n, shift)) for shift in (0, 1)):
                break
        else:
            raise AssertionError(f"No passing T in bounded search for N={n}")
        assert all(determinant(hankel(m, n + 2, shift)) < 0 for shift in (0, 1))
        lines.append(f"| {n} | {t} | 양의 정부호 | 둘 다 음수 |")
    lines += ["", f"- 계수 재귀와 별도 영점 거듭제곱합의 일치: {coefficient_comparisons}개 계수 PASS",
              "- 모형 7개에서 N단계 양의 정부호·N+2단계 음의 행렬식: PASS",
              "- 무한 범위의 주장은 note.md의 연속성·Vandermonde 논증에 의존한다.", ""]
    output = "\n".join(lines)
    Path(__file__).with_name("results.md").write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
