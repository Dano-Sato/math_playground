# 계산 기록

[연구 노트](note.md)

- 실행일: 2026-10-29
- 환경: Windows 11, Python 3.10.11, 표준 라이브러리만 사용
- 명령: `python research/2026-10-29-real-log-concavity/verify.py` (저장소 루트에서)
- 난수 시드: 2026 (비균등 간격 무작위 40개)
- 정밀도: `decimal` 130자리, 2계 중심 차분 간격 $10^{-15}$. 정수 지수 값과 $\delta=1$ 항등식은 `fractions`로 정확 계산.
- 소요 시간: 약 57초

## 실제 출력

```text
[curvature, uniform] 280 cases PASS: -sum < (log D)'' < 0
[curvature, spacings] 308 cases PASS (seed 2026, 40 random + 4 fixed)
  closest to 0 (a->0 end): (log D)''/gap = -1.422222e-56 at a=1/100, h=[1], s=30
  closest to -1 (a->oo end): 1 + (log D)''/gap = 2.062689e-08 at a=100, h=[1], s=1/20
[two-point ratio] 420 cases PASS: 1 < ratio < product bound
[delta=1 exact identity] 276 (n,r) pairs PASS (Fraction)
[argmax] a>1: integer argmax within {floor s*, ceil s*}; s_lo < s* < s_hi
  a=3/2, h=[1]: s*=1.596041 in (1.0914, 2.4663), integer argmax=[2]
  a=6/5, h=[1,1,1]: s*=3.577116 in (1.3871, 15.4949), integer argmax=[4]
  a=11/10, h=[1,1,1,1,1,1,1,1]: s*=5.643274 in (1.4445, 80.4990), integer argmax=[6]
  a=2, h=[1,1,1,1,1,1,1,1]: s*=2.780280 in (1.3420, 8.4922), integer argmax=[3]
  a=21/20, h=[1/2,3]: s*=5.652376 in (0.9880, 40.4980), integer argmax=[6]
  a=5/4, h=[2,2,2,2]: s*=2.608906 in (0.9083, 16.4953), integer argmax=[3]
[n=0] (log D)'' = 0.00e+00 (expected 0 up to roundoff)
ALL CHECKS PASSED
```

## 해석

- 곡률 비율 $(\log D)''/\sum(s+i)^{-2}$는 모든 점에서 $(-1,0)$ 안에 있었다. 0에 가장 가까운 점은 $a$가 작고 $s$가 큰 곳, $-1$에 가장 가까운 점은 $a$가 크고 $s$가 작은 곳으로, §5의 날카로움 분석과 맞는다.
- 정수 최대점 6개 사례는 모두 $\lceil s^*\rceil$이었다. 일반적으로 $\lfloor s^*\rfloor$일 수도 있으며 여기서 어느 쪽인지 예측하는 규칙은 얻지 않았다.
- §7의 위치 경계는 실제로 성립했지만 $a\to1^+$나 큰 $n$에서 상한이 크게 느슨했다(예: $a=11/10,n=8$에서 상한 80.5, 실제 5.64).
- 이 계산은 유한한 매개변수에서의 관찰이다.
