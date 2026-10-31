"""Q-018 self-checks; Python >=3.10, standard library, no randomness.

Run: python research/2026-10-29-fixed-a-lattice-correction/verify.py
Finite quadrature checks are observations, not certified interval proofs.
Bounded inputs: a in {1.5,2,3,5}, log(n)<=640, grids <=8000 panels.
"""
import json
from fractions import Fraction as Q
from math import comb, exp, floor, lgamma, log, log1p
from pathlib import Path


def psi(x):
    out = 0.0
    while x < 20:
        out -= 1 / x
        x += 1
    z = 1 / x
    return out + log(x) - z / 2 - z*z/12 + z**4/120 - z**6/252 + z**8/240


def poly(k, x):
    out = 0.0
    while x < 20:
        out += (1 if k == 1 else -2) / x**(k+1)
        x += 1
    if k == 1:
        return out + 1/x + 1/(2*x*x) + 1/(6*x**3) - 1/(30*x**5) + 1/(42*x**7) - 1/(30*x**9)
    return out - 1/x**2 - 1/x**3 - 1/(2*x**4) + 1/(6*x**6) - 1/(6*x**8) + 3/(10*x**10)


def constants(a):
    mu, var, third = -psi(a-1), poly(1, a-1), -poly(2, a-1)
    eta = -var - third/2
    return mu+0.5, eta-1/24, eta


class Integral:
    def __init__(self, n, a, panels):
        self.lam = log(n)
        # Left omitted segment is exponentially suppressed by (1-exp(-t))**n.
        lo, hi = 1e-8, self.lam + 65/(a-1)
        self.step = (hi-lo)/panels
        self.rows = []
        for i in range(panels+1):
            t = lo + i*self.step
            weight = 1 if i in (0, panels) else (4 if i % 2 else 2)
            self.rows.append((log(t), -a*t + n*log1p(-exp(-t)), weight))

    def values(self, s):
        logs = [(s-1)*lt+base for lt, base, _ in self.rows]
        shift = max(logs)
        z = moment = 0.0
        for (lt, _, w), lw in zip(self.rows, logs):
            mass = w*exp(lw-shift)
            z += mass
            moment += mass*lt
        return log(z*self.step/3)+shift-lgamma(s), moment/z-psi(s)

    def roots(self, kappa):
        center = self.lam+kappa
        def root(fn):
            lo, hi = max(0.500001, center-8), center+3
            assert fn(lo) > 0 > fn(hi)
            for _ in range(45):
                mid = (lo+hi)/2
                if fn(mid) > 0:
                    lo = mid
                else:
                    hi = mid
            return (lo+hi)/2
        real = root(lambda s: self.values(s)[1])
        lattice = root(lambda s: self.values(s+0.5)[0]-self.values(s-0.5)[0])
        return real, lattice


def exact_algebra():
    count = 0
    for mu in map(Q, (-2, -1, 0, 1, 2)):
        for var in map(Q, (1, 2, 3, 4, 5)):
            for third in map(Q, (-2, -1, 0, 1, 2)):
                kappa = mu+Q(1, 2)
                def B(x):
                    return (x-Q(3,2)-mu)*var-third/2-mu*mu/2+x*x/2-x/2+Q(1,12)
                assert B(kappa) == -var-third/2-Q(1,24)
                # Exact integral of the quadratic over [z-1/2,z+1/2].
                for z in map(Q, (-2, -1, 0, 1, 2)):
                    C = -Q(3,2)*var-mu*var-third/2-mu*mu/2+Q(1,12)
                    antideriv = lambda x: x**3/6+(var-Q(1,2))*x*x/2+C*x
                    assert antideriv(z+Q(1,2))-antideriv(z-Q(1,2)) == B(z)+Q(1,24)
                    count += 1
    return count


def main():
    algebra = exact_algebra()
    worst = 0.0
    calibration = 0
    for n in (20, 50):
        for a in (2, 3, 5):
            integral = Integral(n, a, 8000)
            for r in range(1, 9):
                exact = sum(Q((-1)**j*comb(n,j), (a+j)**r) for j in range(n+1))
                err = abs(integral.values(r)[0]-log(exact))
                worst = max(worst, err)
                assert err < 1e-9, (n, a, r, err)
                calibration += 1
    rows = []
    max_grid_difference = 0.0
    for a in (1.5, 2.0, 3.0, 5.0):
        kappa, delta, eta = constants(a)
        for target in (20, 40, 80, 160, 320, 640):
            n = round(exp(target))
            coarse = Integral(n, a, 4000).roots(kappa)
            fine = Integral(n, a, 8000).roots(kappa)
            grid_diff = max(abs(x-y) for x,y in zip(coarse,fine))
            max_grid_difference = max(max_grid_difference, grid_diff)
            assert grid_diff < 2e-7, (a, target, grid_diff)
            lam = log(n)
            s, m = fine
            rows.append(dict(a=a, log_n=lam, real=s, lattice=m,
                real_scaled=lam*(s-lam-kappa), delta=delta,
                lattice_scaled=lam*(m-lam-kappa), eta=eta,
                gap_scaled=lam*(m-s), gap_limit=1/24,
                real_remainder_scaled=lam*lam*(s-lam-kappa-delta/lam),
                lattice_remainder_scaled=lam*lam*(m-lam-kappa-eta/lam)))
        assert abs(rows[-1]['gap_scaled']-1/24) < 0.002
        assert abs(rows[-1]['real_scaled']-delta) < 0.8
        assert abs(rows[-1]['lattice_scaled']-eta) < 0.8
    counterexamples = []
    a = 3.0
    kappa, delta, eta = constants(a)
    for j in (25, 45, 85, 155):
        L = j+0.5-kappa
        n = round(exp(L-(delta+eta)/(2*L)))
        s, m = Integral(n, a, 8000).roots(kappa)
        k = floor(s+0.5)
        integral = Integral(n,a,8000)
        best = max((j-1,j,j+1,j+2), key=lambda r: integral.values(r)[0])
        counterexamples.append(dict(a=a,n=str(n),j=j,real=s,lattice=m,
                                   rounded_real=k,integer_max=best,
                                   log_ratio=integral.values(j+1)[0]-integral.values(j)[0]))
    assert counterexamples[-1]['rounded_real'] != counterexamples[-1]['integer_max']
    result = dict(exact_algebra_cases=algebra,calibration_cases=calibration,
                  max_log_calibration_error=worst,max_grid_root_difference=max_grid_difference,
                  asymptotic_observations=rows,rounding_observations=counterexamples)
    Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'PASS exact rational algebra: {algebra} cases')
    print(f'PASS quadrature calibration: {calibration} cases; max log error {worst:.3g}')
    print(f'PASS roots: {len(rows)} settings, two grids; max root difference {max_grid_difference:.3g}')
    for row in counterexamples:
        print(f"a=3, j={row['j']}: round(s*)={row['rounded_real']}, integer max={row['integer_max']}, log ratio={row['log_ratio']:.9g}")
    print('PASS; numerical values are observations, not interval certificates.')


if __name__ == '__main__':
    main()
