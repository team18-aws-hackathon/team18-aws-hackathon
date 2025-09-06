import json
import os
import random
from datetime import datetime
from jamo import h2j, j2hcj
import boto3
from botocore.exceptions import ClientError

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

s3_client = boto3.client('s3', region_name='us-east-1')
S3_BUCKET = os.environ.get('S3_BUCKET')

char_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', ' ']
char_sounds_high = {}
sounds_loaded = False

CONSONANT_MAP = {
    'ㄱ': 'ㅋ', 'ㄲ': 'ㅋ', 'ㄴ': 'ㄴ', 'ㄷ': 'ㅌ', 'ㄸ': 'ㅌ',
    'ㄹ': 'ㄹ', 'ㅁ': 'ㅁ', 'ㅂ': 'ㅍ', 'ㅃ': 'ㅍ', 'ㅅ': 'ㅅ',
    'ㅆ': 'ㅅ', 'ㅇ': 'ㅇ', 'ㅈ': 'ㅊ', 'ㅉ': 'ㅊ', 'ㅊ': 'ㅊ',
    'ㅋ': 'ㅋ', 'ㅌ': 'ㅌ', 'ㅍ': 'ㅍ', 'ㅎ': 'ㅎ'
}

def handle_generate_voice(event, headers):
    """
    칭찬 음성 생성 API 핸들러
    """
    try:
        body = json.loads(event.get('body', '{}'))
        diary_id = body.get('diary_id', '')
        compliment = body.get('compliment', '')
        
        if not diary_id or not compliment:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'diary_id and compliment are required'})
            }
        
        kk_sound = convert_to_kk_style(compliment)
        voice_url = generate_voice_file(kk_sound, diary_id)
        
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

def convert_to_kk_style(text):
    result = []
    for char in text:
        if '가' <= char <= '힣':
            jamos = j2hcj(h2j(char))
            if jamos and jamos[0] in CONSONANT_MAP:
                result.append(CONSONANT_MAP[jamos[0]])
    return ''.join(result)

def load_padata_sounds():
    global sounds_loaded, char_sounds_high
    
    if sounds_loaded or not PYDUB_AVAILABLE:
        return sounds_loaded
    
    try:
        high_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'sources', 'high')
        
        if not os.path.exists(high_dir):
            return False
        
        for idx, item in enumerate(char_list):
            high_file = os.path.join(high_dir, f'{idx + 1:02d}.padata')
            if os.path.exists(high_file):
                char_sounds_high[item] = AudioSegment.from_file(high_file)
        
        sounds_loaded = len(char_sounds_high) > 0
        return sounds_loaded
        
    except Exception:
        return False

def generate_voice_file(kk_sound, diary_id):
    if not load_padata_sounds():
        return None
    
    try:
        result_sound = None
        
        for char in kk_sound:
            if char in char_sounds_high:
                char_sound = char_sounds_high[char]
                octaves = 2 * random.uniform(0.96, 1.15)
                new_sample_rate = int(char_sound.frame_rate * (2.0 ** octaves))
                
                pitch_char_sound = char_sound._spawn(
                    char_sound.raw_data, 
                    overrides={'frame_rate': new_sample_rate}
                )
                
                result_sound = pitch_char_sound if result_sound is None else result_sound + pitch_char_sound
        
        if result_sound:
            filename = f"{diary_id}.wav"
            
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                result_sound.export(temp_file.name, format="wav")
                
                s3_key = f"voices/{filename}"
                s3_url = upload_to_s3(temp_file.name, s3_key)
                
                os.unlink(temp_file.name)
                
                return s3_url
        
        return None
        
    except Exception:
        return None

def upload_to_s3(file_path, s3_key):
    """
    파일을 S3에 업로드하고 URL 반환
    """
    try:
        s3_client.upload_file(
            file_path, 
            S3_BUCKET, 
            s3_key,
            ExtraArgs={'ContentType': 'audio/wav'}
        )
        
        s3_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"
        return s3_url
        
    except ClientError as e:
        print(f"S3 업로드 실패: {e}")
        return None