# 주기 상한·다중 순환의 문헌 비교

- 조사일: 2026-10-29
- 조사자: 작성 세션
- 독립 검토: 미실시
- 결론: 같은 구간 그래프의 독립집합 상한, 3진 매칭의 보편 상한, 인접 하한의 실제 순환 반례는 위키 내부의 새 진전이다. 최종 외부 신규성은 미확인이다.

## 후보 기여를 나누어 평가

1. **초기화 개선:** 터미널 높이의 전부 1인 상태에서 구간 전이 $J$회로 실제 초기 상태를 구한다.
2. **상한 개선:** 실제 초기 상태부터 같은 구간 그래프 $A_c$의 독립집합만 가능하여 $\mu+\lambda\le I(A_c)$이다. 산술 간선 $u,3u$로 매칭을 만들면 $I(A_c)\le3^m2^{r-2m}=12^{r/4}c^{O(1)}$이다.
3. **구체적 반례:** 같은 고정 함수의 실제 게임 두 개가 서로 다른 순환을 선택한다($c=64,65$). 로그 계수의 단조성도 실패한다($c=32,33$).

유한 궤도의 반복, 독립집합 개수의 삭제 점화식, 매칭마다 세 가지를 세는 논증, 일반 유한 동역학의 여러 순환 자체는 알려진 아이디어다. 이 요소들 자체를 새 이론으로 주장하지 않는다.

## 가장 가까운 확인 자료

### Barrett–Chen–Zheng(2004)

“Discrete dynamical systems on graphs and Boolean functions”, Mathematics and Computers in Simulation 66(6), 487–497.

[저자 소속기관 원문](https://cfc.nankai.edu.cn/_upload/article/files/33/c9/99a45e764e18b406dc60b6f33ed6/901466cd-732d-4e1c-a352-0e39e3d20727.pdf).

실제 확인: §5의 Lemma 5.2(출력이 독립집합), Lemma 5.3(표준 모형의 독립집합 위 전단사), Theorems 5.5–5.6(과도 길이와 순환 상태 관계).

이번 노트의 출력 독립성 논증은 이와 같은 유형의 알려진 관찰이다. 다만 이번 전이는 현재 구간 의존과 이전 구간 의존이 서로 다른 마스크여서, 이 논문의 표준 무방향 NOR 모형과 자동으로 같아지지 않는다. 실제 게임에는 길이 1을 넘는 과도가 있으므로 전단사·폭 1 정리를 무근거로 적용하지 않았다. 이번의 $u,3u$ 산술 매칭과 실제 하한별 궤도는 이 논문에서 확인한 대상이 아니다.

### Aledo–Diaz–Martinez–Valverde(2017)

“On periods and equilibria of computational sequential systems”, Information Sciences 409–410, 27–34, DOI 10.1016/j.ins.2017.05.002.

[출판사 페이지](https://www.sciencedirect.com/science/article/abs/pii/S0020025517307132).

실제 확인: 초록, 서론, 공개된 절 요약. 일반 불 순차 동역학에서 서로 다른 길이의 순환 공존을 다룬다. 전체 증명은 읽지 않았다.

따라서 다중 순환이라는 현상 자체는 새 발견이 아니다. 이번 반례의 의미는 약수 게임의 인접한 두 하한이 같은 함수의 다른 순환을 실제로 선택한다는 구체적 인증이다.

### 약수 Nim의 관련 후속 원문 공백

Maeyama–Makino–Ochiai(2017), 「約数ニムのグランディ数(2)」, 早稲田大学数学教育学会誌 35(1), 49–60.
[NDL 서지](https://ndlsearch.ndl.go.jp/books/R000000004-I029975967).

이 서지는 앞선 세션에서 확인했고 본문은 계속 미확인이다. 하한 변형이나 주기 상한을 포함하지 않는다고 단정할 수 없다.

## 검색어와 접근 범위

실제로 사용한 검색어:

- "divisor Nim" "sequential" period
- "NOR" "sequential dynamical systems" periodic
- "divisor game" "logarithmic" density
- "約数ニム" "周期" "下限"
- "sequential dynamical systems" "independent sets" nor Reidys Mortveit pdf
- "divisor nim" "independent sets"
- "Discrete dynamical systems on graphs and Boolean functions" pdf nankai
- "On periods and equilibria of computational sequential systems" pdf authors
- "divisor" "3-adic" "period" game

확인한 검색 범위에서 이번 하한 가족의 산술 매칭 상한이나 $64,65$ 순환 및 $32,33$ 계수의 동일한 진술을 찾지 못했다. 이는 최초 발표의 증거가 아니다.

처음 찾은 CiteSeer 및 일부 기관·저장소 PDF 요청은 502·시간 초과로 실패했다. Barrett 등 원문은 나중에 Nankai 소속기관 공개 PDF로 읽었다. Aledo 등 출판사 열기는 403이었지만 검색 도구가 제공한 출판사 본문에는 초록·서론·절 요약이 있어 그 범위만 확인했다고 기록했다.

## 자체 평가의 한계

보편 상한을 더 작게 했고, 일반 추측 둘을 실제 게임의 무한 꼬리 반례로 부정했다. 그러나 독립집합·매칭·다중 순환이라는 방법론은 알려져 있고, 이번 게임 특유의 결과도 관련 후속 원문과 최종 대조가 끝나지 않았다. 범위가 작은 구조 개선과 정확한 탐색 기록으로 평가한다. 점수 원본과 이력은 [meta.json](meta.json)에만 둔다.
