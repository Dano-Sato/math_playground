# 전환점 신규성 조사: 추가 검산

[집중 조사](transition-novelty-review.md) · [검산 코드](verify_transition_novelty.py)

명령: `python research/2026-10-29-critical-mode-boundary/verify_transition_novelty.py`

환경: Python 3.10.11, 표준 라이브러리, 난수 없음.

- 정확한 기하분포 합과 교대합의 이웃 비율 대응: 256건 통과.
- 생성함수 계수 추출과 전환점 상수 보정의 유리수 항등식: 144건 통과.

첫 검산 범위: n=1..8, a=3/2,2,5,101/10, k=1..8.

둘째 검산 범위: 형식 변수 theta=1/10,1/2,1,3, k=1..12, beta=beta_star-1,beta_star,beta_star+1. 초월수 theta_k를 유리수로 간주하지 않는다.

유한 검산이며 점근 나머지의 증명이나 문헌 신규성 검증이 아니다.
