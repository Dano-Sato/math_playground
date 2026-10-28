# 계산 기록

[연구 노트](note.md)

- 실행일: 2026-10-29
- 환경: Windows 11, Python 3.10.11, 표준 라이브러리만 사용, 난수 없음
- 명령: `python research/2026-10-29-fixed-a-argmax/verify.py` (저장소 루트), 약 9초

## 실제 출력

```text
[quadrature] Simpson log F vs exact Fraction sum, 72 cases: max |error| = 2.0e-14
[real maximizer] s* vs log n + kappa (+ delta/log n)
  a=1.5: kappa=2.46351, delta=-13.3909
    n=1e2 : s*=6.24690, s*-log n-kappa=-0.82178, log n*(..)=-3.7844, minus delta=+9.6064
    n=1e4 : s*=11.07927, s*-log n-kappa=-0.59458, log n*(..)=-5.4763, minus delta=+7.9146
    n=1e6 : s*=15.80473, s*-log n-kappa=-0.47429, log n*(..)=-6.5525, minus delta=+6.8383
    n=1e9 : s*=22.81731, s*-log n-kappa=-0.36947, log n*(..)=-7.6566, minus delta=+5.7342
    n=1e12: s*=29.78956, s*-log n-kappa=-0.30497, log n*(..)=-8.4267, minus delta=+4.9641
    n=1e16: s*=39.05616, s*-log n-kappa=-0.24872, log n*(..)=-9.1631, minus delta=+4.2278
  a=2.0: kappa=1.07722, delta=-2.8887
    n=1e2 : s*=5.34703, s*-log n-kappa=-0.33536, log n*(..)=-1.5444, minus delta=+1.3443
    n=1e4 : s*=10.07362, s*-log n-kappa=-0.21393, log n*(..)=-1.9704, minus delta=+0.9183
    n=1e6 : s*=14.73612, s*-log n-kappa=-0.15660, log n*(..)=-2.1636, minus delta=+0.7251
    n=1e9 : s*=21.68788, s*-log n-kappa=-0.11260, log n*(..)=-2.3335, minus delta=+0.5552
    n=1e12: s*=28.62002, s*-log n-kappa=-0.08822, log n*(..)=-2.4376, minus delta=+0.4511
    n=1e16: s*=37.84998, s*-log n-kappa=-0.06859, log n*(..)=-2.5271, minus delta=+0.3616
  a=3.0: kappa=0.07722, delta=-0.8887
    n=1e2 : s*=4.53799, s*-log n-kappa=-0.14440, log n*(..)=-0.6650, minus delta=+0.2237
    n=1e4 : s*=9.19923, s*-log n-kappa=-0.08833, log n*(..)=-0.8135, minus delta=+0.0751
    n=1e6 : s*=13.83244, s*-log n-kappa=-0.06029, log n*(..)=-0.8329, minus delta=+0.0557
    n=1e9 : s*=20.75957, s*-log n-kappa=-0.04091, log n*(..)=-0.8477, minus delta=+0.0409
    n=1e12: s*=27.67724, s*-log n-kappa=-0.03099, log n*(..)=-0.8564, minus delta=+0.0323
    n=1e16: s*=36.89514, s*-log n-kappa=-0.02344, log n*(..)=-0.8635, minus delta=+0.0252
  a=5.0: kappa=-0.75612, delta=-0.3655
    n=1e2 : s*=3.79747, s*-log n-kappa=-0.05158, log n*(..)=-0.2375, minus delta=+0.1280
    n=1e4 : s*=8.41113, s*-log n-kappa=-0.04309, log n*(..)=-0.3969, minus delta=-0.0314
    n=1e6 : s*=13.03135, s*-log n-kappa=-0.02804, log n*(..)=-0.3874, minus delta=-0.0219
    n=1e9 : s*=19.94884, s*-log n-kappa=-0.01831, log n*(..)=-0.3794, minus delta=-0.0139
    n=1e12: s*=26.86131, s*-log n-kappa=-0.01360, log n*(..)=-0.3757, minus delta=-0.0102
    n=1e16: s*=36.07512, s*-log n-kappa=-0.01012, log n*(..)=-0.3730, minus delta=-0.0075
[integer argmax] nearest integer to s* and to log n + kappa
  42 settings: argmax in {floor s*, ceil s*} and = round(s*) away from half-integers: PASS
  argmax = round(log n + kappa) in 41/42 settings (o(1) offset can flip near half-integers)
ALL CHECKS PASSED
```

## 해석

- $s^*-\log n-\kappa$는 모든 $a$에서 $n$이 커질수록 0으로 단조 감소했다(정리 1과 일치).
- $\log n\cdot(s^*-\log n-\kappa)-\delta$도 네 경우 모두 감소했다. $a=3$에서는 $n=10^{16}$일 때 0.025로, 남은 오차가 대략 $(\log n)^{-2}$ 크기임을 시사한다(주장 3의 관찰).
- $\log n+\kappa$의 반올림과 정수 최대점이 다른 1개 설정은 $\delta/\log n$ 보정이 반올림 방향을 바꾼 경우다.
