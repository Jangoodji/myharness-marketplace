---
name: round
description: 기능을 라운드 단위(spec → plan → 구현 → 검증 → 정리 → review)로 개발할 때 사용한다. 새 라운드를 시작하거나, 라운드를 끝내기 전에 종료 조건을 점검할 때 쓴다.
---

# 라운드 단위 개발

## 문서
- `docs/ROADMAP.md`: 개발 전에 정한 라운드 계획. 지금 어느 라운드인지는 여기서 확인한다.
- `docs/SSOT.md`: 진실의 원천. 지금 서비스의 API, 데이터 모델, 규칙.
- `docs/roundNN/`: 라운드마다 `spec.md` → `plan.md` → `review.md`.

문서가 없으면 위 구조로 먼저 만들고, 라운드 계획은 사람에게 확인받는다.

## 진행 순서
1. `docs/ROADMAP.md`에서 이번 라운드와 목표를 확인한다.
2. `docs/roundNN/spec.md`를 쓴다. 목표 · 요구사항 · 지난 라운드에서 남은 정리 · 범위 밖.
3. `docs/roundNN/plan.md`에 작업 순서를 번호로 적는다.
4. plan대로 구현하고 테스트를 더한다.
5. verifier 에이전트로 spec 기준 검증을 받고, 나온 문제를 고친다.
6. cleaner 에이전트로 죽은 코드와 어긋난 문서를 정리한다.
7. `docs/roundNN/review.md`에 구현 · 검증 결과 · 정리 결과를 적는다.
8. `docs/SSOT.md`와 `docs/ROADMAP.md`를 고친다.

## Hook에 막혔을 때
- Hook에 막힌 작업은 다른 명령으로 우회하지 말고 멈춰서 사람에게 보고한다.

## 라운드 종료 조건
라운드를 끝내기 전에 아래를 모두 지킨다. 하나라도 안 되면 끝났다고 보고하지 않는다.
1. `docs/roundNN/spec.md` · `plan.md` · `review.md`가 지금 코드와 맞는다.
2. `docs/SSOT.md`를 지금 코드 기준으로 고쳤다. (현재 라운드, API 목록, 데이터 모델)
3. cleaner 에이전트로 죽은 코드를 정리했고, 결과를 `review.md`에 적었다.
4. 프로젝트의 테스트와 린트 명령(`CLAUDE.md`에 적힌 것)이 통과한다.
5. `docs/ROADMAP.md`에서 이번 라운드를 완료로 표시했다.
