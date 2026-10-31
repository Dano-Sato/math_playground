"""Exact checks for the phase bootstrap counterexample.

Python >=3.10, standard library only, no randomness.
Run: python research/2026-10-31-rh-phase-bootstrap/verify.py
Grid: r=j/8, 8<=j<=40; c=k/8, -8<=k<=8 (561 inputs).
Here c=cos(4t), r=cosh(4h); the proof treats their whole domains.
"""

from fractions import Fraction as F


def laguerre(c):
    return 9+6*c+2*c*c+3*c**3


def bracket(c, r):
    return 2*r**3+7*r+2*r*c*c+9*r*r*c+3*c**3-3*c


def main():
    count = 0
    for j in range(8, 41):
        r = F(j, 8)
        for k in range(-8, 9):
            c = F(k, 8)
            mod_c = c*c+r*r-1
            mod_d = 9+6*c*r+mod_c
            product_identity = r*mod_d+mod_c*(3*c+r)
            assert product_identity == bracket(c, r)
            assert laguerre(c) == bracket(c, F(1))
            assert laguerre(c) >= 2
            derivative = 4*r*c+9*r*r+9*c*c-3
            square_form = 9*(c+2*r/9)**2+F(77, 9)*r*r-3
            assert derivative == square_form and derivative >= F(50, 9)
            assert bracket(c, r) >= bracket(F(-1), r)
            assert bracket(F(-1), r) == r*(2*r-3)*(r-3)
            count += 1
    print(f"PASS: exact phase polynomial identities and bounds at {count} inputs.")
    r, s, c = F(17, 8), F(15, 8), F(-1)
    assert r*r-s*s == 1
    value = -r*(3-r)/4
    wronskian = s*bracket(c, r)/4
    phase_derivative = -wronskian/(value*value)
    assert value == F(-119, 256)
    assert wronskian == F(-8925, 8192)
    assert phase_derivative == F(600, 119)
    print(f"At t=pi/4, h=log(4)/4: F(t+ih) = {value}")
    print(f"W_h(t) = {wronskian} < 0")
    print(f"Phase derivative = {phase_derivative} > 0")
    for r in (F(5, 4), F(17, 8), F(4)):
        sign = bracket(F(-1), r)
        print(f"Minimum phase bracket at cosh(4h)={r}: {sign}")
    print("PASS: positive small/large shifts and negative intermediate shift.")
    print("Actual xi pointwise phase positivity remains unproved.")


if __name__ == "__main__":
    main()
