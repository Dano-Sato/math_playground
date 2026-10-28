"""Exact finite checks for Turan bounds, simplex moments, and unimodality."""

from decimal import Decimal, localcontext
from fractions import Fraction as Q
from math import comb, factorial, prod
from pathlib import Path
import platform


def direct(n, r, a):
    return sum(((-1)**j * comb(n, j) / (a + j)**r for j in range(n + 1)), Q(0))


def homogeneous(variables, degree):
    coefficients = [Q(1)] + [Q(0)] * degree
    for x in variables:
        for k in range(1, degree + 1):
            coefficients[k] += x * coefficients[k - 1]
    return coefficients


def compositions(total, count):
    if count == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, count - 1):
            yield (first,) + rest


def simplex_moment(variables, degree):
    m = len(variables)
    value = Q(0)
    for powers in compositions(degree, m):
        factorial_product = prod(factorial(p) for p in powers)
        multinomial = factorial(degree) // factorial_product
        monomial_moment = Q(factorial(m - 1) * factorial_product, factorial(m + degree - 1))
        value += multinomial * monomial_moment * prod((x**p for x, p in zip(variables, powers)), start=Q(1))
    return value


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def threshold_bracket(n):
    low, high = Q(1), Q(n + 1)
    for _ in range(48):
        midpoint = (low + high) / 2
        harmonic = sum((1 / (midpoint + j) for j in range(n + 1)), Q(0))
        if harmonic > 1:
            low = midpoint
        else:
            high = midpoint
    return low, high


def main():
    parameters = [Q(1, 5), Q(1, 2), Q(1), Q(6, 5), Q(3, 2), Q(2), Q(3), Q(8)]
    identity_cases = bound_cases = regime_cases = value_bound_cases = 0
    for n in range(13):
        for a in parameters:
            variables = [1 / (a + j) for j in range(n + 1)]
            h = homogeneous(variables, 24)
            b = direct(n, 1, a)
            values = [Q(0)] + [direct(n, r, a) for r in range(1, 26)]
            for r in range(1, 26):
                require(values[r] == b * h[r - 1], ("direct identity", n, a, r))
                identity_cases += 1
                k, m = r - 1, n + 1
                total, maximum, minimum = sum(variables), max(variables), min(variables)
                mean = total / m
                jensen = comb(m + k - 1, k) * mean**k
                old_lower = total**k / factorial(k)
                require(jensen >= old_lower and ((jensen > old_lower) == (k >= 2)), ("lower improvement", n, a, r))
                new_lower = max(maximum**k, jensen)
                old_upper = prod((total + i * maximum for i in range(k)), start=Q(1)) / factorial(k)
                chord = comb(m + k - 1, k) * maximum**k if maximum == minimum else comb(m + k - 1, k) * ((maximum - mean) * minimum**k + (mean - minimum) * maximum**k) / (maximum - minimum)
                require(new_lower <= h[k] <= min(old_upper, chord), ("new value bounds", n, a, r))
                value_bound_cases += 1
            for r in range(2, 25):
                ratio = values[r]**2 / (values[r - 1] * values[r + 1])
                upper = 1 + Q(n, (r - 1) * (n + r))
                require((ratio == 1) if n == 0 else (1 < ratio < upper), ("Turan bounds", n, a, r, ratio, upper))
                bound_cases += 1
            ratios = [values[r + 1] / values[r] for r in range(1, 25)]
            if n:
                require(all(ratios[i] > ratios[i + 1] for i in range(23)), ("ratio decrease", n, a))
                require(all(value > 1 / a for value in ratios), ("ratio limit bound", n, a))
                if a <= 1:
                    require(all(value > 1 for value in ratios), ("increasing regime", n, a))
                elif sum(variables) <= 1:
                    require(all(value < 1 for value in ratios[1:]), ("decreasing regime", n, a))
            else:
                require(all(value == 1 / a for value in ratios), ("geometric boundary", a))
            regime_cases += 1

    vectors = [[Q(2)], [Q(1), Q(1)], [Q(1), Q(2)], [Q(1, 3), Q(1, 2), Q(1)], [Q(1, 7), Q(2, 3), Q(5, 2), Q(4)]]
    moment_cases = normalization_cases = 0
    for variables in vectors:
        m = len(variables)
        h = homogeneous(variables, 10)
        moments = [simplex_moment(variables, k) for k in range(11)]
        for k in range(11):
            require(moments[k] == h[k] / comb(m + k - 1, k), ("simplex moment", variables, k))
            moment_cases += 1
        for k in range(1, 10):
            left, right = moments[k]**2, moments[k - 1] * moments[k + 1]
            require(left <= right and ((left == right) == (len(set(variables)) == 1)), ("normalized equality", variables, k))
            normalization_cases += 1

    defect_cases = 0
    for variables in vectors:
        old = homogeneous(variables, 13)
        for x in (Q(1, 2), Q(3)):
            new = homogeneous(variables + [x], 13)
            for k in range(1, 13):
                pieces = [x**i * (old[k] * old[k - i] - (old[k + 1] * old[k - 1 - i] if i < k else 0)) for i in range(k + 1)]
                require(all(piece >= 0 for piece in pieces) and pieces[-1] > 0, ("positive defect pieces", variables, x, k))
                require(sum(pieces) == new[k]**2 - new[k - 1] * new[k + 1], ("defect identity", variables, x, k))
                defect_cases += 1

    peak_values = [direct(1, r, Q(3, 2)) for r in range(1, 13)]
    require(peak_values[1] > peak_values[0] and all(peak_values[i] > peak_values[i + 1] for i in range(1, 11)), "peak at r=2")

    thresholds = []
    with localcontext() as context:
        context.prec = 60
        e = Decimal(1).exp()
        for n in (1, 2, 5, 12, 50):
            low, high = threshold_bracket(n)
            require(sum((1 / (low + j) for j in range(n + 1)), Q(0)) >= 1, ("threshold lower", n))
            require(sum((1 / (high + j) for j in range(n + 1)), Q(0)) <= 1, ("threshold upper", n))
            midpoint = (Decimal(low.numerator) / Decimal(low.denominator) + Decimal(high.numerator) / Decimal(high.denominator)) / 2
            predicted_low = Decimal(n + 1) / (e - 1)
            require(predicted_low < midpoint < predicted_low + 1, ("approximate e boundary", n))
            thresholds.append(f"| {n} | {midpoint:.12f} | {float(high-low):.3e} |")

    status = [
        f"PASS: {identity_cases} exact direct-sum / positive-coefficient identities.",
        f"PASS: {bound_cases} exact Turan bounds, including n=0 equality.",
        f"PASS: {value_bound_cases} improved value bounds and strict lower-improvement checks.",
        f"PASS: {regime_cases} ratio and monotonicity-regime configurations.",
        f"PASS: {moment_cases} independently expanded exact simplex moments.",
        f"PASS: {normalization_cases} normalized log-convexity and equality checks.",
        f"PASS: {defect_cases} exact positive-defect identities.",
        "PASS: 1 non-monotone example with a unique peak at r=2.",
        "PASS: 5 exact rational threshold brackets (48 bisection steps each).",
        "OBSERVED: all 5 midpoint approximations lie inside the e-based bounds at 60 digits.",
    ]
    report = [
        "# 계산 기록: 로그 오목성과 단봉성", "", "[연구 노트](note.md)", "",
        "- 연구일: 2026-10-29", f"- 환경: Python {platform.python_version()} ({platform.system()})",
        "- Fraction 정확 산술, 난수 없음. e를 사용하는 마지막 비교만 Decimal 근사 관찰.", "",
        "```powershell", "python research/2026-10-29-turan-unimodality/verify.py", "```", "",
        "```text", *status, "```", "",
        "## 입력 범위", "",
        "n=0..12, a=1/5,1/2,1,6/5,3/2,2,3,8, 직접 합 r=1..25, 이웃 항 경계 r=2..24.",
        "개선된 값의 상하계와 이전 하계 대비 엄격한 개선 여부도 r=1..25 전체에서 확인했다.",
        "비율의 단조성은 각 설정에서 r=1..24를 검산했다. 무한 꼬리에 대한 결론은 노트의 증명에 의존한다.", "",
        "단체 적률: 변수 벡터 (2), (1,1), (1,2), (1/3,1/2,1), (1/7,2/3,5/2,4), 차수 k=0..10.",
        "정규화 부등식 k=1..9. 결손 항등식은 같은 벡터에 x=1/2 또는3을 추가하고 k=1..12에서 확인했다.", "",
        "## 전환 매개변수", "", "아래 소수는 정확한 이분 구간의 중점 근사다. 구간의 양 끝에서는 H_n(a)-1의 부호를 유리수로 확인했다.", "",
        "| n | alpha_n 중점 근사 | 정확 구간 폭의 소수 근사 |", "| --- | --- | --- |", *thresholds, "",
        "e 기반 경계 비교는 엄밀한 구간 산술 인증이 아니다. 해당 경계와 점근식의 근거는 노트 §7의 증명이다.", "",
    ]
    Path(__file__).with_name("results.md").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(status))
    print("WROTE: results.md")


if __name__ == "__main__":
    main()
