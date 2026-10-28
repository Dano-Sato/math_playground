"""Checks for the proportional-regime maximizer note.

Run from the repository root:
    python research/2026-10-29-proportional-argmax/verify.py

Standard library only (decimal, fractions, math). No randomness.
F_n(s) = sum_j (-1)^j C(n,j) (a+j)^(-s) with a = theta*n.
Real-exponent values use decimal with precision scaled to the cancellation
size; integer exponents use exact Fractions.  Finite checks are observations.
"""

from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb, exp, factorial, floor, log


def digamma(x):
    """psi(x) for x > 0, float: recurrence to x >= 10, then asymptotic series."""
    acc = 0.0
    while x < 10:
        acc -= 1 / x
        x += 1
    x2 = 1 / (x * x)
    return acc + log(x) - 0.5 / x - x2 * (1 / 12 - x2 * (1 / 120 - x2 * (1 / 252 - x2 / 240)))


def trigamma(x):
    acc = 0.0
    while x < 10:
        acc += 1 / (x * x)
        x += 1
    x2 = 1 / (x * x)
    return acc + 1 / x + 0.5 * x2 + x2 / x * (1 / 6 - x2 * (1 / 30 - x2 / 42))


def bisect(f, lo, hi, it=200):
    for _ in range(it):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def limits(theta):
    """t0, s_inf, c(theta) from the note (float)."""
    t0 = log(1 + 1 / theta)
    s_inf = bisect(lambda s: log(t0) - digamma(s), 1e-12, 200.0)
    c = ((2 * s_inf - 3) + (2 * theta + 1) * t0) / (
        2 * theta * (theta + 1) * t0 ** 2 * trigamma(s_inf))
    return t0, s_inf, c


def real_maximizer(n, theta):
    """s* with L'(s*) = 0, L' = -sum T_j log(a+j) / sum T_j (decimal)."""
    nats = n * (log(2) + (theta + 1) * log(theta + 1) - theta * log(theta))
    getcontext().prec = int(nats / log(10)) + 60
    a = Decimal(theta) * n if isinstance(theta, int) else Decimal(repr(theta)) * n
    logs = [(a + j).ln() for j in range(n + 1)]
    coef = [(-1) ** j * comb(n, j) for j in range(n + 1)]

    def dlog(s):
        sd = Decimal(repr(s))
        T = [c * (-sd * lg).exp() for c, lg in zip(coef, logs)]
        return -sum(t * lg for t, lg in zip(T, logs)) / sum(T)

    # Bracket then secant-safeguarded bisection on float s.
    lo, hi = 1e-9, 60.0
    for _ in range(70):
        mid = (lo + hi) / 2
        if dlog(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def check_real_maximizer():
    print("[real maximizer] s*(n, theta n) vs s_inf + c/n")
    rows = []
    for theta in (0.1, 0.5, 1.0, 3.0):
        t0, s_inf, c = limits(theta)
        prev = None
        line = []
        for n in (25, 50, 100, 200):
            s = real_maximizer(n, theta)
            resid = n * (s - s_inf) - c        # expected O(1/n)
            line.append((n, s, n * (s - s_inf), resid))
            if prev is not None:
                assert abs(resid) < abs(prev) * 0.75, (theta, n, resid, prev)
            prev = resid
        rows.append((theta, t0, s_inf, c, line))
        print(f"  theta={theta}: t0={t0:.6f}, s_inf={s_inf:.6f}, c={c:.5f}")
        for n, s, ns, r in line:
            print(f"    n={n:4d}: s*={s:.6f}, n(s*-s_inf)={ns:.5f}, n(s*-s_inf)-c={r:+.5f}")
    return rows


def exact_values(n, a, rmax):
    return [sum(Fraction((-1) ** j * comb(n, j)) / (a + j) ** r for j in range(n + 1))
            for r in range(1, rmax + 1)]


def check_integer_argmax_and_profile():
    print("[integer argmax / Poisson profile] exact Fractions, a = theta n")
    for theta in (Fraction(1, 30), Fraction(1, 10), Fraction(1, 2), Fraction(1), Fraction(3)):
        t0 = log(1 + 1 / float(theta))
        r0 = floor(t0) + 1
        for n in (200, 400):
            a = theta * n
            vals = exact_values(n, a, max(r0 + 4, 6))
            # D_n(1) closed form: n!/(a(a+1)...(a+n)) = B(a, n+1)
            prod = Fraction(1)
            for k in range(n + 1):
                prod *= a + k
            assert vals[0] == Fraction(factorial(n)) / prod
            best = max(range(len(vals)), key=lambda i: vals[i]) + 1
            assert best == r0, (theta, n, best, r0)
            prof = [float(v / vals[0]) for v in vals[:5]]
            pois = [t0 ** (r - 1) / factorial(r - 1) for r in range(1, 6)]
            err = max(abs(p / q - 1) for p, q in zip(prof, pois))
            print(f"  theta={theta}, n={n}: integer argmax={best} (= floor(t0)+1, t0={t0:.4f}),"
                  f" max rel. profile error r<=5: {err:.2e}")


def check_threshold_consistency():
    """t0 = 1  <=>  theta = 1/(e-1): matches the earlier alpha_n/n -> 1/(e-1)."""
    theta = 1 / (exp(1) - 1)
    t0 = log(1 + 1 / theta)
    assert abs(t0 - 1) < 1e-12
    print(f"[threshold] theta=1/(e-1) gives t0={t0:.12f} (D_2 = D_1 boundary in the limit)")


def main():
    check_threshold_consistency()
    check_real_maximizer()
    check_integer_argmax_and_profile()
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
