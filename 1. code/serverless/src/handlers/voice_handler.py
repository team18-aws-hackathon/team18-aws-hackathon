import json
import boto3
import os
from botocore.exceptions import ClientError

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
        
        # 임시 더미 음성 파일 생성 (향후 TTS 서비스 연동 예정)
        voice_url = create_dummy_voice_url(diary_id)
        
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

def create_dummy_voice_url(diary_id):
    """
    더미 음성 URL 생성 (향후 TTS 서비스 연동 예정)
    """
    # 임시로 더미 URL 반환
    return f"https://s3.amazonaws.com/quokka/voices/{diary_id}.mp3"