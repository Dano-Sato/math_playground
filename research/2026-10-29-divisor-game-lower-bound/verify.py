"""Generic proof checker for the lower-bound divisor game.

Game G_c: from n move to n - d with d | n and c <= d < n.  Write n = 2^k o.
Claim shape (for c in NICE): there is M with g(2^k o) = k for all o > M, and
each column o <= M is, from some K0 on, periodic in k with period p: in each
residue class either g = k + a (shift) or g = b (constant).

For each c the script
  [A] brute-forces g for n <= N and reports the exception set;
  [F] fits M, K0, p and the column patterns from the data;
  [B] checks the inductive step for every column o <= M and every k in
      [K*, K* + 3p) with option values from the claimed formula, and that the
      signature of the top-range options is p-periodic (this, with the
      argument in the note, gives all k >= K*);
  [C] checks the large-odd-part case: no move with j = k from 2^k o (o > M)
      can reach value k (finite enumeration plus the constant-pattern test);
  [X] (observation only) for c in WILD prints the largest exceptional odd part.

Run from the repository root:
    python research/2026-10-29-divisor-game-lower-bound/verify.py
Standard library only, no randomness, about a minute.
"""

N = 1 << 20
NICE = (2, 3, 5, 8)
WILD = (4, 6, 7, 9, 10)

spf = list(range(N + 1))
for p_ in range(2, int(N ** 0.5) + 1):
    if spf[p_] == p_:
        for m_ in range(p_ * p_, N + 1, p_):
            if spf[m_] == m_:
                spf[m_] = p_


def divisors(n):
    fs = {}
    while n > 1:
        q = spf[n]
        fs[q] = fs.get(q, 0) + 1
        n //= q
    ds = [1]
    for q, a in fs.items():
        ds = [d * q ** i for d in ds for i in range(a + 1)]
    return ds


def split(n):
    k = (n & -n).bit_length() - 1
    return k, n >> k


def mex(s):
    v = 0
    while v in s:
        v += 1
    return v


def brute(c):
    g = [0] * (N + 1)
    for n in range(2, N + 1):
        g[n] = mex({g[n - d] for d in divisors(n) if c <= d < n})
    return g


def odd_divisors(o):
    return [e for e in range(1, o + 1, 2) if o % e == 0]


class Model:
    def __init__(self, c, g):
        self.c = c
        exc = {}
        for n in range(1, N + 1):
            k, o = split(n)
            if g[n] != k:
                exc.setdefault(o, []).append(k)
        self.M = max(max(exc), c - 1)
        self.table = {}
        cols = [o for o in range(1, self.M + 1, 2)]
        for p in (1, 2, 3, 4, 6):
            for K0 in range(1, 12):
                pat = self.fit(g, cols, p, K0)
                if pat is not None:
                    self.p, self.K0, self.pat = p, K0, pat
                    for o in cols:
                        for k in range(K0):
                            self.table[(k, o)] = g[(1 << k) * o]
                    return
        raise AssertionError(f"c={c}: no periodic pattern found")

    @staticmethod
    def fit(g, cols, p, K0):
        pat = {}
        for o in cols:
            ks = [k for k in range(K0, 40) if (1 << k) * o <= N]
            if len(ks) < 2 * p + 2:
                return None
            for r in range(p):
                vals = [(k, g[(1 << k) * o]) for k in ks if k % p == r]
                if all(v - k == vals[0][1] - vals[0][0] for k, v in vals):
                    pat[(o, r)] = ('shift', vals[0][1] - vals[0][0])
                elif all(v == vals[0][1] for k, v in vals):
                    pat[(o, r)] = ('const', vals[0][1])
                else:
                    return None
        return pat

    def G(self, k, o):
        if o > self.M:
            return k
        if k < self.K0:
            return self.table[(k, o)]
        kind, a = self.pat[(o, k % self.p)]
        return k + a if kind == 'shift' else a

    def options(self, k, o):
        out = []
        for j in range(k + 1):
            for e in odd_divisors(o):
                d = (1 << j) * e
                if d < self.c or (j, e) == (k, o):
                    continue
                if j < k:
                    out.append((j, (o << (k - j)) - e))
                else:
                    v, r = split(o // e - 1)
                    out.append((k + v, e * r))
        return out


def check(c, g):
    m = Model(c, g)
    bad = [n for n in range(1, N + 1) if g[n] != m.G(*split(n))]
    assert not bad, (c, bad[:5])
    W = (m.M + 1).bit_length() + 1           # low options (j <= k-W) have q > M
    consts = [a for kind, a in m.pat.values() if kind == 'const'] + [0]
    Kstar = max(m.K0 + W, max(consts) + W + 2, 12)
    # brute force must cover every column below K* (base of the induction)
    assert all((1 << (Kstar - 1)) * o <= N for o in range(1, m.M + 1, 2)), (c, Kstar)
    for k in range(Kstar, Kstar + 3 * m.p):
        for o in range(1, m.M + 1, 2):
            ops = m.options(k, o)
            for v, q in ops:
                if v <= k - W:
                    assert q > m.M
            assert mex({m.G(v, q) for v, q in ops}) == m.G(k, o), (c, k, o)
    sig = lambda k, o: sorted(
        (v - k, ('c', m.G(v, q)) if (q <= m.M and m.pat.get((q, v % m.p), ('', 0))[0] == 'const')
         else ('s', m.G(v, q) - k)) for v, q in m.options(k, o) if v > k - W)
    for k in range(Kstar, Kstar + m.p):
        for o in range(1, m.M + 1, 2):
            assert sig(k, o) == sig(k + m.p, o), (c, k, o)
    # [C] large odd part, j = k moves landing in a column o' = e r <= M.
    shapes = 0
    for oo in range(1, m.M + 1, 2):
        for e in odd_divisors(oo):
            r = oo // e
            for k in range(0, Kstar + 3 * m.p):
                for t in range(1, Kstar + 3 * m.p):
                    o = e * (1 + (r << t))
                    if o <= m.M or (1 << k) * e < m.c:
                        continue
                    shapes += 1
                    assert m.G(k + t, oo) != k, (c, k, t, e, r)
            # constant patterns: value b reached for all large t in a class
            for (col, ph), (kind, b) in m.pat.items():
                if col == oo and kind == 'const':
                    assert (1 << b) * e < m.c or b >= Kstar + 3 * m.p, (c, oo, e, b)
    return m, Kstar, shapes


def main():
    for c in NICE:
        g = brute(c)
        m, Kstar, shapes = check(c, g)
        cols = ", ".join(
            f"o={o}:" + "/".join(f"{'k' if kd == 'shift' else ''}{a:+d}" if kd == 'shift' else f"{a}"
                                 for kd, a in (m.pat[(o, r)] for r in range(m.p)))
            for o in range(1, m.M + 1, 2)
            if any(m.pat[(o, r)] != ('shift', 0) for r in range(m.p)))
        print(f"c={c}: M={m.M}, period p={m.p}, K0={m.K0}, K*={Kstar}; "
              f"[A][B][C] PASS ({shapes} large-odd shapes)")
        print(f"   eventual nonzero columns (by k mod p): {cols}")
    for c in WILD:
        g = brute(c)
        top = max(split(n)[1] for n in range(1, N + 1) if g[n] != split(n)[0])
        print(f"[X] c={c}: largest exceptional odd part for n <= 2^20: {top}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
