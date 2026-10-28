# 전환점 공식만의 신규성 집중 조사

[원 연구 노트](note.md) · [평가 원본](meta.json) · [기존 조사](novelty.md) · [검산 출력](transition-novelty-checks.md)

- 확인일: 2026-10-29
- 조사자: 원 노트 작성 세션. 별도 에이전트나 별도 세션의 독립 검토는 아니다.
- 평가 대상: 정리 3의 고정된 정수 $k$에 대한 전환점 공식 하나.
- 조사 목적: 현재 점수를 유지하며, 작은 독창적 결과에 해당하는 10점 후보인지 판단할 근거를 보강한다.
- 1차 판단: 표준 Poisson–Charlier 보정으로 같은 상수항을 재구성했다. 이 특정 공식의 선행 발표 여부는 미확인이다. 후보로 기록하되 점수 상향은 보류한다.

## 1. 후보 진술을 고정한다

정수 $n,k\geq1$에 대해

$$
F_{n,r}(a)=\sum_{j=0}^n(-1)^j\binom nj(a+j)^{-r},\qquad
F_{n,k+1}(a_{n,k})=F_{n,k}(a_{n,k})
$$

인 유일한 $a_{n,k}>1$을 잡는다. 후보는 다음 식이다.

$$
\boxed{a_{n,k}=\theta_kn+\beta_k+O(n^{-1}),\quad
\theta_k=(e^k-1)^{-1},\quad \beta_k=\theta_k+\frac32-\frac1k.}
$$

$k$는 고정한다. $k=k(n)$으로 증가하는 영역, 다음 차수, 다른 간격의 일반화는 이번 신규성 후보에 합치지 않는다. 원 노트의 다른 정리들이 이 식의 신규성을 대신 뒷받침하는 것도 아니다.

## 2. 실제 확인한 원문과 적용 범위

| 원문 | 확인한 부분 | 이번 식과의 관계 |
| --- | --- | --- |
| Koenraad Audenaert, [Inverse moments of univariate discrete distributions via the Poisson expansion](https://arxiv.org/html/0809.4155), arXiv:0809.4155v1 (2008) | §2 식 (5)의 계승 누적량 정의, §4 식 (17), (19), (20)의 Poisson–Charlier 전개, 부록 B | 첫 비포아송 항이 $\kappa^{(2)}\nabla^2\pi_\lambda/2$임을 명시한다. 해당 틀로 아래 상수항이 나온다. 이 논문에 우리 전환점 공식이 실려 있다고 주장하지 않는다. |
| Kabluchko–Marynych–Sulzbach, [General Edgeworth expansions with applications to profiles of random trees](https://arxiv.org/pdf/1606.03920), v3 (2017) | §2.1, 인쇄면 8의 $w_n\to\infty$, $\phi''>0$ 조건과 A2–A3; 정리 2.10 | 고정 $a$ 문제의 중요한 비교 대상이다. 이번에는 평균과 분산이 유한한 값으로 수렴하므로 그 정리를 그대로 적용해 신규성을 기각할 수 없다. |
| [NIST DLMF §2.10(i)](https://dlmf.nist.gov/2.10#i) | Euler–Maclaurin 합 공식 | 끝점 보정의 표준 출처. 아래 평균·계승 누적량 합의 전개는 원 노트의 합 근사와 같은 계산이다. |

Barbour (1987), *Asymptotic expansions in the Poisson limit theorem*, DOI [10.1214/aop/1176992169](https://doi.org/10.1214/aop/1176992169)는 Audenaert가 거슬러 올라가는 문헌이다. 이번에는 그 본문을 확보하지 못했다. 따라서 그 논문의 오차 정리가 이 모형에 적용된다고 인용하지 않는다. 필요한 나머지는 다음 절에서 직접 제어한다.

## 3. 기존 보정 틀에서 상수항을 재구성한다

이 절의 상태: **증명됨(작성 세션 자체 점검)**. 확률 모형에 대한 직접 유도이며 문헌상 신규성을 주장하는 별도 정리가 아니다.

### 3.1. 정확한 모형 대응

$a>1$, $x_j=(a+j)^{-1}$로 두고 독립인 기하 확률변수들을

$$
\Pr(G_j=m)=(1-x_j)x_j^m,\quad m\geq0,\qquad K=\sum_{j=0}^nG_j
$$

로 정의한다. 원 노트의 $F_{n,r}=b_nh_{r-1}$에 의해

$$
\Pr(K=m)=h_m(x_0,\ldots,x_n)\prod_{j=0}^n(1-x_j),\qquad
\frac{F_{n,k+1}}{F_{n,k}}=\frac{\Pr(K=k)}{\Pr(K=k-1)}.
$$

즉 $F$의 지수 $k,k+1$ 동률은 $K$의 값 $k-1,k$ 동률이다. 인덱스를 한 칸 잘못 옮기면 상수항도 잘못된다.

$y_j=x_j/(1-x_j)=(a+j-1)^{-1}$라 하면 확률생성함수는

$$
\mathbb E z^K=\prod_{j=0}^n\frac1{1-y_j(z-1)},\qquad
\log\mathbb E z^K=\sum_{\ell\geq1}\frac{(z-1)^\ell}{\ell}\sum_j y_j^\ell.
$$

따라서 평균 $\lambda=\sum_jy_j$, 두 번째 계승 누적량 $\kappa^{(2)}=\sum_jy_j^2>0$이다. Bernoulli 합의 음의 두 번째 계승 누적량을 대신 대입해서는 안 된다.

### 3.2. 유계 평균 영역의 전개와 나머지

$a=\theta_kn+\beta$로 두며 $\beta$는 고정 유계 구간을 움직인다. 이하 $\theta=\theta_k$,

$$
u=\frac12\left(\frac1\theta+\frac1{\theta+1}\right),\quad
v=\frac1{\theta(\theta+1)},\quad d=u+(1-\beta)v
$$

로 쓴다. 끝점 보정과 Taylor 전개로

$$
\lambda=k+\frac d n+O(n^{-2}),\quad
\sum_jy_j^2=\frac v n+O(n^{-2}),\quad
\max_j y_j=O(n^{-1}).
$$

모든 나머지는 이 $\beta$ 구간에서 균일하다. $|z|\leq1$이면 $|z-1|\leq2$이므로 충분히 큰 $n$에서 로그 전개의 $\ell\geq3$ 항 전체는

$$
\sum_{\ell\geq3}\frac{2^\ell}{\ell}\sum_jy_j^\ell
\leq (n+1)\sum_{\ell\geq3}(2\max_jy_j)^\ell=O(n^{-2}).
$$

지수함수를 전개하면 균일하게

$$
\mathbb E z^K=e^{k(z-1)}\left[1+\frac1n\left(d(z-1)+\frac v2(z-1)^2\right)\right]+O(n^{-2}).
$$

오차는 단위원판에서 해석적이다. Cauchy 계수 추출로 고정된 $m$의 확률에도 $O(n^{-2})$ 오차를 얻는다. 무한 Poisson–Charlier 급수의 수렴을 가정할 필요가 없다.

### 3.3. 이웃 확률의 동률을 푼다

$\pi_k(m)=e^{-k}k^m/m!$라 하면

$$
\Pr(K=m)=\pi_k(m)\left[1+\frac{A_m}{n}\right]+O(n^{-2}),
$$

$$
A_m=d\left(\frac m k-1\right)
+\frac v2\left(\frac{m(m-1)}{k^2}-\frac{2m}k+1\right).
$$

이는 평균 이동과 두 번째 Charlier 보정의 합이다. $\pi_k(k)=\pi_k(k-1)>0$와

$$
A_k-A_{k-1}=\frac d k-\frac v{k^2}
=\frac{v}{k}\left(\theta+\frac32-\frac1k-\beta\right)
$$

에서

$$
\frac{F_{n,k+1}(\theta n+\beta)}{F_{n,k}(\theta n+\beta)}
=1+\frac{v}{kn}(\beta_k-\beta)+O(n^{-2})
$$

가 나온다. 여기서 $u/v=\theta+1/2$를 썼다.

원 노트에서 증명한 비율의 $a$에 대한 엄격한 감소를 이용하면, $\beta=\beta_k\pm1$에서 부호가 갈려 전환점을 유계 구간 안에 가둘 수 있다. 그 구간에서의 균일 전개에 실제 전환점을 대입하면 $\beta-\beta_k=O(n^{-1})$이므로 후보 식 전체를 얻는다. $k=1$에도 $m=0$을 포함한 계산이 그대로 성립한다.

상수항은 $u/v+1-1/k$다. 끝점 보정, 기하분포 평균의 한 칸 이동, 두 번째 계승 누적량만으로 결정된다. 따라서 단순히 포아송 극한이 동률이라는 사실보다 강하지만, 새로운 종류의 보정 기법이 필요하지는 않다.

## 4. 신규성 판단과 남은 확인

구별할 사실은 세 가지다.

1. **확인됨:** 이 상수항은 기존 Poisson–Charlier 틀의 첫 보정과 표준 합 근사로 얻어진다. 위 계산은 나머지까지 직접 확인한다.
2. **미확인:** 이 특정 역수 격자 모형의 전환점 식이 기존 원문에 이미 명시되어 있는가. 동일식을 직접 진술한 문헌은 이번 조사에서 확인하지 못했다. 검색 실패가 신규성의 증거는 아니다.
3. **평가 판단:** 기존 도구를 썼다는 이유만으로 새 특수 결과를 배제할 수는 없다. 그러나 이 식이 일반 전개의 단순한 대입을 넘어서는 어떤 기여인지도 아직 확인되지 않았다. 현재 점수는 유지하고 10점 후보의 상향 판단을 보류한다.

다음 별도 세션 검토자는 이 식 하나에 대해 판정하면 된다. 가장 가까운 문헌의 정리 번호·가정·모형 대응을 제시해 **이미 발표된 식 / 알려진 일반 정리의 통상적 특수화 / 선행 결과와 구별되는 작은 결과 / 조사 불충분**을 구분한다. 새로움이 남는다면 정확히 무엇인지 한 문장으로 적는다. 증명의 정확성 통과만으로 상향하지 않는다.

Barbour 원문의 비동일 기하분포 합에 대한 전개와, 이 모형이 다른 이름으로 연구되었는지 확인하는 것이 남아 있다. KMS 정리의 이름이 비슷하다는 이유나, 같은 문자열을 검색하지 못했다는 이유로 판정을 끝내지 않는다.

## 5. 검색과 재현 기록

확인일은 위 날짜와 같다. 검색 결과의 모든 문헌을 읽었다는 뜻은 아니다. 적용 판단에 사용한 원문과 읽은 부분은 §2에 한정했다.

- `Poisson Charlier expansion sum independent geometric variables factorial cumulants second order`
- `"mode" "Poisson-Charlier"`
- `"complete homogeneous" "mode" "geometric"`
- `"Poisson approximation" "mode" "geometric"`
- `"Mod-discrete expansions" Barbour Kowalski Nikeghbali geometric`
- `"Poisson" "geometric" "Charlier" Barbour Roos`
- `"Asymptotic expansions in the Poisson limit theorem" Barbour 1987`
- `"sum of independent geometric" "mode" approximation`
- `"Poisson-Charlier" "mode" correction`
- `"theta" "3/2" "mode" "geometric"`
- `"e^k-1" "mode"`

추가 검산은 [verify_transition_novelty.py](verify_transition_novelty.py)로 재현한다. 정확한 유리수 기하분포 합의 계수와 원래 교대합 비율을 대조하고, 생성함수 계수 추출로 얻은 보정이 상수항과 일치하는지 확인한다. 유한 검산은 위 증명이나 문헌 신규성 판정을 대신하지 않는다.
