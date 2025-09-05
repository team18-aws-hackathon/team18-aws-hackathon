import json
import boto3
import uuid
import os
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

# AWS 클라이언트 초기화
bedrock_client = boto3.client('bedrock-runtime')
s3_client = boto3.client('s3')

S3_BUCKET = os.environ.get('S3_BUCKET')
CLOUDFRONT_DOMAIN = os.environ.get('CLOUDFRONT_DOMAIN')

def lambda_handler(event, context):
    """
    API Gateway에서 호출되는 메인 핸들러
    """
    try:
        # CORS 헤더
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        }
        
        # OPTIONS 요청 처리 (CORS preflight)
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'OK'})
            }
        
        # 요청 본문 파싱
        body = json.loads(event.get('body', '{}'))
        prompt = body.get('prompt', '')
        model_id = body.get('model_id', 'anthropic.claude-3-sonnet-20240229-v1:0')
        
        if not prompt:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'prompt is required'})
            }
        
        # Bedrock 모델 호출
        bedrock_response = invoke_bedrock_model(prompt, model_id)
        
        # S3에 결과 저장
        file_key = save_to_s3(bedrock_response, prompt)
        
        # Pre-signed URL 생성
        presigned_url = generate_presigned_url(file_key)
        
        # CloudFront URL 생성
        cloudfront_url = f"https://{CLOUDFRONT_DOMAIN}/{file_key}"
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Success',
                'file_key': file_key,
                'presigned_url': presigned_url,
                'cloudfront_url': cloudfront_url,
                'bedrock_response': bedrock_response
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def invoke_bedrock_model(prompt, model_id):
    """
    Bedrock 모델을 호출하여 응답을 받습니다.
    """
    try:
        # Claude 모델용 요청 형식
        if 'claude' in model_id:
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        else:
            # 다른 모델들을 위한 기본 형식
            request_body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 1000,
                    "temperature": 0.7
                }
            }
        
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        
        # Claude 응답 파싱
        if 'claude' in model_id:
            return response_body['content'][0]['text']
        else:
            return response_body.get('results', [{}])[0].get('outputText', '')
            
    except ClientError as e:
        raise Exception(f"Bedrock API error: {e}")

def save_to_s3(content, prompt):
    """
    Bedrock 응답을 S3에 저장합니다.
    """
    try:
        # 파일명 생성 (타임스탬프 + UUID)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_id = str(uuid.uuid4())[:8]
        file_key = f"bedrock-results/{timestamp}_{file_id}.json"
        
        # 저장할 데이터 구성
        data = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'response': content,
            'file_id': file_id
        }
        
        # S3에 업로드
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=file_key,
            Body=json.dumps(data, ensure_ascii=False, indent=2),
            ContentType='application/json'
        )
        
        return file_key
        
    except ClientError as e:
        raise Exception(f"S3 upload error: {e}")

def generate_presigned_url(file_key, expiration=3600):
    """
    S3 객체에 대한 pre-signed URL을 생성합니다.
    """
    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': file_key},
            ExpiresIn=expiration
        )
        return presigned_url
        
    except ClientError as e:
        raise Exception(f"Presigned URL generation error: {e}")