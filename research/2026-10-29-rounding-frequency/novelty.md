# 신규성 조사와 범위

[연구 노트](note.md)

- 날짜: 2026-10-29
- 작성 세션의 문헌 비교. 독립 검토 아님.
- 후보: 정확한 실수 최대점의 반올림 실패 집합에서 X/log X 계수의 진동,
  두 보편 극한 상수, 역수 합에서 log log X를 뺀 상수항의 존재.

## 실제 검색어

- `fractional parts log n distribution no asymptotic distribution exponential intervals Benford`
- `shrinking intervals log n counting asymptotic n log n rounding mode Edgeworth`

검색은 일반적인 로그 소수 부분·반올림 예외 문헌을 찾기 위한 것이다.
검색 결과의 다른 논문이나 서적을 읽은 것처럼 인용하지 않았다.

## 가장 가까운 원문

1. [Kabluchko–Marynych–Sulzbach, Mode and Edgeworth expansion for the Ewens distribution and the Stirling numbers](https://cs.uwaterloo.ca/journals/JIS/VOL19/Kabluchko/kabl2.pdf).
   Theorem 7(iii)–(iv)와 (iii)의 증명, 특히 식 (15)와 이어지는 지수 구간 합을 읽었다.
   고정 폭의 로그 격자 근방을 직접 세며, log n의 소수 부분을 균등분포로 놓을 수 없다고 명시한다.
   따라서 지수 구간으로 옮기는 방법과 성공 밀도 1이라는 현상을 새 방법으로 주장하지 않는다.
2. [같은 저자들, General Edgeworth expansions, v3 §3.6](https://arxiv.org/html/1606.03920v3#S3.SS6).
   Proposition 3.19의 진술과 주변 설명을 읽었다. 정수 최빈값과 점근 중심의 반올림을 비교한다.
   이 정리의 전체 가정 검증이나 전체 증명 검토를 수행하지 않았다.

두 원문의 확인일은 2026-10-29이다.

## 일치와 차이

- 일치: 로그 격자 근방을 지수 구간의 길이 합으로 세는 기본 기법, 희소한 무한 반올림 예외라는 맥락.
- 대상 차이: 이 연구의 반올림 기준은 주어진 양수 적분 보간의 **정확한 실수 최대점**이다.
  선행 진술의 점근 중심과 정의가 같다거나 그 선행 결과를 개선한다고 단정하지 않는다.
- 이번 위키의 추가 내용: 이미 얻은 두 역로그 보정항의 차이 h=1/24를 사용하여,
  폭이 1/T_j로 줄어드는 비대칭 구간의 정확한 점근 계수를 계산했다.
  현재 구간을 자르는 항을 포함해 전 위상에서 균일한 공식을 주고,
  보편 극한점 구간과 역수 합의 상수항 수렴을 증명했다.
- 읽은 부분에서는 이번 대상과 두 상수 1/[24(e−1)], e/[24(e−1)] 및 역수 합 상수항을
  같은 진술로 확인하지 못했다. 그러나 방법이 매우 가깝고 계산이 초등적이므로,
  그 사실만으로 독창적 새 정리라고 판정할 수 없다.

## 평가 결론

외부 신규성은 미확인이다. 위키의 기존 무한 반례 결과를 정량화한 작은 후속 연구로 평가한다.
일반적 방법과 밀도 1 결론은 알려진 부분으로 분리한다. 외부 최초성 또는 전문 분야의 중요도를
확보했다고 주장하지 않으며, 10점 이상으로 포장하지 않는다.
평가 원본은 [meta.json](meta.json)이다.
