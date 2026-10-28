# 계산 기록: 실수 지수와 비균등 차분

[연구 노트](note.md)

- 연구일: 2026-10-29
- 실행 환경: Python 3.10.11 (Windows)
- 난수 없음. 정수 지수는 Fraction, 반정수 지수는 Decimal.sqrt 사용.

```powershell
python research/2026-10-29-real-power-differences/verify.py
```

```text
PASS: 270 exact polynomial cube-integral identities (s=0,-1,...,-9).
PASS: 135 exact positive-integer exponent sign checks (s=1..5).
PASS: 243 half-integer configurations checked at both 80 and 120 digits.
PASS: 1 unequal-node counterexample.
```

## 입력 범위

a = 1/3, 1, 5/2. 간격 목록은 다음 9개다.

```text
()
('1',)
('1/2',)
('1', '2')
('1/3', '2/3')
('1', '1', '1')
('1/2', '3/2', '2')
('1', '2', '3', '4')
('1/5', '1/4', '1/3', '1/2', '1')
```

반정수 s = -11/2, -9/2, -7/2, -5/2, -3/2, -1/2, 1/2, 3/2, 5/2.

정수 지수 405개 설정은 정확한 검산이다. 반정수 243개 설정은 각기 두 정밀도에서 확인한 수치 관찰이다.
80자리와 120자리 계산은 구간 산술 인증을 대신하지 않는다. 일반적인 부호와 영점은 노트에서 증명했다.
