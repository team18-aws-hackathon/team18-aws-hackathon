## Introduction

> This is front-end sources of quokka-core mindset project.
> React + Vite + TypeScript based SPA -> Deployed on AWS S3 + CloudFront  
> For detailed operations and guidelines, please refer to the GitHub Wiki
> [![Docs: Wiki](https://img.shields.io/badge/docs-Wiki-0366d6)](https://github.com/QQQ-Q-Developer-Hackathon/front/wiki)

## TL;DR

```bash
# requirements: Node.js 22+, npm
cp .env.example .env                 # 환경 변수 채우기
npm ci                               # 의존성 설치
npm run dev                          # http://localhost:5173

# 프로덕션 빌드
npm run build                        # dist/ 산출물 생성
npm run preview                      # 로컬 미리보기(배포 에뮬)
```

## 1) Overview

- **Goal**: 사용자가 일기를 작성하면 일기 내용을 AI를 통해 분석하여 마치 쿼카가 답변해주는 듯한 인터페이스 제공

## 2) Tech Stack

- **Language**: TypeScript
- **Framework**: React, Vite
- **Status Management**: Zustand
- **UI**: MUI
- **Code Quality Checks**: ESLint, Prettier, Husky, lint-staged

## 3) Environment Variables

Vite는 **`VITE_` 접두사**가 붙은 변수만 클라이언트에 노출됩니다.

`.env.example`

```env
# API endpoint
VITE_API_BASE_URL=http://localhost:8080/api/

# App
VITE_APP_NAME=quokka-core-mindset
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_USE_MOCK_DATA=false
VITE_DEBUG_MODE=true
```

**Caution**

> Separate values by deployment environment, such as in `.env.production` and `.env.development` files.  
> Do not commit sensitive information to the repository. (Use GitHub Actions secrets instead)

---

## 4) Commands

```bash
npm ci                # 의존성 설치
npm run dev           # 개발 서버(Hot Reload)
npm run build         # 프로덕션 빌드(dist/)
npm run preview       # 빌드 결과 미리보기
npm run lint          # ESLint 검사
npm run lint:fix      # ESLint 자동 고침
npm run format        # Prettier 포맷
npm run format:check  # 포맷 체크
```

## 5) API integration

- base URL: `VITE_API_BASE_URL`
- refer to backend api spec.

## 6) Deployment

- **target**: S3 static hosting + CloudFront CDN deployment
- **cache/invalidation**: Static assets are cached and then CloudFront invalidation is performed after deployment.

## 7) Code Quality Checks

- **Husky** pre-commit 훅에서 `pre-commit`로 변경 파일만 ESLint/Prettier 실행, import 순서/unused 검사
- PR 시 GitHub Actions에서 **포맷/린트/타입 체크** 실패 시 머지 불가

`.husky/pre-commit` 예시

```sh
#!/usr/bin/env sh
npm run pre-commit
```

## 8) Co-Working

- **브랜치 전략**: `main`, `develop`, `feature/*`, (main은 보호 브랜치, PR 필수)
- **Commit Convention**: Conventional Commits
