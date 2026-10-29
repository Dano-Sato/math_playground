# 부분순서 폐포 압축의 신규성 조사

- 확인일: 2026-10-29
- 조사자: 작성 세션
- 독립 검토: 미실시
- 결론: 이번 약수 전이의 정확한 부분순서 높이와 압축을 통한 전체 순환 분류는 위키에서 새로 도출했다. 최종 외부 신규성은 미확인이다.

## 후보 기여와 알려진 원리 구분

후보는 세 가지다.

1. 이전 구간 참조 관계가 부분순서이며 높이가 1/2/3으로 완전히 분류되고, 첫 높이 3이 c=136에서 생긴다.
2. 그 아래 폐포 Q와 응답 R로 F=RQ, T=QR를 구성하여 모든 순환을 보존하는 구체적 압축을 얻는다.
3. c=64,65의 공통 32비트 함수에서 75개 순환과 독립집합 초기 상태의 극값을 완전히 분류한다.

부분순서와 멱등 관계의 연결, 폐포라는 개념, 함수 합성에 의한 순환 대응, 유한 함수 그래프에서 순환을 찾는 알고리즘 자체는 새로운 원리라고 주장하지 않는다.

## 실제 확인한 가장 가까운 자료

### Plemmons–West(1970)

“On the semigroup of binary relations”, Pacific Journal of Mathematics 35(3), 743–757.
[원문](https://msp.org/pjm/1970/35-3/pjm-v35-n3-p23-s.pdf).

초록과 관계 합성의 정의, Theorem 2.4 및 증명을 확인했다. 부분순서가 멱등 관계를 준다는 사실은 고전적인 내용이다. 이번 논증의 차이는 약수 조건의 비율을 사용해 특정 B가 추이적이고 높이가 최대 3임을 보이는 부분이다. 일반 관계 대수의 새 정리를 얻었다고 하지 않는다.

### España–Funez–Ugalde(2025), 확인 버전 v1

“Dominant vertices and attractors’ landscape for Boolean networks”, arXiv:2509.03654v1, 2025-09-03.
[확인한 원문](https://arxiv.org/html/2509.03654v1).

§3의 Theorem 2, 관련 설명, Corollary 1을 확인했다. 지배 정점과 유한 기억에 의한 반공액 축소에서 순환 위의 일대일 대응, 과도 길이 차이의 상한을 다룬다. 일반적인 장기 동역학 보존과 과도 제어는 기존 연구 주제다.

이번 Q는 정점 일부를 투영해 기억을 붙이는 방식이 아니라, 이전 구간의 차단 영향을 아래 폐포로 묶는 사상이다. F=RQ, T=QR의 순환 보존은 본문에서 직접 증명했으며, 그 합성 원리 자체를 독창적인 일반 정리라고 평가하지 않는다. 읽은 것은 명시한 v1이고 이후 버전은 조사하지 않았다.

### Schwieger–Tonello, DMTCS 학술지 페이지

“Reduction for asynchronous Boolean networks: elimination of negatively autoregulated components”, DOI 10.46298/dmtcs.10930.
[학술지 원문 안내](https://dmtcs.episciences.org/articles/13213).

학술지 페이지의 서지와 초록만 확인했다. 비동기 불 네트워크에서 변수 제거가 순환을 자동으로 보존하지 않으며 추가 조건이 필요하다는 연구다. 이번 전이는 결정적 고정 함수이고, 적용하는 사상도 다르다. 이 논문을 근거로 이번 압축이 옳다고 주장하지 않았고, 직접 순환 보존을 증명했다.

## 실제 검색어

- "finite dynamical systems" "AB" "BA"
- "dynamical systems" "factorization" "periodic points" finite
- "Boolean matrix" "idempotent" "partial order" closure
- "divisor game" "poset" periodic
- "finite dynamical systems" reduction "periodic" quotient
- "Boolean networks" "reduction" "attractors" preservation arxiv
- "divisor nim" "closure" "order"

이번 약수 하한 게임의 높이 문턱 136이나 동일 32비트 함수의 전체 순환 분류를 명시한 자료는 이 검색 범위에서 찾지 못했다. 검색 결과가 없다는 것은 신규성 증명이 아니다. 약수 게임의 관련 2017년 후속 원문은 앞선 노트에서도 본문 미확인으로 남아 있어, 최종 대조 공백도 유지한다.

## 위키 내부의 실제 차이와 평가

앞선 [유한 상태 노트](../2026-10-29-divisor-outcome-automaton/note.md)는 실제 초기 상태의 궤도를, [주기 상한 노트](../2026-10-29-divisor-period-growth/note.md)는 독립집합 상한과 두 순환의 존재를 다뤘다. 이번에는 B의 산술 순서 구조를 새로 보이고, 그로부터 압축 함수를 만들어 모든 순환을 완전히 분류했다.

서로 다른 두 생성기와 그래프 분석이 같은 결과를 낸 것은 자체 구현 점검이며 독립 에이전트 검토가 아니다. 외부 신규성·중요도는 확인되지 않았고, 일반 주기 상한이나 전체 Grundy 문턱을 해결하지 않았다. 점수와 근거는 [meta.json](meta.json)에만 기록한다.
