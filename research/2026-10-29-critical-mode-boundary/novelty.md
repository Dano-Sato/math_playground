# 선행 결과 대조와 평가 근거

[연구 노트](note.md)

- 조사일: 2026-10-29
- 조사자: 작성 세션. 독립 신규성 조사 아님.
- 점수: 실제 값은 [meta.json](meta.json)에서 관리한다.

## 비교한 기존 자료

1. [위키의 정수 로그 오목성 노트](../2026-10-29-turan-unimodality/note.md): 이웃 지수의 비율이 감소하고, 첫 전환점의 폭 1 구간을 준다. 모든 지수 쌍의 전환점과 상수 보정은 없다.
2. [비례 영역 노트](../2026-10-29-proportional-argmax/note.md): 극한이 포아송 모양임을 주지만 동률 경계는 미해결로 남겼다. 실수 최대점의 보정은 계산 관찰로 표시되어 있다. 이번 결과는 고정된 정수 차수의 유한 다항 전개로 나머지를 제어한다.
3. [고정 a 노트의 신규성 조사](../2026-10-29-fixed-a-argmax/novelty.md): 정수 지수의 최대점이 기하분포 합의 최빈값 문제이며 일반 분포 전개 이론과 연결됨을 확인했다. 이 배경 때문에 단지 점근식을 얻었다고 높은 신규성을 부여하지 않는다.
4. [Sagan 원문](https://users.math.msu.edu/users/bsagan/Papers/Old/lcs-pub.pdf)의 도입부: 로그 오목성과 비율 순서는 기존 이론이다.
5. [NIST DLMF 2.10](https://dlmf.nist.gov/2.10#i): 합의 끝점 보정은 표준 도구다.
6. [Kabluchko–Marynych–Sulzbach 초록](https://arxiv.org/abs/1606.03920): 일반 mod-phi 전개와 mode 응용을 확인했다. 전면 본문 대조를 하지 않아 이번 상수 보정이 그 일반 이론에 포함되는지 단정하지 않는다.

## 검색어와 범위

다음 검색을 실행했다. 검색 결과에 나타난 모든 문서를 읽은 것은 아니다.

- `complete homogeneous symmetric polynomial ratio bound h k h k-1 sum maximum`
- `mode sum independent geometric distributions bound mean logarithmic series complete homogeneous`
- `Log Concave Sequences of Symmetric Functions Sagan pdf`
- `complete homogeneous mode asymptotic`
- `alternating binomial mode powers`
- `binomial sums maximizing exponent`

해당 검색에서 $a_{n,k}=n/(e^k-1)+1/(e^k-1)+3/2-1/k+O(1/n)$을 직접 진술하는 원문은 확인하지 못했다. 그러나 이것은 신규성의 증거가 아니다. 검색의 용어와 범위가 한정적이며, 기하분포 합의 유한 크기 최빈값 연구에서 다른 표기로 이미 다루었을 수 있다.

## 판단

이번 노트는 위키 내부에서는 명확한 후속 결과지만, 외부 문헌과 구별되는 새 수학적 기여가 확립되지는 않았다. 최초 조사에서는 표준 도구의 종합 적용으로 자체 채점했다. 다만 증명이 짧거나 표준 도구를 사용한다는 사실만으로 작은 독창적 결과의 가능성을 배제할 수는 없다.

## 후속 집중 조사: 2026-10-29

사용자가 전달한 제안에 따라 현재 점수는 유지하고 **정리 3의 전환점 공식 하나를 10점 후보**로 분리했다. [별도 조사 문서](transition-novelty-review.md)에 원문·가정·모형 대응·직접 유도를 기록했다. Poisson–Charlier 첫 보정으로 상수항을 재구성했으나 동일 모형의 선행 발표는 미확인이다. 후보 상태와 실제 점수를 구별하며 상향은 보류한다. 작성 세션의 추가 조사로, 별도 세션의 독립 검토는 아니다.
