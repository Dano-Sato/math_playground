# 집중 신규성 조사 인계

- 작업 ID: 2026-10-29-divisor-novelty-audit
- 담당 범위: 이 폴더의 조사 산출물. 조율자로서 원 연구 meta.json과 공용 위키에 결과 링크 반영.
- 작성 세션 자체 점검. 독립 검토 미실시. 추가 에이전트 실행 없음.

## 결과

- [고정 명제](claim.md): 모든 c의 승패 유한 닫힘, 지수 방향 주기, 로그 개수 정리를 한 대상에 고정.
- [집중 비교](note.md): 여섯 원문의 관련 부분을 실제 읽고 규칙·적용 범위·주기 변수를 대조.
- [출처별 읽은 범위](sources.json), [검색 경로](search-log.md)를 남겼다.
- 2017년 후속 원문은 확보하지 못했다. 공식 서지나 2018년 검색 추출문을 본문 확인으로 쓰지 않았다.
- 기존 정리에서 가법 비주기성이 나옴을 짧게 증명해 유한 뺄셈집합과의 비교를 명확히 했다.
- [원문 대조 체크리스트와 미발송 문의 초안](next-step.md)을 준비했다.
- 원 연구 자체 평가를 유지하고 근거·이력을 보강한다. 이 조사 자체에는 기존 성과 점수를 중복 부여하지 않는다.

## 자체 점검

- $p_c$의 1은 패배, 직접 DP의 1은 승리이므로 부호를 반대로 비교했다.
- c=2,3에서 n=4가 다른 것을 규칙만으로도 확인했다.
- i-MARK 비교는 항등 좌표 아래 이동 그래프에 한정했다. 임의의 부호화 환원의 불가능성을 주장하지 않는다.
- 가법 비주기성의 논증은 $\alpha_c>0$와 로그 개수 정리에 의존한다. 제한 계산이 그 증명은 아니다.
- 원문을 읽은 여섯 자료도 읽은 절·정리만 적었다. 자료 전체의 모든 증명을 검토했다고 하지 않는다.
- 가장 가까운 후속 논문이 미독이라는 공백 때문에 최종 신규성 판단은 보류했다.

## 검증 명령과 실제 결과

~~~text
python research/2026-10-29-divisor-novelty-audit/verify.py

c=2: period=2, alpha=1/2, p(1)=1, p(4)=0 PASS
c=3: period=2, alpha=1/2, p(1)=1, p(4)=1 PASS
c=4: period=3, alpha=2/3, p(1)=1, p(4)=1 PASS
c=5: period=3, alpha=2/3, p(1)=1, p(4)=1 PASS
c=64: period=8, alpha=19/2, p(1)=1, p(4)=1 PASS
PASS: 20480 exact outcome comparisons and rule witnesses
~~~

Python 표준 라이브러리, 정확한 정수·유리수, 난수 없음.
n<=4096, c=2,3,4,5,64. 기존 유한 모델 코드는 수정하지 않았다.
데이터: [witnesses.json](witnesses.json).

위키 및 파일 검사 실제 결과:

~~~text
python tools/check_wiki.py
PASS: 535 local links in 75 Markdown files.
Templates and code skipped; headings and external URLs not checked.

git diff --check
exit 0, whitespace errors 없음

JSON parse check
PASS: 4 JSON files parsed
~~~

Git의 LF→CRLF 안내 한 건은 있었다. 내용 오류나 검사 실패는 아니다.
위키 검사기는 외부 URL의 현재 접속 여부나 수학적 정확성을 판정하지 않는다.

## 미해결과 다음 작업

2017년 「約数ニムのグランディ数(2)」35(1), pp.49–60 본문 확보가 핵심이다.
본문이 일반 c의 닫힘을 포함하는지 원문 쪽수와 정리 번호로 판정한다.
그 결과로 원 연구의 점수를 재평가할 수 있다.
외부 연락이나 유료 복사 신청을 실행한 것은 아니다.

## 공용 위키 반영 링크

- [Home](../../wiki/Home.md): 기존 승패 정리의 신규성 대조 링크.
- [ResearchNotes](../../wiki/ResearchNotes.md): 조사 자료와 메타데이터 링크.
- [ResearchLog](../../wiki/ResearchLog.md): 자체 조사·평가 유지와 미독 공백 기록.
- [Questions](../../wiki/Questions.md): Q-022의 수학적 해결 상태를 유지하고 신규성 대조 링크 추가.
- [Topics](../../wiki/Topics.md): 조합 게임 이론·문헌 대조 항목.
