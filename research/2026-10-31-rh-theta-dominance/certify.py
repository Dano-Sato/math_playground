"""One global Taylor polynomial and a uniform theta remainder, no quadrature grid.

Run: python research/2026-10-31-rh-theta-dominance/certify.py
Python >=3.10, standard library only. No randomness or floating-point decisions.
Uses read-only interval arithmetic helpers from ../2026-10-31-rh-first-hankel/
certify.py; does not execute that file's main or read its numerical certificate.
Scope: theta n=1, moments k=0..3, one degree-96 polynomial on [0,1].
"""

from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import platform
import runpy
import sys

FOLDER = Path(__file__).resolve().parent
SUPPORT = FOLDER.parent / "2026-10-31-rh-first-hankel" / "certify.py"
HELPERS = runpy.run_path(str(SUPPORT))
Interval = HELPERS["Interval"]
exp_interval = HELPERS["exp_interval"]
pi_interval = HELPERS["pi_interval"]
convolution = HELPERS["convolution"]
SCALE, ZERO = HELPERS["SCALE"], HELPERS["ZERO"]
DEGREE = 96


def exp_partial(x, count):
    return sum((x ** j / factorial(j) for j in range(count + 1)), Q(0))


def first_term_series(pi):
    c = Q(1, 2)
    q = pi * exp_interval(1)
    exponent = [-q * Q(2) ** j / factorial(j) for j in range(DEGREE + 1)]
    exponential = [exp_interval(-q)]
    for k in range(1, DEGREE + 1):
        exponential.append(sum((j * exponent[j] * exponential[k - j]
                                for j in range(1, k + 1)), ZERO) / k)
    e9c, e5c = exp_interval(Q(9, 2) * c), exp_interval(Q(5, 2) * c)
    prefactor = [4 * pi ** 2 * e9c * Q(9, 2) ** j / factorial(j)
                 - 6 * pi * e5c * Q(5, 2) ** j / factorial(j)
                 for j in range(DEGREE + 1)]
    return convolution(exponential, prefactor, DEGREE)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    pi = pi_interval()
    assert pi.strictly_inside(Q(157, 50), Q(22, 7))
    assert exp_partial(Q(471, 50), 50) > 12000
    assert Q(27, 12000) + Q(324, 18 ** 8) < Q(1, 400)
    assert exp_partial(Q(2), 20) > Q(369, 50)
    assert exp_partial(Q(6), 30) > 400
    cutoff, rate = Q(369, 50), Q(157, 50)
    assert exp_partial(cutoff * rate, 80) > 10 ** 10
    tail_poly = sum((Q(factorial(5), factorial(5 - j)) * cutoff ** (5 - j)
                     / rate ** (j + 1) for j in range(6)), Q(0))
    assert tail_poly < 10000
    tail_error = Q(8, 10 ** 8)  # 32/400 * 10000 * 10^-10.
    assert 64 * 3 ** 6 + 24 * 3 ** 4 < 2 ** 16
    assert Q(5, 4) ** 6 < 4
    taylor_error = Q(3 * 2 ** 18) * Q(2, 3) ** (DEGREE + 1)
    phi = first_term_series(pi)
    moments = []
    for k in range(4):
        monomial = [Interval.of(comb(2 * k, j) * Q(1, 2) ** (2 * k - j)) for j in range(2 * k + 1)]
        integrand = convolution(phi, monomial, DEGREE)
        integral = sum((integrand[j] * Q(2) * Q(1, 2) ** (j + 1) / (j + 1)
                        for j in range(0, DEGREE + 1, 2)), ZERO)
        # Symmetric Taylor error; only a positive tail from [1,infinity).
        left_error = Interval.of(-taylor_error)
        right_error = Interval.of(taylor_error + tail_error)
        moments.append(integral + Interval(left_error.lo, right_error.hi))
    table_low = [Q(n, 10 ** 8) for n in (24847451, 1148570, 148141, 29963)]
    table_high = [Q(n, 10 ** 8) for n in (24847460, 1148579, 148151, 29973)]
    for k, (box, lo, hi) in enumerate(zip(moments, table_low, table_high)):
        assert box.strictly_inside(lo, hi), f"Moment {k}: {Q(box.lo, SCALE)} .. {Q(box.hi, SCALE)} outside {lo} .. {hi}"
    first_ratio_lower = 9 * table_low[1] ** 3 * table_low[3] / (5 * table_high[0] * table_high[2] ** 3)
    threshold = Q(1011, 1000)
    assert first_ratio_lower > threshold
    perturbation_factor = Q(401, 400) ** 4
    assert threshold > perturbation_factor
    full_ratio_lower = threshold / perturbation_factor
    assert full_ratio_lower > Q(10009, 10000)
    first_r_upper = table_high[0] * table_high[2] / table_low[1] ** 2
    assert Q(401, 400) ** 2 * first_r_upper < 3
    r_lower = table_low[0] * table_low[2] / (Q(401, 400) ** 2 * table_high[1] ** 2)
    r_upper = Q(401, 400) ** 2 * first_r_upper
    b1_lower = table_low[1] / (Q(401, 400) * table_high[0])
    b2_lower = table_low[2] / (Q(401, 400) * table_high[0])
    determinant_lower = b1_lower ** 2 * b2_lower / 864 * ((3 - r_upper) ** 2
                         + r_lower ** 2 * (full_ratio_lower - 1))
    assert determinant_lower > Q(6, 10 ** 10)
    # Positive boundary derivative: -8*pi^2+30*pi-15 > value at 22/7.
    assert -8 * Q(22, 7) ** 2 + 30 * Q(22, 7) - 15 == Q(13, 49) > 0
    certificate = {
        "scope": "n=1, k=0..3, one global degree-96 Taylor polynomial on [0,1]",
        "scale_denominator": str(SCALE), "degree": DEGREE,
        "support_path": "../2026-10-31-rh-first-hankel/certify.py",
        "support_sha256": hashlib.sha256(SUPPORT.read_bytes()).hexdigest(),
        "pi": pi.encoded(), "taylor_error": str(taylor_error),
        "positive_integral_tail_error": str(tail_error),
        "first_term_moments": [x.encoded() for x in moments],
        "coarse_lower": [str(x) for x in table_low], "coarse_upper": [str(x) for x in table_high],
        "theta_relative_error": "1/400", "first_ratio_lower": str(first_ratio_lower),
        "first_ratio_threshold": str(threshold), "transfer_factor": str(perturbation_factor),
        "full_ratio_lower": str(full_ratio_lower),
        "full_D0_lower": str(determinant_lower),
    }
    (FOLDER / "certificate.json").write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    lines = ["# θ 첫 항과 나머지의 격자 없는 인증", "",
             f"- Python {platform.python_version()}, 표준 라이브러리, 정수·유리수 구간 연산.",
             "- 난수·적분 격자·부동소수점 부호 판정 없음. 이전 실제 적률 인증값을 입력으로 쓰지 않음.",
             "- 이전 certify.py의 일반 구간 연산 함수만 읽기 전용으로 사용.",
             "- 하나의 96차 Taylor 다항식을 [0,1] 전체에 적분하고, 두 무한 꼬리를 별도로 제한.", "",
             "| k | 첫 항 적률 Jk의 정확한 하한 | 정확한 상한 |",
             "| --- | --- | --- |"]
    lines += [f"| {k} | {lo} | {hi} |" for k, (lo, hi) in enumerate(zip(table_low, table_high))]
    lines += ["", "- 위 네 구간의 포함 관계: PASS",
              "- 0 ≤ (Φ-φ1)/φ1 < 1/400을 위한 상수 부등식: PASS",
              "- 9 J1^3 J3 / (5 J0 J2^3) > 1011/1000: PASS",
              "- (401/400)^4 < 1011/1000: PASS",
              "- 전체 핵의 9 I1^3 I3 / (5 I0 I2^3) > 10009/10000 > 1: PASS",
              "- 전체 핵의 r=I0 I2/I1^2 < 3: PASS",
              "- 제곱 항과 양의 여유 분해로 전체 핵의 D0 > 6/10^10: PASS",
              "- 따라서 C2 < (5/3)C1, m1>0, D0>0.",
              "- 첫 항의 경계 미분에 필요한 -8π²+30π-15>13/49>0: PASS", "",
              "격자는 없지만 유한한 급수 계수 계산에 의존하는 계산 보조 증명이다.",
              "모든 크기의 Hankel 양수성 또는 RH의 증명은 아니다.", ""]
    output = "\n".join(lines)
    (FOLDER / "results.md").write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
