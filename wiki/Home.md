# 수학 탐구 위키

질문에서 시작해 관찰, 추측, 증명, 반례를 축적합니다. 분야는 제한하지 않습니다.

| 찾아보기 | 내용 |
| --- | --- |
| [전체 연구 노트](ResearchNotes.md) | 노트 목록과 노트별 평가 원본 |
| [웹뷰어 사용법](Viewer.md) | CMD로 열기, 자동 수집, 검색·점수순 정렬 |
| [점수 기준](Scoring.md) | 100점 밀레니엄급·80점 필즈급의 내부 척도 |
| [분야별 목록](Topics.md) | 주제별 연구 노트 |
| [열린 질문](Questions.md) | 다음 탐구 후보와 진행 상태 |
| [연구 기록](ResearchLog.md) | 추가된 결과와 검토 이력 |
| [연구 규약](Conventions.md) | 주장 상태, 검토, 파일 작성 방식 |
| [에이전트 지침](../AGENTS.md) | 여러 에이전트의 담당 범위와 협업 규칙 |

## 최근 연구

| 연구 | 핵심 결과 | 검토 |
| --- | --- | --- |
| [부분순서 폐포로 압축한 약수 게임](../research/2026-10-29-divisor-order-quotient/note.md) | 이전 구간 관계의 높이는 최대 3, 첫 높이 3은 c=136. 모든 순환을 보존하는 압축으로 c=64,65 공통 함수의 75개 순환 완전 분류. | 자체 채점 · 검토 미실시 |
| [약수 게임의 주기 상한과 서로 다른 순환](../research/2026-10-29-divisor-period-growth/note.md) | 독립집합·3진 매칭으로 상태 상한 개선. 같은 전이의 c=64,65가 주기 8,6을 선택하고 c=32→33에서 로그 계수가 감소. | 자체 채점 · 검토 미실시 |
| [모든 하한의 약수 게임: 승패의 유한 상태](../research/2026-10-29-divisor-outcome-automaton/note.md) | 모든 $c\ge2$에서 지수 방향 승패의 꼬리 주기 증명. 패배 위치 수는 $\lceil N/2\rceil+\alpha_c\log_2N+O_c(1)$, $\alpha_c$는 계산 가능한 양의 유리수. | 자체 채점 · 검토 미실시 |
| [하한 4 약수 게임: 최적 문턱 87과 주기 3](../research/2026-10-29-divisor-four-period/note.md) | Q-019의 $c=4$ 해결: 전체 Grundy 공식, 최적 문턱 87, 지수 28 이후 3잔여류 규칙. 승패는 별도 손 증명. | 자체 채점 · 검토 미실시 |
| [포아송 동률 경계와 유한 전환점](../research/2026-10-29-critical-mode-boundary/note.md) | Q-016: 큰 정수 지수 쪽이 선택되는 방향과 명시적 충분조건, 전환점 $a_{n,k}=n\theta_k+\theta_k+3/2-1/k+O(1/n)$. | 자체 채점 · 검토 미실시 |
| [약수 뺄셈 게임의 하한 일반화](../research/2026-10-29-divisor-game-lower-bound/note.md) | Q-019: $c\le d<n$ 게임에서 $c=3$은 "2의 거듭제곱이 아니면 $g=v_2$"(손 증명), $c=5,8$ 완전 결정, 모든 $c$의 문턱값 존재 추측. | 자체 채점 · 검토 미실시 |
| [자명하지 않은 약수를 빼는 게임의 Grundy 값](../research/2026-10-29-nontrivial-divisor-game/note.md) | $n\mapsto n-d$ ($1<d<n$, $d\mid n$): 홀수 부분 17 이상이면 $g=v_2(n)$, 작은 홀수 부분 여덟 열의 예외를 완전 결정. OEIS 미등록. 패배 위치는 Codeforces 1537D로 알려짐. | [v1 검토: 수정 필요 → v2 반영](../research/2026-10-29-nontrivial-divisor-game-review/review.md) |
| [고정된 a에서 최대 지수의 점근](../research/2026-10-29-fixed-a-argmax/note.md) | Q-015·Q-011(고정 영역): $s^*_n=\log n+	frac12-\psi(a-1)+o(1)$, 정수 최대점은 그 근사의 반올림. | 자체 채점 · 검토 미실시 |
| [비례 영역의 최대 지수와 포아송 모양 극한](../research/2026-10-29-proportional-argmax/note.md) | Q-013·Q-011(비례 영역): $a=\theta n$에서 지수 방향 모양이 포아송으로 수렴, 정수 최대점 $\lfloor\log(1+1/\theta)\rfloor+1$. | 자체 채점 · 검토 미실시 |
| [실수 지수 로그 오목성과 날카로운 곡률 경계](../research/2026-10-29-real-log-concavity/note.md) | Q-010·012: 양의 실수 지수 전체와 비균등 간격에서 엄격한 로그 오목성과 양면 날카로운 곡률 경계. 정수 경계 재증명, 실수 단봉성. 로그 오목성은 Berwald–Borell 부등식의 직접적 따름정리임을 확인. | [v1 검토: 수정 필요(경미)→v1.1 반영](../research/2026-10-29-real-log-concavity-review/review.md) |
| [로그 오목성·날카로운 경계·단봉성](../research/2026-10-29-turan-unimodality/note.md) | Q-006·007: 이웃 항의 날카로운 비율 경계, 지수 방향의 단봉성, 적률에 의한 이전 하계 개선. | [독립 검토 통과](../research/2026-10-29-turan-review/review.md) |
| [교대 이항합의 양수 표현과 안정적인 계산](../research/2026-10-29-reciprocal-binomial/note.md) | 역수 거듭제곱 합의 일반식, 양수성, 상하계, 점근식. 직접 실수 계산의 상쇄 오차도 재현. | [독립 검토 통과](../research/2026-10-29-reciprocal-review/review.md) |
| [실수 지수와 비균등 차분](../research/2026-10-29-real-power-differences/note.md) | 모든 실수 지수에서 영점·부호를 분류. 양의 비균등 차분 간격에도 확장. | [독립 검토 통과](../research/2026-10-29-reciprocal-review/review-real.md) |

## 첫 연구 노트

[유한 차분으로 보는 교대 이항합](../research/2026-10-29-finite-differences/note.md)

이항계수가 섞인 교대합이 왜 0이 되는지 살펴보고, 다항식과 전사 함수의 개수로 연결합니다. 일반적인 항등식의 자체 증명과 정확한 정수 계산이 포함되어 있습니다. 독립 에이전트 검토는 대기 중입니다.

## 새 연구 시작

[연구 노트 양식](../templates/research-note.md)을 자신의 연구 폴더에 복사합니다. 진행 중인 연구는 다른 사람이 이어받을 수 있도록 가정, 시도, 실패 이유를 남깁니다.
