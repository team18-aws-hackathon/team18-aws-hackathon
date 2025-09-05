import json
import boto3
import base64
import os
from botocore.exceptions import ClientError

bedrock_client = boto3.client('bedrock-runtime')
s3_client = boto3.client('s3')

S3_BUCKET = os.environ.get('S3_BUCKET')

def handle_generate_image(event, headers):
    """
    칭찬 이미지 생성 API 핸들러
    """
    try:
        # 요청 본문 파싱
        body = json.loads(event.get('body', '{}'))
        diary_id = body.get('diary_id', '')
        compliment = body.get('compliment', '')
        
        # 입력 검증
        if not diary_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'diary_id is required'})
            }
        
        if not compliment:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'compliment is required'})
            }
        
        # Bedrock으로 이미지 생성
        image_data = generate_quokka_image(compliment)
        
        # S3에 이미지 업로드
        image_url = upload_image_to_s3(diary_id, image_data)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'image_url': image_url
            })
        }
        
    except Exception as e:
        print(f"Image generation error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error'})
        }

def generate_quokka_image(compliment):
    """
    Bedrock Titan Image Generator를 사용하여 쿼카 이미지 생성
    """
    try:
        prompt = f"""
A cute, friendly quokka character saying: "{compliment}"
- Cartoon style, kawaii aesthetic
- Warm, encouraging expression
- Pastel colors
- Simple background
- Speech bubble with the compliment text
- High quality, detailed illustration
"""
        
        request_body = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt,
                "negativeText": "dark, scary, aggressive, realistic, photo"
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 512,
                "width": 512,
                "cfgScale": 8.0,
                "seed": 42
            }
        }
        
        response = bedrock_client.invoke_model(
            modelId='amazon.titan-image-generator-v1',
            body=json.dumps(request_body),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        image_data = base64.b64decode(response_body['images'][0])
        
        return image_data
        
    except ClientError as e:
        raise Exception(f"Bedrock image generation error: {e}")

def upload_image_to_s3(diary_id, image_data):
    """
    생성된 이미지를 S3에 업로드하고 pre-signed URL 반환
    """
    try:
        key = f"images/{diary_id}.png"
        
        # S3에 이미지 업로드
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=image_data,
            ContentType='image/png'
        )
        
        # Pre-signed URL 생성
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': key},
            ExpiresIn=3600
        )
        
        return presigned_url
        
    except ClientError as e:
        raise Exception(f"S3 upload error: {e}")