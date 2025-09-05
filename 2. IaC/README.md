# Quokka-core Mindset - Infrastructure as Code

AWS 서버리스 아키텍처를 위한 Terraform 인프라 코드입니다.

## 아키텍처 개요

```
Frontend: CloudFront → S3(* 정적 웹사이트)
Backend: API Gateway → Lambda → Bedrock → S3(* 파일 저장)
```

## 현재 구성 (Foundation + Storage + Compute Layer)

### 리소스
- **S3 버킷 (Frontend)**: 정적 웹사이트 호스팅용
- **S3 버킷 (Backend)**: Bedrock 생성 파일 저장용
- **CloudFront**: CDN 배포, HTTPS 리다이렉트, 캐싱 설정
- **Lambda 함수**: API 처리 (Python 3.11, 1GB 메모리, 60초 타임아웃)
- **API Gateway**: REST API (3개 엔드포인트, CORS 설정)
- **IAM 역할**: Lambda 실행 역할 (Bedrock, S3 접근 권한 포함)

### 파일 구조
```
├── main.tf                 # 메인 리소스 정의
├── variables.tf           # 변수 정의
├── outputs.tf            # 출력값 정의
├── terraform.tfvars.example # 변수 설정 예시
├── .gitignore
└── README.md
```

## 사용 방법

### 1. 초기 설정
```bash
# 변수 파일 생성
cp terraform.tfvars.example terraform.tfvars

# 필요시 terraform.tfvars 파일 수정
# aws_region, phase, prefix 설정
```

### 2. Terraform 초기화 및 배포
```bash
# Terraform 초기화
terraform init

# 코드 포맷팅 및 검증 (권장)
terraform fmt && terraform validate

# 실행 계획 확인 + 시뮬레이션 tfplan 파일 생성
terraform plan -out=tfplan

# 배포 실행
# 직전에 생성한 tfplan 파일을 사용해 적용
terraform apply tfplan
```

### 3. 리소스 확인
```bash
# 현재 상태 파일(terraform.tfstate)에 기록된 리소스 목록
terraform state list

# 출력값 확인
terraform output
```

### 4. API 테스트
```bash
# API Gateway URL 확인
terraform output api_gateway_url

# 엔드포인트 테스트 (curl)
curl -X POST $(terraform output -raw api_gateway_url)/generate/text \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello World"}'

# 브라우저 개발자 도구에서 테스트
# F12 → Console에서 실행:
# fetch('API_URL/generate/text', {
#   method: 'POST',
#   headers: { 'Content-Type': 'application/json' },
#   body: JSON.stringify({ prompt: 'Hello World' })
# }).then(r => r.json()).then(console.log)
```

### 5. 리소스 삭제
```bash
# S3 버킷 비우기 (필요시)
aws s3 rm s3://<bucket_name> --recursive

# 모든 리소스 삭제
terraform destroy

# 안전한 방법 (계획 확인 후)
terraform plan -destroy -out=destroy.tfplan
terraform apply destroy.tfplan
```
### 권장 삭제 방법
- **개발 환경**: `terraform destroy`
- **프로덕션**: `terraform plan -destroy` → 검토 → `terraform apply` (안전)

## 백엔드 개발자를 위한 정보

### Lambda 환경 변수
- `S3_BUCKET_NAME`: 백엔드 파일 저장용 S3 버킷
- `ENVIRONMENT`: 현재 환경 (dev/staging/prod)
- `BEDROCK_TEXT_MODEL_ID`: amazon.titan-text-premier-v1:0
- `BEDROCK_IMAGE_MODEL_ID`: amazon.titan-image-generator-v1

### 코드 배포 방법
```bash
# AWS CLI로 Lambda 코드 업데이트
aws lambda update-function-code \
  --function-name $(terraform output -raw lambda_function_name) \
  --zip-file fileb://deployment.zip
```

## API 엔드포인트

| 엔드포인트 | 메서드 | 용도 | Bedrock 모델 |
|------------|--------|------|-------------|
| `/generate/text` | POST | 텍스트 생성 | amazon.titan-text-premier-v1:0 |
| `/generate/image` | POST | 이미지 생성 | amazon.titan-image-generator-v1 |
| `/generate/voice` | POST | 음성 생성 | 미정 |

## 다음 단계 (예정)

1. **AI Layer**: Bedrock 모델 연동 및 실제 코드 구현
2. **Security Layer**: WAF, 추가 보안 정책
3. **Monitoring Layer**: CloudWatch, 로깅 설정

## 주의사항

- `terraform.tfvars` 파일은 민감한 정보를 포함할 수 있으므로 Git에 커밋하지 마세요
- AWS 자격 증명이 올바르게 설정되어 있는지 확인하세요
- 리소스 삭제 시 `terraform destroy` 명령어를 사용하세요
- **API 테스트**: 브라우저 주소창에서 GET 요청 시 "Missing Authentication Token" 메시지는 정상입니다 (POST 요청만 허용)

## 변수 설명

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `aws_region` | AWS 리전 | `us-east-1` |
| `phase` | 개발 단계 (dev/staging/prod) | `dev` |
| `prefix` | 리소스 이름 접두사 | `qqq` |
| `lambda_memory_size` | Lambda 메모리 크기 (MB) | `1024` |
| `lambda_timeout` | Lambda 타임아웃 (초) | `60` |

## 리소스 명명 규칙

모든 AWS 리소스는 `${phase}-${prefix}-{resource-type}` 형식으로 명명됩니다.
- 예시: `dev-qqq-frontend`, `prod-qqq-lambda-role`

## 출력값

| 출력명 | 설명 |
|--------|------|
| `frontend_bucket_name` | 프론트엔드 S3 버킷명 |
| `frontend_bucket_website_endpoint` | 프론트엔드 웹사이트 엔드포인트 |
| `backend_bucket_name` | 백엔드 S3 버킷명 |
| `cloudfront_distribution_id` | CloudFront 배포 ID |
| `cloudfront_domain_name` | CloudFront 도메인명 (CDN URL) |
| `api_gateway_url` | API Gateway 호출 URL |
| `lambda_function_name` | Lambda 함수명 |
| `lambda_role_arn` | Lambda 실행 역할 ARN |
| `lambda_role_name` | Lambda 실행 역할명 |