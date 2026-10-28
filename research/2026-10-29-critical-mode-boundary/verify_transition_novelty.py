"""Exact finite checks of the probability map and first correction; Python 3.10+."""

from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import platform


def direct(n, r, a):
    return sum(((-1)**j * comb(n, j) / (a + j)**r
                for j in range(n + 1)), Q(0))


def geometric_sum(n, a, degree):
    # Convolution of actual pmfs, including normalization, truncated only in degree.
    pmf = [Q(1)] + [Q(0)] * degree
    for j in range(n + 1):
        x = 1 / (a + j)
        pmf = [sum((pmf[m - t] * (1 - x) * x**t
                    for t in range(m + 1)), Q(0))
               for m in range(degree + 1)]
    return pmf


def poisson_polynomial_coefficient(mean, degree, polynomial):
    # Coefficient of exp(mean*z) times a polynomial; exp(-mean) cancels in ratios.
    return sum((c * mean**(degree - j) / factorial(degree - j)
                for j, c in enumerate(polynomial) if j <= degree), Q(0))


def main():
    mapped = corrected = 0
    for n in range(1, 9):
        for a in (Q(3, 2), Q(2), Q(5), Q(101, 10)):
            pmf = geometric_sum(n, a, 8)
            for k in range(1, 9):
                if pmf[k] / pmf[k - 1] != direct(n, k + 1, a) / direct(n, k, a):
                    raise AssertionError(("probability map", n, a, k))
                mapped += 1

    # theta is formal here: exact rational checks of the algebra after t=k.
    # These do not pretend a rational theta satisfies log(1+1/theta)=k.
    for theta in (Q(1, 10), Q(1, 2), Q(1), Q(3)):
        u = (1 / theta + 1 / (theta + 1)) / 2
        v = 1 / (theta * (theta + 1))
        for k in range(1, 13):
            beta_star = theta + Q(3, 2) - Q(1, k)
            for beta in (beta_star - 1, beta_star, beta_star + 1):
                d = u + (1 - beta) * v
                # d*(z-1) + v/2*(z-1)^2, in ascending powers of z.
                polynomial = [-d + v / 2, d - v, v / 2]
                corrections = []
                for m in (k - 1, k):
                    base = Q(k)**m / factorial(m)
                    corrections.append(poisson_polynomial_coefficient(Q(k), m, polynomial) / base)
                if corrections[1] - corrections[0] != v / k * (beta_star - beta):
                    raise AssertionError(("first correction", theta, k, beta))
                corrected += 1

    output = (
        "# 전환점 신규성 조사: 추가 검산\n\n"
        "[집중 조사](transition-novelty-review.md) · [검산 코드](verify_transition_novelty.py)\n\n"
        "명령: `python research/2026-10-29-critical-mode-boundary/verify_transition_novelty.py`\n\n"
        f"환경: Python {platform.python_version()}, 표준 라이브러리, 난수 없음.\n\n"
        f"- 정확한 기하분포 합과 교대합의 이웃 비율 대응: {mapped}건 통과.\n"
        f"- 생성함수 계수 추출과 전환점 상수 보정의 유리수 항등식: {corrected}건 통과.\n\n"
        "첫 검산 범위: n=1..8, a=3/2,2,5,101/10, k=1..8.\n\n"
        "둘째 검산 범위: 형식 변수 theta=1/10,1/2,1,3, k=1..12, "
        "beta=beta_star-1,beta_star,beta_star+1. 초월수 theta_k를 유리수로 간주하지 않는다.\n\n"
        "유한 검산이며 점근 나머지의 증명이나 문헌 신규성 검증이 아니다.\n"
    )
    Path(__file__).with_name("transition-novelty-checks.md").write_text(output, encoding="utf-8")
    print(f"Exact probability maps: {mapped}; first-correction identities: {corrected}. All passed.")


if __name__ == "__main__":
    main()
