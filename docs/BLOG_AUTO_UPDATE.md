# 블로그 자동 갱신

공개 RSS `https://rss.blog.naver.com/gilbert61.xml`을 Python 표준 라이브러리로 읽는다.
GitHub Actions `.github/workflows/update-blog.yml`이 매시간 17분에 확인한다.
컴퓨터나 브라우저가 켜져 있을 필요가 없다. GitHub 실행 대기 및 네이버 RSS 반영에 따라 지연될 수 있다.

## 데이터와 권한

- `scripts/update_blog.py`: 최신 게시글 3개의 제목, 날짜, URL, 대표 이미지만 수집한다.
- `dist/blog/posts.json`과 `latest-게시글번호` 이미지 파일이 데이터 저장소다.
- GitHub Actions의 해당 저장소 전용 `GITHUB_TOKEN`으로 데이터 변경을 main에 커밋한다.
- 별도 개인 토큰이나 비밀값은 필요 없다. 공개 블로그 정보만 저장한다.
- 홈페이지는 공개 raw.githubusercontent.com 경로에서 새 데이터를 읽는다.
- 갱신 실패 시 이전 게시글을 유지하고 GitHub Actions 실행에 오류를 남긴다.
- 새 글 갱신에는 홈페이지 재배포가 필요 없다.

## 읽기와 확인

1. `python scripts/update_blog.py` 실행 또는 GitHub Actions의 `Update latest blog posts`를 실행한다.
2. `dist/blog/posts.json`에 날짜순 최신 3개와 대표 이미지가 있는지 확인한다.
3. GitHub Actions가 성공했는지, 해당 변경 커밋이 main에 저장됐는지 확인한다.
4. 공개 `https://raw.githubusercontent.com/staypleur/-web/main/dist/blog/posts.json`에서 저장 결과를 읽는다.
5. 홈페이지 블로그 카드에 같은 제목과 링크가 표시되는지 확인한다.

웹페이지는 처음 로드할 때 배포 당시의 데이터로 먼저 표시한 뒤 공개 최신 데이터로 바꾼다.
열어 둔 페이지는 15분 간격으로 새 데이터를 확인한다. 공개 파일의 캐시로 추가 지연이 있을 수 있다.
RSS 또는 대표 이미지 다운로드에 실패하면 JSON을 교체하지 않는다.
제목은 HTML이 아닌 텍스트로 렌더링하고, 게시글 URL과 이미지 파일명은 허용된 형식만 사용한다.

GitHub 정책에 따라 공개 저장소에서 60일 동안 저장소 활동이 없으면 예약 실행이 비활성화될 수 있다.
이 경우 Actions에서 워크플로를 다시 활성화하거나 수동 실행한다.
