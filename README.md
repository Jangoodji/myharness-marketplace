# myharness-marketplace

practice-m3 하네스(agents · hooks · skills)를 다른 프로젝트에서 쓰기 위한 로컬 플러그인 마켓플레이스.

## 들어 있는 것 · `plugins/myharness`

| 종류 | 이름 | 하는 일 |
|---|---|---|
| agent | verifier | spec 기준으로 검증하고 문제만 보고한다 |
| agent | cleaner | 죽은 코드 · 어긋난 문서를 정리한다 |
| skill | round | 라운드 진행 순서와 종료 조건 (spec → plan → review) |
| hook | PreToolUse · guard.py | rm -rf, 재귀 강제 삭제, git push --force, `.env` 읽기를 막는다 |
| hook | PostToolUse · project_lint.py | 프로젝트에 `scripts/arch_lint.py` 가 있으면 Edit · Write 뒤에 실행한다 |

## 설치

Claude Code 에서:

```
/plugin marketplace add Jangoodji/myharness-marketplace
/plugin install myharness@myharness-marketplace
```

로컬에 받은 폴더로 설치하려면 `Jangoodji/myharness-marketplace` 대신 이 폴더 경로를 넣는다.

## 쓰는 프로젝트가 준비할 것
- `CLAUDE.md` 에 그 프로젝트의 코드 규칙, 테스트 · 린트 명령을 적는다. (verifier · cleaner 가 여기서 읽는다)
- 아키텍처 린트를 원하면 `scripts/arch_lint.py` 를 둔다. 위반 시 exit 2 와 함께 stderr 에 수정 지침을 남기면 된다.
- Hook 실행에 `uv` 가 필요하다. (스크립트는 표준 라이브러리만 쓴다)
