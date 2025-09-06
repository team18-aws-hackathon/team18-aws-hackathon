# 🚀 GitHub Actions Workflows

Quokka-core Mindset 프로젝트의 CI/CD 파이프라인 가이드입니다.

## 📋 워크플로우 개요

| 워크플로우 | 트리거 | 용도 | 환경 |
|------------|--------|------|------|
| `front-end-ci.yaml` | PR/Push (main, develop) | 프론트엔드 코드 검증 | CI |
| `dev-frontend-cd.yml` | Push (develop) | 프론트엔드 배포 | Development |
| `dev-backend-cd.yml` | Push (develop) | 백엔드 배포 | Development |

## 🏗️ Dev Phase 배포 아키텍처

```
개발자 Push (develop 브랜치)
    ↓
GitHub Actions 자동 트리거
    ↓
┌─────────────────┬─────────────────┐
│  Frontend CD    │   Backend CD    │
│                 │                 │
│ React + Vite    │ Python Lambda   │
│ Build → S3      │ ZIP → Lambda    │
│ CloudFront 무효화 │ 함수 업데이트     │
└─────────────────┴─────────────────┘
    ↓
AWS Dev 환경 (dev-qqq-*) 즉시 반영
```

## 🎯 Dev Phase 배포 특징

### **자동 배포**
- **트리거**: `develop` 브랜치에 push 시 자동 실행
- **경로 기반**: 변경된 디렉토리만 배포 (모노레포 최적화)
- **병렬 처리**: 프론트엔드/백엔드 독립적 배포

### **빠른 피드백**
- **프론트엔드**: 빌드 → S3 업로드 → CloudFront 무효화 (약 2-3분)
- **백엔드**: 패키징 → Lambda 업데이트 (약 1-2분)
- **즉시 테스트**: 배포 완료 후 바로 개발 환경에서 확인 가능

## 🔧 사용 방법

### **프론트엔드 개발자**
```bash
# 1. 프론트엔드 코드 수정
cd "1. code/front"
# 코드 수정...

# 2. develop 브랜치에 push
git add .
git commit -m "feat: update frontend feature"
git push origin develop

# 3. GitHub Actions 자동 실행
# 4. CloudFront URL에서 즉시 확인 가능
```

### **백엔드 개발자**
```bash
# 1. 백엔드 코드 수정
cd "1. code/serverless"
# 코드 수정...

# 2. develop 브랜치에 push
git add .
git commit -m "feat: update lambda handler"
git push origin develop

# 3. GitHub Actions 자동 실행
# 4. API Gateway URL에서 즉시 테스트 가능
```

## ⚙️ 필수 설정

### **GitHub Secrets**
Repository Settings → Secrets and variables → Actions에서 설정:

```
AWS_ACCESS_KEY_ID       # AWS 액세스 키
AWS_SECRET_ACCESS_KEY   # AWS 시크릿 키
AWS_REGION             # us-east-1
```

### **AWS 권한 요구사항**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket",
        "cloudfront:CreateInvalidation",
        "lambda:UpdateFunctionCode",
        "lambda:GetFunction"
      ],
      "Resource": "*"
    }
  ]
}
```

## 📊 워크플로우 상세

### **Frontend CD (`dev-frontend-cd.yml`)**
```yaml
트리거: develop 브랜치 + 1. code/front/** 경로 변경
과정:
  1. 코드 체크아웃
  2. Node.js 22 설정
  3. 의존성 설치 (npm ci)
  4. 코드 품질 검사 (lint, format, type check)
  5. Vite 빌드 (dist/ 생성)
  6. Terraform 출력값 조회 (S3 버킷명, CloudFront ID)
  7. S3 동기화 (--delete 옵션으로 정리)
  8. CloudFront 캐시 무효화
```

### **Backend CD (`dev-backend-cd.yml`)**
```yaml
트리거: develop 브랜치 + 1. code/serverless/** 경로 변경
과정:
  1. 코드 체크아웃
  2. Python 3.11 설정
  3. 의존성 설치 (pip install -t src/)
  4. ZIP 패키징 (src/ 디렉토리)
  5. Terraform 출력값 조회 (Lambda 함수명)
  6. Lambda 함수 코드 업데이트
  7. 업데이트 완료 대기
  8. 배포 검증
```

## 🔍 모니터링 및 디버깅

### **배포 상태 확인**
```bash
# GitHub Actions 탭에서 실시간 로그 확인
# 또는 AWS CLI로 직접 확인

# 프론트엔드 배포 확인
aws s3 ls s3://dev-qqq-frontend/

# 백엔드 배포 확인
aws lambda get-function --function-name dev-qqq-api
```

### **로그 확인**
```bash
# Lambda 로그 실시간 확인
aws logs tail /aws/lambda/dev-qqq-api --follow

# CloudFront 무효화 상태 확인
aws cloudfront list-invalidations --distribution-id <DISTRIBUTION_ID>
```

## 🚨 문제 해결

### **일반적인 문제들**

**1. AWS 권한 오류**
```
Error: AccessDenied
해결: GitHub Secrets의 AWS 자격 증명 확인
```

**2. Terraform 출력값 오류**
```
Error: terraform output failed
해결: 2. IaC 디렉토리에서 terraform apply 완료 여부 확인
```

**3. 빌드 실패**
```
Error: npm run build failed
해결: 로컬에서 빌드 테스트 후 push
```

**4. Lambda 패키징 오류**
```
Error: deployment package too large
해결: 불필요한 파일 제외 (.pyc, __pycache__ 등)
```

### **디버깅 팁**
- **GitHub Actions 로그**: 각 단계별 상세 로그 확인
- **AWS CloudWatch**: Lambda 실행 로그 확인
- **로컬 테스트**: 배포 전 로컬에서 빌드/테스트 완료

## 🔄 향후 확장

### **Production 환경 (예정)**
- `prod-frontend-cd.yml`: main 브랜치 트리거
- `prod-backend-cd.yml`: 수동 승인 후 배포
- 환경별 변수 관리 (dev/prod)