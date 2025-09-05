import json
import boto3
import uuid
import os
import re
import html
from datetime import datetime
from botocore.exceptions import ClientError

bedrock_client = boto3.client('bedrock-runtime')
s3_client = boto3.client('s3')

# 최적화된 패턴들
PHONE_PATTERN = re.compile(r'01[0-9][-\s]?\d{3,4}[-\s]?\d{4}')
EMAIL_PATTERN = re.compile(r'\S+@\S+\.\S+')
HTML_TAG_PATTERN = re.compile(r'<[^>]*?>')
WHITESPACE_PATTERN = re.compile(r'\s+')

def validate_input(user_type, content):
    """입력 검증 함수"""
    if not isinstance(user_type, str) or not isinstance(content, str):
        return "입력값은 문자열이어야 합니다", None

    if not user_type or user_type.lower() not in ['t', 'f']:
        return "사용자 타입은 't' 또는 'f'여야 합니다", None

    # 안전한 HTML 처리
    try:
        content_clean = html.unescape(content)
    except Exception:
        content_clean = content

    content_clean = WHITESPACE_PATTERN.sub(' ', HTML_TAG_PATTERN.sub('', content_clean)).strip()

    # 길이 검증
    if len(content_clean.replace(' ', '')) < 10:
        return "일기 내용은 공백을 제외하고 최소 10자 이상이어야 합니다", None

    if len(content_clean) > 1000:
        return "일기 내용은 최대 1000자까지 입력 가능합니다", None

    # 의미있는 내용 검증
    if not re.search(r'[가-힣a-zA-Z]', content_clean):
        return "의미있는 내용을 입력해주세요 (한글 또는 영문 포함)", None

    # 개인정보 체크
    if PHONE_PATTERN.search(content_clean) or EMAIL_PATTERN.search(content_clean):
        return "개인정보는 입력하지 말아주세요", None

    return None, content_clean

def handle_generate_text(event, headers):
    """
    칭찬 텍스트 생성 API 핸들러
    """
    try:
        # JSON 파싱 예외 처리
        try:
            body = json.loads(event.get('body', '{}'))
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': '잘못된 JSON 형식입니다'})
            }
        
        user_type = body.get('type', '')
        content = body.get('content', '')
        
        # 입력 검증
        error_msg, cleaned_content = validate_input(user_type, content)
        if error_msg:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': error_msg})
            }
        
        # diary_id 생성
        timestamp = datetime.now().strftime('%Y%m%d')
        diary_id = f"diary-{timestamp}-{str(uuid.uuid4())[:3]}"
        
        # Bedrock으로 칭찬 메시지 생성
        compliment = generate_compliment(cleaned_content, user_type.lower())
        
        # S3에 일기 데이터 저장 (로컬 환경에서는 스킵)
        if os.environ.get('AWS_SAM_LOCAL') == 'true':
            print(f"로컬 환경 - S3 저장 스킵: {diary_id}")
        else:
            bucket_name = os.environ.get('S3_BUCKET')
            if bucket_name and bucket_name != 'ContentBucket':
                save_diary_data(bucket_name, diary_id, cleaned_content, user_type.lower(), compliment)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'diary_id': diary_id,
                'compliment': compliment
            })
        }
        
    except Exception as e:
        print(f"Text generation error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error'})
        }

def generate_compliment(content, user_type):
    """
    Bedrock을 사용하여 칭찬 메시지 생성
    """
    try:
        # 성격 유형별 프롬프트 설정
        personality_prompt = {
            't': "논리적이고 분석적인 성향을 가진 사용자에게 적합한",
            'f': "감정적이고 공감적인 성향을 가진 사용자에게 적합한"
        }
        
        prompt = f"""
다음은 {personality_prompt[user_type]} 사용자가 작성한 일기입니다:

"{content}"

이 일기를 읽고 쿼카(quokka)의 따뜻하고 긍정적인 목소리로 칭찬 메시지를 작성해주세요.
- 50자 이내로 작성
- 이모지 1-2개 포함
- 따뜻하고 격려하는 톤
- 사용자의 감정과 노력을 인정하는 내용

칭찬 메시지:
"""
        
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        response = bedrock_client.invoke_model(
            modelId='amazon.nova-pro-v1:0',
            body=json.dumps(request_body),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['output']['message']['content'][0]['text'].strip()
        
    except ClientError as e:
        raise Exception(f"Bedrock API error: {e}")

def save_diary_data(bucket_name, diary_id, content, user_type, compliment):
    """
    일기 데이터를 S3에 저장
    """
    try:
        data = {
            'diary_id': diary_id,
            'timestamp': datetime.now().isoformat(),
            'content': content,
            'type': user_type,
            'compliment': compliment
        }
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"diaries/{diary_id}.json",
            Body=json.dumps(data, ensure_ascii=False, indent=2),
            ContentType='application/json'
        )
        
    except ClientError as e:
        raise Exception(f"S3 save error: {e}")
