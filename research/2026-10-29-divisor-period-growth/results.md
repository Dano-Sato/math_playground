# 실제 실행 기록

- 실행일: 2026-10-29
- 환경: Windows PowerShell, Python 3.10.11
- 표준 라이브러리, 정확한 정수·유리수, 난수 없음
- 탐색: c=2..512, 각 궤도 최대 20,000상태

## 탐색

~~~powershell
python research/2026-10-29-divisor-period-growth/explore.py
~~~

종료 코드 0, 실제 출력:

~~~text
period record c=2: mu=0, period=2, alpha=1/2
period record c=4: mu=0, period=3, alpha=2/3
period record c=64: mu=3, period=8, alpha=19/2
checkpoint c=64: mu=3, period=8, alpha=19/2
checkpoint c=128: mu=4, period=2, alpha=39/2
checkpoint c=256: mu=6, period=2, alpha=81/2
checkpoint c=512: mu=4, period=2, alpha=161/2
max preperiod: (10, 466)
distinct periods: [2, 3, 6, 8]
Wrote periods.json (c=2..512)
~~~

## 검증

~~~powershell
python research/2026-10-29-divisor-period-growth/verify.py
~~~

종료 코드 0, 실제 출력:

~~~text
[A] c=2..512: 2840 orbit states and matching bounds PASS
[B] terminal-shell seeds vs previous direct seeds: 63 PASS
[C] identical stationary maps for adjacent pairs: 255 PASS
[I] c=4: I(A)=3, raw=4, recurrence subproblems=3
[I] c=28: I(A)=287, raw=16384, recurrence subproblems=57
[I] c=32: I(A)=858, raw=65536, recurrence subproblems=64
[I] c=64: I(A)=401846, raw=4294967296, recurrence subproblems=1835
[D] exhaustive independent-set masks: 81924 PASS
[E] direct outcome comparisons: 393216 PASS
[F] periods 8/6, alpha decrease, and power-of-two witnesses PASS
ALL CHECKS PASSED; wrote certificate.json
~~~

생성 자료는 [periods.json](periods.json)과 [certificate.json](certificate.json)이다. 전자의 범위 밖 하한의 분포는 계산하지 않았다. 후자의 순환이 닫힌다는 유한 인증과 보편 전이 정리가 각 사례의 무한 꼬리를 보장한다.

## 자료 형식과 위키 검사

JSON 파싱, 자체 채점 상태, 탐색 511행과 핵심 순환 인증 7개를 확인했다.

~~~text
PASS: metadata, 511 parameter rows, 7 cycle certificates.
~~~

명령:

~~~powershell
python tools/check_wiki.py
git diff --check
~~~

위키 검사 종료 코드 0, 실제 출력:

~~~text
PASS: 409 local links in 60 Markdown files.
Templates and code skipped; headings and external URLs not checked.
~~~

추적 중인 문서의 공백 검사도 오류 출력 없이 통과했다. 위키 검사 자체는 수학적 주장과 외부 URL을 검사하지 않는다.
