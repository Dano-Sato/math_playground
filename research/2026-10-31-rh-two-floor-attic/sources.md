# 문헌 확인과 신규성 판단

- 확인일: 2026-10-31 (Asia/Seoul)
- 목적: 리만 가설의 알려진 적률 환원을 새 해결책으로 오인하지 않고, 사용하는 외부 정리의 정확한 가정을 확인한다.
- 이 조사는 작성 세션의 조사이며 독립 검토가 아니다.

## 실제 사용한 검색어

- `Riemann hypothesis Hankel matrices power sums zeros Stieltjes moment criterion xi function`
- `site.claymath.org Riemann hypothesis problem description xi function`
- `Stieltjes moment problem positive semidefinite Hankel two matrices theorem paper pdf`
- `site.dlmf.nist.gov 25.4 xi function 25.10 zeros`

검색 결과의 초록이나 요약만 보고 참이라고 채택하지 않았다. 아래 자료의 실제 열린 본문 범위를 사용했다. 모든 논문 전체를 검토했다고 주장하지 않는다.

## 확인한 원문과 사용 범위

1. Clay Mathematics Institute, [Riemann Hypothesis](https://www.claymath.org/millennium/riemann-hypothesis/).
   공식 문제 진술과 `Unsolved` 분류를 확인했다. 웹페이지에 적힌 수치 검증 개수는 연구의 근거로 사용하지 않았다.
2. NIST DLMF, [§25.4 Reflection Formulas](https://dlmf.nist.gov/25.4), 식 25.4.3–4와 [§25.10 Zeros](https://dlmf.nist.gov/25.10), (i).
   ξ의 정의·함수방정식, 비자명 영점과 임계선의 관계를 확인했다.
3. Ruiming Zhang, [On Power Sums of Positive Numbers, arXiv:1510.03420v2](https://arxiv.org/html/1510.03420), 2016-02-22 개정본.
   §2의 정준곱·제곱근 변환, §3 Corollary 4와 Theorem 5, §4.3의 증명을 읽었다. 같은 제곱근 변환과 영점 역수 거듭제곱합을 이용한 RH 판정이 선행한다. 그 논문은 Hausdorff 적률의 유한차분 양수성으로 서술한다. 우리 두 Hankel 행렬 표현은 Stieltjes 정리를 적용한 다른 표기이며, 그 차이로 신규성을 주장하지 않는다.
4. Konrad Schmüdgen, [The Stieltjes condition and multidimensional K-moment problems](https://link.springer.com/article/10.1007/s00013-021-01599-9), Archiv der Mathematik 117 (2021), 179–188.
   §1 및 §2 식 (4)까지 확인했다. 일변수에서는 모든 다항식 p에 대한 L(p²)≥0, L(xp²)≥0가 양의 반직선 적률 표현의 필요충분조건임을 사용했다. 다변수 일반화의 증명은 이번 연구에 사용하지 않았다.

## 주장별 평가

| 주장 | 가까운 선행 이론 | 차이와 평가 |
| --- | --- | --- |
| 두 Hankel 층과 RH의 동치 | Zhang의 genus 0 영점·적률 판정, 고전적 Stieltjes 정리 | 알려진 구조의 재유도. 돌파구 아님 |
| 유한 크기 양수성 뒤의 비실수 영점 | 양의 정부호의 개방성, 유한 지지 적률, Vandermonde 행렬식 | 명시적인 모형으로 구성. 표준 원리의 적용이며 외부 최초성 미확인 |
| 양의 Fourier 밀도·차수·띠만으로 부족 | 양의 Fourier 변환과 실수 영점의 구별 | 설명용 삼각밀도 반례를 직접 구성. 새 일반 이론이 아님 |

이 노트에서 10점 이상 잠재 성과로 볼 만한 선행 결과 대비 개선은 확인되지 않았다. 문헌상 신규성이나 RH 해결을 주장하지 않는다. 더 광범위한 Hankel 판정 문헌의 완전한 서지 조사는 수행하지 않았다.
