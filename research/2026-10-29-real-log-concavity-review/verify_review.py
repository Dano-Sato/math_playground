"""Independent spot checks for research/2026-10-29-real-log-concavity/note.md (v1).

Run from the repository root:
    python research/2026-10-29-real-log-concavity-review/verify_review.py

Python 3 standard library only (decimal, fractions, math, random).
Random seed: 20261029 (random nodes / spacings).  Writes no files.

Methods deliberately differ from the author's verify.py:
  [A] (log D)'' from the closed-form sums D, D', D'' (no finite differences),
      Decimal with PREC (=60) digits; reduced grid for a ~30 s runtime cap.
  [B] (log D)'' = -sum 1/(s+i)^2 + Var_s(log Y), the tilted variance computed by
      composite Gauss-Legendre quadrature against the box-spline density of
      Y = a + sum h_i T_i (float).  Cross-checks [A] and the decomposition in Thm 2.
  [C] Lemma A tested directly on non-integer m with several root-concave f,
      against psi'(s) - psi'(s+m+1) (trigamma by recurrence + asymptotics).
  [D] Corollary 3 near delta -> s, [E] Corollary 4 incl. s* < 1 and floor cases,
  [F] Section 8 identity F = n!/(a)_{n+1} [x_0..x_n] z^{s+n-1} (exact for integer s)
      and log-concavity of divided differences at random nodes.
These are finite numerical observations, not proofs.
"""

from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations
from math import comb, factorial
import math
import random

PREC = 60
getcontext().prec = PREC
Dc = Decimal
SEED = 20261029


def dec(x):
    if isinstance(x, Fraction):
        return Dc(x.numerator) / Dc(x.denominator)
    return Dc(str(x)) if isinstance(x, float) else Dc(x)


# ---------------------------------------------------------------- [A] closed form
def terms_general(a, hs):
    out = []
    n = len(hs)
    for k in range(n + 1):
        for S in combinations(range(n), k):
            out.append(((-1) ** k, dec(a) + sum((dec(hs[i]) for i in S), Dc(0))))
    return out


def terms_uniform(a, n):
    return [((-1) ** j * comb(n, j), dec(a) + j) for j in range(n + 1)]


def curvature_A(terms, s):
    """Return (D, (log D)', (log D)'') from exact derivative sums.

    Internally bases are divided by the smallest base a (E = a^s D), which leaves
    (log D)'' unchanged and avoids cancellation when q = a/(a+h) is tiny.
    """
    s = dec(s)
    b0 = min(b for _, b in terms)
    D0 = D1 = D2 = Dc(0)
    for c, b in terms:
        lb = (b / b0).ln()
        v = c * (-s * lb).exp()
        D0 += v
        D1 -= lb * v
        D2 += lb * lb * v
    lb0 = b0.ln()
    return D0 * (-s * lb0).exp(), D1 / D0 - lb0, D2 / D0 - (D1 / D0) ** 2


def gap(s, n):
    s = dec(s)
    return sum(1 / (s + i) ** 2 for i in range(n))


# ---------------------------------------------------------------- [B] quadrature
def gauss_legendre(N):
    xs, ws = [], []
    for i in range(1, N + 1):
        x = math.cos(math.pi * (i - 0.25) / (N + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, N + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = N * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


GLX, GLW = gauss_legendre(40)


def integrate(func, lo, hi, panels=8):
    total = 0.0
    step = (hi - lo) / panels
    for k in range(panels):
        u, v = lo + k * step, lo + (k + 1) * step
        m, r = (u + v) / 2, (v - u) / 2
        total += r * sum(w * func(m + r * x) for x, w in zip(GLX, GLW))
    return total


def curvature_B(a, hs, s):
    """-sum 1/(s+i)^2 + Var of log Y under density ~ y^{-s-n} p(y)."""
    n = len(hs)
    offs = []
    for k in range(n + 1):
        for S in combinations(range(n), k):
            offs.append(((-1) ** k, a + sum(hs[i] for i in S)))
    bps = sorted(set(b for _, b in offs))
    norm = 1.0 / (math.prod(hs) * factorial(n - 1))

    def p(y):
        tot = 0.0
        for c, b in offs:
            if y > b:
                tot += c * (y - b) ** (n - 1)
        return tot * norm

    mom = [0.0, 0.0, 0.0]
    for u, v in zip(bps, bps[1:]):
        for j in range(3):
            mom[j] += integrate(lambda y, j=j: y ** (-s - n) * math.log(y) ** j * p(y), u, v)
    var = mom[2] / mom[0] - (mom[1] / mom[0]) ** 2
    return -sum(1 / (s + i) ** 2 for i in range(n)) + var


# ---------------------------------------------------------------- [C] Lemma A
def trigamma(x):
    acc = 0.0
    while x < 30:
        acc += 1 / (x * x)
        x += 1
    acc += 1 / x + 1 / (2 * x ** 2) + 1 / (6 * x ** 3) - 1 / (30 * x ** 5) + 1 / (42 * x ** 7) - 1 / (30 * x ** 9)
    return acc


def logM_curv(f, c, d, s, panels=400):
    # graded split near both endpoints to handle (t-c)^m behaviour
    pts = [c + (d - c) * (k / panels) ** 1 for k in range(panels + 1)]
    mom = [0.0, 0.0, 0.0]
    for u, v in zip(pts, pts[1:]):
        m_, r = (u + v) / 2, (v - u) / 2
        for x, w in zip(GLX, GLW):
            t = m_ + r * x
            base = r * w * t ** (s - 1) * f(t)
            lt = math.log(t)
            mom[0] += base
            mom[1] += base * lt
            mom[2] += base * lt * lt
    return mom[2] / mom[0] - (mom[1] / mom[0]) ** 2


# ---------------------------------------------------------------- helpers
def rising(x, n):
    p = x * 0 + 1
    for i in range(n):
        p *= x + i
    return p


def divided_difference(xs, g):
    """Recursive divided difference table (exact for Fraction / Decimal)."""
    col = [g(x) for x in xs]
    n = len(xs)
    for k in range(1, n):
        col = [(col[i + 1] - col[i]) / (xs[i + k] - xs[i]) for i in range(n - k)]
    return col[0]


def main():
    F = Fraction
    rng = random.Random(SEED)

    # [A] new parameters, edge cases
    cases = []
    # a^s D ~ (s)_n a^{-n} for large a while single terms are ~ binom(n, n/2):
    # the a-range for large n is limited so that PREC digits suffice.
    # Reduced scope (runtime cap ~30 s requested by coordinator): n <= 6, PREC 60.
    for n in (1, 2, 4, 6):
        for a in (F(1, 10 ** 12), F(1, 1000), F(7, 3), F(1000)):
            cases.append(("uniform", n, a, None))
    extreme = [(F(1, 10 ** 9), [F(1, 10 ** 8), F(10 ** 8)]),
               (F(10 ** 3), [F(1, 10 ** 8), F(10 ** 8)]),
               (F(1), [F(1, 10 ** 6)] * 3 + [F(10 ** 6)]),
               (F(1, 3), [F(10 ** 4), F(1, 10 ** 4), F(1), F(2), F(3), F(5)])]
    for _ in range(8):
        n = rng.randint(2, 6)
        a = F(rng.randint(1, 10 ** 4), rng.randint(1, 10 ** 4))
        hs = [F(rng.randint(1, 10 ** 4), rng.randint(1, 10 ** 3)) for _ in range(n)]
        extreme.append((a, hs))
    for a, hs in extreme:
        cases.append(("general", len(hs), a, hs))
    s_vals = (F(1, 10 ** 6), F(1, 3), F(5, 2), F(41), F(300))
    cnt, rmax, rmin = 0, None, None
    for kind, n, a, hs in cases:
        terms = terms_uniform(a, n) if kind == "uniform" else terms_general(a, hs)
        for s in s_vals:
            D0, L1, L2 = curvature_A(terms, s)
            g = gap(s, n)
            assert D0 > 0, (kind, n, a, s)
            assert -g < L2 < 0, (kind, n, a, hs, s, L2, g)
            r = L2 / g
            rmax = r if rmax is None or r > rmax else rmax
            rmin = r if rmin is None or r < rmin else rmin
            cnt += 1
    print(f"[A] closed-form (log D)'': {cnt} points PASS -gap < (log D)'' < 0 "
          f"(n<=6, a in [1e-12,1e3], s in [1e-6,300], extreme spacings, PREC 60)")
    print(f"    ratio (log D)''/gap range: max {rmax:.3e}, 1 + min {(1 + rmin):.3e}")

    # Sharpness trends at fixed n, h, s.
    print("    sharpness trend, uniform n=3, s=1/3: a -> ratio")
    for a in (F(1, 10 ** 12), F(1, 10 ** 6), F(1), F(10 ** 3), F(10 ** 6)):
        _, _, L2 = curvature_A(terms_uniform(a, 3), F(1, 3))
        print(f"      a={float(a):.0e}: {float(L2 / gap(F(1, 3), 3)):.12f}")

    # [B] cross-check with quadrature (float), n <= 4
    worst = 0.0
    nb = 0
    for a, hs in [(0.5, [1.0]), (2.0, [1.0, 1.0]), (0.3, [0.2, 1.7]), (1.5, [1.0, 2.0, 0.5]),
                  (0.05, [1.0, 1.0, 1.0, 1.0]), (7.0, [3.0, 0.1, 2.0, 5.0])]:
        for s in (0.01, 0.5, 2.0, 9.0):
            fa = [F(x).limit_denominator(10 ** 6) for x in hs]
            _, _, LA = curvature_A(terms_general(F(a).limit_denominator(10 ** 6), fa), F(s).limit_denominator(10 ** 6))
            LB = curvature_B(a, hs, s)
            rel = abs(float(LA) - LB) / float(gap(F(s).limit_denominator(10 ** 6), len(hs)))
            worst = max(worst, rel)
            nb += 1
    assert worst < 1e-10, worst
    print(f"[B] tilted-variance quadrature vs closed form: {nb} points, max abs diff / gap {worst:.2e} PASS")

    # n=1 closed form of Section 5
    worst = 0.0
    for a, h, s in [(F(1, 7), F(3), F(1, 5)), (F(9), F(1, 9), F(4)), (F(1, 10 ** 6), F(1), F(2))]:
        _, _, LA = curvature_A(terms_general(a, [h]), s)
        kap = (dec(a + h) / dec(a)).ln()
        x = (kap * dec(s))
        closed = -kap * kap * x.exp() / (x.exp() - 1) ** 2
        worst = max(worst, float(abs(LA - closed) / abs(closed)))
    assert worst < 1e-40
    print(f"[A'] n=1 formula -k^2 e^(ks)/(e^(ks)-1)^2 matches, max rel. diff {worst:.1e} PASS")

    # [C] Lemma A for non-integer m
    nc = 0
    tests = []
    for m in (0.5, 1.3, 2.7):
        for (c, d) in ((0.2, 1.0), (1.0, 5.0), (3.0, 3.5)):
            tests += [(m, c, d, "((t-c)(d-t))^m", lambda t, m=m, c=c, d=d: ((t - c) * (d - t)) ** m),
                      (m, c, d, "(d-t)^m", lambda t, m=m, c=c, d=d: (d - t) ** m),
                      (m, c, d, "(t-c)^m", lambda t, m=m, c=c, d=d: (t - c) ** m),
                      (m, c, d, "const", lambda t: 1.0)]
    min_margin = None
    for m, c, d, name, f in tests:
        for s in (0.05, 1.0, 6.0):
            lhs = logM_curv(f, c, d, s)
            rhs = trigamma(s) - trigamma(s + m + 1)
            assert 0 < lhs < rhs, (m, c, d, name, s, lhs, rhs)
            mg = (rhs - lhs) / rhs
            min_margin = mg if min_margin is None or mg < min_margin else min_margin
            nc += 1
    print(f"[C] Lemma A, m in {{0.5,1.3,2.7}}: {nc} tests PASS 0 < (log M_f)'' < psi'(s)-psi'(s+m+1); "
          f"min relative margin {min_margin:.3e}")
    # c -> 0 with f = (d-t)^m approaches equality (boundary remark)
    lhs = logM_curv(lambda t: (1.0 - t) ** 2.7, 1e-9, 1.0, 1.0, panels=2000)
    rhs = trigamma(1.0) - trigamma(4.7)
    print(f"    boundary c=1e-9, f=(1-t)^2.7, s=1: (log M)''/rhs = {lhs / rhs:.6f} (-> 1 as c -> 0)")

    # [D] Corollary 3 incl. delta close to s
    nd = 0
    for a, hs in [(F(1, 50), [F(1)] * 2), (F(40), [F(1), F(3), F(1, 9)]), (F(3, 2), [F(2)] * 5)]:
        terms = terms_general(a, hs)
        n = len(hs)
        for s, dl in [(F(1, 1000), F(999, 1000000)), (F(3), F(2999, 1000)), (F(7, 2), F(1, 10 ** 6)),
                      (F(20), F(19)), (F(5), F(1))]:
            sd, dd = dec(s), dec(dl)
            Dv = lambda x: curvature_A(terms, x)[0]
            ratio = Dv(sd) ** 2 / (Dv(sd - dd) * Dv(sd + dd))
            bound = rising(sd, n) ** 2 / (rising(sd - dd, n) * rising(sd + dd, n))
            assert 1 < ratio < bound, (a, hs, s, dl)
            nd += 1
    print(f"[D] Corollary 3: {nd} cases PASS incl. delta/s = 0.999 and 0.9997")

    # [E] Corollary 4
    # s* < 1 example: n=1, h=1, a=3: L'(1) = kappa*a - log a < 0, integer argmax must be 1
    a = F(3)
    vals = [a ** -r - (a + 1) ** -r for r in range(1, 30)]
    assert vals.index(max(vals)) == 0
    _, L1, _ = curvature_A(terms_general(a, [F(1)]), 1)
    assert L1 < 0
    print(f"[E] s*<1 example n=1,h=1,a=3: L'(1)={float(L1):.4f}<0 and exact integer argmax r=1 PASS")

    def s_star(terms):
        lo, hi = Dc("1e-12"), Dc(2000)
        for _ in range(60):
            mid = (lo + hi) / 2
            if curvature_A(terms, mid)[1] > 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    getcontext().prec = 40
    floor_hits, ceil_hits, total = 0, 0, 0
    example_floor = None
    for n in (1, 2, 3):
        for a in [F(k, 4) for k in range(5, 25, 2)]:
            hs = [F(1)] * n
            terms = terms_general(a, hs)
            st = s_star(terms)
            ex = {r: sum(((-1) ** len(S)) * (a + sum(hs[i] for i in S)) ** (-r)
                         for k in range(n + 1) for S in combinations(range(n), k))
                  for r in range(1, 60)}
            best = max(ex.values())
            arg = [r for r, v in ex.items() if v == best]
            fl, ce = max(1, math.floor(st)), max(1, math.ceil(st))
            assert set(arg) <= {fl, ce}, (n, a, float(st), arg)
            total += 1
            if st >= 1 and arg == [math.floor(st)] and math.floor(st) != math.ceil(st):
                floor_hits += 1
                example_floor = example_floor or (n, a, float(st), arg)
            elif st >= 1:
                ceil_hits += 1
    getcontext().prec = PREC
    print(f"[E] {total} uniform cases (n<=3, a=5/4,7/4,..,23/4): integer argmax in {{floor,ceil}}(s*) PASS; "
          f"floor-only {floor_hits}, ceil/other {ceil_hits}; floor example {example_floor}")
    # a = 1: strictly increasing
    t1 = terms_uniform(F(1), 4)
    assert all(curvature_A(t1, s)[1] > 0 for s in (F(1, 100), F(1), F(10), F(200)))
    print("[E] a=1, n=4: L'(s) > 0 at s in {0.01,1,10,200} PASS")

    # [F] Section 8
    nf = 0
    for n in range(1, 7):
        for a in (F(1, 3), F(2), F(17, 5)):
            xs = [1 / (a + j) for j in range(n + 1)]
            b = F(factorial(n)) / rising(a, n + 1)
            for r in range(1, 7):
                Fv = sum((-1) ** j * comb(n, j) * (a + j) ** (-r) for j in range(n + 1))
                dd = divided_difference(xs, lambda z: z ** (r + n - 1))
                assert Fv == b * dd
                nf += 1
    # real s in Decimal
    for n, a, s in [(3, F(1, 3), F(1, 7)), (5, F(2), F(9, 4))]:
        xs = [1 / dec(a + j) for j in range(n + 1)]
        b = dec(F(factorial(n))) / rising(dec(a), n + 1)
        q = dec(s) + n - 1
        dd = divided_difference(xs, lambda z: (z.ln() * q).exp())
        Fv = curvature_A(terms_uniform(a, n), s)[0]
        assert abs(Fv - b * dd) / Fv < Dc("1e-40")
        nf += 1
    print(f"[F] F = n!/(a)_(n+1) * [x_0..x_n] z^(s+n-1), x_j=1/(a+j): {nf} checks PASS "
          f"(exact Fraction for integer s, Decimal for 2 real s)")
    # log-concavity in p of divided differences at random distinct nodes, p > n-1
    getcontext().prec = 60
    ng = 0
    Hs = Dc("1e-15")
    for _ in range(30):
        n = rng.randint(1, 6)
        xs = sorted(set(dec(F(rng.randint(1, 10 ** 3), rng.randint(1, 10 ** 2))) for _ in range(n + 1)))
        if len(xs) != n + 1:
            continue
        for eps in (Dc("1e-3"), Dc("0.5"), Dc(7)):
            p = n - 1 + eps
            vals = [divided_difference(xs, lambda z, q=q: (z.ln() * q).exp()) for q in (p - Hs, p, p + Hs)]
            assert all(v > 0 for v in vals)
            c2 = (vals[0].ln() - 2 * vals[1].ln() + vals[2].ln()) / (Hs * Hs)
            assert c2 < 0, (xs, p, c2)
            ng += 1
    # n=0 is not strictly log-concave (log x_0^p is linear)
    print(f"[F] divided differences: {ng} random (nodes, p) with p in n-1+{{1e-3,0.5,7}}, n=1..6: "
          f"(log [x]z^p)'' < 0 PASS (seed {SEED}); (n=0 not tested: log x_0^p is linear in p, so no strictness)")
    getcontext().prec = PREC
    print("ALL REVIEW CHECKS PASSED. No files written.")


if __name__ == "__main__":
    main()
