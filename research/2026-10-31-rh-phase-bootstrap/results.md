# 실행 결과

확인일: 2026-10-31. 정확한 유리수 계산, 난수 없음.

```powershell
python research/2026-10-31-rh-phase-bootstrap/verify.py
```

실제 출력 (종료 코드 0):

```text
PASS: exact phase polynomial identities and bounds at 561 inputs.
At t=pi/4, h=log(4)/4: F(t+ih) = -119/256
W_h(t) = -8925/8192 < 0
Phase derivative = 600/119 > 0
Minimum phase bracket at cosh(4h)=5/4: 35/32
Minimum phase bracket at cosh(4h)=17/8: -595/256
Minimum phase bracket at cosh(4h)=4: 20
PASS: positive small/large shifts and negative intermediate shift.
Actual xi pointwise phase positivity remains unproved.
```

위 검산은 유한 입력에 한정된다. 무한 범위의 주장은 본문에 적은 도함수·인수분해·적분 논증으로 정당화한다.

공용 위키 반영 뒤 `python tools/check_wiki.py` 실행 결과 (종료 코드 0):

```text
PASS: 754 local links in 108 Markdown files.
Templates and code skipped; headings and external URLs not checked.
```

Python json 모듈로 메타데이터를 파싱하여 평가 상태와 최초 평가 이력도 확인했다 (종료 코드 0).
