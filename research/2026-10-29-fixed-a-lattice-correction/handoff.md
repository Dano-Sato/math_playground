# 작업 인계와 자체 점검

- 작업 ID: 2026-10-29-fixed-a-lattice-correction
- 날짜: 2026-10-29
- 작성 세션 단독 작업. 추가 에이전트 실행 없음. 독립 검토 미실시.
- 결과: [note.md](note.md), 평가: [meta.json](meta.json), 문헌 비교: [novelty.md](novelty.md).

## 결과

Q-018의 고정 a>1 역로그 보정항을 증명했다. 실수 최대점의 보정은 delta,
정수 선택 중심의 보정은 eta=delta+1/24이다. 정확한 실수 최대점을 반올림해도
정수 최대점을 틀리는 n이 무한히 많음을 명시적인 수열로 증명했다.
기존 노트의 반정수에서 떨어진 영역의 반올림 정리와 모순되지 않는다.

## 자체 점검

- n>=1, a>1, s>0을 명시했다. log n의 역수는 n→∞ 점근식에서만 사용한다.
- a=1은 Gamma(a−1)와 무한 꼬리 때문에 제외되며 균일성을 주장하지 않는다.
- 정규화 분모는 Gamma(b)>0으로 수렴하므로 나눗셈이 정당하다.
- Taylor 전개는 중심 구간에서만 수행했다. 중간 꼬리와 아래 끝점의 로그 특이점을 따로 제어했다.
- x의 유계 구간에서 균일한 나머지를 얻은 뒤 근에 대입했다.
- 도함수 점근식 자체를 다시 미분하지 않고 길이 1 구간에 적분해 정수 보정을 얻었다.
- m_n의 존재·유일성과 전역적인 정수 선택은 모든 n>=1에서 증명했다.
  반정수 동률은 두 최대점으로 명시했다.
- 반례 수열 n_j의 정수 반올림 오차가 지수적으로 작음을 확인했다.
- 계산 결과를 무한 범위의 증명이나 독립 검토로 기록하지 않았다.

## 실제 검증 명령과 출력

환경: Python 3.10.11, 표준 라이브러리. 난수 없음.

~~~text
python research/2026-10-29-fixed-a-lattice-correction/verify.py
PASS exact rational algebra: 625 cases
PASS quadrature calibration: 48 cases; max log error 1.24e-14
PASS roots: 24 settings, two grids; max root difference 1.38e-09
a=3, j=25: round(s*)=26, integer max=26, log ratio=9.03330995e-05
a=3, j=45: round(s*)=46, integer max=46, log ratio=2.09391249e-05
a=3, j=85: round(s*)=85, integer max=86, log ratio=4.55155035e-06
a=3, j=155: round(s*)=155, integer max=156, log ratio=1.15020049e-06
PASS; numerical values are observations, not interval certificates.
~~~

실제 상세 값은 [verification.json](verification.json)에 있다.
구성한 n_j에서 충분히 큰 j만 반례라는 점에 주의한다. j=25,45는 반례가 아니며 삭제하지 않았다.
처음 log n<=160의 a=1.5 수치 검산에서 점근 잔차 허용 기준이 실패했다.
큰 보정계수와 느린 수렴을 확인한 뒤 탐색 범위를 log n<=640으로 늘렸다.
이는 이론의 n 문턱을 명시적으로 인증한 것이 아니다.

## 위키 반영과 미해결

추가 링크: [실수 최대점과 정수 선택의 로그 보정](note.md).
Q-018은 자체 증명 완료·독립 검토 미실시로 변경한다.
공용 홈·분야별 목록·노트 목록·연구 기록에 같은 링크를 반영한다.

기존 노트 원문과 기존 meta.json은 수정하지 않는다. Q-017의 중간 영역,
a→1 동시 극한, 명시적인 오차 상수, 반정수의 더 작은 창의 판정은 미해결이다.
기존 작업트리의 수정·미추적 연구는 보존했다.

최종 검사:

~~~text
python tools/check_wiki.py
PASS: 593 local links in 81 Markdown files.
Templates and code skipped; headings and external URLs not checked.
git diff --check
[공백 오류 없음. 기존 수정 파일의 LF/CRLF 안내만 출력됨.]
~~~
