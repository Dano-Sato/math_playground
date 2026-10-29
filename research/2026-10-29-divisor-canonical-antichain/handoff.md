# 인수인계: 정규 반사슬과 압축 상태 계수

- 작업 ID: 2026-10-29-divisor-canonical-antichain
- 작성일: 2026-10-29
- 작업자: 연구·조율 에이전트(작성 세션)
- 독립 검토: 미실시
- 추가 에이전트 실행: 없음
- 본문: [note.md](note.md), 문헌 조사: [novelty.md](novelty.md)
- 평가 원본: [meta.json](meta.json)

## 이번 결과

핵심 주장은 본문에 완결된 증명을 제시하여 모두 증명됨으로 표시했다.

1. $Q(\mathcal I(A))$의 정규 대표는 $A$와 순서 비교 그래프의 합집합 $C_c$의 독립집합이다.
2. 합집합 그래프의 변은 gcd로 약분한 홀수 쌍의 $l=2^ts\pm1$ 조건과 같다.
3. 압축 전이를 정규 대표로 공액 표현하여 이전 폐포 공간과 전체 함수 그래프를 보존한다.
4. 여섯 원소 곱셈 블록으로 정확한 유한 곱 상한과
   $(2^{43}3^85^2)^{r/78}\exp(O((\log c)^2))$의 보편 상한을 얻었다.
5. 대표별 원상 수를 유도 부분그래프의 독립집합 수로 표현했다.

$c=128$의 36,489,348,992개 압축 상태 크기 계산과 검증 범위는
유한 계산 결과로 따로 표시했다. $c=128$의 모든 상태나 순환을 열거한 것은 아니다.

## 실제 실행 명령과 결과

Python 표준 라이브러리, 난수 없음.

~~~text
python -u research/2026-10-29-divisor-canonical-antichain/explore.py
~~~

정상 종료, exit 0. [counts.json](counts.json) 생성.

| c | 정확한 압축 상태 수 | 첫 계수 부분문제 | 여섯 원소 블록 곱 상한 |
| --- | --- | --- | --- |
| 4 | 3 | 2 | 3 |
| 28 | 249 | 25 | 2,304 |
| 32 | 708 | 33 | 9,216 |
| 64 | 229,649 | 328 | 35,389,440 |
| 128 | 36,489,348,992 | 20,102 | 626,206,231,756,800 |

~~~text
python -u research/2026-10-29-divisor-canonical-antichain/verify.py
~~~

최종 코드 정상 종료, exit 0. [verification.json](verification.json) 생성.

~~~text
[A] arithmetic/direct-move graph equality: 511 maps, 5559680 pairs PASS
[B] maxima projection: 2044 samples PASS; six-block count formulas: 3066 cases PASS
[C] c=4: originals 3, representatives 3, cycles {3: 1}, every fiber formula PASS
[C] c=28: originals 287, representatives 249, cycles {2: 6}, every fiber formula PASS
[C] c=32: originals 858, representatives 708, cycles {2: 14}, every fiber formula PASS
[C] c=64: originals 401846, representatives 229649, cycles {2: 68, 6: 6, 8: 1}, every fiber formula PASS
[D] originals 402994, canonical 230609, full cube 81924 PASS
[E] c=128 alternate counting 36489348992, subproblems 4192 PASS
[F] six-block exponential base (display only): 1.709268364
~~~

첫 검산 실행의 최소 차수 분기는 c=128에서 10,496,284개 부분문제로 동일한 값에 도달했다.
이 비용을 줄이고 탐색을 명시적으로 제한하기 위해 최대 차수의 다른 동률 선택과
연결 성분 분리로 수정한 뒤 위 명령을 다시 실행했다.
최종 두 계수기 모두 입력마다 부분문제 상한 200,000개를 둔다.

~~~text
python tools/check_wiki.py
~~~

정상 종료, exit 0.

~~~text
PASS: 469 local links in 67 Markdown files.
Templates and code skipped; headings and external URLs not checked.
~~~

추가로 git diff --check를 실행하여 종료 0, 경고 없음을 확인했다.

## 자체 점검

- $c=2$와 $c=3$: 한 좌표, 자기 관계는 그래프 고리에서 제외하고 공집합 포함 두 대표를 센다.
- 폐포를 생성하는 극대 원소 집합의 유일성에는 유한성이 필요하며 본문에 명시했다.
- 폐포의 모든 아래 집합이 가능한 것은 아니다. 극대 원소의 $A$-독립 조건을 보존했다.
- 극대 원소 투영 $M$은 감소 사상이지 일반적인 단조 폐포가 아니다. 단조성을 가정하지 않았다.
- 산술 변의 양방향 증명에서 약분한 홀수 쌍과 연속 정수를 대응시켰다.
  역방향 이동은 충분한 2배 확대 후 하한을 충족하고 같은/직전 구간에 들어간다.
- 여섯 원소 블록은 v3의 3잔여류와 v5의 2잔여류로 분할하여 서로 겹치지 않는다.
  $c$에 잘린 작은 블록까지 각각 세었으며 6개가 다 있다고 가정하지 않았다.
- 블록 전체 그래프는 K6에서 한 변만 빠진 그래프이다. 첫 다섯 원소는 K5이다.
- 밑수 밀도 오차는 O(log²t), 최종 인자는 exp(O(log²c))로 유지했다.
  다항식 오차 인자나 다항식 주기 상한을 주장하지 않았다.
- μ+λ 상한의 +1은 복원 과도 한 단계이며, 고정 전이의 초기 상태가 I(A)에 속하는 범위로 적었다.
- 압축 비트의 개수를 원래 패배 좌표 수로 해석하지 않았다. 로그 계수 α의 일반식은 미해결이다.
- 원상 수 공식은 공집합에도 성립하며, 작은 모든 대표에서 직접 원상 개수와 대조했다.
- 두 구현 대조는 작성 세션의 자체 점검이다. 독립 에이전트나 외부 전문가 검토로 표기하지 않았다.

## 위키 반영

반영 완료한 링크:
[정규 반사슬과 산술 그래프](note.md).

- Home.md 최근 연구에 추가.
- ResearchNotes.md에 노트와 평가 원본 연결.
- Topics.md에 그래프·부분순서·게임 주제로 추가.
- Questions.md의 Q-023에 새 상한을 연결하고 Q-026(열거 없는 압축 상태 계수)을 해결 상태로 등록.
- ResearchLog.md에 증명·계수·검산 범위와 독립 검토 미실시를 기록.

## 미해결·재평가

- 외부 신규성은 미확인. 관련 2017년 약수 님 후속 원문을 읽지 못한 공백이 남는다.
- 더 큰 곱셈 블록의 최적 선택, i(C_c)의 정확한 점근 성장률, T(Z) 크기,
  가중 흡인 영역 계수, 다항식 주기 상한, 전체 Grundy 문턱은 미해결이다.
- 자체 채점 원본은 meta.json이며 다른 Markdown 파일에 점수를 중복하지 않았다.
