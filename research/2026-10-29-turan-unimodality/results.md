# 계산 기록: 로그 오목성과 단봉성

[연구 노트](note.md)

- 연구일: 2026-10-29
- 환경: Python 3.10.11 (Windows)
- Fraction 정확 산술, 난수 없음. e를 사용하는 마지막 비교만 Decimal 근사 관찰.

```powershell
python research/2026-10-29-turan-unimodality/verify.py
```

```text
PASS: 2600 exact direct-sum / positive-coefficient identities.
PASS: 2392 exact Turan bounds, including n=0 equality.
PASS: 2600 improved value bounds and strict lower-improvement checks.
PASS: 104 ratio and monotonicity-regime configurations.
PASS: 55 independently expanded exact simplex moments.
PASS: 45 normalized log-convexity and equality checks.
PASS: 120 exact positive-defect identities.
PASS: 1 non-monotone example with a unique peak at r=2.
PASS: 5 exact rational threshold brackets (48 bisection steps each).
OBSERVED: all 5 midpoint approximations lie inside the e-based bounds at 60 digits.
```

## 입력 범위

n=0..12, a=1/5,1/2,1,6/5,3/2,2,3,8, 직접 합 r=1..25, 이웃 항 경계 r=2..24.
개선된 값의 상하계와 이전 하계 대비 엄격한 개선 여부도 r=1..25 전체에서 확인했다.
비율의 단조성은 각 설정에서 r=1..24를 검산했다. 무한 꼬리에 대한 결론은 노트의 증명에 의존한다.

단체 적률: 변수 벡터 (2), (1,1), (1,2), (1/3,1/2,1), (1/7,2/3,5/2,4), 차수 k=0..10.
정규화 부등식 k=1..9. 결손 항등식은 같은 벡터에 x=1/2 또는3을 추가하고 k=1..12에서 확인했다.

## 전환 매개변수

아래 소수는 정확한 이분 구간의 중점 근사다. 구간의 양 끝에서는 H_n(a)-1의 부호를 유리수로 확인했다.

| n | alpha_n 중점 근사 | 정확 구간 폭의 소수 근사 |
| --- | --- | --- |
| 1 | 1.618033988750 | 3.553e-15 |
| 2 | 2.214319743378 | 7.105e-15 |
| 5 | 3.975681966413 | 1.776e-14 |
| 12 | 8.058178495114 | 4.263e-14 |
| 50 | 30.178892031786 | 1.776e-13 |

e 기반 경계 비교는 엄밀한 구간 산술 인증이 아니다. 해당 경계와 점근식의 근거는 노트 §7의 증명이다.
