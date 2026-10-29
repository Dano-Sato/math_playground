# 정규 반사슬·산술 그래프 상한의 문헌 비교

- 확인일: 2026-10-29
- 조사자: 작성 세션
- 독립 검토: 미실시
- 결론: 위키 내부의 새 진술·방법을 확인했다. 최종 외부 신규성은 미확인이다.

## 조사할 후보를 분리

잠재적인 기여는 다음의 **특정 약수 하한 게임에 대한 결합**이다.

1. 폐포 영상의 정확한 개수 $|Q(\mathcal I(A))|=i(C_c)$.
2. $C_c$의 변이 $\gcd$로 약분한 홀수 쌍 $l,s$의 $l=2^ts\pm1$로 결정된다는 산술식.
3. $\{u,3u,5u,9u,15u,45u\}$ 블록 분할에서 얻는
   $\beta=(2^{43}3^85^2)^{1/78}$의 보편 주기 상한.
4. 정규 대표의 원상 수를 유도 부분그래프의 독립집합 수로 세는 식.

유한 부분순서의 극대 원소 대응, 반사슬과 비교 가능성 그래프의 독립집합 대응,
독립집합 삭제 재귀, 그래프 사이의 변을 지워 곱 상한을 얻는 방법 자체는 독창적 원리가 아니다.
부호·계수와 같은 단순 적용상의 변화만으로 외부 신규성을 주장하지 않는다.

## 실제 확인한 원문과 차이

### Stanley, Two Poset Polytopes

[저자 공개 PDF](https://math.mit.edu/~rstan/transparencies/polytopes.pdf),
“Order ideals and antichains”(PDF 99–101쪽)의 대응을 확인했다.
아래 집합의 극대 원소를 취하고 반사슬의 아래 폐포를 취하는 두 사상은 이미 알려진 전단사이다.
따라서 이번 정규화의 기본 원리는 재유도이다.

이번 적용에서는 생성자들이 별도 그래프 $A$의 독립집합이어야 한다.
그 조건이 극대 생성자들에게만 필요하므로 비교 가능성 그래프와 $A$의 합집합으로 환원된다.
이 보조정리는 고전 대응의 짧은 따름정리이며, 이것만으로 큰 독창적 성과로 평가하지 않는다.
후보 차이는 특정 약수 의존 그래프를 산술식과 작은 곱셈 블록으로 구체화한 부분이다.

### Maeyama–Makino–Ochiai(2016)

「約数ニムのグランディ数」, pp.1–5,
[기관 공개 원문](https://www.ns.kogakuin.ac.jp/~ft40433/kumss/20160716-fuzzy-sympo-175-proceedings-r.pdf).
§7–8, 정리 1–2와 이어지는 증명 일부의 추출 본문을 직접 확인했다.
규칙은 1과 자기 자신을 제외한 약수를 빼는 $c=2$이다.
승패 분류와 큰 수의 Grundy 공식을 제시한다.

확인한 본문에서는 일반 하한 $c$의 폐포 개수, 이번 산술 그래프, 여섯 원소 블록 상한을 찾지 못했다.
그러나 이는 확인한 문헌에서의 차이이며, 관련 문헌 전체에서 선행 발표가 없다는 뜻은 아니다.
특히 $c=2$의 결과를 본 노트의 독창성 근거로 삼지 않는다.

### Iannucci–Larsson, Game values of arithmetic functions

[v3 원문](https://arxiv.org/html/2101.07608v3), §1.1.2를 직접 확인했다.
SALIQUOT에서는 $d=1$과 $d=n$을 모두 허용하여 0으로 이동할 수 있다.
따라서 이번 $c\le d<n$, $c\ge2$ 게임과 규칙이 다르다.
그 절의 값 공식을 이번 압축·주기 상한의 선행 정리로 적용하지 않았다.

### Maeyama–Makino–Ochiai(2017), 본문 공백

「約数ニムのグランディ数(2)」,
早稲田大学数学教育学会誌 35(1), pp.49–60.
[NDL 공식 서지](https://ndlsearch.ndl.go.jp/books/R000000004-I029975967)의 제목·저자·연도·쪽수만 확인했다.
본문을 읽지 않았으므로 일반 하한이나 이번 상한이 포함되는지 단정할 수 없다.
이 공백 때문에 최종 외부 신규성 판정을 유보한다.

## 실제 검색어와 접근 실패

- "finite poset" "order ideals" "antichains" bijection maximal elements
- "independent sets" "graph" "clique partition" upper bound
- "independent sets" "I(G-v)" "I(G-N[v])"
- "independent sets" "antichains" "closure" graph
- "divisor game" "antichain"
- "divisor nim" "quotient" independent sets
- "divisor game" Maeyama Makino Ochiai 2016
- "divisor game" "1, 3, 5, 15"
- "divisor" "subtraction" game "period" lower bound divisor
- "約数ニム" "下限"
- "divisor" "game" "antichain" period
- "divisor" game "lower bound" "period"
- "subtraction" "divisor" "737280"
- "2^43" "3^8" "independent" graph
- "divisor" "1.708997"

마지막 수치 검색은 근삿값을 확정하기 전에 사용한 검색어이며,
최종 증명 상수의 근삿값은 1.709268364이다. 검색 부재는 신규성 근거가 아니다.

계수 재귀를 설명하는 [MDPI 문헌](https://www.mdpi.com/2227-7390/12/6/922)은 열기에서 429,
[Dalhousie 학위논문 PDF 주소](https://dalspaceb.library.dal.ca/server/api/core/bitstreams/c903bf10-142c-4ffe-965a-1927ad52197a/content)는 열기에서 시간 초과였다.
검색 결과에 식이 보였지만 해당 본문을 읽은 자료로 기록하지 않았다.
재귀 (5)는 노트에서 경우를 나눠 직접 증명했다.

## 평가와 재평가 조건

이번 노트는 이전 위키의 결과를 단순히 나열하지 않는다.
기존에는 $Z$를 원래 독립집합의 폐포 영상으로 생성했지만,
이번에는 정규 대표와 산술 그래프로 크기를 직접 계산하고,
그 구조에서 보편 지수 상한을 개선했다.

이는 위키 내부의 명확한 진전이다. 다만 일반 대응과 계수 원리는 알려져 있으며,
관련 후속 약수 게임 문헌의 원문 대조가 끝나지 않았다.
검색에서 같은 상한을 찾지 못했다는 이유로 선취가 확인되었다고 하지 않는다.
자체 평가의 원본과 재평가 조건은 [meta.json](meta.json)에 둔다.
