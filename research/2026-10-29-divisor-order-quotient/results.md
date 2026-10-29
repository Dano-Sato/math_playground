# 실제 실행 기록

- 실행일: 2026-10-29
- Python 3.10.11, Windows PowerShell
- 표준 라이브러리, 정확한 정수·유리수, 난수 없음
- 구조 점검 c=2..512, 전체 분류 c=4,28,32,64

## 압축 전이 탐색

~~~powershell
python research/2026-10-29-divisor-order-quotient/explore.py
~~~

종료 코드 0, 실제 최종 출력:

~~~text
c=4: independent=3, quotient=3, image=3, cycles={3: 1}
  image sizes=[3]; max quotient transient=0
c=28: independent=287, quotient=249, image=46, cycles={2: 6}
  image sizes=[249, 46, 24, 16, 12]; max quotient transient=4
c=32: independent=858, quotient=708, image=115, cycles={2: 14}
  image sizes=[708, 115, 58, 37, 31, 29, 28]; max quotient transient=6
c=64: independent=401846, quotient=229649, image=6287, cycles={2: 68, 6: 6, 8: 1}
  image sizes=[229649, 6287, 1536, 684, 382, 284, 234, 208, 194, 188, 183, 181, 180]; max quotient transient=12
Wrote quotients.json
~~~

## 별도 검증

~~~powershell
python -u research/2026-10-29-divisor-order-quotient/verify.py
~~~

종료 코드 0, 실제 최종 출력:

~~~text
[A] exact order heights and transitivity: 511 maps PASS (377 have height 3)
[B] closure/factorization samples: 2555 PASS; actual-game quotient orbits: 511 PASS
[C] c=4: cycles={3: 1}, max_mu=0, max(mu+period)=3 PASS
[C] c=28: cycles={2: 6}, max_mu=4, max(mu+period)=6 PASS
[C] c=32: cycles={2: 14}, max_mu=6, max(mu+period)=8 PASS
[C] c=64: cycles={2: 68, 6: 6, 8: 1}, max_mu=12, max(mu+period)=18 PASS
[D] independently generated independent-set states: 402994 PASS
[E] complete Boolean-state comparison (r<=16): 81924 PASS
ALL CHECKS PASSED; wrote verification.json
~~~

[verification.json](verification.json)의 마지막 극값 증인은 상태 705202697, 과도 길이 12, 최소 주기 6이다. [quotients.json](quotients.json)의 순환별 평균 분포도 본문의 표와 대조해 일치했다.

완전 분류 범위 밖의 큰 c에 대해서는 모든 순환을 열거하지 않았다. 32비트 전체 불 공간의 순환 완전성은 모든 순환이 독립집합에 포함된다는 손 증명으로 범위를 줄인 뒤, 그 집합을 빠짐없이 열거하여 얻었다.

## 자료 형식과 위키 검사

JSON 파싱, 자체 채점 상태, 네 사례의 완전 분류, 마지막 사례의 순환 75개·주기점 180개 및 극값 18을 재확인했다.

~~~text
PASS: metadata, 4 complete classifications, 75 cycles, 180 periodic states, extremum 18.
~~~

명령:

~~~powershell
python tools/check_wiki.py
git diff --check
~~~

위키 검사 종료 코드 0:

~~~text
PASS: 443 local links in 64 Markdown files.
Templates and code skipped; headings and external URLs not checked.
~~~

추적 중인 문서의 공백 검사도 오류 출력 없이 통과했다. 위키 검사 자체는 수학적 정확성과 외부 URL을 검사하지 않는다.
