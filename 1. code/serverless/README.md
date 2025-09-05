# Bedrock Serverless Backend

AWS SAM을 사용한 서버리스 백엔드 애플리케이션입니다.

## 아키텍처

- **API Gateway**: REST API 엔드포인트 제공
- **Lambda**: Bedrock 모델 호출 및 비즈니스 로직 처리
- **Bedrock**: AI 모델 서비스
- **S3**: Bedrock 결과물 저장
- **CloudFront**: S3 콘텐츠 배포

## 사전 요구사항

1. AWS CLI 설치 및 구성
2. AWS SAM CLI 설치
3. Python 3.11
4. Docker (로컬 테스트용)

## 로컬 개발 환경 설정

### 1. 사전 요구사항 확인
```bash
# Python 3.11 버전 확인
python --version

# AWS CLI 설치 및 구성 확인
aws --version
aws configure list

# Docker 실행 확인 (로컬 테스트용)
docker --version
```

### 2. SAM CLI 설치
```bash
# pip를 통한 설치
pip install aws-sam-cli

# 설치 확인
sam --version
```

### 3. 프로젝트 빌드
```bash
# 의존성 설치 및 빌드
sam build

# 빌드 결과 확인
ls .aws-sam/build/
```

### 4. 로컬 테스트

#### API Gateway 로컬 실행
```bash
# 로컬 API 서버 시작 (기본 포트: 3000)
sam local start-api

# 커스텀 포트로 실행
sam local start-api --port 8080

# 환경 변수 파일과 함께 실행
sam local start-api --env-vars env.json
```

#### Lambda 함수 직접 테스트
```bash
# 테스트 이벤트로 함수 실행
sam local invoke QuokkaFunction --event events/test-text.json

# 환경 변수와 함께 실행
sam local invoke QuokkaFunction --event events/test-text.json --env-vars env.json

# 디버그 모드로 실행
sam local invoke QuokkaFunction --event events/test-text.json --debug
```

#### 로컬 API 테스트
```bash
# curl을 사용한 API 테스트
# 텍스트 생성 API
curl -X POST http://localhost:3000/generate/text \
  -H "Content-Type: application/json" \
  -d '{"type": "f", "content": "오늘은 조금 힘들었어..."}

# 이미지 생성 API
curl -X POST http://localhost:3000/generate/image \
  -H "Content-Type: application/json" \
  -d '{"diary_id": "diary-20240901-001", "compliment": "감정을 이해하는 당신은 정말 멋져요"}

# 음성 생성 API
curl -X POST http://localhost:3000/generate/voice \
  -H "Content-Type: application/json" \
  -d '{"diary_id": "diary-20240901-001", "compliment": "감정을 이해하는 당신은 정말 멋져요"}'
```

### 5. 환경 변수 설정 (선택사항)

로컬 테스트 시 환경 변수가 필요한 경우 `env.json` 파일 생성:
```json
{
  "BedrockProcessorFunction": {
    "S3_BUCKET": "test-bucket",
    "CLOUDFRONT_DOMAIN": "test-domain.cloudfront.net"
  }
}
```

### 6. 로그 확인
```bash
# 실시간 로그 확인
sam logs -n QuokkaFunction --stack-name bedrock-serverless-backend --tail
```



## API 사용법

### 1. POST /generate/text - 칭찬 텍스트 생성

**요청:**
```json
{
  "type": "f",
  "content": "오늘은 조금 힘들었어..."
}
```

**응답:**
```json
{
  "diary_id": "diary-20240901-001",
  "compliment": "스스로를 다독일 줄 아는 당신, 참 따뜻해요 🌷"
}
```

### 2. POST /generate/image - 칭찬 이미지 생성

**요청:**
```json
{
  "diary_id": "diary-20240901-001",
  "compliment": "감정을 이해하는 당신은 정말 멋져요 💚"
}
```

**응답:**
```json
{
  "image_url": "https://s3.amazonaws.com/quokka/images/diary-20240901-001.png"
}
```

### 3. POST /generate/voice - 칭찬 음성 생성

**요청:**
```json
{
  "diary_id": "diary-20240901-001",
  "compliment": "감정을 이해하는 당신은 정말 멋져요"
}
```

**응답:**
```json
{
  "voice_url": "https://s3.amazonaws.com/quokka/voices/diary-20240901-001.mp3"
}
```

## 환경 변수

- `S3_BUCKET`: S3 버킷 이름 (자동 설정)
- `CLOUDFRONT_DOMAIN`: CloudFront 도메인 (자동 설정)

## 주의사항

### 로컬 개발 시
1. Docker가 실행 중이어야 합니다
2. 로컬 테스트 시 실제 AWS 리소스(Bedrock, S3)에 접근하므로 AWS 자격 증명이 필요합니다
3. `sam local invoke` 명령은 실제 AWS 서비스를 호출하므로 비용이 발생할 수 있습니다

### 일반 주의사항
1. Bedrock 모델 사용 권한이 필요합니다
2. 리전별로 사용 가능한 Bedrock 모델이 다를 수 있습니다

## 개발 팁

### 디버깅
```bash
# 상세 로그와 함께 실행
sam local start-api --debug

# Lambda 함수 환경 변수 확인
sam local invoke QuokkaFunction --event events/test-text.json --debug
```