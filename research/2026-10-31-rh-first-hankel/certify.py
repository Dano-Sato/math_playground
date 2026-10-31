"""Certify the first two 2x2 Hankel determinants of the actual Riemann Xi.

Run: python research/2026-10-31-rh-first-hankel/certify.py
Python >=3.10, standard library only, integer interval arithmetic, no randomness.
Fixed scope: moments I_k, k=0..4; u in [0,2]; theta terms n=1..4;
128 Taylor panels, degree 32, scale 10**180. Explicit analytic tails in note.md.
Writes certificate.json and results.md in this directory.
"""

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from math import comb, factorial, isqrt
from pathlib import Path
import json
import platform
import sys
import time

SCALE = 10 ** 180
DEGREE = 32
PANELS = 128


def ceil_div(a, b):
    assert b != 0
    return -((-a) // b)


@dataclass(frozen=True, slots=True)
class Interval:
    lo: int
    hi: int

    def __post_init__(self):
        assert self.lo <= self.hi

    @classmethod
    def of(cls, value):
        if isinstance(value, cls):
            return value
        value = Q(value)
        return cls(value.numerator * SCALE // value.denominator,
                   ceil_div(value.numerator * SCALE, value.denominator))

    def __add__(self, other):
        other = self.of(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-self.of(other))

    def __rsub__(self, other):
        return self.of(other) - self

    def __mul__(self, other):
        other = self.of(other)
        products = (self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi)
        return Interval(min(products) // SCALE, ceil_div(max(products), SCALE))

    __rmul__ = __mul__

    def inverse(self):
        assert self.lo * self.hi > 0, "Division interval contains zero"
        return Interval(SCALE * SCALE // self.hi,
                        ceil_div(SCALE * SCALE, self.lo))

    def __truediv__(self, other):
        return self * self.of(other).inverse()

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        value, base = self.of(1), self
        while n:
            if n & 1:
                value = value * base
            base = base * base
            n //= 2
        return value

    def contains(self, value):
        value = Q(value)
        return self.lo * value.denominator <= value.numerator * SCALE <= self.hi * value.denominator

    def strictly_inside(self, low, high):
        return Q(self.lo, SCALE) > Q(low) and Q(self.hi, SCALE) < Q(high)

    def encoded(self):
        return {"lower_numerator": str(self.lo), "upper_numerator": str(self.hi)}

    def sqrt(self):
        assert self.lo >= 0
        low = isqrt(self.lo * SCALE)
        high = isqrt(self.hi * SCALE)
        if high * high < self.hi * SCALE:
            high += 1
        return Interval(low, high)


ZERO, ONE = Interval.of(0), Interval.of(1)


def exp_interval(x):
    x = Interval.of(x)
    if x.hi <= 0:
        if x.lo == x.hi == 0:
            return ONE
        return exp_interval(-x).inverse()
    assert x.lo >= 0
    reductions = 0
    while x.hi * 8 > SCALE:
        x = x / 2
        reductions += 1
    total = term = ONE
    for k in range(1, 101):
        term = term * x / k
        total = total + term
    next_term = term * x / 101
    # All terms are nonnegative; successive tail ratios are at most 1/8.
    total = Interval(total.lo, total.hi + 2 * next_term.hi)
    for _ in range(reductions):
        total = total * total
    return total


def atan_inverse_bounds(n):
    total = sum((Q((-1) ** k, (2 * k + 1) * n ** (2 * k + 1))
                 for k in range(161)), Q(0))
    following = -Q(1, 323 * n ** 323)
    return Interval.of(total + following) + Interval(0, ceil_div(-following.numerator * SCALE, following.denominator))


def pi_interval():
    # Machin identity; both alternating series have 161 terms.
    return 16 * atan_inverse_bounds(5) - 4 * atan_inverse_bounds(239)


def convolution(a, b, degree):
    return [sum((a[j] * b[k - j] for j in range(max(0, k - len(b) + 1), min(k + 1, len(a)))), ZERO)
            for k in range(degree + 1)]


def kernel_series(center, pi):
    c = Interval.of(center)
    e2c = exp_interval(2 * c)
    e9c = exp_interval(Q(9, 2) * c)
    e5c = exp_interval(Q(5, 2) * c)
    alpha9 = [Interval.of(Q(9, 2) ** j / factorial(j)) for j in range(DEGREE + 1)]
    alpha5 = [Interval.of(Q(5, 2) ** j / factorial(j)) for j in range(DEGREE + 1)]
    alpha2 = [Interval.of(Q(2) ** j / factorial(j)) for j in range(DEGREE + 1)]
    result = [ZERO] * (DEGREE + 1)
    for n in range(1, 5):
        q = pi * n * n * e2c
        exponent = [-q * coefficient for coefficient in alpha2]
        exponential = [exp_interval(-q)]
        for k in range(1, DEGREE + 1):
            exponential.append(sum((j * exponent[j] * exponential[k - j]
                                    for j in range(1, k + 1)), ZERO) / k)
        prefactor = [4 * pi ** 2 * n ** 4 * e9c * alpha9[j]
                     - 6 * pi * n ** 2 * e5c * alpha5[j]
                     for j in range(DEGREE + 1)]
        term = convolution(exponential, prefactor, DEGREE)
        result = [x + y for x, y in zip(result, term)]
    return result


def integral_intervals():
    assert 64 * 354 * 3 ** 10 + 24 * 30 * 3 ** 6 < 2 ** 31
    assert 3 ** 8 < 2 ** 13
    assert Q(8, 3) ** 4 > 50
    assert Q(40960000, 18 ** 25) < Q(1, 10 ** 22)
    # Integral_50^infinity v^4 exp(-3v) dv / exp(-150).
    gamma_polynomial = sum((Q(factorial(4), factorial(4 - j)) * 50 ** (4 - j) / 3 ** (j + 1)
                            for j in range(5)), Q(0))
    assert gamma_polynomial < 3 * 10 ** 6
    assert 64 * 3 * 10 ** 6 < 2 ** 28
    pi = pi_interval()
    assert pi.strictly_inside(3, 4)
    totals = [ZERO] * 5
    half_width = Q(1, 128)
    integral_weights = [Interval.of(2 * half_width ** (j + 1) / (j + 1))
                        if j % 2 == 0 else ZERO for j in range(DEGREE + 1)]
    for panel in range(PANELS):
        center = Q(2 * panel + 1, 128)
        phi = kernel_series(center, pi)
        for k in range(5):
            power = [Interval.of(comb(2 * k, j) * center ** (2 * k - j)) for j in range(2 * k + 1)]
            integrand = convolution(phi, power, DEGREE)
            totals[k] = totals[k] + sum((integrand[j] * integral_weights[j]
                                        for j in range(0, DEGREE + 1, 2)), ZERO)
        if (panel + 1) % 32 == 0:
            print(f"Certified Taylor panels: {panel + 1}/{PANELS}", flush=True)
    taylor_error = 2 * Q(2 ** 45) * Q(1, 16) ** (DEGREE + 1) / (1 - Q(1, 16))
    theta_tail = Q(40960000, 18 ** 25)
    integral_tail = Q(1, 2 ** 122)
    error_interval = Interval(-ceil_div(taylor_error.numerator * SCALE, taylor_error.denominator),
                             ceil_div((taylor_error + theta_tail + integral_tail).numerator * SCALE,
                                      (taylor_error + theta_tail + integral_tail).denominator))
    return [value + error_interval for value in totals], pi, {
        "taylor_absolute_error": str(taylor_error),
        "theta_positive_tail": str(theta_tail),
        "u_ge_2_positive_tail": str(integral_tail),
    }


def moments_from_beta(beta):
    a = [(-1) ** k * beta[k] / factorial(2 * k) for k in range(5)]
    a[0] = ONE
    m = []
    for n in range(4):
        m.append(-(n + 1) * a[n + 1]
                 - sum((a[j] * m[n - j] for j in range(1, n + 1)), ZERO))
    return m


def cumulants(beta):
    b1, b2, b3, b4 = beta[1:]
    return [b1, b2 - 3 * b1 ** 2,
            b3 - 15 * b1 * b2 + 30 * b1 ** 3,
            b4 - 28 * b1 * b3 - 35 * b2 ** 2 + 420 * b1 ** 2 * b2 - 630 * b1 ** 4]


def arithmetic_checks():
    # Exact endpoint arithmetic checks with rational inputs, all sign combinations.
    count = 0
    for a in [Q(-7, 3), Q(-1, 13), Q(0), Q(2, 7), Q(11, 5)]:
        for b in [Q(-5, 7), Q(1, 17), Q(9, 4)]:
            x, y = Interval.of(a), Interval.of(b)
            for computed, exact in [(x + y, a + b), (x - y, a - b),
                                    (x * y, a * b), (x / y, a / b)]:
                assert computed.contains(exact)
                count += 1
    assert exp_interval(0).contains(1)
    assert exp_interval(1).strictly_inside(Q(2718, 1000), Q(2719, 1000))
    # Use a rational model to check both independent algebraic formulas.
    beta = [ONE] + [Interval.of(Q(1, 2 * k + 1)) for k in range(1, 5)]
    m = moments_from_beta(beta)
    k2, k4, k6, k8 = cumulants(beta)
    alternative = [k2 / 2, -k4 / 12, k6 / 240, -k8 / 10080]
    for x, y in zip(m, alternative):
        assert x.lo <= y.hi and y.lo <= x.hi
    return count


def approx(value):
    with localcontext() as context:
        context.prec = 35
        return str(Decimal(value.lo + value.hi) / (2 * SCALE))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    started = time.perf_counter()
    checks = arithmetic_checks()
    integrals, pi, errors = integral_intervals()
    assert all(value.lo > 0 for value in integrals)
    beta = [ONE] + [value / integrals[0] for value in integrals[1:]]
    m = moments_from_beta(beta)
    d0, d1 = m[0] * m[2] - m[1] ** 2, m[1] * m[3] - m[2] ** 2
    assert all(value.lo > 0 for value in m)
    assert d0.strictly_inside(Q(1949, 10 ** 12), Q(1950, 10 ** 12))
    assert d1.strictly_inside(Q(3860, 10 ** 18), Q(3861, 10 ** 18))
    k2, k4, k6, k8 = cumulants(beta)
    alt0 = (3 * k2 * k6 - 10 * k4 ** 2) / 1440
    alt1 = (10 * k4 * k8 - 21 * k6 ** 2) / 1209600
    assert alt0.lo > 0 and alt1.lo > 0
    assert d0.lo <= alt0.hi and alt0.lo <= d0.hi
    assert d1.lo <= alt1.hi and alt1.lo <= d1.hi
    # Finite two-node quadrature, valid for exactly moments m0..m3.
    trace = (m[0] * m[3] - m[1] * m[2]) / d0
    product = d1 / d0
    gap = (trace ** 2 - 4 * product).sqrt()
    nodes = [(trace - gap) / 2, (trace + gap) / 2]
    alpha0 = m[1] / m[0]
    weights = [m[0] * (nodes[1] - alpha0) / gap,
               m[0] * (alpha0 - nodes[0]) / gap]
    assert all(x.lo > 0 for x in nodes + weights)
    for k in range(4):
        reconstructed = sum((weight * node ** k for weight, node in zip(weights, nodes)), ZERO)
        assert reconstructed.lo <= m[k].hi and m[k].lo <= reconstructed.hi
    assert (beta[2] / beta[1] ** 2).strictly_inside(Q(27, 10), Q(29, 10))
    certificate = {
        "scale_denominator": str(SCALE), "degree": DEGREE, "panels": PANELS,
        "theta_terms": 4, "u_cutoff": 2, "errors": errors, "pi": pi.encoded(),
        "half_line_integrals": [x.encoded() for x in integrals],
        "normalized_even_moments": [x.encoded() for x in beta],
        "log_derivative_moments": [x.encoded() for x in m],
        "D0": d0.encoded(), "D1": d1.encoded(),
        "two_node_quadrature": {"nodes": [x.encoded() for x in nodes],
                                "weights": [x.encoded() for x in weights]},
    }
    folder = Path(__file__).resolve().parent
    (folder / "certificate.json").write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    lines = ["# 실제 리만 함수의 첫 두 Hankel 행렬: 검증 결과", "",
             f"- Python {platform.python_version()}, 표준 라이브러리, 정수 구간 연산.",
             "- 난수·부동소수점·리만 영점 목록을 인증에 사용하지 않음.",
             f"- 유리수 연산 포함성 점검 {checks}건 PASS; 두 누적량 항등식 교차 점검 PASS.",
             "- [0,2]의 128개 패널, Taylor 차수 32, θ항 n=1..4, 고정 소수점 180자리.",
             "- 절단·Taylor·정수 반올림 오차를 모두 포함함. 자세한 유리수 끝점은 certificate.json.", "",
             "| 양 | 구간 중점의 표시용 근삿값 |", "| --- | --- |"]
    lines += [f"| I{k} | {approx(x)} |" for k, x in enumerate(integrals)]
    lines += [f"| m{k} | {approx(x)} |" for k, x in enumerate(m)]
    lines += [f"| D0 | {approx(d0)} |", f"| D1 | {approx(d1)} |", "",
              "## 정확한 유리수 포함 관계", "",
              "- 1949/10^12 < D0 < 1950/10^12: PASS",
              "- 3860/10^18 < D1 < 3861/10^18: PASS",
              "- m0,m1,m2,m3의 구간 하한 모두 양수: PASS",
              "- 따라서 실제 Ξ의 두 2×2 Hankel 행렬은 양의 정부호.",
              "- 27/10 < β2/β1^2 < 29/10: PASS; 단순 Cauchy–Schwarz 충분조건은 적용 불가.",
              "- 두 절점·가중치의 구간 하한 양수 및 m0..m3 재구성 교차 점검: PASS.",
              "- 임의 크기 행렬의 양수성, RH, 일반적인 제곱 적분 표현은 증명하지 않음.", "",
              "## m0..m3만 일치시키는 두 원자 측도", "",
              "아래는 표시용 근삿값이다. 실제 영점의 역제곱이라고 해석하지 않는다.", "",
              f"- x_minus ≈ {approx(nodes[0])}; x_plus ≈ {approx(nodes[1])}",
              f"- w_minus ≈ {approx(weights[0])}; w_plus ≈ {approx(weights[1])}", "",
              f"실행 시간: {time.perf_counter() - started:.2f}초.", ""]
    output = "\n".join(lines)
    (folder / "results.md").write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
