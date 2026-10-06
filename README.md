# 다함재가복지센터 웹사이트

경기도 화성시 다함재가복지센터의 핑크색 브랜드 홈페이지입니다. HTML, CSS, JavaScript만으로 동작합니다.

## 실행

프로젝트 루트에서 `python -m http.server 4173 --directory dist`를 실행한 뒤 http://localhost:4173 에 접속합니다. 별도 설치나 빌드가 필요 없습니다.

## 구성

- `dist/index.html`: 센터 소개, 서비스, 이용 절차, FAQ, 블로그 소식, 상담·위치
- `dist/style.css`: 핑크 브랜드 및 모바일 반응형 스타일
- `dist/script.js`: 모바일 메뉴 동작
- `dist/care.png`: AI로 제작한 설명용 돌봄 이미지. 실제 센터 사진이 아닙니다.
- `docs/PROGRESS.md`: 진행 상황 및 남은 작업
- `docs/BLOG_REVIEW.md`: 블로그 검토 근거와 반영 판단

수정 사항은 의미 있는 단위로 커밋하고 `main`에 올립니다. 개인정보, 인증키, 실제 이용자 건강정보는 저장하지 않습니다.
