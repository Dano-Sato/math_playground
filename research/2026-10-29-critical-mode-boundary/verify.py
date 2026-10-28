"""Exact checks and explicitly separated Decimal observations. No dependencies."""

from decimal import Decimal as D, localcontext
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import platform


def homogeneous(variables, degree):
    one = variables[0] * 0 + 1
    h = [one] + [one * 0] * degree
    for x in variables:
        for r in range(1, degree + 1):
            h[r] += x * h[r - 1]
    return h


def direct(n, r, a):
    return sum(((-1)**j * comb(n, j) / (a + j)**r for j in range(n + 1)), Q(0))


def ratio(n, r, a):
    h = homogeneous([1 / (a + j) for j in range(n + 1)], r)
    return h[r] / h[r - 1]


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def rational_root(n, k):
    low, high = Q(1), Q(n + 1)
    for _ in range(40):
        mid = (low + high) / 2
        if ratio(n, k, mid) > 1:
            low = mid
        else:
            high = mid
    require(ratio(n, k, low) >= 1 >= ratio(n, k, high), ("exact root bracket", n, k))
    return low, high


def decimal_root(n, k, precision):
    with localcontext() as context:
        context.prec = precision
        low, high = D(1), D(n + 1)
        for _ in range(65):
            mid = (low + high) / 2
            if ratio(n, k, mid) > 1:
                low = mid
            else:
                high = mid
        return (low + high) / 2


def certified_boundary(k):
    # Taylor series and a geometric tail give a rigorous rational enclosure for e.
    order = 18
    e_low = sum((Q(1, factorial(j)) for j in range(order + 1)), Q(0))
    e_high = e_low + Q(1, order * factorial(order))
    theta_low, theta_high = 1 / (e_high**k - 1), 1 / (e_low**k - 1)
    sufficient = (k + 1) / theta_low
    n = sufficient.numerator // sufficient.denominator + 1
    require(Q(n) > (k + 1) / theta_low, ("sufficient n", k))
    # a_low <= a <= a_high; every coefficient is increasing in every x_j.
    a_low, a_high = n * theta_low, n * theta_high
    h_low = homogeneous([1 / (a_high + j) for j in range(n + 1)], k + 1)
    h_high = homogeneous([1 / (a_low + j) for j in range(n + 1)], k + 1)
    require(h_low[k] / h_high[k - 1] > 1, ("certified R_k > 1", k, n))
    require(h_high[k + 1] / h_low[k] < 1, ("certified R_k+1 < 1", k, n))
    return n


def main():
    parameters = [Q(1, 5), Q(1, 2), Q(1), Q(3, 2), Q(2), Q(5)]
    identities = bounds = derivatives = 0
    for n in range(13):
        for a in parameters:
            variables = [1 / (a + j) for j in range(n + 1)]
            h = homogeneous(variables, 13)
            total, maximum = sum(variables), max(variables)
            base = direct(n, 1, a)
            for r in range(1, 13):
                require(direct(n, r + 1, a) == base * h[r], ("sum identity", n, a, r))
                identities += 1
                current, following = h[r] / h[r - 1], h[r + 1] / h[r]
                require(total / r <= current <= (total + (r - 1) * maximum) / r, ("finite ratio bounds", n, a, r))
                bounds += 1
                logarithmic_derivative = r * current - (r + 1) * following
                require(logarithmic_derivative < 0, ("a monotonicity", n, a, r))
                derivatives += 1

    vectors = [[Q(2)], [Q(1), Q(1)], [Q(1, 2), Q(1), Q(3)], [Q(1, 7), Q(2, 3)]]
    equality_cases = 0
    for variables in vectors:
        h = homogeneous(variables, 12)
        total, maximum = sum(variables), max(variables)
        for q in range(1, 13):
            value = h[q] / h[q - 1]
            lower, upper = total / q, (total + (q - 1) * maximum) / q
            require(lower <= value <= upper, ("general ratio bound", variables, q))
            require((value == lower) == (q == 1), ("lower equality", variables, q))
            require((value == upper) == (q == 1 or len(set(variables)) == 1), ("upper equality", variables, q))
            equality_cases += 1

    brackets = 0
    for n in (1, 3, 8):
        previous = None
        for k in range(1, 5):
            low, high = rational_root(n, k)
            require(low > 1, ("root above one", n, k))
            if previous:
                require(high < previous[0], ("threshold order", n, k))
            previous = low, high
            brackets += 1
    certified = [(k, certified_boundary(k)) for k in (1, 2, 3)]

    boundary_rows, root_rows = [], []
    with localcontext() as context:
        context.prec = 80
        for k in range(1, 6):
            theta = 1 / (D(k).exp() - 1)
            beta = theta + D("1.5") - 1 / D(k)
            v = 1 / (theta * (theta + 1))
            threshold = D(k + 1) / theta
            first_n = int(threshold) + 1
            for n in (first_n, 4 * first_n):
                a = theta * n
                h = homogeneous([1 / (a + j) for j in range(n + 1)], k + 1)
                r_left, r_right = h[k] / h[k - 1], h[k + 1] / h[k]
                require(r_left > 1 > r_right, ("decimal boundary", n, k))
                boundary_rows.append(f"| {k} | {n} | {r_left:.10f} | {r_right:.10f} | {n*(r_left-1):.8f} | {v*beta/D(k):.8f} |")
        for k in range(1, 5):
            theta = 1 / (D(k).exp() - 1)
            beta = theta + D("1.5") - 1 / D(k)
            for n in (20, 80, 320):
                root = decimal_root(n, k, 80)
                other = decimal_root(n, k, 50)
                require(abs(root - other) < D("1e-12"), ("precision agreement", n, k))
                offset = root - theta * n
                root_rows.append(f"| {k} | {n} | {offset:.10f} | {beta:.10f} | {n*(offset-beta):.8f} |")

    status = [
        f"PASS: {identities} exact direct-sum / coefficient identities.",
        f"PASS: {bounds} exact finite-size ratio bounds.",
        f"PASS: {derivatives} exact signs in the logarithmic a-derivative identity.",
        f"PASS: {equality_cases} general-variable bound and equality cases.",
        f"PASS: {brackets} rational root brackets and their strict order (40 bisections).",
        "PASS: 3 critical-boundary certificates using rational bounds for e.",
        "OBSERVED: 10 Decimal boundary configurations satisfy R_k > 1 > R_k+1.",
        "OBSERVED: 12 root approximations agree at 50/80 digits within 1e-12.",
    ]
    report = [
        "# 계산 기록: 유한 크기 전환점", "", "[연구 노트](note.md)", "",
        "- 연구일: 2026-10-29", f"- 환경: Python {platform.python_version()} ({platform.system()})",
        "- 표준 라이브러리만 사용. 난수 없음. Fraction 검산과 Decimal 관찰을 구분한다.", "",
        "```powershell", "python research/2026-10-29-critical-mode-boundary/verify.py", "```", "",
        "```text", *status, "```", "",
        "## 정확 검산 범위", "",
        "n=0..12, a=1/5,1/2,1,3/2,2,5, 비율 r=1..12. n=0은 경계 검산용이며 주정리는 n>=1이다.",
        "일반 변수: (2), (1,1), (1/2,1,3), (1/7,2/3), q=1..12.",
        "전환점 유리수 구간: n=1,3,8, k=1..4, 각 40회 이분법.", "",
        "## 초월수 경계의 유리수 인증", "",
        "e의 Taylor 합 S18과 S18+1/(18*18!)로 e의 엄밀한 구간을 얻었다.",
        "이 구간으로 각 x_j 및 양수 계수 h_q를 양쪽에서 끼웠다. 분자와 분모를 반대쪽 끝값으로 나누어도 두 비율이 1의 어느 쪽인지 결정된다.", "",
        "| k | 인증된 n | 결론 |", "| --- | --- | --- |",
        *(f"| {k} | {n} | R_k > 1 > R_(k+1), 유일한 최대 지수 k+1 |" for k, n in certified), "",
        "## 경계 비율의 근사 관찰", "",
        "아래 표는 80자리 Decimal 계산이다. k=4,5는 유리수 인증을 수행하지 않았으며, 일반 결론은 본문 증명에 의존한다.", "",
        "| k | n | R_k | R_(k+1) | n(R_k-1) | 예측 극한 v_k beta_k/k |", "| --- | --- | --- | --- | --- | --- |", *boundary_rows, "",
        "## 전환점의 상수 보정", "",
        "65회 Decimal 이분법. 50자리와 80자리의 일치는 엄밀한 구간 인증이 아니다. 마지막 열이 유계로 보이는 것은 O(1/n) 예측을 뒷받침하는 관찰이다.", "",
        "| k | n | a_(n,k)-theta_k n | 예측 beta_k | n(관측 보정-beta_k) |", "| --- | --- | --- | --- | --- |", *root_rows, "",
    ]
    Path(__file__).with_name("results.md").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(status))
    print("WROTE: results.md")


if __name__ == "__main__":
    main()
