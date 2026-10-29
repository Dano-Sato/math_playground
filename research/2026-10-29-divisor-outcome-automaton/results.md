# 실제 실행 기록

- 실행일: 2026-10-29
- Python 3.10.11, Windows PowerShell
- 표준 라이브러리, 정확한 정수·유리수, 난수 없음
- 범위: $2\le c\le64$, 직접 위치 $n\le65536$, 각 궤도 최대 100,000상태

명령:

~~~powershell
python research/2026-10-29-divisor-outcome-automaton/verify.py
~~~

종료 코드 0. 실제 최종 출력:

~~~text
c=2: r=1, H=2, mu=0, period=2, alpha=1/2
c=3: r=1, H=4, mu=0, period=2, alpha=1/2
c=4: r=2, H=4, mu=0, period=3, alpha=2/3
c=5: r=2, H=6, mu=0, period=3, alpha=2/3
c=6: r=3, H=6, mu=0, period=2, alpha=1
c=7: r=3, H=6, mu=0, period=2, alpha=1
c=8: r=4, H=6, mu=0, period=2, alpha=3/2
c=9: r=4, H=8, mu=0, period=2, alpha=3/2
c=10: r=5, H=8, mu=0, period=2, alpha=3/2
c=11: r=5, H=8, mu=0, period=2, alpha=3/2
c=12: r=6, H=8, mu=0, period=2, alpha=2
c=13: r=6, H=8, mu=1, period=2, alpha=2
c=14: r=7, H=8, mu=1, period=2, alpha=5/2
c=15: r=7, H=8, mu=4, period=2, alpha=5/2
c=16: r=8, H=8, mu=3, period=2, alpha=5/2
c=32: r=16, H=10, mu=4, period=2, alpha=11/2
c=64: r=32, H=12, mu=3, period=8, alpha=19/2
[A] direct outcome comparisons: 4128768 PASS
[B] regenerated small-odd successor edges: 17184 PASS
[C] exponent-1000 periodicity checks: 1024 PASS
[D] c=4 hand formula: 5005 checks PASS
[D2] exact counting comparisons: 812 PASS; c=4, N=2^1000 has 668 even losing positions
[E] largest observed period: 8 at c=64
ALL CHECKS PASSED; wrote report.json
~~~

추가로 [report.json](report.json)의 $c=64$ 순환을 읽어, 높이 14부터 $o=35$ 좌표가 10000000으로 반복됨을 확인했다. $\ell(35)=5$이므로 이는 $k\ge9$에서 $k\equiv1\pmod8$일 때만 P라는 뜻이다.

$c=2,\ldots,64$에서 최대 초기 길이는 9였고 $c=53$에서 나타났다. 이 범위 밖의 초기 길이 상한을 9라고 주장하지 않는다.

## 저장 자료와 위키 검사

report.json의 63개 행에서 $0<\alpha_c\le r/2$와 $\mu+\lambda\le2^r$를 유리수·정수 연산으로 재확인했고, meta.json의 자체 채점 상태와 JSON 파싱도 확인했다. 실제 출력:

~~~text
PASS: 63 report rows, coefficient bounds, state bounds, metadata.
~~~

명령:

~~~powershell
python tools/check_wiki.py
git diff --check
~~~

위키 검사 종료 코드 0:

~~~text
PASS: 379 local links in 56 Markdown files.
Templates and code skipped; headings and external URLs not checked.
~~~

추적 중인 공용 문서의 차이 공백 검사도 오류 출력 없이 통과했다. 링크 검사는 수학적 정확성이나 외부 URL을 검사하지 않는다.
