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

## 1차 결론과 점수 판단 (2차 조사로 대체됨)

- 신규성 상태: **선행 결과와의 차이를 구체적으로 설명함 · 최종 신규성 미확인**(가장 가까운 원문 미열람).
- 점수 기준상 신규성 미확인이면 원칙적으로 0–9점이다. 따라서 10점은 주지 않는다. 다만 차이를 구체화했으므로 5점에서 6점으로 조정한다.
- 처음에 "10점 이상을 노릴 수 있다"고 예상한 근거는 이 문제가 정수 지수 결과로부터 바로 나오지 않는 점근 문제라는 점이었다. 실제로는 재합산 표현을 찾자 증명이 짧아졌다. 이 사실 자체가 전문가에게 일상적인 수준일 가능성을 시사한다.
- **10점 이상으로 재평가할 조건:** (1) Flajolet–Sedgewick(1995)과 *Analytic Combinatorics*의 Rice·특이점 절을 읽고 $s\sim\log n$ 균등 결과가 없음을 확인하고, (2) 주장 3($1/\log n$ 보정)을 엄밀히 증명하거나 중간 영역 $a=n^\beta$까지 잇는 통합 정리(Q-017)를 얻는 것.

## 2차 조사: 기하분포 합의 최빈값으로 다시 보기 (2026-10-29)

사용자 요청으로 추가 조사했다.

### 핵심 관찰 (증명됨, 정확한 유리수로 확인)

$a>1$이면 $x_j=1/(a+j)\in(0,1)$이다. 서로 독립인 $G_j\sim\mathrm{Geom}(x_j)$, $\Pr(G_j=m)=(1-x_j)x_j^m$에 대해 $K=\sum_{j=0}^nG_j$로 두면 $\Pr(K=k)=h_k(x)\prod_j(1-x_j)$이다. 이전 노트의 $F_{n,r}(a)=b_n(a)h_{r-1}(x)$와 합치면

$$
F_{n,r}(a)=\frac{b_n(a)}{\prod_j(1-x_j)}\Pr(K=r-1).
$$

즉 **정수 최대점은 $K$의 최빈값 + 1**이다($n=6$, $a=5/2$, $k\le12$에서 비율이 상수임을 정확한 유리수로 확인). 또 확률생성함수는

$$
\mathbb E[t^K]=\prod_{j=0}^n\frac{a+j-1}{a+j-t}=\frac{\Gamma(a+n)\,\Gamma(a-t)}{\Gamma(a-1)\,\Gamma(a+n+1-t)}\sim n^{t-1}\frac{\Gamma(a-t)}{\Gamma(a-1)}
$$

이다. 이는 $\lambda_n=\log n$, 극한함수 $\Phi(t)=\Gamma(a-t)/\Gamma(a-1)$인 mod-Poisson 수렴 구조다.

### 가장 가까운 선행 결과

- **Kabluchko–Marynych–Sulzbach, 일반 Edgeworth 전개(arXiv:1606.03920) Theorem 2.10.** $W_n(\beta)=e^{-\phi(\beta)w_n}\sum_kL_n(k)e^{\beta k}\to W_\infty(\beta)$ (가정 A1–A4)이면, 큰 $n$에서 최빈값이 $\{\lfloor u_n^*\rfloor,\lceil u_n^*\rceil\}$ 안에 있다. 여기서 $u_n^*=\phi'(0)w_n+(\log W_\infty)'(0)-\phi'''(0)/(2\phi''(0))$이다(ar5iv 판에서 진술 확인, 증명 미확인).
  - $L_n(k)=\Pr(K=k)$, $\phi(\beta)=e^\beta-1$, $w_n=\log n$, $W_\infty(\beta)=\Gamma(a-e^\beta)/\Gamma(a-1)$를 넣으면 $u_n^*=\log n-\psi(a-1)-\tfrac12$이다.
  - 이는 이 노트 정리 2의 위치와 **정확히 일치**한다(정수 최대점 $=$ 최빈값 $+1$).
  - 가정 A2–A4의 성립 여부는 조율자가 확인하지 않았다. 그러나 수렴 속도가 $O(1/n)=e^{-w_n}$이고, $|e^\beta|<a$에서 $\Gamma(a-e^\beta)$가 해석적이고 0이 아니라는 점에서 적용 가능성이 높다.
- **같은 저자들의 Ewens 분포·제1종 Stirling 수 논문**(J. Integer Seq. 19 (2016), 16.8.8). 최빈값 $\theta\log n-\theta\psi(\theta)-\tfrac12$를 위 일반 정리로 얻는다.
  - 이 노트에서 $a=2$이면 $K$의 최빈값 위치가 $\log n+\gamma-\tfrac12$로, $\theta=1$의 Stirling 수 결과와 같은 식이 된다.
  - 이 논문은 Hammersley(1951), Erdős(1953)의 고전적 결과를 잇는다. 최빈값이 가장 가까운 정수가 되는 $n$의 밀도가 1이지만 무한히 많은 예외가 있다는 결과도 포함한다. 이 노트에서 반정수 근처의 예외(42개 중 1개)가 나타난 것과 같은 현상이다.

### 판단

- **정리 2(정수 최대점)는 알려진 일반 정리(KMS Thm 2.10)의 직접 적용으로 보인다.** 같은 위치 공식이 알려진 틀에서 바로 나온다.
- **정리 1(실수 최대점 $s^*_n$)**은 정수 최빈값이 아니라 $s$를 실수로 보간한 최대점이므로 KMS의 진술 자체는 아니다. 하지만 같은 메커니즘의 연속판이며 새 아이디어는 크지 않다.
- 주장 3($1/\log n$ 보정)도 KMS의 Edgeworth 전개가 같은 종류의 보정을 체계적으로 준다.
- 따라서 6점 → 4점으로 낮춘다. 10점 이상의 근거는 남지 않았다.

### 확인한 자료 (확인일 2026-10-29)

- Z. Kabluchko, A. Marynych, H. Sulzbach, *General Edgeworth expansions with applications to profiles of random trees*, [arXiv:1606.03920](https://arxiv.org/abs/1606.03920). Theorem 2.10과 가정 A1–A4의 진술을 [ar5iv 판](https://ar5iv.labs.arxiv.org/html/1606.03920)에서 요약 도구로 확인.
- Z. Kabluchko, A. Marynych, H. Sulzbach, *Mode and Edgeworth expansion for the Ewens distribution and the Stirling numbers*, J. Integer Seq. 19 (2016), Article 16.8.8. [초록](https://cs.uwaterloo.ca/journals/JIS/VOL19/Kabluchko/kabl2.html), [TeX 원문](https://ftp6.gwdg.de/pub/EMIS/journals/JIS/VOL19/Kabluchko/kabl2.tex)에서 주정리·증명 방법·참고문헌 확인.
- Dal Borgo–Méliot–Nikeghbali, *Local limit theorems and mod-φ convergence*, [arXiv:1710.10679](https://arxiv.org/pdf/1710.10679), 검색 결과로만 확인.

## 1차 조사의 자료

- P. Flajolet, R. Sedgewick, *Mellin transforms and asymptotics: Finite differences and Rice's integrals*, Theoret. Comput. Sci. 144 (1995). [PDF](https://algo.inria.fr/flajolet/Publications/FlSe95.pdf). 스캔 이미지라 본문을 읽지 못함. 검색 요약만 확인.
- P. Flajolet, X. Gourdon, P. Dumas, *Mellin transforms and asymptotics: Harmonic sums*. [PDF](https://algo.inria.fr/flajolet/Publications/FlGoDu95.pdf). 검색 요약만 확인.
- B. Hackl, S. Wagner 등, *Binomial Sums and Mellin Asymptotics with Explicit Error Bounds: A Case Study*. [PDF](https://uu.diva-portal.org/smash/get/diva2:1926998/FULLTEXT02.pdf). 검색 요약만 확인.
