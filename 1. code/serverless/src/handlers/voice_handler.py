import json
import boto3
import os
from botocore.exceptions import ClientError

polly_client = boto3.client('polly')
s3_client = boto3.client('s3')

S3_BUCKET = os.environ.get('S3_BUCKET')

def handle_generate_voice(event, headers):
    """
    칭찬 음성 생성 API 핸들러
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
        
        # Polly로 음성 생성
        audio_data = generate_voice(compliment)
        
        # S3에 음성 파일 업로드
        voice_url = upload_voice_to_s3(diary_id, audio_data)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'voice_url': voice_url
            })
        }
        
    except Exception as e:
        print(f"Voice generation error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error'})
        }

def generate_voice(text):
    """
    Amazon Polly를 사용하여 음성 생성
    """
    try:
        # 이모지 제거 (Polly가 처리하지 못함)
        clean_text = ''.join(char for char in text if ord(char) < 0x1F600 or ord(char) > 0x1F64F)
        clean_text = ''.join(char for char in clean_text if ord(char) < 0x1F300 or ord(char) > 0x1F5FF)
        clean_text = ''.join(char for char in clean_text if ord(char) < 0x1F680 or ord(char) > 0x1F6FF)
        clean_text = ''.join(char for char in clean_text if ord(char) < 0x2600 or ord(char) > 0x26FF)
        
        response = polly_client.synthesize_speech(
            Text=clean_text,
            OutputFormat='mp3',
            VoiceId='Seoyeon',  # 한국어 여성 목소리
            Engine='neural'
        )
        
        return response['AudioStream'].read()
        
    except ClientError as e:
        raise Exception(f"Polly TTS error: {e}")

def upload_voice_to_s3(diary_id, audio_data):
    """
    생성된 음성 파일을 S3에 업로드하고 pre-signed URL 반환
    """
    try:
        key = f"voices/{diary_id}.mp3"
        
        # S3에 음성 파일 업로드
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=audio_data,
            ContentType='audio/mpeg'
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