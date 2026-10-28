"""Independent review checks for research/2026-10-29-nontrivial-divisor-game/note.md.

Run from the repository root:
    python research/2026-10-29-nontrivial-divisor-game-review/verify_review.py
Python 3.10+, standard library only, no randomness, about 5-15 seconds.

Different method from the note's verify.py:
  [R1] Brute force to N = 2^17 * 3 = 393216 using divisors obtained from a
       smallest-prime-factor sieve (factorisation, not a multiples sieve).
       The claimed formula is NOT used to generate data; instead we collect
       the exception set {n : g(n) != v2(n)} and the per-column values, and
       compare them with the note's statement afterwards.
  [R2] Recursion on actual integers n = 2^k * o (o <= 15, 6 <= k <= 400):
       options are formed as the integers n - d, their 2-adic valuation and
       odd part are taken with bit operations, and values are looked up by
       memoised recursion; positions with odd part >= 17 get value v2 (case A,
       re-proved by hand in review.md), odd positions get 0 (Theorem 1).
       Base values for valuation <= 16 come from R1's brute force.
  [R3] Control game 1 <= d < n: g = v2(n) for n <= 20000.
  [R4] Prints the first terms used for OEIS searches.
"""
import time

T0 = time.time()
N = (1 << 17) * 3


def spf_sieve(n):
    spf = list(range(n + 1))
    i = 2
    while i * i <= n:
        if spf[i] == i:
            for m in range(i * i, n + 1, i):
                if spf[m] == m:
                    spf[m] = i
        i += 1
    return spf


def divisors(n, spf):
    ds = [1]
    while n > 1:
        p, c = spf[n], 0
        while n % p == 0:
            n //= p
            c += 1
        ds = [d * p ** a for d in ds for a in range(c + 1)]
    return ds


def v2(n):
    return (n & -n).bit_length() - 1


def mex(s):
    v = 0
    while v in s:
        v += 1
    return v


spf = spf_sieve(N)
g = [0] * (N + 1)
for n in range(2, N + 1):
    g[n] = mex({g[n - d] for d in divisors(n, spf) if 1 < d < n})

# [R1] exceptions and columns
exc = [n for n in range(1, N + 1) if g[n] != v2(n)]
bad_odd = sorted({n >> v2(n) for n in exc if (n >> v2(n)) >= 17})
print(f"[R1] brute force n <= {N} (spf divisors): {len(exc)} exceptions to g = v2;"
      f" odd parts of exceptions >= 17: {bad_odd or 'none'}")
print("     odd parts occurring among exceptions:", sorted({n >> v2(n) for n in exc}))
pos = [n for n in range(1, 400) if g[n] == 0]
ok = all(n % 2 or (n & (n - 1) == 0 and v2(n) % 2) for n in pos) and \
    all(g[n] == 0 for n in range(1, N + 1) if n % 2 or (n & (n - 1) == 0 and v2(n) % 2))
ok2 = all((g[n] == 0) == (n % 2 == 1 or (n & (n - 1) == 0 and v2(n) % 2 == 1))
          for n in range(1, N + 1))
print(f"     P-positions == odd numbers + odd powers of 2 for all n <= {N}: {ok2}")
SMALL = (1, 3, 5, 7, 9, 11, 13, 15)
print("     column values g(2^k o) - k, k = 1..17 (from brute force):")
for o in SMALL:
    row = []
    for k in range(1, 18):
        n = (1 << k) * o
        if n <= N:
            row.append('Z' if g[n] == 0 else f"{g[n] - k:+d}")
    print(f"       o={o:2d}: " + " ".join(row))

# note's claimed formula, typed in from the note only for the final comparison
TABLE1 = {1: [0, 2, 1, 1, 1, 1, 1, 1], 2: [1, 3, 3, 2, 2, 2, 2, 2],
          3: [0, 4, 4, 4, 4, 4, 3, 4], 4: [2, 3, 3, 5, 5, 5, 5, 5],
          5: [0, 6, 6, 6, 6, 6, 6, 6]}


def claimed(k, o):
    if k == 0:
        return 0
    if o >= 17:
        return k
    if k <= 5:
        return TABLE1[k][SMALL.index(o)]
    if o == 1:
        return 0 if k % 2 else k - 1
    return {3: k - 2, 5: k + 2}.get(o, k + 1)


mism = [n for n in range(1, N + 1) if g[n] != claimed(v2(n), n >> v2(n))]
print(f"     note's formula (incl. Table 1) vs brute force, n <= {N}: "
      f"{'agree' if not mism else 'MISMATCH ' + str(mism[:5])}")

# [R2] recursion on actual integers
memo = {}


def val(n):
    k = v2(n)
    o = n >> k
    if k == 0 or o >= 17:
        return k if k else 0
    if n <= N:
        return g[n]
    if n in memo:
        return memo[n]
    odd_divs = [e for e in range(1, o + 1, 2) if o % e == 0]
    opts = set()
    for j in range(k + 1):
        for e in odd_divs:
            d = (1 << j) * e
            if 1 < d < n:
                opts.add(val(n - d))
    memo[n] = mex(opts)
    return memo[n]


KMAX = 400
bad = [(k, o) for o in SMALL for k in range(6, KMAX + 1)
       if val((1 << k) * o) != claimed(k, o)]
print(f"[R2] integer recursion, o <= 15, 6 <= k <= {KMAX}: "
      f"{'agree with formula' if not bad else 'MISMATCH ' + str(bad[:5])}")

# [R3] control game with d = 1 allowed
M = 20000
h = [0] * (M + 1)
for n in range(2, M + 1):
    h[n] = mex({h[n - d] for d in divisors(n, spf) if d < n})
print(f"[R3] game 1 <= d < n: g = v2(n) for all n <= {M}: "
      f"{all(h[n] == v2(n) for n in range(1, M + 1))}")

# [R4] OEIS query terms
print("[R4] g(1..40):", ",".join(map(str, g[1:41])))
print("     N-positions:", ",".join(str(n) for n in range(1, 80) if g[n]))
print(f"elapsed {time.time() - T0:.1f}s")
