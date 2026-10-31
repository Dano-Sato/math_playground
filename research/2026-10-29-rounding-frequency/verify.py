"""Bounded self-checks for rounding-failure counts; standard library, no RNG.

Run: python research/2026-10-29-rounding-frequency/verify.py
Imports constants only from the preceding note. Float quadrature is observational.
Bounds: a=2,3,5; j<=140; panels<=3000; 42 bisections per boundary.
"""
import importlib.util
import json
from math import exp, expm1, floor, log, log1p
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('previous', HERE.parent/'2026-10-29-fixed-a-lattice-correction'/'verify.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
H = 1/24


class BoundarySolver:
    def __init__(self, a, panels):
        self.a = a
        self.step = (12+65/(a-1))/panels
        self.rows = []
        for i in range(panels+1):
            v = -12+i*self.step
            weight = 1 if i in (0,panels) else (4 if i%2 else 2)
            self.rows.append((v,exp(-v),weight))

    def moment(self, lam, s, kind):
        n = exp(lam)
        rows = []
        for v,u,w in self.rows:
            assert v > -lam
            z = log1p(v/lam)
            lw = (s-1)*z-self.a*v+n*log1p(-u/n)
            rows.append((lw,w,z if kind=='log' else v))
        shift = max(r[0] for r in rows)
        mass = total = 0.0
        for lw,w,value in rows:
            weight = w*exp(lw-shift)
            mass += weight
            total += weight*value
        return log(lam)+total/mass if kind=='log' else lam+total/mass

    def boundaries(self, j):
        kappa,delta,eta = previous.constants(self.a)
        T = j+0.5-kappa
        def solve(kind):
            s = j+0.5 if kind=='log' else j
            target = previous.psi(s) if kind=='log' else j
            lo,hi = T-2,T+2
            f = lambda lam: self.moment(lam,s,kind)-target
            assert f(lo)<0<f(hi), (self.a,j,kind)
            for _ in range(42):
                mid = (lo+hi)/2
                if f(mid)<0:
                    lo=mid
                else:
                    hi=mid
            return (lo+hi)/2
        lower,upper = solve('mean'),solve('log')
        assert lower<upper
        return dict(a=self.a,j=j,T=T,lower=lower,upper=upper,
                    lower_remainder_scaled=T*T*(lower-T+eta/T),
                    upper_remainder_scaled=T*T*(upper-T+delta/T),
                    log_width_scaled=T*(upper-lower),width_limit=H)


def scaled_lengths(lam, intervals):
    """log(X)/X times CONTINUOUS lengths, not an exact integer count."""
    return lam*sum(exp(row['lower']-lam)*expm1(min(lam,row['upper'])-row['lower'])
                   for row in intervals if row['lower']<lam)


def phase_prediction(lam,kappa,eta):
    j = floor(lam+kappa-0.5)
    T = j+0.5-kappa
    u = lam-T
    clipped = min(H,max(0,T*expm1(u)+eta))
    return exp(-u)*(H/(exp(1)-1)+clipped)


def exact_window_check():
    """Independent integer enumeration versus interval-length rounding error."""
    from fractions import Fraction as Q
    intervals = [(Q(3,2),Q(11,4)),(Q(4),Q(9,2)),(Q(7),Q(10))]
    count=0
    for X in range(1,16):
        actual=sum(any(a<n<b for a,b in intervals) for n in range(1,X+1))
        lengths=sum(max(Q(0),min(Q(X),b)-a) for a,b in intervals)
        assert abs(actual-lengths)<=len(intervals)
        count+=1
    return count


def main():
    exact_cases=exact_window_check()
    grid_cases=[]
    max_diff=0.0
    for a in (2.0,3.0,5.0):
        coarse,fine=BoundarySolver(a,1500),BoundarySolver(a,3000)
        for j in (20,40,80,140):
            c,f=coarse.boundaries(j),fine.boundaries(j)
            diff=max(abs(c[key]-f[key]) for key in ('lower','upper'))
            max_diff=max(max_diff,diff)
            assert diff<1e-7, (a,j,diff)
            grid_cases.append(f)
        assert abs(grid_cases[-1]['log_width_scaled']-H)<0.002
    solver=BoundarySolver(3.0,1500)
    intervals=[solver.boundaries(j) for j in range(20,141)]
    kappa,delta,eta=previous.constants(3.0)
    counts=[]
    for j in (40,80,140):
        T=j+0.5-kappa
        for u in (0,0.1,0.5,0.9):
            lam=T+u
            actual=scaled_lengths(lam,intervals)
            prediction=phase_prediction(lam,kappa,eta)
            counts.append(dict(j=j,phase=u,scaled_continuous_count=actual,
                               prediction=prediction,scaled_error=lam*(actual-prediction)))
        # Cross the shrinking current window, including both endpoints.
        for row in (intervals[j-20],):
            for label,lam in [('left',row['lower']),('middle',(row['lower']+row['upper'])/2),('right',row['upper'])]:
                actual=scaled_lengths(lam,intervals)
                counts.append(dict(j=j,position=label,phase=lam-T,scaled_continuous_count=actual,
                                   prediction=phase_prediction(lam,kappa,eta)))
    # Harmonic sum of the continuous windows. Integer discrepancy is summable
    # theoretically; this computation does not determine the full constant C_a.
    harmonics=[]
    for J in (40,80,140):
        total=sum(r['upper']-r['lower'] for r in intervals if r['j']<=J)
        L=intervals[J-20]['upper']
        harmonics.append(dict(j=J,centered_continuous_harmonic=total-H*log(L)))
    result=dict(exact_interval_cases=exact_cases,boundary_grid_cases=grid_cases,
                max_grid_boundary_difference=max_diff,intervals_a3=intervals,
                continuous_count_observations=counts,harmonic_observations=harmonics,
                theoretical_liminf=H/(exp(1)-1),theoretical_limsup=H*exp(1)/(exp(1)-1))
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'PASS exact integer interval checks: {exact_cases}')
    print(f'PASS boundary roots: {len(grid_cases)} settings, two grids; max difference {max_diff:.3g}')
    print(f'Computed {len(intervals)} a=3 windows (j=20..140); all have positive widths.')
    print(f"Theoretical scaled range: [{result['theoretical_liminf']:.9f}, {result['theoretical_limsup']:.9f}]")
    for r in counts:
        if r['j']==140:
            print(f"j=140, {r.get('position',str(r['phase']))}: observed={r['scaled_continuous_count']:.9f}, predicted={r['prediction']:.9f}")
    for r in harmonics:
        print(f"Harmonic observation j={r['j']}: centered={r['centered_continuous_harmonic']:.9f}")
    print('PASS; quadrature and continuous counts are observations, not integer-count certificates.')


if __name__=='__main__':
    main()
