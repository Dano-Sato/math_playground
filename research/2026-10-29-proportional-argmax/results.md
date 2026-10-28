# 계산 기록

[연구 노트](note.md)

- 실행일: 2026-10-29
- 환경: Windows 11, Python 3.10.11, 표준 라이브러리만 사용, 난수 없음
- 명령: `python research/2026-10-29-proportional-argmax/verify.py` (저장소 루트), 약 24초

## 실제 출력

```text
[threshold] theta=1/(e-1) gives t0=1.000000000000 (D_2 = D_1 boundary in the limit)
[real maximizer] s*(n, theta n) vs s_inf + c/n
  theta=0.1: t0=2.397895, s_inf=2.880831, c=10.76306
    n=  25: s*=3.465122, n(s*-s_inf)=14.60727, n(s*-s_inf)-c=+3.84421
    n=  50: s*=3.127808, n(s*-s_inf)=12.34885, n(s*-s_inf)-c=+1.58579
    n= 100: s*=2.995766, n(s*-s_inf)=11.49348, n(s*-s_inf)-c=+0.73042
    n= 200: s*=2.936404, n(s*-s_inf)=11.11453, n(s*-s_inf)-c=+0.35147
  theta=0.5: t0=1.098612, s_inf=1.563286, c=1.45030
    n=  25: s*=1.624949, n(s*-s_inf)=1.54157, n(s*-s_inf)-c=+0.09127
    n=  50: s*=1.593177, n(s*-s_inf)=1.49452, n(s*-s_inf)-c=+0.04422
    n= 100: s*=1.578007, n(s*-s_inf)=1.47208, n(s*-s_inf)-c=+0.02177
    n= 200: s*=1.570592, n(s*-s_inf)=1.46111, n(s*-s_inf)-c=+0.01080
  theta=1.0: t0=0.693147, s_inf=1.140994, c=0.52065
    n=  25: s*=1.162559, n(s*-s_inf)=0.53915, n(s*-s_inf)-c=+0.01849
    n=  50: s*=1.151589, n(s*-s_inf)=0.52976, n(s*-s_inf)-c=+0.00910
    n= 100: s*=1.146245, n(s*-s_inf)=0.52517, n(s*-s_inf)-c=+0.00452
    n= 200: s*=1.143608, n(s*-s_inf)=0.52290, n(s*-s_inf)-c=+0.00225
  theta=3.0: t0=0.287682, s_inf=0.690964, c=0.06886
    n=  25: s*=0.693778, n(s*-s_inf)=0.07037, n(s*-s_inf)-c=+0.00152
    n=  50: s*=0.692356, n(s*-s_inf)=0.06961, n(s*-s_inf)-c=+0.00075
    n= 100: s*=0.691656, n(s*-s_inf)=0.06923, n(s*-s_inf)-c=+0.00038
    n= 200: s*=0.691309, n(s*-s_inf)=0.06904, n(s*-s_inf)-c=+0.00019
[integer argmax / Poisson profile] exact Fractions, a = theta n
  theta=1/30, n=200: integer argmax=4 (= floor(t0)+1, t0=3.4340), max rel. profile error r<=5: 1.82e-01
  theta=1/30, n=400: integer argmax=4 (= floor(t0)+1, t0=3.4340), max rel. profile error r<=5: 8.64e-02
  theta=1/10, n=200: integer argmax=3 (= floor(t0)+1, t0=2.3979), max rel. profile error r<=5: 9.75e-02
  theta=1/10, n=400: integer argmax=3 (= floor(t0)+1, t0=2.3979), max rel. profile error r<=5: 4.76e-02
  theta=1/2, n=200: integer argmax=2 (= floor(t0)+1, t0=1.0986), max rel. profile error r<=5: 5.87e-02
  theta=1/2, n=400: integer argmax=2 (= floor(t0)+1, t0=1.0986), max rel. profile error r<=5: 2.90e-02
  theta=1, n=200: integer argmax=1 (= floor(t0)+1, t0=0.6931), max rel. profile error r<=5: 5.39e-02
  theta=1, n=400: integer argmax=1 (= floor(t0)+1, t0=0.6931), max rel. profile error r<=5: 2.67e-02
  theta=3, n=200: integer argmax=1 (= floor(t0)+1, t0=0.2877), max rel. profile error r<=5: 5.14e-02
  theta=3, n=400: integer argmax=1 (= floor(t0)+1, t0=0.2877), max rel. profile error r<=5: 2.55e-02
ALL CHECKS PASSED
```

## 해석

- 실수 최대점: 잔차 $n(s^*-s_\infty)-c(	heta)$가 $n$을 두 배로 할 때마다 거의 정확히 절반이 된다. 주장 4의 $O(n^{-2})$ 나머지와 맞는 관찰이다.
- 정수 최대점은 시험한 10개 설정 모두 $\lfloor t_0floor+1$이었다. 포아송 모양의 상대 오차는 $n$을 두 배로 하면 약 절반이 된다($O(1/n)$로 보임).
- 작성 중에 $	heta=1/100$, $n=100$($a=1$)에서는 정수 최대점이 9로 극한값 5와 달랐다. 비례 영역에 아직 들어가지 않은 경우이므로 최종 검사에서 제외했다. 이 관찰은 §6에 남겼다.
