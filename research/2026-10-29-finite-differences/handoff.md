# 작업 인계

- 작업 ID: 2026-10-29-finite-differences
- 연구 노트: [유한 차분으로 보는 교대 이항합](note.md)
- 완료한 내용: 차분의 이항합 표현, 다항식 소거, 전사 함수와 집합 분할의 관계를 자체 증명했다.
- 주장 상태: 핵심 주장 3개 증명됨. 신규성 주장 없음.
- 독립 검토 상태: 대기. 별도 에이전트를 실행하지 않았다.
- 한계: 문헌 대조 및 독립 검토 미수행. 유한 검산은 증명을 대체하지 않는다.
- 공용 위키 반영: 홈, 분야별 목록, 연구 기록에 연결했고 후속 질문 2개를 열린 질문에 등록했다.
- 다음 담당자: 부호와 $n=0,m=0$ 경계, 포함배제의 적용을 검토하고 간격 $h$의 차분 확장을 탐구할 수 있다.

## 실제 실행한 검증

2026-10-29, Python 3.10.11, 저장소 루트에서 실행:

```powershell
python research/2026-10-29-finite-differences/verify.py
```

출력:

```text
PASS: 169 alternating-sum / partition-count pairs (0 <= n,m <= 12).
PASS: 44 polynomial finite-difference cases.
Finite checks support the examples; see note.md for proofs.
```
