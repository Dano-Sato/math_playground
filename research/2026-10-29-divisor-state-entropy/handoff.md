# 인수인계: 압축 상태의 지수 장벽과 이진 삼각형 상한

- 작업 ID: 2026-10-29-divisor-state-entropy
- 작성일: 2026-10-29
- 작성자: 연구·조율 에이전트(작성 세션)
- 독립 검토: 미실시
- 추가 에이전트: 실행하지 않음
- [연구노트](note.md) · [문헌 비교](novelty.md) · [평가 원본](meta.json)

## 결과

핵심 명제는 본문에서 증명했고, 정수·유리수 검산으로 보조했다.

1. 최소 변 비율 5/3의 독립 구간에서 현재 압축 공간이 2^(2r/5+O(1))개 이상이다.
   그 크기 자체에 대한 다항식 상한을 반박했다.
2. n을 odd(n−1), odd(n+1)에 잇는 부분그래프 Gamma_r를 구성했다.
3. 계수 a'=a²+b², b'=ab로 beta를 정의하고 불완전 층을 분해해
   beta^r/(64r²) <= i(Gamma_r) <= 6r beta^r를 모든 r>=1에 증명했다.
4. 실제 승패 주기는 lambda <= i(Gamma_r) <= 6r(154171/100000)^r이다.

실제 주기가 지수적이라는 결론이나 C_c 성장률 극한 존재는 얻지 않았다.

## 실제 실행과 출력

Python 3.10 이상, 표준 라이브러리, 난수 없음.

~~~text
python -u research/2026-10-29-divisor-state-entropy/explore.py
~~~

exit 0. [blocks.json](blocks.json) 생성.
고정 아홉 설정 중 일곱 개 완료, 두 개는 200000 부분문제에서 중단했다.
완료한 표시용 밑은 1.709268364214, 1.669620884787, 1.652028982962,
1.648598616089, 1.645520237351, 1.630377435250, 1.627315133868이다.
이 중간 수치들은 최종 상한 증명에 쓰지 않았다.

~~~text
python -u research/2026-10-29-divisor-state-entropy/skeleton.py
~~~

exit 0. [skeleton.json](skeleton.json) 생성.
r=1,2,3,4,8,14,16,32,64,128,256,512,1024,4096의 정확한 계수를 저장했다.
예를 들어 r=14: 438, r=32: 1053681, r=64: 1089025219761이다.
표시용 beta=1.541700913363은 증명에 쓰지 않았다.

~~~text
python -u research/2026-10-29-divisor-state-entropy/verify.py
~~~

exit 0. [verification.json](verification.json) 생성.

~~~text
[A] rational certificate: 1.54168 < beta < 1.54171 PASS
[B] skeleton subgraph/parents/independent band: r=1..256 PASS
[C] Boolean states 131070; generic deletion 40 cases PASS
[D] decomposition 255 cases; rational uniform bounds PASS
[E] complete-level formula 12 cases, r<=4096 PASS
[F] five exact canonical counts lie in the new sandwich PASS
~~~

유리수 인증은 h=12와 로그 급수 16항을 사용한다.
구현 대조와 문헌 검색은 독립 검토가 아니다.

~~~text
python tools/check_wiki.py
~~~

exit 0.

~~~text
PASS: 500 local links in 70 Markdown files.
Templates and code skipped; headings and external URLs not checked.
~~~

git diff --check도 exit 0, 경고 없음이었다. 산출물 JSON 네 파일의 파싱도 통과했다.

## 자체 점검

- r=1의 단일 정점과 r=2의 시작 변을 별도로 확인했다.
- odd(0)을 호출하지 않는다. n=1에는 부모를 정의하지 않고 n=3의 중복 변은 합친다.
- n>=5의 두 부모가 서로 다르고 서로 이미 연결되어 있음을 손으로 증명했다.
- 부분그래프 계수는 C_c 계수의 상한이다. 하한은 실제 C_c의 독립 구간에서 따로 얻었다.
- 마지막 층의 불완전 부분트리는 깊이당 최대 하나이다.
  완전 부분트리 수 s<=p+2, 별도 정점 p<=ceil(log2r)을 확인했다.
- 서로 다른 뿌리 부분트리 사이에는 직접 변이 없다.
  경계·분해 경로를 비우면 곱 하한, 제약을 지우면 곱 상한이 된다.
- 로그 나머지의 2^(-h) 인자와 유리수 비교 방향을 확인했다.
- 전 입력 인자는 6r이고 mu+lambda에는 한 단계를 더한다.
- O(r)은 정수 산술 연산 수이다. 큰 정수의 비트 비용을 상수로 단정하지 않았다.
- 알려진 Farey 구조와 OEIS 수열을 문헌상 새 성과로 기록하지 않았다.

## 위키 반영·정정 제안

새 [노트](note.md)를 Home, ResearchNotes, Topics, ResearchLog에 반영했다.
Q-023 상한을 갱신하고 Q-027을 반박됨으로, 성장률 극한 Q-028을 부분 해결로 등록했다.

앞선 canonical-antichain/note.md의 점근식 두 곳은 줄 시작 O 앞 +가 빠져 있다.
각각 합과 r 계수 뒤에 +O((log c)^2)를 적는 표기 정정을 제안한다.
기존 연구 폴더의 원문을 이번 연구에서 임의로 고치지 않았으며
이번 증명은 그 표시식에 의존하지 않는다.

## 미해결

i(C_c) 성장률 극한, 나머지 gcd 확대 변을 포함하는 작은 경계 동적 계획,
실제 주기의 다항식 상한·지수 하한, 관련 Farey·약수 게임 원문의 직접 대조가 남았다.
