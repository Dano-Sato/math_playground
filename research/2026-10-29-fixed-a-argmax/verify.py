"""Checks for the fixed-a maximizer note.

Run from the repository root:
    python research/2026-10-29-fixed-a-argmax/verify.py

Standard library only (math, fractions). No randomness. About 10 seconds.
F_n(s) = sum_j (-1)^j C(n,j) (a+j)^(-s)
       = Gamma(s)^(-1) * int_0^oo t^(s-1) e^(-a t) (1-e^(-t))^n dt.
The integral has no cancellation, so composite Simpson in floats (log-scaled)
is used for large n; it is validated against exact Fractions for small n.
Finite checks are observations; the general statements rely on the proofs.
"""

from fractions import Fraction
from math import comb, exp, floor, lgamma, log, log1p


def digamma(x):
    acc = 0.0
    while x < 10:
        acc -= 1 / x
        x += 1
    x2 = 1 / (x * x)
    return acc + log(x) - 0.5 / x - x2 * (1 / 12 - x2 * (1 / 120 - x2 * (1 / 252 - x2 / 240)))


def polygamma(k, x):
    """psi^(k)(x) for k = 1, 2 by recurrence + asymptotic series."""
    acc = 0.0
    while x < 15:
        acc += (1 if k == 1 else -2) / x ** (k + 1)
        x += 1
    if k == 1:
        return acc + 1 / x + 1 / (2 * x * x) + 1 / (6 * x ** 3) - 1 / (30 * x ** 5) + 1 / (42 * x ** 7)
    return acc - 1 / x ** 2 - 1 / x ** 3 - 1 / (2 * x ** 4) + 1 / (6 * x ** 6) - 1 / (6 * x ** 8)


def kappa_delta(a):
    b = a - 1
    return 0.5 - digamma(b), -polygamma(1, b) + polygamma(2, b) / 2 - 1 / 24


def simpson_moments(n, a, s, N=20000):
    """Return (log of int t^(s-1) e^(-at)(1-e^(-t))^n dt, E[log T])."""
    lo, hi = 1e-9, log(n) + 80
    h = (hi - lo) / N
    ts = [lo + i * h for i in range(N + 1)]
    lws = [(s - 1) * log(t) - a * t + n * log1p(-exp(-t)) for t in ts]
    m = max(lws)
    Z = M = 0.0
    for i, (t, lw) in enumerate(zip(ts, lws)):
        c = 1 if i in (0, N) else (4 if i % 2 else 2)
        w = c * exp(lw - m)
        Z += w
        M += w * log(t)
    return log(Z * h / 3) + m, M / Z


def logF(n, a, s):
    return simpson_moments(n, a, s)[0] - lgamma(s)


def dlogF(n, a, s):
    return simpson_moments(n, a, s, 4000)[1] - digamma(s)


def real_max(n, a):
    lo, hi = 0.05, log(n) + 60
    for _ in range(60):
        mid = (lo + hi) / 2
        if dlogF(n, a, mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def check_quadrature():
    worst = 0.0
    for n in (50, 120):
        for a in (Fraction(3, 2), Fraction(2), Fraction(5)):
            for r in range(1, 13):
                exact = sum(Fraction((-1) ** j * comb(n, j)) / (a + j) ** r for j in range(n + 1))
                err = abs(logF(n, float(a), r) - log(exact))
                worst = max(worst, err)
                assert err < 1e-9, (n, a, r, err)
    print(f"[quadrature] Simpson log F vs exact Fraction sum, 72 cases: max |error| = {worst:.1e}")


def check_real_max():
    print("[real maximizer] s* vs log n + kappa (+ delta/log n)")
    for a in (1.5, 2.0, 3.0, 5.0):
        k, d = kappa_delta(a)
        print(f"  a={a}: kappa={k:.5f}, delta={d:.4f}")
        prev = prev2 = None
        for e in (2, 4, 6, 9, 12, 16):
            n = 10 ** e
            lam = log(n)
            s = real_max(n, a)
            r1 = s - lam - k
            r2 = lam * r1 - d
            print(f"    n=1e{e:<2d}: s*={s:.5f}, s*-log n-kappa={r1:+.5f},"
                  f" log n*(..)={lam * r1:+.4f}, minus delta={r2:+.4f}")
            if prev is not None:
                assert abs(r1) < abs(prev), (a, e)
                if a >= 3:
                    assert abs(r2) < abs(prev2), (a, e)
            prev, prev2 = r1, r2


def check_integer_argmax():
    print("[integer argmax] nearest integer to s* and to log n + kappa")
    agree_kappa = total = 0
    for a in (2.0, 3.0, 5.0):
        k, _ = kappa_delta(a)
        for e in range(3, 17):
            n = 10 ** e
            s = real_max(n, a)
            cand = range(max(1, floor(s) - 2), floor(s) + 4)
            best = max(cand, key=lambda r: logF(n, a, r))
            assert best in (floor(s), floor(s) + 1), (a, e, s, best)
            if abs(s - floor(s) - 0.5) > 0.05:
                assert best == round(s), (a, e, s, best)
            total += 1
            agree_kappa += best == round(log(n) + k)
    print(f"  42 settings: argmax in {{floor s*, ceil s*}} and = round(s*) away from half-integers: PASS")
    print(f"  argmax = round(log n + kappa) in {agree_kappa}/{total} settings (o(1) offset can flip near half-integers)")


def main():
    check_quadrature()
    check_real_max()
    check_integer_argmax()
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
