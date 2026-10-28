# 고정된 $a$에서 최대 지수의 점근: $\log n+\tfrac12-\psi(a-1)$

[위키 홈](../../wiki/Home.md) · [비례 영역 최대점](../2026-10-29-proportional-argmax/note.md) · [실수 지수 로그 오목성](../2026-10-29-real-log-concavity/note.md) · [열린 질문](../../wiki/Questions.md)

- 작업 ID: 2026-10-29-fixed-a-argmax
- 작성자: 연구·조율 에이전트(자유 탐구로 Q-015 선택)
- 작성일: 2026-10-29
- 수정일: 2026-10-29
- 수학 본문 버전: v1
- 분야: 점근해석, 조합론
- 문헌 관계: 고정 지수 $s$에서의 점근 $F_{n,s}(a)\sim\Gamma(a)(\log n)^{s-1}/(\Gamma(s)n^a)$는 Rice 적분 방법(Flajolet–Sedgewick)의 전형적인 대상으로 알려진 유형으로 보인다(원문 미확인). 최대점이 $n$과 함께 움직이는 영역의 위치 공식은 검색에서 찾지 못했다. **신규성 미확인**. [신규성 조사](novelty.md)
- 독립 검토: 미실시(작성 세션 자체 점검)
- 성과 평가: [평가 메타데이터](meta.json) · [평가 기준](../../wiki/Scoring.md)

## 1. 질문과 결론

$F_{n,s}(a)=\sum_{j=0}^n(-1)^j\binom nj(a+j)^{-s}$에서 $a>1$을 고정하고 $n\to\infty$를 본다. [로그 오목성 노트](../2026-10-29-real-log-concavity/note.md)에 따라 $s\mapsto F_{n,s}(a)$에는 유일한 최대점 $s^*_n$이 있다. Q-015는 $s^*_n$이 $\log n$ 크기로 자라는지, 그리고 2차 항이 무엇인지 묻는다.

$\lambda=\log n$, $b=a-1>0$로 두면 다음이 성립한다.

| | 내용 | 상태 |
| --- | --- | --- |
| 정리 1 | $s^*_n=\log n+\kappa(a)+o(1)$, $\kappa(a)=\tfrac12-\psi(a-1)$ | 증명됨 |
| 정리 2 | $\log n+\kappa$가 반정수에서 $\varepsilon$ 이상 떨어져 있으면, 충분히 큰 $n$에서 정수 최대점은 $\log n+\kappa$에 가장 가까운 정수 | 증명됨 |
| 주장 3 | $s^*_n=\log n+\kappa+\delta(a)/\log n+O((\log n)^{-2})$, $\delta=-\psi'(b)+\tfrac12\psi''(b)-\tfrac1{24}$ | 형식 유도 + 계산 관찰 |

예: $a=2$이면 $\kappa=\tfrac12+\gamma\approx1.0772$이므로 정수 최대점은 대략 $\log n+1.08$에 가장 가까운 정수다. $a\to1^+$이면 $\kappa\to+\infty$이다. 이는 $a\le1$에서 최대점이 없다(지수에 대해 계속 증가)는 [기존 분류](../2026-10-29-turan-unimodality/note.md)와 맞물린다. 조건 $a>1$은 아래 극한 분포 Gamma$(a-1)$이 존재하는 조건으로 자연스럽게 나타난다.

이 노트는 [비례 영역 노트](../2026-10-29-proportional-argmax/note.md)($a=\theta n$, 최대점이 상수로 수렴)와 짝을 이룬다. 두 노트를 합치면 Q-011(정수 최대점의 정량적 예측)이 두 점근 영역에서 답해진다.

## 2. 표현

$\Gamma(s)(a+j)^{-s}=\int_0^\infty t^{s-1}e^{-(a+j)t}dt$를 더한 뒤 $t=\lambda+v$로 치환하면, $e^{-t}=e^{-v}/n$이므로

$$
\Gamma(s)F_{n,s}(a)=\lambda^{s-1}n^{-a}\int_{-\lambda}^{\infty}q_{n,s}(v)\,dv,\qquad
q_{n,s}(v)=\Bigl(1+\frac v\lambda\Bigr)^{s-1}e^{-av}\Bigl(1-\frac{e^{-v}}n\Bigr)^n.
$$

$L_n(s)=\log F_{n,s}(a)$의 도함수는

$$
L_n'(s)=\log\lambda+\mathbb E_{n,s}\Bigl[\log\Bigl(1+\frac V\lambda\Bigr)\Bigr]-\psi(s)
$$

이다. 여기서 $V$는 $q_{n,s}$에 비례하는 밀도를 가진다.

## 3. 핵심 보조정리: 극한 분포는 $-\log\mathrm{Gamma}(a-1)$

상태: 증명됨.

$x\in\mathbb R$을 고정하고 $s=\lambda+x$로 두면

$$
\lambda\,\mathbb E_{n,\lambda+x}\Bigl[\log\Bigl(1+\frac V\lambda\Bigr)\Bigr]\longrightarrow-\psi(a-1)\qquad(n\to\infty).
$$

**증명.** $q_\infty(v)=e^{(1-a)v}\exp(-e^{-v})$로 두자. $u=e^{-v}$로 치환하면 $\int q_\infty=\int_0^\infty u^{a-2}e^{-u}du=\Gamma(a-1)$이다. 또 $\int v\,q_\infty=-\int\log u\cdot u^{a-2}e^{-u}du=-\psi(a-1)\Gamma(a-1)$이다. 따라서 $Z_n=\int q_{n,s}\to\Gamma(a-1)$과 $N_n=\int\lambda\log(1+v/\lambda)q_{n,s}\,dv\to-\psi(a-1)\Gamma(a-1)$을 보이면 된다. 적분 구간을 둘로 나눈다.

*(i) $v\ge-\lambda/2$.* 다음이 성립한다.

- 점별 수렴: $(\lambda+x-1)\log(1+v/\lambda)\to v$이고 $(1-e^{-v}/n)^n\to\exp(-e^{-v})$이므로 $q_{n,s}\to q_\infty$이다. 또 $\lambda\log(1+v/\lambda)\to v$이다.
- 지배 함수: $1<1+\varepsilon<a$인 $\varepsilon$을 고르고 $n$을 충분히 크게 잡으면 $1-\varepsilon\le(\lambda+x-1)/\lambda\le1+\varepsilon$이다. $\log(1+y)\le y$이므로 $v\ge0$이면 $(1+v/\lambda)^{s-1}\le e^{(1+\varepsilon)v}$, $v<0$이면 $\le e^{(1-\varepsilon)v}$이다. 또 $(1-e^{-v}/n)^n\le\exp(-e^{-v})$이다. 따라서

$$
q_{n,s}(v)\le H(v):=\begin{cases}e^{(1+\varepsilon-a)v}&v\ge0,\\ e^{(1-\varepsilon-a)v}\exp(-e^{-v})&v<0.\end{cases}
$$

- $y\ge-\tfrac12$이면 $|\log(1+y)|\le2|y|$이므로 $|\lambda\log(1+v/\lambda)|\le2|v|$이다. $(1+|v|)H(v)$는 적분 가능하므로, 지배 수렴 정리에 의해 이 구간의 $Z_n$, $N_n$은 각각 $\Gamma(a-1)$, $-\psi(a-1)\Gamma(a-1)$로 수렴한다.

*(ii) $-\lambda<v<-\lambda/2$.* $t=\lambda+v\in(0,\lambda/2)$이고 다음이 성립한다.

- $s\ge1$이면 $(1+v/\lambda)^{s-1}=(t/\lambda)^{s-1}\le1$이다.
- $e^{-av}\le e^{a\lambda}=n^a$이다.
- $(1-e^{-v}/n)^n=(1-e^{-t})^n\le\exp(-ne^{-t})\le\exp(-\sqrt n)$이다.
- $\int_{-\lambda}^{-\lambda/2}|\lambda\log(1+v/\lambda)|\,dv=\lambda^2\int_0^{1/2}|\log y|\,dy\le\lambda^2$이다.

따라서 이 구간의 기여는 $Z_n$, $N_n$ 모두에서 $n^a\lambda^2e^{-\sqrt n}\to0$ 이하이다. $\blacksquare$

## 4. 정리 1: 실수 최대점

상태: 증명됨.

$\psi(z)=\log z-\frac1{2z}+O(z^{-2})$이므로 $\lambda[\psi(\lambda+x)-\log\lambda]\to x-\tfrac12$이다. 보조정리와 합치면 각 $x$에서

$$
\lambda\,L_n'(\lambda+x)\longrightarrow\kappa-x,\qquad\kappa=\tfrac12-\psi(a-1). \tag{1}
$$

$\delta>0$에 대해 $x=\kappa\pm\delta$를 넣으면, 충분히 큰 $n$에서 $L_n'(\lambda+\kappa-\delta)>0>L_n'(\lambda+\kappa+\delta)$이다. $L_n$은 엄격히 오목하므로 $L_n'$은 감소하고, 유일한 최대점은 $|s^*_n-\lambda-\kappa|<\delta$를 만족한다. $\blacksquare$

## 5. 정리 2: 정수 최대점

상태: 증명됨.

$\lambda L_n'(\lambda+x)$는 $x$에 대해 감소하는 함수열이고 연속 함수 $\kappa-x$로 점별 수렴한다. 연속 극한으로 점별 수렴하는 단조 함수열은 콤팩트 집합에서 균등 수렴한다. 정수 $k$에 대해 $x_k=k-\lambda$라 하면

$$
\lambda\bigl[L_n(k+1)-L_n(k)\bigr]=\int_{x_k}^{x_k+1}\lambda L_n'(\lambda+x)\,dx=\kappa-x_k-\tfrac12+o(1)
$$

이다. 이 $o(1)$은 $x_k\in[\kappa-3,\kappa+3]$에서 균등하다. 따라서 $\lambda+\kappa$가 반정수에서 $\varepsilon$ 이상 떨어져 있으면, 큰 $n$에서 이 창 안의 모든 $k$에 대해 $L_n(k+1)>L_n(k)\iff k+\tfrac12<\lambda+\kappa$이다. 창 밖은 오목성(단봉성)으로 처리된다. 그러므로 정수 최대점은 $\lambda+\kappa$에 가장 가까운 정수다. $\blacksquare$

반정수 근처($\lambda+\kappa\approx m+\tfrac12$)에서는 주장 3의 $\delta/\lambda$ 보정이 결과를 정한다. 검증에서 42개 설정 중 1개가 실제로 이 경우였다.

## 6. 주장 3: $1/\log n$ 보정항

상태: 계산 관찰. 형식 전개로 얻었고 나머지 항의 균일한 제어는 하지 않았다.

$V_\infty=-\log U$, $U\sim\mathrm{Gamma}(b)$이면 $\mathbb EV_\infty=-\psi(b)$, $\operatorname{Var}V_\infty=\psi'(b)$, 3차 중심적률은 $-\psi''(b)$이다. 다음 세 전개를 사용한다.

- $(\lambda+x-1)\log(1+v/\lambda)=v+\frac{(x-1)v-v^2/2}{\lambda}+O(\lambda^{-2})$
- $\lambda\log(1+v/\lambda)=v-\frac{v^2}{2\lambda}+\cdots$
- $\lambda[\psi(\lambda+x)-\log\lambda]=x-\tfrac12+\frac{-x^2/2+x/2-1/12}{\lambda}+\cdots$

포아송화 오차 $O(1/n)$은 무시한다. 이를 (1)에 넣고 $x=\kappa+\delta/\lambda$로 풀면

$$
\delta(a)=-\psi'(a-1)+\tfrac12\psi''(a-1)-\tfrac1{24}.
$$

수치(§8): $a=3$이면 $\delta=-0.8887$이고 $n=10^{16}$에서 $\lambda(s^*-\lambda-\kappa)=-0.8635$이다. $a=5$이면 $\delta=-0.3655$, 관측값은 $-0.3730$이다. 남은 차이는 $n$이 커질수록 단조 감소했다. $a=1.5$, $2$에서는 $\delta$가 크고 다음 차수 항도 커서 수렴이 느리지만, 차이는 역시 감소했다.

## 7. 실패한 시도와 한계

- 처음 형식 계산(비례 영역 노트 §7)에서는 고정된 $s$의 점근 $(\log n)^{s-1}$만 보고 $t^{s-1}$ 인자를 상수처럼 다뤘다. 그런데 최대점에서는 $s\approx\lambda$이므로 $(1+v/\lambda)^{s-1}\approx e^v$가 극한 분포를 Gamma$(a)$에서 Gamma$(a-1)$로 **이동시킨다**. 이 이동이 $\kappa$에 $\psi(a-1)$이 들어가는 이유다.
- 고정된 $s$의 점근 자체는 Rice 적분 문헌의 표준 결과로 보이며, 이 노트는 그것을 다시 증명하지 않았다(필요 없음).
- 비균등 간격, $a\downarrow1$과 $n\to\infty$가 동시에 움직이는 전이 영역은 다루지 않았다. 주장 3의 엄밀화와 반정수 근처의 결정도 미해결이다.

## 8. 계산과 재현

Python 3.10 표준 라이브러리(`math`, `fractions`), 난수 없음, 약 9초.

```powershell
python research/2026-10-29-fixed-a-argmax/verify.py
```

- 적분 표현에는 상쇄가 없으므로 로그 스케일 Simpson 적분(부동소수점)으로 큰 $n$을 계산한다. 이 방법은 $n\in\{50,120\}$, $a\in\{3/2,2,5\}$, $r=1..12$의 72개 경우에서 정확한 유리수 합과 비교해 최대 오차 $2\times10^{-14}$로 검증했다.
- 실수 최대점: $a\in\{1.5,2,3,5\}$, $n=10^2,\ldots,10^{16}$. $|s^*-\lambda-\kappa|$가 단조 감소하는지 확인했다. $a\ge3$에서는 $|\lambda(s^*-\lambda-\kappa)-\delta|$의 단조 감소도 확인했다.
- 정수 최대점: $a\in\{2,3,5\}$, $n=10^3,\ldots,10^{16}$ 42개 설정. 정수 최대점은 $\{\lfloor s^*\rfloor,\lceil s^*\rceil\}$ 안에 있고, 반정수에서 0.05 이상 떨어진 경우 $s^*$의 반올림과 같았다. $\lambda+\kappa$의 반올림과는 41/42개가 일치했다.
- 실제 출력: [계산 기록](results.md).

## 9. 다음 질문

- 주장 3의 엄밀한 증명, 그리고 반정수 근처에서 정수 최대점을 정하는 규칙.
- 전이 영역: $a=1+\eta_n$, $\eta_n\to0$일 때 $s^*_n$의 거동($\psi(\eta)\approx-1/\eta$이므로 $\kappa\approx1/\eta$).
- 종합 노트 후보: 비례 영역($a=\theta n$)과 고정 영역을 잇는 중간 영역 $a=n^\beta$ ($0<\beta<1$)에서의 단일 공식. AGENTS.md의 종합 연구노트 규칙에 해당할 수 있다.

## 10. 출처

- P. Flajolet, R. Sedgewick, *Mellin transforms and asymptotics: Finite differences and Rice's integrals*, Theoretical Computer Science 144 (1995). 검색 결과로만 확인했고 본문은 읽지 않았다(확인일 2026-10-29).
- P. Kirschenhofer, *A note on alternating sums*, Electron. J. Combin. 3(2) (1996) R7. 검색 요약에서 Rice 방법의 설명과 $s=1$ 항등식을 확인했다. [PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v3i2r7/pdf) (확인일 2026-10-29)
- 그 밖에는 자체 유도.
