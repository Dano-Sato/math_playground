"""Exact rational checks for the log-concavity obstruction and score covariances.

Run from repository root:
    python research/2026-10-31-rh-logconcavity-obstruction/verify.py
Python >=3.10, standard library only; no randomness or numerical quadrature.
Inputs: a=1/5, eta=10^-12, k=0..3. Reads the prior Riemann certificate.
The super-exponential kernel's moment enclosures use the analytic bound in note.md.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
from decimal import Decimal, localcontext
import json
import platform
import sys


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __post_init__(self):
        assert self.lo <= self.hi

    @classmethod
    def of(cls, x):
        return x if isinstance(x, cls) else cls(Q(x), Q(x))

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
        values = [self.lo * other.lo, self.lo * other.hi,
                  self.hi * other.lo, self.hi * other.hi]
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.of(other)
        assert other.lo * other.hi > 0
        return self * Interval(1 / other.hi, 1 / other.lo)

    def __pow__(self, n):
        assert n >= 0
        value = self.of(1)
        for _ in range(n):
            value = value * self
        return value

    def inside(self, lo, hi):
        return Q(lo) < self.lo <= self.hi < Q(hi)

    def encoded(self):
        return {"lower": str(self.lo), "upper": str(self.hi)}


def gaussian_moment(k):
    return Q(factorial(2 * k), 4 ** k * factorial(k))


def shifted_gaussian_moment(k):
    # Mean 1/2, variance 1/2, even moment of degree 2k.
    return sum((comb(2 * k, 2 * j) * Q(1, 2) ** (2 * k - 2 * j)
                * gaussian_moment(j) for j in range(k + 1)), Q(0))


def normalized_moments(raw):
    return [Interval.of(1)] + [x / raw[0] for x in raw[1:]]


def log_moments(beta):
    a = [(-1) ** k * beta[k] / factorial(2 * k) for k in range(4)]
    m = []
    for n in range(3):
        m.append(-(n + 1) * a[n + 1] - sum((a[j] * m[n - j] for j in range(1, n + 1)), Interval.of(0)))
    return m


def score_covariances(beta):
    b1, b2, b3 = beta[1:4]
    c1 = (3 * b1 ** 2 - b2) / (2 * b1 ** 2)
    c2 = (5 * b2 ** 2 - 3 * b1 * b3) / (2 * b2 ** 2)
    return c1, c2


def midpoint_string(box):
    value = (box.lo + box.hi) / 2
    with localcontext() as context:
        context.prec = 22
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    folder = Path(__file__).resolve().parent
    a, eta = Q(1, 5), Q(1, 10 ** 12)
    raw0 = [gaussian_moment(k) + a * gaussian_moment(k + 1)
            + a * a / 2 * gaussian_moment(k + 2) for k in range(4)]
    beta0 = normalized_moments([Interval.of(x) for x in raw0])
    m0 = log_moments(beta0)
    d0 = m0[0] * m0[2] - m0[1] ** 2
    expected = [Q(275, 892), Q(115, 99458), Q(91, 44358268)]
    assert all(box.lo == box.hi == value for box, value in zip(m0, expected))
    assert d0.lo == d0.hi == -Q(125, 177433072)

    # Perturbation by exp(-eta*(cosh(x)-1)); exp(1/4)<4/3.
    shifted = [shifted_gaussian_moment(k) + a * shifted_gaussian_moment(k + 1)
               + a * a / 2 * shifted_gaussian_moment(k + 2) for k in range(4)]
    raw_eta = [Interval(x - eta * Q(4, 3) * t, x) for x, t in zip(raw0, shifted)]
    assert all(x.lo > 0 for x in raw_eta)
    beta_eta = normalized_moments(raw_eta)
    m_eta = log_moments(beta_eta)
    d_eta = m_eta[0] * m_eta[2] - m_eta[1] ** 2
    assert all(x.lo > 0 for x in m_eta)
    assert d_eta.inside(-Q(705, 10 ** 9), -Q(704, 10 ** 9))
    c1_bad, c2_bad = score_covariances(beta_eta)
    assert c1_bad.lo > 0 and c2_bad.lo > 0
    assert (5 * c1_bad - (beta_eta[2] / beta_eta[1] ** 2) * c2_bad).hi < 0

    # Family [1/5,41/200]: endpoint signs and positive polynomial derivatives.
    upper = Q(41, 200)
    determinant_polynomial = lambda t: 105 * t ** 3 + 194 * t ** 2 + 32 * t - 16
    assert determinant_polynomial(upper) == -Q(612099, 1600000) < 0
    assert 27 * a * a + 36 * a - 8 == Q(7, 25) > 0

    prior_path = folder.parent / "2026-10-31-rh-first-hankel" / "certificate.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    scale = int(prior["scale_denominator"])
    beta_actual = [Interval(Q(int(x["lower_numerator"]), scale),
                            Q(int(x["upper_numerator"]), scale))
                   for x in prior["normalized_even_moments"][:4]]
    c1, c2 = score_covariances(beta_actual)
    assert c1.lo > 0 and c2.lo > 0
    ratio = c2 / c1
    assert ratio.inside(Q(141, 100), Q(142, 100))
    assert (Q(5, 3) * c1 - c2).lo > 0
    certificate = {
        "a": str(a), "eta": str(eta),
        "base_m": [x.encoded() for x in m0], "base_D0": d0.encoded(),
        "perturbed_raw": [x.encoded() for x in raw_eta],
        "perturbed_m": [x.encoded() for x in m_eta], "perturbed_D0": d_eta.encoded(),
        "actual_C1": c1.encoded(), "actual_C2": c2.encoded(),
        "actual_C2_over_C1": ratio.encoded(),
        "prior_input": "../2026-10-31-rh-first-hankel/certificate.json",
    }
    (folder / "certificate.json").write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    lines = ["# 로그 오목성 경로의 정확 검산", "",
             f"- Python {platform.python_version()}, 표준 라이브러리 Fraction; 난수·부동소수점 검산 없음.",
             "- 입력: a=1/5, eta=10^-12, 적률 차수 k=0..3. Decimal은 표시용 중점에만 사용.", "",
             "## 명시적 Gaussian 다항식 핵", "",
             f"- m0,m1,m2 = {', '.join(str(x.lo) for x in m0)} > 0: PASS",
             f"- D0 = {d0.lo} < 0: PASS",
             "- a∈[1/5,41/200] 전체의 부호 판정에 필요한 다항식 끝점: PASS", "",
             "## 초지수 꼬리로 바꾼 핵", "",
             "- eta=10^-12에서 m0,m1,m2의 하한 모두 양수: PASS",
             "- -705/10^9 < D0 < -704/10^9 < 0: PASS",
             "- 두 공분산의 하한 양수지만 행렬식에 필요한 비교식은 음수: PASS", "",
             "## 실제 리만 핵: 이전 인증 구간의 정확한 귀결", "",
             f"- C1 구간 중점 ≈ {midpoint_string(c1)}",
             f"- C2 구간 중점 ≈ {midpoint_string(c2)}",
             "- 141/100 < C2/C1 < 142/100 < 5/3: PASS",
             "- 이 비교는 이전 적률 구간에서 계산한 결과이며, 계산 없는 핵 부등식의 증명이 아님.", ""]
    output = "\n".join(lines)
    (folder / "results.md").write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
