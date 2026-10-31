"""Exact arithmetic checks; Python >=3.10, standard library, no randomness.

Run: python research/2026-10-31-rh-double-helix/verify.py
Grid: u=k/4 (-6<=k<=6), y,h=j/8 (1<=j<=4), b=k/8 (0<=k<=4).
Finite checks support the written algebra and are not a proof of RH.
"""

from fractions import Fraction as F


def norm_q(u, v, b):
    return (u*u-v*v+b*b)**2 + 4*u*u*v*v


def norm_p(x, y, b):
    return norm_q(x-2, y, b)*norm_q(x+2, y, b)/(4+b*b)**4


def main():
    count = 0
    for k in range(-6, 7):
        u = F(k, 4)
        for j in range(1, 5):
            y = F(j, 8)
            for l in range(1, 5):
                h = F(l, 8)
                for n in range(5):
                    b = F(n, 8)
                    lhs = norm_q(u, y+h, b)-norm_q(u, y-h, b)
                    rhs = 8*y*h*(u*u+y*y+h*h-b*b)
                    assert lhs == rhs
                    if h >= b:
                        assert lhs > 0
                    count += 1
    print(f"PASS: quadratic modulus identity at {count} exact rational inputs.")
    b, h, x, y = F(1, 4), F(1, 8), F(2), F(1, 8)
    numerator = norm_p(x, y+h, b)
    denominator = norm_p(x, y-h, b)
    assert numerator == 0 and denominator > 0
    print(f"Counterexample |P(z+ih)|^2 = {numerator}")
    print(f"Counterexample |P(z-ih)|^2 = {denominator}")
    # Im P'/P = -sum (h-Im rho)/((x-Re rho)^2+(h-Im rho)^2).
    phase_derivative = -sum(
        (h-v)/((x-a)**2+(h-v)**2)
        for a in (F(2), F(-2)) for v in (b, -b)
    )
    expected = F(16, 3)+F(8, 1025)-F(24, 1033)
    assert phase_derivative == expected and phase_derivative > 0
    print(f"Counterexample phase derivative = {phase_derivative} > 0")
    print("PASS: normalized even polynomial counterexample and reversed phase.")
    print("No actual xi zero computation; RH remains unresolved.")


if __name__ == "__main__":
    main()
