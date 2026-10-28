# 웹뷰어 외부 라이브러리

이 뷰어는 아래 라이브러리를 프로젝트 내부에 포함한다. 페이지를 열 때 CDN이나 외부 폰트 서버에 접속하지 않으므로, 최초 설치된 파일만으로 Markdown과 수식을 오프라인 렌더링할 수 있다.

버전 확인일: 2026-10-29. 공식 npm registry의 당시 `latest` 안정 배포를 확인하고 버전 및 배포 압축파일 SHA-512를 고정했다. 향후 실행 시 임의로 최신판으로 바꾸지 않는다.

| 라이브러리 | 고정 버전 | 용도 | 원문·배포 출처 | 포함한 라이선스 |
| --- | --- | --- | --- | --- |
| Marked | 18.1.2 | Markdown·표·목록 렌더링 | [원문](https://github.com/markedjs/marked/tree/v18.1.2), [공식 npm 메타데이터](https://registry.npmjs.org/marked/18.1.2) | [MIT 및 원문 고지](vendor/marked/LICENSE) |
| DOMPurify | 3.4.17 | 렌더링한 HTML의 위험한 요소 제거 | [원문](https://github.com/cure53/DOMPurify/tree/3.4.17), [공식 npm 메타데이터](https://registry.npmjs.org/dompurify/3.4.17) | [Apache-2.0](vendor/dompurify/LICENSE), [MPL-2.0](vendor/dompurify/LICENSE-MPL) 대안 라이선스 고지 보존 |
| KaTeX | 0.19.1 | 인라인·블록 수식 렌더링 및 수식 폰트 | [원문](https://github.com/KaTeX/KaTeX/tree/v0.19.1), [공식 npm 메타데이터](https://registry.npmjs.org/katex/0.19.1) | [MIT](vendor/katex/LICENSE) |

## 포함 파일

- `vendor/marked/marked.umd.js`: 원문 배포의 `lib/marked.umd.js`.
- `vendor/dompurify/purify.min.js`: 원문 배포의 `dist/purify.min.js`.
- `vendor/katex/katex.min.js`, `katex.min.css`: 원문 배포의 `dist/` 브라우저 배포.
- `vendor/katex/auto-render.min.js`: 원문 배포의 `dist/contrib/auto-render.min.js`.
- `vendor/katex/fonts/`: 해당 CSS가 참조하는 원문 배포의 `dist/fonts/` 폰트 60개. 상대 경로를 유지한다.
- 각 라이브러리의 원문 라이선스 파일을 수정 없이 보존한다.

## 다시 받기

저장소 루트에서 Python 3 표준 라이브러리만 사용한다. 이 명령의 다운로드 단계에는 인터넷이 필요하다. 이미 포함된 뷰어를 사용하는 데는 필요하지 않다.

```powershell
python tools/vendor_viewer_assets.py
```

스크립트는 공식 npm registry의 고정 버전 압축파일을 받는다. `tools/vendor_viewer_assets.py`에 기록한 SHA-512와 일치하는지 먼저 검증하며, 모든 배포 파일의 검증과 파일 선택이 끝난 뒤 `viewer/vendor/`에 저장한다. 패키지 설치 스크립트나 임의 코드를 실행하지 않고, 압축파일의 명시된 일반 파일만 읽어 복사한다. 전역 Python·Node 패키지를 설치하지 않는다.

버전을 변경할 때는 공식 버전별 메타데이터의 `dist.integrity`와 배포 구성을 확인하고 스크립트 및 이 문서를 함께 갱신한다. 변경 후 실제 Markdown·HTML 정제·수식 렌더링을 다시 확인한다.
