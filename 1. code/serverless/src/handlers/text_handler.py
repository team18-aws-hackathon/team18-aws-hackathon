import json
import boto3
import uuid
import os
from datetime import datetime
from botocore.exceptions import ClientError

bedrock_client = boto3.client('bedrock-runtime')
s3_client = boto3.client('s3')

def handle_generate_text(event, headers):
    """
    칭찬 텍스트 생성 API 핸들러
    """
    try:
        # 요청 본문 파싱
        body = json.loads(event.get('body', '{}'))
        user_type = body.get('type', '').lower()
        content = body.get('content', '')
        
        # 입력 검증
        if not user_type or user_type not in ['t', 'f']:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Invalid type. Must be "t" or "f"'})
            }
        
        if not content:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'content is required'})
            }
        
        # diary_id 생성
        timestamp = datetime.now().strftime('%Y%m%d')
        diary_id = f"diary-{timestamp}-{str(uuid.uuid4())[:3]}"
        
        # Bedrock으로 칭찬 메시지 생성
        compliment = generate_compliment(content, user_type)
        
        # S3에 일기 데이터 저장 (로컬 환경에서는 스킵)
        if os.environ.get('AWS_SAM_LOCAL') == 'true':
            print(f"로컬 환경 - S3 저장 스킵: {diary_id}")
        else:
            bucket_name = os.environ.get('S3_BUCKET')
            if bucket_name and bucket_name != 'ContentBucket':
                save_diary_data(bucket_name, diary_id, content, user_type, compliment)
        
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
