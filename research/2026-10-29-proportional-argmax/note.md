# 비례 영역의 최대 지수: 포아송 모양의 극한과 최대점의 수렴

[위키 홈](../../wiki/Home.md) · [실수 지수 로그 오목성](../2026-10-29-real-log-concavity/note.md) · [정수 단봉성 분류](../2026-10-29-turan-unimodality/note.md) · [열린 질문](../../wiki/Questions.md)

- 작업 ID: 2026-10-29-proportional-argmax
- 작성자: 연구·조율 에이전트(자유 탐구로 Q-011·Q-013 선택)
- 작성일: 2026-10-29
- 수정일: 2026-10-29
- 수학 본문 버전: v1
- 분야: 점근해석, 조합론
- 문헌 관계: 라플라스 방법과 오목성만 쓰는 자체 유도. 고정된 $a$의 유한 차분 점근은 Flajolet–Sedgewick의 Rice 적분 이론이 다루지만, $a\propto n$인 이 영역을 다룬 자료는 검색에서 찾지 못했다. **신규성 미확인**이며 표준 도구의 직접 적용이다.
- 독립 검토: 미실시(작성 세션 자체 점검)
- 성과 평가: [평가 메타데이터](meta.json) · [평가 기준](../../wiki/Scoring.md)

## 1. 질문과 결론

$F_{n,s}(a)=\sum_{j=0}^n(-1)^j\binom nj(a+j)^{-s}$에서 $a=\theta n$ ($\theta>0$ 고정)으로 두고 $n\to\infty$를 본다. [앞선 노트](../2026-10-29-real-log-concavity/note.md)에서 $a>1$이면 $s\mapsto F_{n,s}(a)$에 유일한 최대점 $s^*_n$이 있고, 정수 최대점은 그 근처에 있음을 보였다.

- **Q-013:** $s^*_n/n$의 극한은? → **0**이다. 더 정확히는 $s^*_n$이 유한한 상수로 수렴한다.
- **Q-011 (비례 영역):** 정수 최대점을 $n,a$로 예측할 수 있는가? → $n$이 크면 $\lfloor t_0\rfloor+1$이다.

$$
t_0=\log\Bigl(1+\frac1\theta\Bigr)
$$

결과(정리 1–3 증명됨, 주장 4는 형식 유도와 계산 관찰):

| | 내용 |
| --- | --- |
| 정리 1 (포아송 모양) | $F_{n,s}(\theta n)/F_{n,1}(\theta n)\to t_0^{\,s-1}/\Gamma(s)$ (각 $s>0$) |
| 정리 2 (실수 최대점) | $s^*_n\to s_\infty(\theta)$, $\psi(s_\infty)=\log t_0$ |
| 정리 3 (정수 최대점) | $t_0\notin\mathbb Z$이면 충분히 큰 $n$에서 정수 최대점 $=\lfloor t_0\rfloor+1$ |
| 주장 4 (보정항) | $s^*_n=s_\infty+c(\theta)/n+O(n^{-2})$, $c$는 §6의 닫힌식 |

정수 $r$에서 극한 모양 $t_0^{r-1}/(r-1)!$은 평균 $t_0$인 포아송 분포의 확률질량에 비례한다. 정수 최대점이 포아송 최빈값에 1을 더한 것이 되는 이유다.

## 2. 표현과 이전 결과

$\Gamma(s)(a+j)^{-s}=\int_0^\infty t^{s-1}e^{-(a+j)t}dt$를 더하면 $a=\theta n$일 때

$$
F_{n,s}(\theta n)=\frac{I_n(s)}{\Gamma(s)},\qquad I_n(s)=\int_0^\infty t^{s-1}e^{-nG(t)}dt,\qquad G(t)=\theta t-\log(1-e^{-t}).
$$

또 $s=1$에서는 닫힌식 $F_{n,1}(a)=n!/\prod_{k=0}^n(a+k)$가 있다([앞선 정수 지수 노트](../2026-10-29-reciprocal-binomial/note.md)의 $b_n$). 이전 노트에서 $L_n(s)=\log F_{n,s}(\theta n)$은 $s>0$에서 엄격히 오목하고, $\theta n>1$이면 유일한 최대점 $s^*_n$을 가진다.

## 3. 정리 1: 포아송 모양의 극한

상태: 증명됨. 라플라스 방법(표준 결과, 이번 작업에서 원문 미확인)을 사용.

**$G$의 성질.** $G'(t)=\theta-1/(e^t-1)$은 엄격히 증가한다. 따라서 $G$는 엄격히 볼록하고, $e^{t_0}-1=1/\theta$인 $t_0=\log(1+1/\theta)$에서 유일한 최소를 가진다. 이때

$$
G''(t_0)=\frac{e^{t_0}}{(e^{t_0}-1)^2}=\theta(\theta+1)>0,\qquad
G(t_0)=(\theta+1)\log(\theta+1)-\theta\log\theta.
$$

$t\to0^+$이면 $G\to+\infty$이고 $e^{-G(t)}\sim t$이며, $t\to\infty$이면 $G(t)\sim\theta t$이다.

**라플라스 방법.** $g(t)=t^{s-1}$은 $t_0$에서 연속이다. $\int_0^\infty|g|e^{-G}dt<\infty$이다(0 근처 피적분함수 $\sim t^{s}$, 무한대에서 지수 감소). 또 $t_0$의 임의의 근방 밖에서 $\inf G>G(t_0)$이다. 그러므로 표준 라플라스 정리에 의해

$$
I_n(s)\sim t_0^{\,s-1}e^{-nG(t_0)}\sqrt{\frac{2\pi}{n\,G''(t_0)}}\qquad(n\to\infty).
$$

$s$와 무관한 인자가 비율에서 소거되므로

$$
\boxed{\frac{F_{n,s}(\theta n)}{F_{n,1}(\theta n)}\longrightarrow\frac{t_0^{\,s-1}}{\Gamma(s)}\qquad(s>0\text{ 고정}).}\qquad\blacksquare
$$

같은 계산의 $s=1$ 경우는 $F_{n,1}(\theta n)=\mathrm B(\theta n,n+1)$의 Stirling 점근과 일치한다. 지수 인자 $e^{-nG(t_0)}$는 직접 합에서 일어나는 지수적 상쇄의 크기이기도 하다. 계산 코드는 이 크기로 정밀도를 정한다.

## 4. 정리 2: 실수 최대점의 수렴

상태: 증명됨.

$\ell(s)=(s-1)\log t_0-\log\Gamma(s)$로 두자. $(\log\Gamma)''=\psi'>0$이므로 $\ell$은 엄격히 오목하다. $\psi$는 $(0,\infty)$에서 $-\infty$부터 $\infty$까지 증가하므로 $\ell'(s)=\log t_0-\psi(s)=0$인 유일한 $s_\infty(\theta)>0$이 있다. 이제

$$
\lim_{n\to\infty}s^*_n=s_\infty(\theta),\qquad \psi(s_\infty)=\log\log\Bigl(1+\frac1\theta\Bigr).
$$

**증명.** $0<\varepsilon<s_\infty$를 고정한다. $\ell$의 엄격 오목성으로 $\ell(s_\infty)>\ell(s_\infty\pm\varepsilon)$이다. 정리 1에서 세 점에서 $L_n(s)-L_n(1)\to\ell(s)$이므로, 충분히 큰 $n$에서 $L_n(s_\infty)>L_n(s_\infty\pm\varepsilon)$이다. $\theta n>1$이면 $L_n$은 $(0,s^*_n]$에서 증가하고 $[s^*_n,\infty)$에서 감소한다. 만약 $s^*_n\ge s_\infty+\varepsilon$이면 $L_n(s_\infty)\le L_n(s_\infty+\varepsilon)$이 되어 모순이다. 반대쪽도 같다. 따라서 $|s^*_n-s_\infty|<\varepsilon$이다. $\blacksquare$

특히 $s^*_n/n\to0$이므로 Q-013의 답은 0이다. $\theta\to\infty$이면 $t_0\to0$, $s_\infty\to0$이다. $\theta\to0^+$이면 $s_\infty\sim\log(1/\theta)$로 커진다($\psi(x)\approx\log x$).

| $\theta$ | $t_0$ | $s_\infty$ |
| --- | --- | --- |
| 1/10 | 2.397895 | 2.880831 |
| 1/2 | 1.098612 | 1.563286 |
| 1 | 0.693147 | 1.140994 |
| 3 | 0.287682 | 0.690964 |

## 5. 정리 3: 정수 최대점

상태: 증명됨.

양의 정수 $r$에 대해 $\ell(r+1)-\ell(r)=\log t_0-\log r$이다. 따라서 $t_0\notin\mathbb Z$이면 $\ell$을 정수 위에서 최대로 만드는 점은 유일하며 $r_0=\lfloor t_0\rfloor+1$이다. 정리 2의 증명처럼 $r_0-1,r_0,r_0+1$(양의 정수인 것만)에서 $L_n$이 $\ell$로 수렴한다. 그러면 큰 $n$에서 $L_n(r_0)>L_n(r_0\pm1)$이고, 오목성으로 정수 최대점은 $r_0$이다. $\blacksquare$

- 정수 최대점이 $k$에서 $k+1$로 바뀌는 경계는 $t_0=k$, 즉 $\theta_k=1/(e^k-1)$이다.
- $k=1$이면 $\theta_1=1/(e-1)$이다. 이는 [앞선 노트 주장 5](../2026-10-29-turan-unimodality/note.md)의 $\alpha_n/n\to1/(e-1)$("처음부터 감소" 경계)과 일치하므로 독립적인 정합성 확인이 된다.
- $t_0\in\mathbb Z$ (경계 위)이면 극한에서 두 항이 동률이다. 어느 쪽이 이기는지는 $1/n$ 보정이 정하며 여기서는 결정하지 않았다.

## 6. 주장 4: $1/n$ 보정항

상태: 계산 관찰. 형식적 2차 라플라스 전개로 유도했다. 전개의 $s$에 대한 균일성과 도함수 교환은 증명하지 않았다.

$G_2=\theta(\theta+1)$, $G_3=G'''(t_0)=-\theta(\theta+1)(2\theta+1)$로 두자. 2차 라플라스 전개 $I_n(s)\approx(\text{공통 인자})\,t_0^{s-1}[1+A(s)/n]$에서

$$
A'(s)=\frac{2s-3}{2G_2t_0^2}-\frac{G_3}{2G_2^2t_0}=\frac{(2s-3)+(2\theta+1)t_0}{2\theta(\theta+1)t_0^2}
$$

이다. $L_n'(s^*_n)=0$을 $s_\infty$ 주위로 전개하면

$$
s^*_n\approx s_\infty+\frac{c(\theta)}n,\qquad c(\theta)=\frac{(2s_\infty-3)+(2\theta+1)t_0}{2\theta(\theta+1)\,t_0^2\,\psi'(s_\infty)}.
$$

수치 확인(§8)에서 $n(s^*_n-s_\infty)-c(\theta)$는 $n=25,50,100,200$에서 매번 정확히 절반이 되었다. 이는 나머지가 $O(n^{-2})$라는 예측과 맞는다. 예: $\theta=1$이면 $c=0.52065$이고, $n=200$에서 $n(s^*-s_\infty)=0.52290$이다.

작은 $\theta$에서는 $c(\theta)$가 커서($\theta=1/10$에서 $c\approx10.8$) 극한이 느리게 나타난다. 같은 이유로 $\theta=1/100$, $n=100$($a=1$)에서는 정수 최대점이 아직 극한값과 다르다(검증 중 실제로 관찰).

## 7. 실패한 시도와 한계

- 처음에는 $s=\sigma n$ 크기를 가정한 큰 편차 계산을 시도했다. $\mathbb E\log Y$에 들어 있는 $\log n$ 항을 빠뜨린 오류여서 버렸다. 올바른 크기는 $s=O(1)$이다.
- 고정된 $a>1$에서 $n\to\infty$인 영역은 다루지 않았다. 형식 계산으로는 $F_{n,s}(a)\approx\Gamma(a)(\log n)^{s-1}/(\Gamma(s)n^a)$이고 $s^*_n$이 대략 $\log n$ 크기로 자랄 것으로 보인다. 하지만 최대점이 무한대로 움직여 $t^{s-1}$ 인자가 안장점을 이동시키므로 위 증명이 그대로 적용되지 않는다.
- 비균등 간격으로의 확장, $a_n/n\to\theta$(정확히 비례하지 않는 경우), 동률 경계 $t_0\in\mathbb Z$는 미해결이다.
- 직접 합은 지수적으로 상쇄되므로 실수 지수 계산에는 $n$에 비례하는 정밀도가 필요하다.

## 8. 계산과 재현

Python 3.10 표준 라이브러리(`decimal`, `fractions`, `math`), 난수 없음, 약 24초.

```powershell
python research/2026-10-29-proportional-argmax/verify.py
```

- 실수 최대점: $\theta\in\{0.1,0.5,1,3\}$, $n\in\{25,50,100,200\}$. 정밀도는 상쇄 크기 $n(\log2+G(t_0))/\ln10$자리 + 60자리. 잔차 $n(s^*-s_\infty)-c$가 $n$을 두 배로 할 때마다 0.75배 이하로 줄어드는지 확인한다.
- 정수 최대점과 포아송 모양: $\theta\in\{1/30,1/10,1/2,1,3\}$, $n\in\{200,400\}$, 정확한 유리수 계산. 최대점이 $\lfloor t_0\rfloor+1$과 같은지, 그리고 $s=1$ 닫힌식을 확인하고, $r\le5$에서 모양의 상대 오차를 출력한다(오차는 $n$을 두 배로 하면 약 절반).
- 실제 출력은 [계산 기록](results.md)에 있다.

## 9. 다음 질문

- 고정된 $a>1$에서 $s^*_n$의 점근($\log n$ 크기의 증명과 2차 항).
- 동률 경계 $\theta=1/(e^k-1)$에서 큰 $n$의 정수 최대점은 $k$와 $k+1$ 중 어느 쪽인가?
- 비균등 간격 $h_i$에서 같은 극한: $G(t)=\theta t-\frac1n\sum\log(1-e^{-h_it})$가 되며 간격의 경험 분포에 의존할 것이다.

## 10. 출처

- 라플라스 방법: 표준 결과로 사용했고 이번 작업에서 원문을 확인하지 않았다.
- P. Flajolet, R. Sedgewick, *Mellin transforms and asymptotics: Finite differences and Rice's integrals*, Theoretical Computer Science 144 (1995). 검색 결과 요약으로만 존재와 주제를 확인했고 본문은 읽지 않았다(확인일 2026-10-29).
- [Nørlund–Rice integral (Wikipedia)](https://en.wikipedia.org/wiki/N%C3%B8rlund%E2%80%93Rice_integral), 검색 결과로만 확인(확인일 2026-10-29).
- 그 밖에는 자체 유도.
