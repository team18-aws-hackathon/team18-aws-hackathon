# 🗂️ Terraform Remote State 설정 가이드

## 📋 설정 순서

### 1. 백엔드 인프라 생성
```bash
# 현재 디렉토리: 2. IaC

# 1. 백엔드용 S3 버킷과 DynamoDB 테이블 생성
terraform apply -target=aws_s3_bucket.terraform_state
terraform apply -target=aws_dynamodb_table.terraform_locks
terraform apply -target=random_id.bucket_suffix
terraform apply -target=aws_s3_bucket_versioning.terraform_state
terraform apply -target=aws_s3_bucket_server_side_encryption_configuration.terraform_state
terraform apply -target=aws_s3_bucket_public_access_block.terraform_state

# 2. 생성된 버킷명과 테이블명 확인
terraform output terraform_state_bucket
terraform output terraform_locks_table
```

### 2. Backend 설정 파일 생성
출력된 버킷명을 사용하여 `backend.tf` 파일을 생성합니다:

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "team18-terraform-state-12345678"  # 실제 출력된 버킷명
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "team18-terraform-locks"
    encrypt        = true
  }
}
```

### 3. 로컬 상태를 Remote로 마이그레이션
```bash
# backend.tf 생성 후 실행
terraform init -migrate-state

# 질문에 "yes" 응답
# Do you want to copy existing state to the new backend? yes
```

### 4. 백엔드 설정 파일 정리
```bash
# 백엔드 설정이 완료되면 setup 파일들 제거
rm backend-setup.tf
rm setup-backend.md
```

## ✅ 설정 완료 확인

### 상태 파일 위치 확인
```bash
# 로컬에 terraform.tfstate 파일이 없어야 함
ls -la terraform.tfstate  # 파일이 없어야 정상

# S3에서 상태 파일 확인
aws s3 ls s3://team18-terraform-state-12345678/dev/
```

### GitHub Actions에서 테스트
```bash
# 워크플로우에서 terraform output 명령어가 정상 작동해야 함
terraform output frontend_bucket_name
```

## 🚨 주의사항

1. **버킷명 기록**: 생성된 S3 버킷명을 안전한 곳에 기록
2. **팀 공유**: 모든 팀원이 같은 backend.tf 설정 사용
3. **권한 확인**: GitHub Actions IAM 역할에 S3/DynamoDB 접근 권한 필요

## 🔄 롤백 방법

Remote State를 로컬로 되돌리려면:
```bash
# backend.tf 파일 삭제 또는 주석 처리
# backend.tf 내용을 주석 처리

# 로컬로 마이그레이션
terraform init -migrate-state
```