"""Independent exact checks. Does not write source or shared wiki files."""

from fractions import Fraction as Q
from itertools import combinations_with_replacement
from math import comb, factorial, prod


def direct(n, r, a):
    return sum((Q((-1)**j * comb(n, j)) / (a + j)**r for j in range(n + 1)), Q(0))


def enumerated_h(variables, degree):
    return sum(
        (prod((variables[i] for i in indices), start=Q(1))
         for indices in combinations_with_replacement(range(len(variables)), degree)),
        Q(0),
    )


def harmonic(n, a):
    return sum((1 / (a + j) for j in range(n + 1)), Q(0))


def alpha_product(left, right):
    # Exact multiplication in Q[alpha], alpha^2=alpha+1.
    x, y = left
    z, w = right
    return x*z + y*w, x*w + y*z + y*w


def alpha_power(value, exponent):
    result = (Q(1), Q(0))
    for _ in range(exponent):
        result = alpha_product(result, value)
    return result


def main():
    cases = value_bounds = 0
    for n in (0, 1, 3, 9, 17, 25):
        for a in (Q(1, 100), Q(2, 7), Q(7, 4), Q(11, 3), Q(31)):
            values = [Q(0)] + [direct(n, r, a) for r in range(1, 36)]
            m = n+1
            variables = [1/(a+j) for j in range(m)]
            total, maximum, minimum = sum(variables), max(variables), min(variables)
            mean = total/m
            for r in range(2, 35):
                ratio = values[r]**2 / (values[r-1]*values[r+1])
                upper = Q(r*(n+r-1), (r-1)*(n+r))
                if not (ratio == 1 if n == 0 else 1 < ratio < upper):
                    raise AssertionError(("bounds", n, a, r))
                cases += 1
                k = r-1
                coefficient = values[r]/values[1]
                old_lower = total**k/factorial(k)
                lower = comb(m+k-1, k)*mean**k
                old_upper = prod((total+i*maximum for i in range(k)), start=Q(1))/factorial(k)
                chord = comb(m+k-1, k)*maximum**k if maximum == minimum else comb(m+k-1, k)*((maximum-mean)*minimum**k+(mean-minimum)*maximum**k)/(maximum-minimum)
                if not (max(maximum**k, lower) <= coefficient <= min(old_upper, chord)
                        and (lower > old_lower if k >= 2 else lower == old_lower)):
                    raise AssertionError(("improved value bounds", n, a, r))
                value_bounds += 1
            if n:
                ratios = [values[r+1] / values[r] for r in range(1, 35)]
                if not all(x > y > 1/a for x, y in zip(ratios, ratios[1:])):
                    raise AssertionError(("ratio decrease", n, a))
    print(f"PASS: {cases} additional exact Turan bounds and ratio configurations.")
    print(f"PASS: {value_bounds} additional exact improved-value bound checks.")

    for second, expected_chord, expected_old in ((Q(3,4), Q(75,32), Q(77,32)), (Q(1,4), Q(51,32), Q(45,32))):
        total, mean = 1+second, (1+second)/2
        chord = 3*((1-mean)*second**2+(mean-second))/(1-second)
        old = total*(total+1)/2
        if (chord, old) != (expected_chord, expected_old):
            raise AssertionError(("chord comparison counterexamples", second))
    print("PASS: both exact chord-versus-old-bound comparison examples.")

    enumeration_cases = 0
    for n in range(4):
        for a in (Q(1, 100), Q(7, 4), Q(31)):
            b = direct(n, 1, a)
            variables = [1 / (a+j) for j in range(n+1)]
            for k in range(8):
                if b * enumerated_h(variables, k) != direct(n, k+1, a):
                    raise AssertionError(("independent monomial enumeration", n, a, k))
                enumeration_cases += 1
    print(f"PASS: {enumeration_cases} independently enumerated homogeneous coefficients.")

    # At alpha=(1+sqrt(5))/2, alpha^-1=alpha-1 and (alpha+1)^-1=2-alpha.
    plateau = []
    for r in (1, 2, 3):
        p = alpha_power((Q(-1), Q(1)), r)
        q = alpha_power((Q(2), Q(-1)), r)
        plateau.append((p[0]-q[0], p[1]-q[1]))
    if plateau != [(Q(-3), Q(2)), (Q(-3), Q(2)), (Q(-16), Q(10))]:
        raise AssertionError(("golden ratio plateau", plateau))
    # F2-F3 = 13-8alpha = 9-4sqrt(5)>0, since 81>80.
    if not Q(9)**2 > Q(4)**2 * 5:
        raise AssertionError("plateau strict tail")
    print("PASS: exact algebraic F1=F2>F3 boundary at a=(1+sqrt(5))/2, n=1.")

    # e is between the factorial partial sum and that sum + 1/(N*N!).
    terms = 20
    e_low = sum((Q(1, factorial(k)) for k in range(terms+1)), Q(0))
    e_high = e_low + Q(1, terms*factorial(terms))
    threshold_cases = 0
    for n in (1, 3, 7, 19, 100):
        low, high = Q(1), Q(n+1)
        for _ in range(64):
            middle = (low+high)/2
            if harmonic(n, middle) > 1:
                low = middle
            else:
                high = middle
        # Stronger comparisons against enclosing rational bounds certify each sample.
        if not (harmonic(n, low) >= 1 >= harmonic(n, high)
                and Q(n+1)/(e_low-1) < low
                and high < Q(n+1)/(e_high-1)+1):
            raise AssertionError(("certified threshold bounds", n))
        threshold_cases += 1
    print(f"PASS: {threshold_cases} rationally certified threshold brackets and e-based bounds.")
    print("No source or shared wiki files written.")


if __name__ == "__main__":
    main()
