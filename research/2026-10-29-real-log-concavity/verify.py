"""Numerical checks for the real-exponent log-concavity note.

Run from the repository root:
    python research/2026-10-29-real-log-concavity/verify.py

Standard library only (decimal, fractions, random). Random seed: 2026.
Real powers are evaluated with decimal at PREC significant digits; the
second derivative of log D is a central difference with step H.  These are
finite numerical observations; the general statements rely on the proofs.
"""

from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations
import math
import random

PREC = 130
H = Decimal("1e-15")
getcontext().prec = PREC
D = Decimal


def dec(x):
    if isinstance(x, Fraction):
        return D(x.numerator) / D(x.denominator)
    return D(x)


def subset_sums(hs):
    """Return (sign, offset) for every subset S of the spacings."""
    out = []
    n = len(hs)
    for k in range(n + 1):
        for S in combinations(range(n), k):
            out.append(((-1) ** k, sum((hs[i] for i in S), Fraction(0))))
    return out


def D_value(a, terms, s):
    """D_h(a,s) = sum_S (-1)^|S| (a + h_S)^(-s), real s, as Decimal."""
    total = D(0)
    for sign, off in terms:
        base = dec(a + off)
        total += sign * (-s * base.ln()).exp()
    return total


def log_curvature(a, terms, s):
    lp = D_value(a, terms, s + H).ln()
    l0 = D_value(a, terms, s).ln()
    lm = D_value(a, terms, s - H).ln()
    return (lp - 2 * l0 + lm) / (H * H)


def trigamma_gap(s, n):
    """psi'(s) - psi'(s+n) = sum_{i<n} 1/(s+i)^2."""
    return sum(1 / (s + i) ** 2 for i in range(n))


def rising(s, n):
    p = D(1)
    for i in range(n):
        p *= s + i
    return p


def check_curvature(cases, s_values):
    """Theorem 2: -sum 1/(s+i)^2 < (log D)'' < 0."""
    count = 0
    worst_upper = None   # largest (log D)'' / gap, must be < 0
    worst_lower = None   # smallest (log D)'' / gap, must be > -1
    for a, hs in cases:
        terms = subset_sums(hs)
        n = len(hs)
        for s in s_values:
            sd = dec(s)
            c = log_curvature(a, terms, sd)
            g = trigamma_gap(sd, n)
            assert -g < c < 0, (a, hs, s, c, g)
            r = c / g
            if worst_upper is None or r > worst_upper[0]:
                worst_upper = (r, a, hs, s)
            if worst_lower is None or r < worst_lower[0]:
                worst_lower = (r, a, hs, s)
            count += 1
    return count, worst_upper, worst_lower


def check_two_point(cases, triples):
    """Corollary 3: 1 < D(s)^2/(D(s-d)D(s+d)) < (s)_n^2/((s-d)_n (s+d)_n)."""
    count = 0
    for a, hs in cases:
        terms = subset_sums(hs)
        n = len(hs)
        for s, d in triples:
            sd, dd = dec(s), dec(d)
            ratio = D_value(a, terms, sd) ** 2 / (
                D_value(a, terms, sd - dd) * D_value(a, terms, sd + dd))
            bound = rising(sd, n) ** 2 / (rising(sd - dd, n) * rising(sd + dd, n))
            assert 1 < ratio < bound, (a, hs, s, d, ratio, bound)
            count += 1
    return count


def exact_integer_bound():
    """delta=1, integer s=r: product bound equals 1 + n/((r-1)(n+r)) exactly."""
    count = 0
    for n in range(1, 13):
        for r in range(2, 25):
            def rf(x):
                p = Fraction(1)
                for i in range(n):
                    p *= x + i
                return p
            prod = rf(Fraction(r)) ** 2 / (rf(Fraction(r - 1)) * rf(Fraction(r + 1)))
            assert prod == 1 + Fraction(n, (r - 1) * (n + r))
            count += 1
    return count


def exact_D(a, hs, r):
    return sum(sign * (a + off) ** (-r) for sign, off in subset_sums(hs))


def real_maximizer(a, terms, lo=D("1e-6"), hi=D(200)):
    """Bisection for (log D)'(s*) = 0, derivative by central difference."""
    def dlog(s):
        return (D_value(a, terms, s + H).ln() - D_value(a, terms, s - H).ln()) / (2 * H)
    if dlog(hi) > 0:
        return None
    for _ in range(120):
        mid = (lo + hi) / 2
        if dlog(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def phi_root(n, target):
    """Root of sum_{i<n} 1/(s+i) = target > 0 by bisection."""
    lo, hi = D("1e-30"), D(10) ** 6
    for _ in range(300):
        mid = (lo + hi) / 2
        if sum(1 / (mid + i) for i in range(n)) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def check_argmax(cases):
    """Corollary 4: for a>1 the integer argmax lies in {floor s*, ceil s*} (with s* >= 1 handling)."""
    rows = []
    for a, hs in cases:
        terms = subset_sums(hs)
        s_star = real_maximizer(a, terms)
        vals = {r: exact_D(a, hs, r) for r in range(1, 400)}
        best = max(vals.values())
        argmax = sorted(r for r, v in vals.items() if v == best)
        lo = max(1, math.floor(s_star))
        hi = max(1, math.ceil(s_star))
        assert set(argmax) <= {lo, hi}, (a, hs, s_star, argmax)
        # Bracket: phi(s) = sum_{i<n} 1/(s+i) is decreasing; phi(s*) lies in
        # (log a, log(a + sum h)), so s_lo < s* < s_hi.
        n = len(hs)
        s_lo = phi_root(n, dec(a + sum(hs)).ln())
        s_hi = phi_root(n, dec(a).ln())
        assert s_lo < s_star < s_hi, (a, hs, s_lo, s_star, s_hi)
        rows.append((a, hs, s_star, argmax, s_lo, s_hi))
    return rows


def fmt(hs):
    return "[" + ",".join(str(h) for h in hs) + "]"


def main():
    F = Fraction
    uniform = [(a, [F(1)] * n)
               for n in (1, 2, 3, 5, 8)
               for a in (F(1, 100), F(1, 10), F(1, 2), F(1), F(3, 2), F(3), F(10), F(100))]
    nonuniform = [(F(1), [F(1), F(2)]), (F(1, 2), [F(1, 3), F(5)]),
                  (F(2), [F(1, 100), F(1), F(7)]), (F(1, 7), [F(2), F(2), F(1, 2), F(9)])]
    rng = random.Random(2026)
    for _ in range(40):
        n = rng.randint(1, 7)
        a = F(rng.randint(1, 400), rng.randint(1, 40))
        hs = [F(rng.randint(1, 300), rng.randint(1, 30)) for _ in range(n)]
        nonuniform.append((a, hs))
    s_values = (F(1, 20), F(3, 10), F(1), F(7, 4), F(3), F(10), F(30))

    c1, up, lowr = check_curvature(uniform, s_values)
    c2, up2, low2 = check_curvature(nonuniform, s_values)
    print(f"[curvature, uniform] {c1} cases PASS: -sum < (log D)'' < 0")
    print(f"[curvature, spacings] {c2} cases PASS (seed 2026, 40 random + 4 fixed)")
    r, a, hs, s = max(up, up2, key=lambda t: t[0])
    print(f"  closest to 0 (a->0 end): (log D)''/gap = {float(r):.6e} at a={a}, h={fmt(hs)}, s={s}")
    r, a, hs, s = min(lowr, low2, key=lambda t: t[0])
    print(f"  closest to -1 (a->oo end): 1 + (log D)''/gap = {float(1 + r):.6e} at a={a}, h={fmt(hs)}, s={s}")

    triples = [(F(1, 2), F(1, 4)), (F(1), F(1, 3)), (F(5, 2), F(2)), (F(4), F(1)), (F(12), F(7, 2))]
    c3 = check_two_point(uniform + nonuniform, triples)
    print(f"[two-point ratio] {c3} cases PASS: 1 < ratio < product bound")

    c4 = exact_integer_bound()
    print(f"[delta=1 exact identity] {c4} (n,r) pairs PASS (Fraction)")

    am_cases = [(F(3, 2), [F(1)]), (F(6, 5), [F(1)] * 3), (F(11, 10), [F(1)] * 8),
                (F(2), [F(1)] * 8), (F(21, 20), [F(1, 2), F(3)]), (F(5, 4), [F(2)] * 4)]
    print("[argmax] a>1: integer argmax within {floor s*, ceil s*}; s_lo < s* < s_hi")
    for a, hs, s_star, argmax, s_lo, s_hi in check_argmax(am_cases):
        print(f"  a={a}, h={fmt(hs)}: s*={float(s_star):.6f} in ({float(s_lo):.4f}, {float(s_hi):.4f}),"
              f" integer argmax={argmax}")

    # Endpoint / n=0 sanity: D = a^{-s} has (log D)'' = 0 exactly (no strictness).
    c0 = log_curvature(F(3), subset_sums([]), D(2))
    print(f"[n=0] (log D)'' = {float(c0):.2e} (expected 0 up to roundoff)")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
