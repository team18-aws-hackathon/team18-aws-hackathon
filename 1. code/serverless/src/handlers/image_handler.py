import json
import boto3
import base64
import os
from botocore.exceptions import ClientError

bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
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
        image_data = generate_quokka_image(compliment, diary_id)
        
        # 배경 제거
        bg_removed_image = remove_background(image_data)
        
        # S3에 이미지 업로드
        image_url = upload_image_to_s3(diary_id, bg_removed_image)
        
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

def generate_quokka_image(compliment, diary_id=None):
    """
    Bedrock Nova Image Generator를 사용하여 쿼카 이미지 생성
    """
    try:
        prompt = f"""
        A cute quokka character expressing: "{compliment}". Create unique expression and pose that match this specific compliment:
        - Pixel art style with kawaii aesthetic
        - Show only ONE single quokka (not multiple)
        - FULL BODY view showing the complete quokka from head to feet
        - Pose direction: either front-facing OR turned 45 degrees to the left
        - Soft pastel color palette that reflects the compliment's emotion
        - Clean, simple background
        - High quality, detailed pixel art illustration
        - Make quokka as UNIQUE and DIFFERENT as you can imagine
        """
        
        request_body = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt,
                "negativeText": "character sheet format, multiple quokkas, 2quokkas, text, watermark, text box, dark, shadow, background-color, scary, aggressive, realistic, photo, extra limbs, deformed, low quality",
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 512,
                "width": 512,
                "cfgScale": 8.0,
                "seed": hash(diary_id) % 1000000 if diary_id else 42
            }
        }
        
        response = bedrock_client.invoke_model(
            modelId='amazon.nova-canvas-v1:0',
            body=json.dumps(request_body),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        image_data = base64.b64decode(response_body['images'][0])
        
        return image_data
        
    except ClientError as e:
        raise Exception(f"Bedrock image generation error: {e}")

def remove_background(image_data):
    """
    Amazon Nova Canvas를 사용하여 이미지 배경 제거
    """
    try:
        # 이미지를 base64로 인코딩
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        request_body = {
            "taskType": "BACKGROUND_REMOVAL",
            "backgroundRemovalParams": {
                "image": image_base64
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 512,
                "width": 512
            }
        }
        
        response = bedrock_client.invoke_model(
            modelId='amazon.nova-canvas-v1:0',
            body=json.dumps(request_body),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        bg_removed_data = base64.b64decode(response_body['images'][0])
        
        return bg_removed_data
        
    except ClientError as e:
        print(f"Background removal error: {e}")
        # 배경 제거 실패 시 원본 이미지 반환
        return image_data

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
        print(f"S3 upload error: {e}")
        raise Exception(f"S3 upload error: {e}")