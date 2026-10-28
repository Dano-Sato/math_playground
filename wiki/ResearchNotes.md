# 연구 노트 목록

[홈](Home.md) · [웹뷰어 사용법](Viewer.md) · [점수 기준](Scoring.md) · [분야별 목록](Topics.md)

연구 노트의 검색·점수순 정렬은 로컬 웹뷰어의 **연구 노트** 화면에서 한다. 저장소 루트의 `open_wiki.cmd`를 실행하면 열린다. Markdown 목록의 순서는 점수와 관계없으며 수동 정렬하지 않는다.

| 연구 노트 | 평가 원본 | 증명 검토 |
| --- | --- | --- |
| [포아송 동률 경계와 유한 전환점](../research/2026-10-29-critical-mode-boundary/note.md) | [meta.json](../research/2026-10-29-critical-mode-boundary/meta.json) | 미실시(자체 점검·자체 채점) |
| [유한 차분으로 보는 교대 이항합](../research/2026-10-29-finite-differences/note.md) | [meta.json](../research/2026-10-29-finite-differences/meta.json) | 대기 |
| [교대 이항합의 양수 표현과 안정적인 계산](../research/2026-10-29-reciprocal-binomial/note.md) | [meta.json](../research/2026-10-29-reciprocal-binomial/meta.json) | [독립 검토 통과](../research/2026-10-29-reciprocal-review/review.md) |
| [실수 지수와 비균등 차분](../research/2026-10-29-real-power-differences/note.md) | [meta.json](../research/2026-10-29-real-power-differences/meta.json) | [독립 검토 통과](../research/2026-10-29-reciprocal-review/review-real.md) |
| [로그 오목성·날카로운 경계·단봉성](../research/2026-10-29-turan-unimodality/note.md) | [meta.json](../research/2026-10-29-turan-unimodality/meta.json) | [독립 검토 통과](../research/2026-10-29-turan-review/review.md) |
| [약수 뺄셈 게임의 하한 일반화](../research/2026-10-29-divisor-game-lower-bound/note.md) | [meta.json](../research/2026-10-29-divisor-game-lower-bound/meta.json) | 미실시(자체 채점) |
| [자명하지 않은 약수를 빼는 게임의 Grundy 값](../research/2026-10-29-nontrivial-divisor-game/note.md) | [meta.json](../research/2026-10-29-nontrivial-divisor-game/meta.json) | [v1 검토: 수정 필요 → v2 반영](../research/2026-10-29-nontrivial-divisor-game-review/review.md) |
| [고정된 a에서 최대 지수의 점근](../research/2026-10-29-fixed-a-argmax/note.md) | [meta.json](../research/2026-10-29-fixed-a-argmax/meta.json) | 미실시(자체 채점) |
| [비례 영역의 최대 지수와 포아송 모양 극한](../research/2026-10-29-proportional-argmax/note.md) | [meta.json](../research/2026-10-29-proportional-argmax/meta.json) | 미실시(자체 채점) |
| [실수 지수 로그 오목성과 날카로운 곡률 경계](../research/2026-10-29-real-log-concavity/note.md) | [meta.json](../research/2026-10-29-real-log-concavity/meta.json) | [v1 검토: 수정 필요(경미)→v1.1 반영](../research/2026-10-29-real-log-concavity-review/review.md) |

## 평가 정보의 원본

각 노트 폴더의 `meta.json`에 현재 점수, 신규성, 평가 상태, 평가 근거, 재평가 조건과 점수 변경 이력을 보관한다. 기존 평가의 근거와 이력도 해당 파일로 옮겼다. 웹뷰어는 이 파일을 읽어 점수와 평가 근거를 표시한다. 점수가 없으면 미평가로 보이며 0점과 구분한다.

점수는 새로운 수학적 기여에 대한 내부 평가이고, 노트의 완성도나 정확성 검토와는 별개다. 자세한 기준은 [성과 점수 기준](Scoring.md)을 따른다.

## 유지 방법

새 노트는 별도의 중앙 등록 없이 웹뷰어에 자동으로 나타난다. 이 Markdown 목록은 직접 파일을 탐색할 때의 안내용 링크 모음이다. 추가해도 되고 정렬할 필요는 없다. 원문 내용은 `note.md`, 점수·평가 정보는 같은 폴더의 `meta.json`을 수정한다. [새 평가 양식](../templates/meta.json)
