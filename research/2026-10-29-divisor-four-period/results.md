# 실제 실행 기록

- 실행일: 2026-10-29
- 환경: Windows PowerShell, Python 3.10.11, 표준 라이브러리
- 정수 계산, 난수 없음

## 후보 생성

명령:

~~~powershell
python research/2026-10-29-divisor-four-period/explore.py --write-candidate
~~~

종료 코드 0. 홀수 부분 $1,\ldots,87$, 최상위 지수 $0,\ldots,180$을 탐색했다. 생성기의 경계 가정은 별도 인증 전에는 미증명이다.

출력 중 마지막 두 줄:

~~~text
CacheInfo(hits=40030, misses=8007, maxsize=None, currsize=8007)
Wrote candidate.json; requires independent finite-certificate checks.
~~~

## 최종 인증과 별도 직접 계산

명령:

~~~powershell
python research/2026-10-29-divisor-four-period/verify.py
~~~

종료 코드 0. 실제 출력:

~~~text
[A] finite mex equations: 1760 PASS
[B] symbolic tail classes: 132 PASS (k >= 40)
[C] large-odd boundary: 215 transient, 31 negative-shift, 4 constant cases PASS
[D] direct n-based sieve: 262144 values PASS; max exceptional odd part=87
[E] sharpness witness: g(178176)=g(2^11 * 87)=13 != 11 PASS
[F] losing-position formula: 1364 initial/phase checks PASS
ALL CHECKS PASSED
~~~

실행 시간은 호스트 부하에 따라 달라지므로, 탐색과 인증을 위의 고정된 입력 범위로 제한했다.

## 추가 경계 확인

초기 표에서 $G(27,3)=29$임을 확인했다. 이는 꼬리 식 $27+3=30$과 다르다. 따라서 공통 시작점을 27로 내릴 수 없다.

## 위키 검사

명령:

~~~powershell
python tools/check_wiki.py
git diff --check
~~~

위키 검사 종료 코드 0, 실제 출력:

~~~text
PASS: 347 local links in 52 Markdown files.
Templates and code skipped; headings and external URLs not checked.
~~~

차이 공백 검사도 오류 출력 없이 통과했다. 외부 링크와 수식의 참·거짓은 위키 검사 대상이 아니며, 수학적 인증은 위의 별도 검증기가 담당한다.
