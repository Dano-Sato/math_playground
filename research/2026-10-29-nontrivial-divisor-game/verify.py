"""Checks for the nontrivial-divisor subtraction game note.

Game: from n >= 1 move to n - d where d | n and 1 < d < n.
Run from the repository root:
    python research/2026-10-29-nontrivial-divisor-game/verify.py
Standard library only, no randomness, a few seconds.

Parts (see note section numbers):
  [A] brute-force Grundy values for n <= N_BRUTE agree with the formula G.
  [B] the inductive step for small odd parts o <= 15 and every k in
      [10, K_MAX], with option values taken from the formula (the step is
      2-periodic in k for k >= 10, so k = 10, 11 already suffice; we check
      far beyond as a guard).
  [C] the finite check needed in the proof of the large-odd-part case.
"""

N_BRUTE = 1 << 15          # 32768 >= 2^9 * 15 (all base cases k <= 9, o <= 15)
K_MAX = 200
SMALL = (1, 3, 5, 7, 9, 11, 13, 15)


def brute(N):
    divs = [[] for _ in range(N + 1)]
    for d in range(2, N + 1):
        for m in range(2 * d, N + 1, d):
            divs[m].append(d)
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        seen = {g[n - d] for d in divs[n]}
        v = 0
        while v in seen:
            v += 1
        g[n] = v
    return g


def split(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k, n


# Table for k <= 5 and small odd part o (filled from brute force in main and
# printed; the note reproduces it).
TABLE = {}


def G(k, o):
    """Claimed Grundy value of 2^k * o (o odd)."""
    if k == 0:
        return 0
    if o >= 17:
        return k
    if k <= 5:
        return TABLE[(k, o)]
    if o == 1:
        return 0 if k % 2 else k - 1
    if o == 3:
        return k - 2
    if o == 5:
        return k + 2
    return k + 1


def odd_divisors(o):
    return [e for e in range(1, o + 1, 2) if o % e == 0]


def options(k, o):
    """Options of n = 2^k o as (valuation, odd part), via d = 2^j e."""
    out = []
    for j in range(k + 1):
        for e in odd_divisors(o):
            if (j, e) == (0, 1) or (j, e) == (k, o):
                continue
            if j < k:
                out.append((j, (o << (k - j)) - e))
            else:
                v, r = split(o // e - 1)
                out.append((k + v, e * r))
    return out


def mex(s):
    v = 0
    while v in s:
        v += 1
    return v


def main():
    g = brute(N_BRUTE)
    for k in range(1, 6):
        for o in SMALL:
            TABLE[(k, o)] = g[(1 << k) * o]
    print("[table] G(2^k o) for 1<=k<=5, o<=15:")
    for k in range(1, 6):
        print(f"  k={k}: " + ", ".join(f"o={o}:{TABLE[(k, o)]}" for o in SMALL))

    bad = [n for n in range(1, N_BRUTE + 1) if g[n] != G(*split(n))]
    assert not bad, bad[:10]
    print(f"[A] brute force n <= {N_BRUTE}: Grundy value = formula for every n  PASS")
    P = [n for n in range(1, 200) if g[n] == 0]
    assert all(n % 2 or (n & (n - 1) == 0 and split(n)[0] % 2) for n in P)
    print(f"    P-positions are the odd numbers and odd powers of 2 (n < 200 listed check)  PASS")

    for k in range(10, K_MAX + 1):
        for o in SMALL:
            vals = {G(v, q) for v, q in options(k, o)}
            assert mex(vals) == G(k, o), (k, o)
    print(f"[B] inductive step, o <= 15, 10 <= k <= {K_MAX}: mex(option values) = formula  PASS")
    # 2-periodicity: option shapes near the top depend only on k - j and parity.
    sig = {}
    for k in (10, 11, 12, 13):
        for o in SMALL:
            top = sorted((v - k, (G(v, q) - k) if G(v, q) else 'zero')
                         for v, q in options(k, o) if v >= k - 4)
            sig[(k, o)] = top
    assert all(sig[(k, o)] == sig[(k + 2, o)] for k in (10, 11) for o in SMALL)
    print("    top-of-range option offsets identical for k and k+2 (k = 10, 11)  PASS")

    count = 0
    for k in range(1, 5):
        for t in range(1, 6 - k):
            for e in SMALL:
                for r in SMALL:
                    if e * r > 15:
                        continue
                    m = e * (1 + (r << t))
                    if m >= 17:
                        count += 1
                        assert G(k + t, e * r) != k, (k, t, e, r)
    print(f"[C] large odd part, k+t <= 5: {count} option shapes never take value k  PASS")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
