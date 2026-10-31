# 로그 계수 발산 하한 인계

- 작업 ID: 2026-10-29-divisor-density-lower-bound
- 담당 범위: 이 연구 폴더. 조율자로서 공용 위키에 링크·질문 상태 반영.
- 독립 검토: 미실시. 작성 세션 자체 점검만 수행.
- 추가 에이전트 실행: 없음.

## 결과

[본문](note.md)에 모든 c의 로그 계수 발산을 손으로 증명했다.
정확한 하한은 r=floor(c/2), R=2r−1에 대해
$\alpha_c\ge r/[48(1+\ln R)^3]$이다.
따라서 $\alpha_c=\Omega(c/(\ln c)^3)$이고 $\ln\alpha_c/\ln c\to1$이다.
고정 전이의 모든 순환에 통하며, 실제 초기 상태를 아는 것이 필요하지 않다.

핵심은 역이동으로 열 가중치를 정확히 세는 식과 시간 평균의 분수 덮개 부등식이다.
체와 정렬을 사용해 c=65536,65537에서 $\alpha_c\ge15839/26$도 인증했다.
이 큰 하한의 실제 순환은 계산하지 않았다.

## 자체 점검

- c=2·3의 r=1, R=1을 별도 확인했다. ln 1은 0이므로 분모가 사라지지 않는다.
- 정상 판·양의 n·고정 c라는 정의역을 유지했다. n=0의 홀수 부분은 사용하지 않았다.
- 열 가중치의 자기 항 2는 현재 자신 1과 반을 빼는 이전 자신 1이다.
- 역이동 n<z≤2n 안에서 같은 홀수 부분이 중복되지 않는 이유를 증명했다.
- 역이동의 작은 약수 하한도 충분히 큰 지수에서 자동 허용됨을 확인했다.
- c=2r과 c=2r+1의 S·가중치는 같지만 평균은 다를 수 있음을 유지했다.
- 빈도는 원래 승패 벡터의 1을 세며 정규 반사슬 대표의 원소 수가 아니다.
- 이차 모멘트 추정은 강한 외부 점근 정리에 의존하지 않고 초등적인 상한부터 증명했다.
- Cauchy–Schwarz에서 f≤1/2의 인자를 확인했다. 역방향으로 쓰지 않았다.
- 선형 하한·단조성·계수 비율의 수렴·다항 주기 상한을 주장하지 않았다.
- 문헌 조사에서 읽은 원문 부분과 초록만 읽은 자료, 미독 후속 논문을 구분했다.

## 실행 명령과 실제 출력

~~~text
python research/2026-10-29-divisor-density-lower-bound/explore.py

c=2: alpha=1/2, max-bound=1/2, moment-bound=1/2, capacity=1/2, max-w=2
c=4: alpha=2/3, max-bound=2/3, moment-bound=4/9, capacity=2/3, max-w=3
c=16: alpha=5/2, max-bound=8/7, moment-bound=64/87, capacity=7/5, max-w=7
c=32: alpha=11/2, max-bound=16/9, moment-bound=256/215, capacity=9/4, max-w=9
c=64: alpha=19/2, max-bound=32/11, moment-bound=512/311, capacity=53/16, max-w=11
c=128: alpha=39/2, max-bound=4, moment-bound=4096/1605, capacity=49/9, max-w=16
c=256: alpha=81/2, max-bound=128/21, moment-bound=8192/2103, capacity=26/3, max-w=21
c=512: alpha=161/2, max-bound=256/25, moment-bound=65536/10467, capacity=186/13, max-w=25
PASS: 511 models; 1142 periodic states
sieve r=512: max-w=33, capacity=410/17
sieve r=1024: max-w=41, capacity=1507/38
sieve r=4096: max-w=64, capacity=2931/25
sieve r=16384: max-w=97, capacity=3857/11
sieve r=32768: max-w=121, capacity=15839/26
~~~

~~~text
python research/2026-10-29-divisor-density-lower-bound/verify.py

[A] 2080 direct reverse-move columns PASS
[B] 8190 Boolean states; 25 complete cycles PASS
[C] 96 saved cycles; 223 states PASS
[D] divisor moment n<=4096; harmonic 128; geometric 33 PASS
[E] 5 graph-free sieve bounds r<=32768 PASS
~~~

Python 3.10 이상, 표준 라이브러리, 정수·유리수 계산, 난수 없음.
기존 계산 코드는 수정하지 않고 import하여 대조했다.

공용 위키와 파일 검사 실제 결과:

~~~text
python tools/check_wiki.py
PASS: 570 local links in 78 Markdown files.
Templates and code skipped; headings and external URLs not checked.

git diff --check
exit 0, whitespace errors 없음

JSON parse check
PASS: 4 JSON files parsed
~~~

기존 다른 메타데이터 파일의 LF→CRLF 안내는 검사 실패가 아니다.
위키 검사기는 외부 링크 접속이나 수학적 정확성을 판정하지 않는다.

## 남은 사항

- 선형 하한 $\alpha_c\ge\kappa c$의 참·거짓.
- 행 제약을 유지한 분수 덮개의 더 강한 하한.
- 특정 약수 게임 결과의 외부 신규성. [novelty.md](novelty.md) 참조.
- 독립 검토는 미실시이며 기본 절차로 추가 실행하지 않았다.

## 공용 위키에 추가할 링크

- [Home](../../wiki/Home.md), [ResearchNotes](../../wiki/ResearchNotes.md),
  [ResearchLog](../../wiki/ResearchLog.md), [Topics](../../wiki/Topics.md).
- [Questions](../../wiki/Questions.md): Q-023에 계수 하한 연결,
  Q-029 발산 질문 해결, Q-030 선형 하한 질문 등록.
