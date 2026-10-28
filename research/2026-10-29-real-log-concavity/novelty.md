# 신규성 조사

[연구 노트](note.md) · [에이전트 지침의 신규성 조사 규칙](../../AGENTS.md)

- 조사일: 2026-10-29
- 조사자: 조율 에이전트(노트 작성자와 같은 세션이므로 독립 조사가 아님)
- 계기: AGENTS.md에 추가한 규칙 "10점 이상의 잠재적 성과가 있는 노트는 가장 가까운 선행연구와 비교하여 신규성을 별도로 조사한다." 이 노트는 위키의 열린 질문 두 개(Q-010, Q-012)를 날카로운 상수와 함께 해결하므로 10점 이상 가능성이 있다고 판단했다.

## 비교 대상으로 삼은 주장

1. 정리 2: $n\ge1$, $a>0$, 임의의 양의 간격에서 $-\sum_{i<n}(s+i)^{-2}<(\log D_{\mathbf h}(a,s))''<0$ ($s>0$). 양 끝 상수가 날카로움.
2. 따름정리 3: 실수 간격 $\delta$의 비율 경계.
3. 따름정리 4: 실수 지수 단봉성과 정수 최대점.

## 사용한 검색과 결과

웹 검색 도구 사용(2026-10-29). 검색어와 결과는 다음과 같다.

| 검색어(요지) | 결과 |
| --- | --- |
| power function $x^p$ 분할 차분의 지수 $p$ 방향 로그 오목성 | 직접 다루는 자료 없음. 가장 가까운 것은 i.i.d. 평균 적률의 **$n$ 방향** 로그 오목·볼록성(arXiv:2001.06439)으로 대상이 다름. |
| $\sum(-1)^k\binom nk(x+k)^{-s}$의 $s$ 방향 로그 오목성 | 직접 다루는 자료 없음. 이항계수·조합 수열의 인덱스 방향 로그 오목성 자료만 검색됨. |
| Stolarsky 평균, 분할 차분, 매개변수 로그 볼록성(Pečarić 등) | 분할 차분으로 만든 지수 볼록(exponentially convex) 함수와 Stolarsky형 평균 연구군이 존재(예: Roqia–Pečarić–Vukelić, *Math. Inequal. Appl.* 16, 논문 82). 이번에는 초록·본문을 열람하지 못해 정확히 어떤 함수족의 $p$ 방향 로그 볼록성을 다루는지 확인하지 못함. |
| Mellin 변환, B-스플라인, Borell, Hermite–Genocchi | Berwald–Borell 부등식(로그 오목 측도의 Mellin 변환을 $\Gamma$로 나누면 로그 오목) 서술을 Klartag–Lehec(arXiv:1802.04176)에서 확인. B-스플라인 로그 오목성(Floater 노트), B-스플라인 적률과 분할 차분의 관계(de Boor 노트)가 검색됨. 이 결합으로 교대합의 지수 방향 곡률을 다룬 자료는 찾지 못함. |

## 가장 가까운 선행 결과와의 비교

1. **Borell 보조정리**(Borell 1973; Fradelizi–Li–Madiman 2020, Prop. 3.2에서 확인). $s$-오목 함수의 Mellin 변환을 베타 함수로 정규화하면 로그 오목하다. 이 노트의 보조정리 A는 그 점별·엄격형이며 **새 기여가 아니다**.
2. **정규화 분할 차분의 로그 볼록성.** $(\log D)''>-\sum(s+i)^{-2}$, 즉 $D/(s)_n$의 로그 볼록성은 양수 측도의 적률이라는 사실에서 바로 나온다. Pečarić 학파의 지수 볼록성 결과들이 이 방향을 포함할 가능성이 높다(본문 미확인). 이 하계는 **알려진 것으로 취급**하는 것이 안전하다.
3. **위키 내부 선행 결과**(정수 지수, 균등 간격). [앞선 노트 주장 3](../2026-10-29-turan-unimodality/note.md)은 대칭함수 방법으로 정수 $r$에서 같은 상수를 얻었다. 이 노트는 그것을 실수 지수·실수 간격·비균등 간격으로 확장한다.

**이 노트에서 구별되는 부분:** 교대 차분 $D_{\mathbf h}(a,s)$를 "$(s)_n\times$ ($1/(n-1)$-오목 함수의 Mellin 변환)"으로 쓰는 관찰(정육면체 단면의 Brunn 정리 + 원근 변환)과, 그 결과로 얻는 실수 지수 로그 오목성 및 양면 날카로운 상수. 검색 범위에서 같은 진술은 찾지 못했다.

## 2차 조사 (2026-10-29, 10점 이상 후보 여부 판단)

계기: 다른 에이전트가 10점 이상 후보일 수 있다고 제안해 사용자가 재검토를 요청함. 두 기준을 확인했다.

### 1. 증명 오류

- v1은 별도 에이전트의 [독립 검토](../2026-10-29-real-log-concavity-review/review.md)에서 핵심 증명에 오류·간극이 없다고 판정받았다.
- v1.1의 수정분(§3 부호 구조 문장, §8 범위)은 조율자가 다시 확인했다. $\beta\le c$, $c<\beta<d$, $\beta\ge d$ 세 경우 모두 $P$가 구간이며 결론은 그대로다.
- 판정: **통과**. 다만 v1.1 재검토는 자체 점검이다.

### 2. 문헌상 신규성

추가 검색: Dirichlet 평균·Carlson $R$ 함수(지수 방향 성질), Hurwitz 제타·완전 단조성·Turán형 부등식.

- **Fradelizi–Li–Madiman Prop. 3.2의 $s=0$ 경우**($C_0(p)=1/\Gamma(p)$, 로그 오목 $\varphi$, $p\in[0,\infty)$)를 원문 요약으로 재확인했다. $D_{\mathbf h}(a,s)=\Gamma(s)^{-1}\int t^{s-1}e^{-at}\prod(1-e^{-h_it})dt$이고 피적분 인자는 로그 오목하므로 **Q-010·Q-012의 로그 오목성은 한 줄짜리 따름정리**다. 1차 조사에서 이 경로를 놓쳤다.
- **Yang(2025, arXiv:2507.10954) Theorem 2:** $t^\theta f(t)$가 로그 오목(볼록)이면 감마 비율 상수를 가진 Turán형 부등식이 성립한다. Hurwitz 제타에 대해서는 $p\mapsto(p-1)\zeta(p,x)$의 로그 오목성과 양면 Turán 경계를 명시한다. $\Gamma(s)\zeta(s,a)=\int t^{s-1}e^{-at}(1-e^{-t})^{-1}dt$이므로 이것은 같은 틀의 이웃 사례이고, 우리 $f=(1-e^{-t})^n$에 적용하면 따름정리 3의 양면 경계가 나온다(조율자 계산).
- Carlson $R$ 함수 쪽에서는 지수 방향 로그 오목성을 명시한 자료를 찾지 못했다(Carlson 1987 *Dirichlet averages of $x^t\log x$* 등은 미열람).

### 2차 결론

- 증명 정확성은 통과했지만 **문헌 기준은 통과하지 못했다.** 노트의 주정리는 알려진 Berwald–Borell 부등식의 직접적 따름정리이고, 양면 비율 경계도 2025년 프리프린트의 일반 정리에서 나온다.
- 남는 기여는 점별·엄격한 곡률 경계와 등호·날카로움 분석, 비균등 간격 교대합으로의 명시적 적용, 실수 단봉성·정수 최대점 정리다. 모두 기존 도구로 쉽게 얻을 수 있는 수준이다.
- 따라서 10점 이상 후보가 아니다. 점수는 7에서 3으로 낮춘다(meta.json 이력).

## 1차 결론 (기록 보존)

- 신규성 상태: **선행 결과와 차이 일부 확인 · 최종 신규성 미확인**. 핵심 도구(Borell, Brunn)는 알려져 있고, 교대합 적용은 해당 분야 전문가에게 "알려진 보조정리의 직접적 따름정리"로 보일 가능성이 크다.
- 같은 결과가 문헌에 없다는 사실은 확인하지 못했다(검색에서 못 찾은 것일 뿐). Pečarić 학파 논문 본문과 Hurwitz 제타·유한 차분 관련 문헌은 열람하지 못했다.
- 점수 판단에 대한 함의: 10점 이상을 주려면 "전문가가 직접적 따름정리로 보지 않는다"는 근거나 동일 진술 부재의 더 강한 확인이 필요하다. 현재 근거로는 0–9 구간 상단이 적절하다.

## 확인한 자료 (확인일 2026-10-29)

- M. Fradelizi, J. Li, M. Madiman, *Concentration of information content for convex measures*, Electron. J. Probab. 25 (2020), no. 20. Prop. 3.2. [arXiv:1512.01490](https://arxiv.org/abs/1512.01490)
- B. Klartag, J. Lehec, *Poisson processes and a log-concave Bernstein theorem*, Berwald–Borell 부등식 서술 부분(검색 요약으로 확인). [arXiv:1802.04176](https://arxiv.org/abs/1802.04176)
- *Log-concavity and log-convexity of moments of averages of i.i.d. random variables*, 초록 수준 확인. [arXiv:2001.06439](https://arxiv.org/abs/2001.06439)
- G. Roqia, J. Pečarić, A. Vukelić, *n-exponential convexity of divided differences and related Stolarsky type means*, Math. Inequal. Appl. 16 (논문 82). 서지 페이지만 확인, 본문 미열람. [논문 페이지](https://mia.ele-math.com/16-82/n-exponential-convexity-of-divided-differences-and-related-Stolarsky-type-means)
- M. Floater, *Log-concavity of B-splines*(노트), 검색 결과로만 확인. [PDF](https://www.mn.uio.no/math/english/people/aca/michaelf/papers/logconcave.pdf)
