# 저장과 공개 방법

## 현재 로컬 위치

프로젝트는 현재 Codex 작업공간 안에 있습니다.

```text
C:\Users\gks12\Documents\Codex\2026-06-07\cli-it-bi-tool-ops-kbo\kbo-player-lab
```

브라우저에서 `kbo-player-lab/index.html`을 열면 실제 페이지인 `web/index.html`로 이동합니다.

## 돈이 추가로 들지 않는 추천 방법

GitHub public repository + GitHub Pages를 추천합니다.

GitHub 공식 문서 기준으로 GitHub Pages는 public repository에서 GitHub Free 플랜으로 사용할 수 있습니다. private repository에서 Pages를 쓰려면 Pro, Team, Enterprise 계정이 필요할 수 있습니다.

## GitHub Pages로 올릴 때

1. GitHub에서 public repository를 만듭니다.
2. 이 `kbo-player-lab` 폴더 내용을 repository에 올립니다.
3. Repository Settings > Pages에서 source를 `Deploy from a branch`로 설정합니다.
4. branch는 `main`, folder는 `/root`를 선택합니다.
5. 배포 후 아래 형식의 주소가 생깁니다.

```text
https://사용자명.github.io/저장소명/
```

이 프로젝트는 루트 `index.html`이 `web/index.html`로 이동하도록 만들어져 있어, GitHub Pages 주소만 저장하면 됩니다.

## 현재 GitHub 커넥터 상태

현재 Codex GitHub 커넥터에서 접근 가능한 저장소 목록이 비어 있습니다.

내일 이어서 하려면 다음 중 하나가 필요합니다.

- GitHub에서 `kbo-player-lab` public repository를 직접 만든 뒤 Codex GitHub 앱 권한을 부여
- 이미 만든 repository가 있다면 Codex GitHub 앱이 그 repository에 접근할 수 있도록 권한 추가

권한이 연결되면 Codex가 파일 업로드, 브랜치 생성, PR 생성까지 이어갈 수 있습니다.

