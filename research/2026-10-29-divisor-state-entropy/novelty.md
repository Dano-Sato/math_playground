# 이진 삼각형 상한의 별도 문헌 조사

- 확인일: 2026-10-29
- 조사자: 작성 세션
- 독립 검토: 미실시
- 결론: 그래프 구성과 재귀 수열은 알려진 내용이다. 약수 게임에 대한 적용의 최종 외부 신규성은 미확인이다.

## 비교할 후보와 확인한 원문

후보는 $C_c$의 두 홀수 부모 부분그래프 포함과
$i(C_c)\le6r\beta^r$, $\beta<1.54171$의 보편 주기 상한이다.
지수 하한은 변의 최소 비율의 짧은 따름정리이므로 큰 독창적 성과로 평가하지 않는다.

### Zhang–Comellas, Farey Graphs as Models for Complex Networks

[arXiv:1105.0575v2 원문](https://arxiv.org/pdf/1105.0575)의
Definition 2.1, 생성 변 설명과 Proposition 2.2를 확인했다.
시작 변에서 새 변마다 다음 단계에 삼각형을 붙이는 구성이 명시되어 있다.
이번 노트의 완전한 경계 부분문제는 같은 구조이다.
이 그래프 가족을 발명했다는 주장은 하지 않는다.

차이는 홀수 n의 odd(n−1), odd(n+1)을 약수 게임의 산술 변에서 고르고,
자연수 순서의 불완전한 마지막 층까지 모든 r의 상한으로 쓰는 적용이다.
그 적용의 선행 발표 여부는 이번 검색으로 확정하지 않았다.

### OEIS A073833, A073834

[분자 수열](https://oeis.org/A073833)과
[분모 수열](https://oeis.org/A073834)의 정의·초기값·재귀를 직접 확인했다.
이번 a_h,b_h는 지표를 하나 옮기면 이 두 수열이다.
분수 y의 y+1/y 반복에서 a'=a²+b², b'=ab가 생기고 서로소성이 보존된다.
첫 항만 비슷한 것이 아니라 전체 수열이 같다.
분자 페이지에는 2008년의 같은 재귀가 명시되어 있다.
재귀나 수열의 재발견을 독창적 결과로 평가하지 않는다.

### Wang–Bao–Zhang(2019), Combinatorial properties of Farey graphs

TCS 796, 70–89,
[학술지 페이지](https://www.sciencedirect.com/science/article/pii/S0304397519305110),
DOI 10.1016/j.tcs.2019.08.022.
검색에 노출된 학술지 초록에서 독립집합의 식·재귀를 다룬다는 점을 확인했다.
열기는 403으로 실패했고 본문 재귀와 상수는 직접 대조하지 못했다.
수열의 그래프 계수 해석까지 처음이라는 주장도 하지 않는다.

### McNew, Counting primitive subsets and other statistics of the divisor graph

[저자 공개 원문](https://www.nathanmcnew.com/PrimitiveSets2.pdf)의
서론과 정리 3의 가정·약수 그래프 정의를 확인했다.
곱셈 구조를 쓰는 계수와 성장률 연구는 이미 있다.
그 그래프는 한 수가 다른 수를 나눌 때 변을 넣는다.
이번 C_c에는 서로 나누지 않는 3,5의 변이 있고,
약수 그래프의 1,45 변은 C_c에 없다.
따라서 그 정리를 C_c 성장률 극한에 자동 적용하지 않았다.
이번 극한 증명의 대상은 부분그래프 Gamma_r이다.

## 실제 검색어와 공백

- primitive sets counting smooth components graph independent sets exponential growth constant Cameron Erdos
- counting multiplicative independent sets finite prime smooth graph components
- "primitive subsets" "smooth" "independent"
- "divisor" "independent sets" "5/3"
- Farey graph independent sets number recurrence a squared b squared
- "Farey graph" "independent" "1.54"
- "Farey" "independence polynomial"
- "2-tree" "independent sets" binary
- "Combinatorial properties of Farey graphs" pdf
- "Farey graphs" "independent sets" arxiv
- "2, 5, 29, 941"
- "1.5417009"
- "969581" "independent"

Angelo의 [arXiv:1711.08107](https://arxiv.org/abs/1711.08107)은 초록과 서지만 읽었다.
그 증명을 읽었다고 기록하지 않는다.
관련 2017년 약수 님 후속 원문의 공백도 앞선 노트에서 계속 남아 있다.

## 평가 판단

위키 내부에서는 상한의 밑·앞 인자가 개선되고 현재 공간 크기의 다항식 가능성도 반박됐다.
그러나 그래프와 수열은 명백히 알려져 있다.
최종 외부 신규성·중요도는 확정하지 않고
[meta.json](meta.json)에 자체 평가와 재평가 조건을 기록한다.
