# 계산 기록: 교대 이항합

[연구 노트](note.md)

- 연구일: 2026-10-29
- 실행 환경: Python 3.10.11 (Windows)
- 산술: 핵심 검산은 Fraction을 이용한 정확한 유리수 계산. 난수 없음.

```powershell
python research/2026-10-29-reciprocal-binomial/verify.py
```

```text
PASS: 624 exact alternating-sum identities and positivity checks.
PASS: 624 independent power-sum coefficient checks.
PASS: 624 exact lower/upper bound checks.
PASS: 576 Pascal recurrence checks.
PASS: 3 counterexample checks and 4 exact stress cases.
```

범위: n=0..12, r=1..8, a=1/5,1/2,1,3/2,2,5. 점화식은 n=1..12.

## 부동소수점 상쇄 실험

a=r=1. 아래 실수 출력은 환경에 따라 달라질 수 있다.

| n | 정확한 값 | 단순 합산 | math.fsum | 양수 곱 점화식 |
| --- | --- | --- | --- | --- |
| 10 | 1/11 | 0.09090909090909091 | 0.09090909090909091 | 0.09090909090909093 |
| 30 | 1/31 | 0.03225806451612903 | 0.03225806451612903 | 0.03225806451612904 |
| 50 | 1/51 | 0.019869624273003053 | 0.0196078431372549 | 0.0196078431372549 |
| 80 | 1/81 | -67052.10401450835 | 0.012345679012345678 | 0.012345679012345682 |

유한 검산은 일반 증명을 대신하지 않는다. 미분 및 점근식은 노트의 증명으로 다룬다.
