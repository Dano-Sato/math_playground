# 문헌 관계와 신규성 한계

- 조사일: 2026-10-29
- 후보: 모든 하한에서 $\alpha_c=\Omega(c/(\ln c)^3)$, 정확한 열 가중치 약수 공식, 순환 없는 하한 인증.
- 외부 신규성: 미확인.
- 독립 검토: 미실시.

## 무엇이 이번 위키에 새로 들어왔는가

[이전 보편 정리](../2026-10-29-divisor-outcome-automaton/note.md)는
각 고정 c에서 $0<\alpha_c\le\lfloor c/2\rfloor/2$를 주었다.
c에 대한 양성의 균일한 발산 하한은 없었다.
[주기 성장 노트](../2026-10-29-divisor-period-growth/note.md)는
비단조성과 개별 유한 순환을 확인했지만 발산은 결정하지 않았다.

이번 [본문](note.md)은 다음을 더한다.

1. 이동을 역으로 보아 한 패배 좌표가 덮는 행의 개수를 약수 식으로 정확히 계산한다.
2. 모든 순환의 시간 평균에 분수 덮개 제약과 빈도 1/2 제한을 적용한다.
3. 가중치의 이차 모멘트를 약수 함수 제곱합으로 제한하여,
   c가 변할 때도 유효한 하한과 발산을 증명한다.
4. 게임의 주기나 전체 간선 그래프를 만들지 않는 체와 정렬로 더 강한 유한 하한을 계산한다.

이는 기존 값의 표를 더 늘리는 데 그치지 않는 새로운 위키 내부 진술이다.
이것만으로 외부 문헌상 새 결과라고 단정하지 않는다.

## 확인한 선행 자료와 구체적인 관계

| 자료 | 실제 읽은 범위 | 알려진 부분 | 이번 적용과의 차이·한계 |
| --- | --- | --- | --- |
| Chappell–Gimbel–Hartman, arXiv:1701.05961v1(2017) | 서론의 분수 지배 정의와 Lemma 1 | 폐이웃의 합 제약, 최대 차수에 의한 일반 하한 | 우리의 덮개 원리를 새 일반 정리로 보지 않는다. 시간 지연·대각 중복이 있는 약수 의존 행렬의 열을 식으로 계산한 것이 적용상의 단계이다. |
| Landesman, Soundararajan 강의 노트(2017), §5.4 | 인쇄 pp.26–27의 약수 함수 제곱합 설명 | $\sum_{n\le X}\tau(n)^2$의 $X(\ln X)^3$ 차수 | 이차 모멘트 추정 자체는 고전적이다. 이 노트는 필요한 약한 명시적 상한을 초등적으로 증명해 약수 게임의 열 가중치에 적용한다. |
| Harutyunyan–Le–Newman–Thomassé, arXiv:1708.00423v3 | 초록·서지 | 유향 분수 지배를 다루는 일반 연구 | 본문 미독. 이 논문의 정리를 적용하지 않았으며 약수 게임의 계수 정리가 없다고 단정하지도 않는다. |
| Maeyama–Makino–Ochiai(2016), 약수 Nim 발표 | 앞선 집중 조사에서 규칙·정리 1–2 확인 | c=2의 승패와 큰 n의 Grundy 공식 | 확인한 부분은 일반 c가 커지는 계수 하한을 진술하지 않는다. |
| 같은 저자의 2017년 후속 (II) | 공식 서지, 본문 미독 | 내용 범위 미판정 | 이전 조사에서 남은 직접 선행연구의 공백이다. 이번에도 확보했다고 하지 않는다. |

## 원문 링크

모두 확인일 2026-10-29.

- [Chappell–Gimbel–Hartman 원문](https://arxiv.org/html/1701.05961).
- [Landesman 강의 노트 원문](https://people.math.harvard.edu/~landesman/assets/analytic-number-theory-notes.pdf).
- [유향 분수 지배의 초록·서지](https://arxiv.org/abs/1708.00423).
- [2016년 발표 원문](https://www.ns.kogakuin.ac.jp/~ft40433/kumss/20160716-fuzzy-sympo-175-proceedings-r.pdf).
- [2017년 후속 공식 서지](https://ndlsearch.ndl.go.jp/books/R000000004-I029975967).
- [앞선 게임 문헌 집중 대조와 접근 기록](../2026-10-29-divisor-novelty-audit/note.md).

## 사용한 검색어

- divisor subtraction game lower bound logarithmic losing positions coefficient
- fractional domination degree square sum lower bound graph domination
- sum divisor function squared x log cubed elementary proof d(n)^2 d4
- divisor Nim logarithmic lower bound
- divisor game domination cutoff
- 約数ニム 下限

첫 번째와 마지막 검색들에서는 같은 하한을 다루는 공개 원문을 찾지 못했다.
이 검색 결과를 논문의 비존재나 후보의 신규성 증명으로 사용하지 않는다.
일반 덮개 이론과 약수 이차 모멘트의 단순 결합이라는 해석 가능성도 평가에 반영한다.

## 평가의 범위

직접 선행연구 전체와의 차이는 아직 확정하지 못했다.
따라서 문헌상 독창성이 확인된 성과 구간으로 올리지 않는다.
재평가에는 2017년 후속을 포함한 하한 매개변수의 선행 분석,
또는 이 특정 열 공식·계수 성장 하한과 일치하는 문헌의 원문 대조가 필요하다.
검색 횟수·검산 수·문서 길이를 기여의 중요도로 환산하지 않는다.
