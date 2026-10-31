# 작업 인계와 자체 점검

- 작업 ID: 2026-10-29-rounding-frequency
- 날짜: 2026-10-29
- 작성 세션 단독 작업. 추가 에이전트 실행 없음. 독립 검토 미실시.
- 결과: [note.md](note.md), 평가: [meta.json](meta.json), 문헌 비교: [novelty.md](novelty.md).

## 결과

Q-031을 새로 다뤘다. 정확한 실수 최대점의 반올림이 틀리는 n의 개수는 Θ(X/log X)이다.
그러나 (log X)E_a(X)/X는 수렴하지 않으며, 극한점 집합이 보편적인 닫힌 구간이다.
실패 n의 역수 합에서 (1/24)log log X를 빼면 유한한 상수로 수렴한다.
상수 C_a의 실제 값은 계산하지 않았다.

## 증명 자체 점검

- n>=1, a>1, s>0을 명시하고, 작은 s의 반올림은 양의 정수 1로 보정했다.
- 점근식에서 log n 또는 T_j로 나누는 것은 충분히 큰 입력에서만 한다.
- 반정수에서는 위쪽 반올림을 사용한다. 정수 최대점이 두 개면 어느 하나도 성공으로 친다.
  따라서 실제 실패 구간의 두 끝점은 모두 제외된다.
- 연속 n 보간에서는 유한 이항합이 아닌 양수 적분을 정의했다.
  연속 n 전체의 로그 오목성을 증명 없이 쓰지 않았다.
- 연속 n에 대한 두 경계의 단조성은 서로 다른 공분산 항등식으로 확인했다.
- 기존 균일 적분 전개는 실수 n에서도 같은 증명으로 작동함을 명시했다.
- 실제 구간과 근사 구간의 끝점 오차를 합쳐 X/(log X)^2 오차를 제어했다.
- 마지막 구간이 일부만 지난 경우를 잘라 세었다. 고정 위상 공식을 전 위상에 잘못 적용하지 않았다.
- 정수 개수와 연속 길이의 차이는 구간당 상수 이하이며, 역수 합 오차는 절대 수렴한다.
- 조화합 상수의 존재에는 유한 초기 실패를 포함시켰다. 값을 구했다고 하지 않았다.
- 기존 반올림 노트·다른 연구 폴더는 수정하지 않았다.

## 실제 검증 명령과 결과

Python 3.10.11, 표준 라이브러리, 난수 없음.

~~~text
python research/2026-10-29-rounding-frequency/verify.py
PASS exact integer interval checks: 15
PASS boundary roots: 12 settings, two grids; max difference 0
Computed 121 a=3 windows (j=20..140); all have positive widths.
Theoretical scaled range: [0.024249029, 0.065915696]
j=140, 0: observed=0.024935673, predicted=0.024249029
j=140, 0.1: observed=0.060929515, predicted=0.059642988
j=140, 0.5: observed=0.040958533, predicted=0.039979891
j=140, 0.9: observed=0.027533256, predicted=0.026799322
j=140, left: observed=0.024788137, predicted=0.024104531
j=140, middle: observed=0.045831410, predicted=0.039977129
j=140, right: observed=0.066871573, predicted=0.061017180
Harmonic observation j=40: centered=-0.122731294
Harmonic observation j=80: centered=-0.122262889
Harmonic observation j=140: centered=-0.122054902
PASS; quadrature and continuous counts are observations, not integer-count certificates.
~~~

상세 입력·출력은 [verification.json](verification.json)에 있다.
두 Simpson 격자의 같은 값은 부동소수점 및 이분법 해상도에서 같다는 뜻이며,
정확한 실수 경계나 개수를 인증하는 구간 계산이 아니다.
121개 구간의 조화합은 초기 구간을 뺐으므로 위의 수치가 C_a 자체는 아니다.

## 공용 위키 반영

추가 링크: [반올림 실패의 빈도와 진동](note.md).
Q-031을 자체 증명 완료·독립 검토 미실시로 등록하고 홈·노트 목록·분야·연구 기록에 연결한다.

## 미해결 사항

명시적인 시작 문턱, 실제 C_a의 인증값, X/(log X)^2 항, a가 움직이는 영역은 미해결이다.
외부 신규성 미확인과 증명의 자체 점검을 구별한다.

최종 검사 실제 결과:

~~~text
python tools/check_wiki.py
PASS: 617 local links in 84 Markdown files.
Templates and code skipped; headings and external URLs not checked.
git diff --check
[공백 오류 없음. 기존 수정 파일의 LF/CRLF 안내만 출력됨.]
JSON parsing
PASS: research JSON files parsed
~~~
