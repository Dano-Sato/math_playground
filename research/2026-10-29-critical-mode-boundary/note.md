# 포아송 동률 경계의 선택과 유한 크기 전환점

[위키 홈](../../wiki/Home.md) · [비례 영역 극한](../2026-10-29-proportional-argmax/note.md) · [정수 로그 오목성](../2026-10-29-turan-unimodality/note.md) · [열린 질문](../../wiki/Questions.md)

- 작업 ID: 2026-10-29-critical-mode-boundary
- 작성자: 연구·조율 에이전트
- 작성일: 2026-10-29
- 수정일: 2026-10-29
- 수학 본문 버전: v1
- 분야: 점근해석, 조합론, 확률론
- 문헌 관계: 기존 대칭다항식 항등식·로그 오목성과 초등 합 근사의 종합 적용. 아래 경계 공식의 문헌상 신규성은 미확인.
- 독립 검토: 미실시(작성 세션 자체 점검)
- 성과 평가: [평가 메타데이터](meta.json) · [신규성 조사](novelty.md)

## 1. 질문과 결론

양의 정수 $n,r$와 실수 $a>0$에 대해

$$
F_{n,r}(a)=\sum_{j=0}^n(-1)^j\binom nj(a+j)^{-r},\qquad
R_{n,r}(a)=\frac{F_{n,r+1}(a)}{F_{n,r}(a)}
$$

로 둔다. [비례 영역 노트](../2026-10-29-proportional-argmax/note.md)는 $a=\theta n$에서 $R_{n,r}\to\log(1+1/\theta)/r$임을 준다. 따라서

$$
\theta_k=\frac1{e^k-1},\qquad k=1,2,\ldots
$$

에서는 $r=k$와 $k+1$의 **극한 값**이 동률이다. Q-016은 유한한 $n$에서 어느 쪽이 이기는지 묻는다.

결론은 다음과 같다.

1. 모든 $n\geq1$에서 $F_{n,k+1}(\theta_kn)>F_{n,k}(\theta_kn)$이다.
2. $n>(k+1)(e^k-1)$이면 **전체 양의 정수 지수 중 유일한 최대점은 $k+1$**이다. 이 조건은 충분조건이며 최소 문턱값이라고 주장하지 않는다.
3. $F_{n,k+1}(a)=F_{n,k}(a)$인 유일한 전환점 $a_{n,k}>1$이 존재하며, 고정된 $k$에 대해

$$
\boxed{a_{n,k}=\theta_kn+\theta_k+\frac32-\frac1k+O(n^{-1}).}
$$

즉 극한 직선 $a=\theta_kn$보다 실제 전환점이 양의 상수만큼 오른쪽으로 이동한다. 이 이동이 극한의 동률을 푼다.

## 2. 종합한 기존 노트와 새로 추가하는 내용

| 기존 노트 | 이번에 사용하는 사실 | 기존 노트에 없던 진술 |
| --- | --- | --- |
| [역수 거듭제곱 일반식](../2026-10-29-reciprocal-binomial/note.md) | $F_{n,r}=b_nh_{r-1}$, Newton 점화식 | 유한 $n$에서 이웃 항 비율을 직접 끼우는 경계 |
| [로그 오목성과 단봉성](../2026-10-29-turan-unimodality/note.md) | $R_{n,r}$의 엄격한 $r$ 감소, 날카로운 이웃 항 경계 | $R_{n,r}$의 $a$ 감소, 모든 지수 사이의 전환점 체계 |
| [비례 영역 최대점](../2026-10-29-proportional-argmax/note.md) | 포아송 모양의 극한, 동률 경계 $\theta_k$ | 동률의 실제 승자, 명시적 충분조건, 전환점의 상수 보정 |

위키 내부의 새 종합 결과라는 뜻이며, 외부 문헌에서 최초라는 뜻은 아니다.

## 3. 보조정리: 유한 크기의 비율 경계

상태: 증명됨(자체 점검).

양수 변수 $x_1,\ldots,x_m$, $H=\sum_i x_i$, $M=\max_i x_i$를 잡고 완전 동차 계수를 $h_q$라 하면 모든 정수 $q\geq1$에서

$$
\boxed{\frac Hq\leq\frac{h_q}{h_{q-1}}\leq\frac{H+(q-1)M}{q}.}
$$

$q=1$에서는 양쪽이 $H$다. $q\geq2$이면 왼쪽은 엄격하며, 변수들이 모두 같지 않으면 오른쪽도 엄격하다.

증명: $P_\ell=\sum_i x_i^\ell$라 하면 Newton 점화식

$$
qh_q=\sum_{\ell=1}^qP_\ell h_{q-\ell}
$$

에서 첫 항만 남기면 하계가 나온다. $q\geq2$에서는 나머지에 양수 항이 있다. 또 $P_\ell\leq MP_{\ell-1}$ ($\ell\geq2$)이므로

$$
qh_q\leq Hh_{q-1}+M\sum_{\ell=2}^qP_{\ell-1}h_{q-\ell}
=[H+(q-1)M]h_{q-1}.
$$

다른 양수 변수가 하나라도 $M$보다 작으면 $P_2<MP_1$이고 상계도 엄격하다.

원래 교대합에서는 $x_j=1/(a+j)$, $H_n(a)=\sum_{j=0}^n1/(a+j)$, $M=1/a$를 넣어

$$
\frac{H_n(a)}r\leq R_{n,r}(a)\leq\frac{H_n(a)+(r-1)/a}{r}
$$

를 얻는다. 이 계산에는 $a>1$이 필요 없다.

## 4. 정리 1: 동률 경계의 승자와 명시적 충분조건

상태: 증명됨(자체 점검). Q-016 해결.

감소 함수 $1/(a+x)$를 적분과 비교하면 모든 $n\geq1,a>0$에서

$$
\log\frac{a+n}{a}<H_n(a)<\log\frac{a+n}{a}+\frac1a.
$$

구체적으로 $\sum_{j=1}^nf(j)<\int_0^nf(x)dx<\sum_{j=0}^{n-1}f(j)$이므로, 하계는 $\int_0^nf<\sum_{j=0}^{n-1}f<H_n$, 상계는 $H_n=f(0)+\sum_{j=1}^nf<f(0)+\int_0^nf$에서 따른다.

$a=\theta_kn$이면 로그가 정확히 $k$다. 보조정리로

$$
R_{n,k}>\frac kk=1,\qquad
R_{n,k+1}<\frac{k+(k+1)/a}{k+1}=\frac{k}{k+1}+\frac1a.
$$

따라서 $a>k+1$, 즉 $n>(k+1)/\theta_k$이면 $R_{n,k+1}<1$이다. [이전의 엄격한 로그 오목성](../2026-10-29-turan-unimodality/note.md)에 의해 $R_{n,r}$는 $r$에 관해 엄격히 감소하므로, 그 전에는 증가하고 그 뒤에는 감소한다. 유일한 최대 지수는 $k+1$이다.

조건을 만족하지 않는 작은 $n$에서는 두 후보의 비교 $F_{k+1}>F_k$는 여전히 맞지만 전체 최대점이 더 오른쪽일 수 있다. 특히 $a\leq1$이면 정수 지수 전체에서 증가하므로 유한 최대점이 없다.

## 5. 정리 2: 유한 전환점의 존재·유일성과 순서

상태: 증명됨(자체 점검).

각 $n\geq1,k\geq1$마다 $R_{n,k}(a)=1$인 유일한 $a_{n,k}>1$이 존재한다. 또

$$
a_{n,k+1}<a_{n,k},\qquad \lim_{k\to\infty}a_{n,k}=1.
$$

증명: 유한합의 미분으로

$$
\frac{d}{da}\log R_{n,r}(a)=rR_{n,r}(a)-(r+1)R_{n,r+1}(a)
$$

이다. 이전 노트의 이웃 항 경계는

$$
\frac{R_{n,r}}{R_{n,r+1}}<\frac{(r+1)(n+r)}{r(n+r+1)}
$$

이므로 로그 미분은 $-(r+1)R_{n,r+1}/(n+r+1)<0$보다도 작다. 따라서 $a$에 관해 엄격히 감소한다. $a=1$에서 $R_{n,r}>1$이고, $a\to\infty$에서 $ax_j\to1$을 이용하면 $R_{n,r}\sim(n+r)/(ra)\to0$이므로 유일한 근이 있다.

$r$에 관한 엄격한 감소에서 근들의 순서가 따른다. 모든 근은 1보다 크고, 고정한 $a>1$에서는 $R_{n,k}\to1/a<1$이므로 결국 $a_{n,k}<a$이다. 따라서 근들의 극한은 1이다.

이로써 전체 정수 최대점도 매개변수로 분류된다. $a>a_{n,1}$이면 최대점은 1이고, $a_{n,k}<a<a_{n,k-1}$ ($k\geq2$)이면 최대점은 $k$다. $a=a_{n,k}$에서는 정확히 $k,k+1$ 두 항이 최대다. $a_{n,1}$은 이전에 구한 $H_n(a)=1$의 근 $\alpha_n$과 같다.

## 6. 정리 3: 전환점의 상수 보정

상태: 증명됨(자체 점검). $k$를 고정한 결과이며 $k=k_n\to\infty$에는 주장하지 않는다.

$\theta>0$, $t=\log(1+1/\theta)$,

$$
u=\frac12\left(\frac1\theta+\frac1{\theta+1}\right),\qquad
v=\frac1{\theta(\theta+1)}
$$

로 두자. $a=\theta n+\beta$이고 $\beta$가 고정된 유계 구간에서 움직일 때

$$
P_1=t+\frac{u-\beta v}{n}+O(n^{-2}),\qquad
P_2=\frac vn+O(n^{-2}),\qquad P_\ell=O(n^{1-\ell})\quad(\ell\geq3).
$$

여기서 필요한 것은 고정된 차수까지의 $P_\ell$뿐이다. 첫 식은 $f(x)=(\theta+x)^{-1}$에 대한 합성 사다리꼴 공식과 $\beta/n$ Taylor 전개로 얻는다. $f$의 2계 도함수가 구간에서 유계여서 오차는 $O(n^{-2})$이고, $\beta$의 유계 구간에서도 균일하다. $\int_0^1f^2=v$, 나머지는 같은 적분 비교로 따른다. [표준 Euler–Maclaurin 공식](https://dlmf.nist.gov/2.10#i)과도 일치한다.

생성함수 $\sum h_qz^q=\exp(\sum_{\ell\geq1}P_\ell z^\ell/\ell)$에서 고정된 $q$의 계수를 취하면

$$
h_q=\frac{t^q}{q!}\left[1+\frac1n\left(\frac{q(u-\beta v)}t+\frac{q(q-1)v}{2t^2}\right)+O(n^{-2})\right].
$$

이는 형식적 관찰만이 아니다. 고정 $q$의 계수는 유한한 정수 분할들의 합이고, $P_3$ 이상을 포함하거나 $P_2$를 두 번 이상 포함한 항은 모두 $O(n^{-2})$이다. $P_1$의 Taylor 오차도 유계다. 따라서 같은 유계 $\beta$ 구간에서 나머지가 균일하다. $q=0$에서도 $h_0=1$로 성립한다.

$h_k/h_{k-1}$를 나누고 $\theta=\theta_k$, $t=k$를 대입하면

$$
\boxed{R_{n,k}(\theta_kn+\beta)=1+\frac{v_k}{kn}(\beta_k-\beta)+O(n^{-2}),\qquad
\beta_k=\theta_k+\frac32-\frac1k.}
$$

여기서 $u/v=\theta+1/2$를 썼다. 먼저 $\beta=\beta_k\pm1$의 부호를 비교하면 유일한 근이 이 두 점 사이에 있으므로 $a_{n,k}-\theta_kn$이 유계임을 안다. 그다음 위 균일 전개를 근 자체에 적용하면 $a_{n,k}-\theta_kn=\beta_k+O(n^{-1})$을 얻는다.

따름결과: 고정 $\beta<\beta_k$이면 큰 $n$의 최대점은 $k+1$, $\beta>\beta_k$이면 $k$다. 바로 옆 비율들의 극한이 각각 $k/(k-1)>1$ ($k\geq2$)과 $k/(k+1)<1$이므로 다른 지수는 최대가 될 수 없다. $k=1$에서는 왼쪽 이웃을 확인할 필요가 없다. $\beta=\beta_k$일 때는 다음 차수의 부호가 필요하며 여기서는 결정하지 않는다.

특히 $k=1$에서는 $\alpha_n=(n+1)/(e-1)+1/2+O(n^{-1})$을 얻어, 이전의 폭 1 구간을 상수항까지 좁힌다.

## 7. 작은 사례와 재현

예를 들어 $k=1$이면 $\theta_1\approx0.5819767$이고, $n=4$는 위 충분조건을 만족한다. 실제 비율은 $R_{4,1}\approx1.30684>1$, $R_{4,2}\approx0.80203<1$이므로 최대 지수는 2다. 이는 근사 관찰이며 §4의 증명이 일반적인 결론의 근거다.

```powershell
python research/2026-10-29-critical-mode-boundary/verify.py
```

Python 3 표준 라이브러리만 사용하고 난수는 없다. 유리수 매개변수에서는 비율 경계·도함수 부호를 정확하게 검산한다. 초월수 $\theta_k$가 필요한 경계에서는 $e$의 유리수 상하계와 양수 계수의 단조성으로 첫 세 사례를 정확하게 인증한다. 큰 표와 전환점 근사는 `Decimal`을 쓰며, 두 정밀도에서 확인한 수치 관찰로 구분한다. 실제 출력은 [계산 기록](results.md)에 남긴다.

## 8. 한계와 다음 질문

- 처음 제안했던 실수 로그 오목성 문제는 이미 다른 노트에서 해결되어 있어 중복 연구를 피했다.
- 명시한 유한 크기 조건은 보수적인 충분조건이다. 최소 문턱값을 구하지 않았다.
- $\beta=\beta_k$인 상수 보정 직선 위의 승자, 전환점의 $1/n$ 항, $k$가 $n$과 함께 커지는 영역은 다루지 않았다.
- 기존 고정 $a$ 최대점 노트의 $1/\log n$ 보정이나 중간 영역 $a=n^\beta$의 문제를 해결한 것으로 해석해서는 안 된다.
- 문헌상 신규성은 미확인이며, 자체 점검과 독립 검토를 구별한다.

## 9. 문헌

확인일: 2026-10-29. 구체적인 검색·비교 범위는 [novelty.md](novelty.md)에 기록했다.

- [NIST DLMF §2.10(i)](https://dlmf.nist.gov/2.10#i): Euler–Maclaurin의 끝점 항과 나머지 구조를 대조했다. 이 노트에는 사다리꼴 공식으로 충분하다.
- [Bruce E. Sagan, *Log Concave Sequences of Symmetric Functions and Analogs of the Jacobi–Trudi Determinants* (1992)](https://users.math.msu.edu/users/bsagan/Papers/Old/lcs-pub.pdf): 도입부의 로그 오목성과 이웃 비율 순서의 관계 및 기존 대칭함수 연구라는 배경을 확인했다. 아래 경계 공식을 이 논문이 증명했다고 주장하지 않는다.
- [Kabluchko–Marynych–Sulzbach, *General Edgeworth expansions with applications to profiles of random trees*](https://arxiv.org/abs/1606.03920): 이 세션에서는 초록의 일반 mod-phi 전개와 mode 응용 범위만 확인했다. 이 노트의 $\theta_k$, $\beta_k$ 공식과 일치하는지 논문 전체를 검토하지 않았다.
