# 신규성 조사

[연구 노트](note.md) · [에이전트 지침의 신규성 조사 규칙](../../AGENTS.md)

- 조사일: 2026-10-29
- 조사자: 조율 에이전트(작성 세션이므로 독립 조사가 아님)
- 계기: 작성 전 "10점 이상을 노릴 수 있는 문제"로 소개했는데 처음 채점(5점)에서 이 규칙의 별도 조사를 생략했다. 사용자가 이를 지적해 사후에 수행한다.

## 검색과 결과

| 검색어(요지) | 결과 |
| --- | --- |
| Rice 적분, 유한 차분, $s$가 $\log n$처럼 자랄 때의 균등 점근 | 직접 다루는 자료 없음. Flajolet–Sedgewick(1995)이 가장 가깝다. 검색 요약에 따르면 $\xi=s\log n$ 형태의 변수 재조정과 안장점 방법의 결합을 언급한다. 원문 PDF는 스캔 이미지라 텍스트를 읽지 못해 내용을 확인하지 못했다. |
| Mellin 점근, $\sum(-1)^k\binom nk(k+a)^{-s}$의 $s$에 대한 최대 | 직접 다루는 자료 없음. Mellin·Rice 방법 일반론(Flajolet–Gourdon–Dumas 1995, Hackl–Wagner 오차 경계 사례 연구, RICA 패키지)만 검색됨. |

## 가장 가까운 선행 결과와의 관계 (조율자 분석)

- **고정 $s$ 점근(알려진 유형):** Rice 방법에서 $z=-a$의 대수·로그 특이점을 처리하면 $F_{n,s}(a)\sim\Gamma(a)(\log n)^{s-1}/(\Gamma(s)n^a)$와 $1/\log n$의 거듭제곱 전개가 나온다. 전개 항은 대략 $\binom{s-1}j(\log n)^{-j}\Gamma^{(j)}(a)$ 꼴이다. 이는 $s$를 고정했을 때의 결과다.
- **이 노트의 영역:** 최대점에서는 $s\approx\log n$이다. 이때 $\binom{s-1}j(\log n)^{-j}\approx1/j!$이 되어 고정 $s$ 전개의 항들이 작아지지 않는다. 즉 기존 전개를 그대로 쓰면 최대점을 얻을 수 없고 재합산이 필요하다. 노트의 표현 $\Gamma(a)\,\mathbb E[(1-\log U/\log n)^{s-1}]$ ($U\sim\mathrm{Gamma}(a)$)이 바로 그 재합산이며, 최대점 부근에서 극한 분포가 Gamma$(a-1)$로 이동하는 것이 핵심 관찰이다.
- **차이:** 기존 결과는 비균등($s$ 고정)이고, 이 노트는 $s=\log n+O(1)$ 창에서 균등한 극한과 최대점 공식 $\log n+\tfrac12-\psi(a-1)$을 준다. 검색 범위에서 이 공식은 찾지 못했다.
- **한계:** 위 고정 $s$ 전개의 정확한 형태는 원문으로 확인한 것이 아니라 방법의 구조에서 추정한 것이다. 또 전문가라면 이 재합산을 짧게 수행할 수 있다. 실제로 노트의 증명은 지배 수렴 한 번과 오목성뿐이다. Flajolet–Sedgewick 원문이나 *Analytic Combinatorics*의 해당 절에 균등 결과가 이미 있을 가능성을 배제하지 못했다.

## 결론과 점수 판단

- 신규성 상태: **선행 결과와의 차이를 구체적으로 설명함 · 최종 신규성 미확인**(가장 가까운 원문 미열람).
- 점수 기준상 신규성 미확인이면 원칙적으로 0–9점이다. 따라서 10점은 주지 않는다. 다만 차이를 구체화했으므로 5점에서 6점으로 조정한다.
- 처음에 "10점 이상을 노릴 수 있다"고 예상한 근거는 이 문제가 정수 지수 결과로부터 바로 나오지 않는 점근 문제라는 점이었다. 실제로는 재합산 표현을 찾자 증명이 짧아졌다. 이 사실 자체가 전문가에게 일상적인 수준일 가능성을 시사한다.
- **10점 이상으로 재평가할 조건:** (1) Flajolet–Sedgewick(1995)과 *Analytic Combinatorics*의 Rice·특이점 절을 읽고 $s\sim\log n$ 균등 결과가 없음을 확인하고, (2) 주장 3($1/\log n$ 보정)을 엄밀히 증명하거나 중간 영역 $a=n^\beta$까지 잇는 통합 정리(Q-017)를 얻는 것.

## 확인한 자료 (확인일 2026-10-29)

- P. Flajolet, R. Sedgewick, *Mellin transforms and asymptotics: Finite differences and Rice's integrals*, Theoret. Comput. Sci. 144 (1995). [PDF](https://algo.inria.fr/flajolet/Publications/FlSe95.pdf). 스캔 이미지라 본문을 읽지 못함. 검색 요약만 확인.
- P. Flajolet, X. Gourdon, P. Dumas, *Mellin transforms and asymptotics: Harmonic sums*. [PDF](https://algo.inria.fr/flajolet/Publications/FlGoDu95.pdf). 검색 요약만 확인.
- B. Hackl, S. Wagner 등, *Binomial Sums and Mellin Asymptotics with Explicit Error Bounds: A Case Study*. [PDF](https://uu.diva-portal.org/smash/get/diva2:1926998/FULLTEXT02.pdf). 검색 요약만 확인.
