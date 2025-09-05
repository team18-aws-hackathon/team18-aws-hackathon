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

# 간단하고 안전한 스팸 패턴
SIMPLE_SPAM_CHECKS = ['ㅋㅋㅋㅋㅋ', '!!!!!!', '??????', 'ㅎㅎㅎㅎㅎ']

def analyze_content_quality(content):
    """최적화된 안전한 품질 분석"""
    
    # 1. 기본 검증
    if not content or not isinstance(content, str):
        return "error", "잘못된 입력"
    
    content_clean = content.strip()
    if not content_clean:
        return "empty", "빈 내용"
    
    try:
        # 2. 간단한 문자 수 계산 (정규식 없이)
        char_count = 0
        for char in content_clean:
            if ('가' <= char <= '힣') or char.isalnum():
                char_count += 1
        
        # 3. 단순 문자열 스팸 검사
        for spam_pattern in SIMPLE_SPAM_CHECKS:
            if spam_pattern in content_clean:
                return "spam", "무의미한 반복 패턴 감지"
        
        # 4. 길이 기반 등급
        if char_count > 80:
            return "high", "상세한 내용"
        elif char_count > 30:
            return "medium", "적당한 내용"
        elif char_count < 10:
            return "low", "내용이 너무 짧습니다"
        else:
            return "medium", "적당한 내용"
            
    except Exception as e:
        # 최종 안전망 - 기본값 반환
        return "medium", "기본 품질"

def validate_input(user_type, content):
    """기본 입력 검증 함수"""
    if not isinstance(user_type, str) or not isinstance(content, str):
        return "입력값은 문자열이어야 합니다", None, None

    if not user_type or user_type.lower() not in ['t', 'f']:
        return "사용자 타입은 't' 또는 'f'여야 합니다", None, None

    # 안전한 HTML 처리 (간단한 태그 제거)
    try:
        content_clean = html.unescape(content)
        content_clean = re.sub(r'<[^>]*?>', '', content_clean)
        content_clean = re.sub(r'\s+', ' ', content_clean).strip()
    except Exception:
        content_clean = content.strip()

    # 기본 길이 검증
    if len(content_clean.replace(' ', '')) < 10:
        return "일기 내용은 공백을 제외하고 최소 10자 이상이어야 합니다", None, None

    if len(content_clean) > 1000:
        return "일기 내용은 최대 1000자까지 입력 가능합니다", None, None

    # 의미있는 내용 검증
    if not re.search(r'[가-힣a-zA-Z]', content_clean):
        return "의미있는 내용을 입력해주세요 (한글 또는 영문 포함)", None, None

    # 간단한 개인정보 체크
    if re.search(r'01[0-9][-\s]?\d{3,4}[-\s]?\d{4}', content_clean):
        return "개인정보 보호를 위해 전화번호는 입력하지 말아주세요", None, None
    
    if re.search(r'\S+@\S+\.\S+', content_clean):
        return "개인정보 보호를 위해 이메일은 입력하지 말아주세요", None, None

    # 품질 분석 수행
    quality_level, quality_reason = analyze_content_quality(content_clean)
    
    # 스팸으로 판정된 경우 거부
    if quality_level == "spam":
        return quality_reason, None, None

    return None, content_clean, quality_level

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
        
        # 입력 검증 및 품질 분석
        validation_result = validate_input(user_type, content)
        if len(validation_result) == 3:
            error_msg, cleaned_content, quality_level = validation_result
        else:
            error_msg, cleaned_content = validation_result
            quality_level = "medium"  # 기본값
            
        if error_msg:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': error_msg})
            }
        
        # diary_id 생성
        timestamp = datetime.now().strftime('%Y%m%d')
        diary_id = f"diary-{timestamp}-{str(uuid.uuid4())[:3]}"
        
        # 품질 기반 Bedrock 칭찬 메시지 생성
        compliment = generate_compliment(cleaned_content, user_type.lower(), quality_level)
        
        # 품질 분석 결과 로깅
        print(f"품질 분석 결과 - diary_id: {diary_id}, quality: {quality_level}")
        
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
                'compliment': compliment,
                'quality_analysis': {
                    'level': quality_level,
                    'message': f"콘텐츠 품질: {quality_level}"
                }
            })
        }
        
    except Exception as e:
        print(f"Text generation error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error'})
        }

def get_quality_based_prompt(content, user_type, quality_level):
    """품질에 따른 맞춤 프롬프트 생성"""
    
    # 성격 유형별 차별화된 접근법 (쿼카의 밝은 톤 유지)
    personality_approach = {
        't': """쿼카답게 밝고 긍정적으로 칭찬하되, 실용적이고 현실적인 관점에서 접근해줘:
- 문제를 단순하게 보고 시원하게 격려해줘 ('그런 거 별거 아니야', '네 잘못 아니니까 괜찮아')
- 다른 재밌는 활동이나 긍정적인 것들을 제안하는 방향으로
- 너무 깊게 생각하지 말고 단순하게 접근하라는 식으로 밝게 조언해줘
- 쿼카처럼 항상 밝고 응원하는 톤을 유지해줘""",
        
        'f': """쿼카답게 밝고 긍정적으로 칭찬하되, 감정적으로 공감하고 따뜻하게 위로해줘:
- 감정 자체를 인정하고 깊이 공감해줘 ('힘들겠다', '충분히 이해해')
- 무조건적인 지지와 따뜻한 위로를 쿼카다운 밝은 에너지로 전달해줘
- 존재 자체를 긍정하고 항상 응원한다는 메시지를 따뜻하게
- 쿼카처럼 항상 밝고 사랑스러운 톤을 유지해줘"""
    }
    
    base_instruction = f"""
다음은 친구가 작성한 일기야:

"{content}"

이 일기를 읽고 쿼카(quokka)가 친한 친구처럼 밝고 따뜻하고 친근한 반말로 칭찬해줘.

{personality_approach[user_type]}

기본 요구사항:
- 40자에서 50자 이내로 작성해줘
- 이모지 1-2개 포함  
- 쿼카답게 밝고 긍정적이면서 친구같이 편안한 반말 톤
- "~야", "~네", "~구나" 같은 친근한 말투 사용
- 문장이 중간에 끊어지지 않도록 완전한 문장으로 마무리해줘
"""

    # 품질별 추가 지침 (성격 유형 고려하되 쿼카 톤 유지)
    if user_type == 't':
        quality_instructions = {
            "high": "- 체계적으로 생각한 부분을 쿼카답게 밝게 칭찬하고 실용적인 관점에서 격려해줘.\n- 효율적인 접근이나 현실적 판단을 구체적으로 인정하면서도 밝은 에너지로 응원해줘.",
            "medium": "- 좋은 점을 찾아서 쿼카답게 밝게 격려해줘.\n- 너무 복잡하게 생각하지 말라는 식으로 시원하면서도 긍정적으로 조언해줘.",
            "low": "- 일기 쓴 것 자체를 쿼카답게 밝게 인정하고 '그런 거면 충분해' 식으로 격려해줘.\n- 단순하게 생각하고 다른 재밌는 거 해보라고 밝게 제안해줘."
        }
    else:  # f type
        quality_instructions = {
            "high": "- 깊이 있는 성찰과 감정 표현을 쿼카답게 따뜻하고 밝게 칭찬해줘.\n- 솔직한 마음을 드러낸 용기를 구체적으로 인정하면서 밝은 에너지로 응원해줘.",
            "medium": "- 감정과 경험에 깊이 공감하면서 쿼카답게 따뜻하고 밝게 응원해줘.\n- 마음을 이해한다는 것을 보여주고 밝은 에너지로 위로해줘.",
            "low": "- 간단해도 마음을 표현한 것 자체를 쿼카답게 따뜻하고 밝게 칭찬해줘.\n- 작은 감정도 소중하다는 식으로 밝은 에너지로 격려해줘."
        }
    
    additional_instruction = quality_instructions[quality_level]
    
    return f"{base_instruction}\n{additional_instruction}\n\n쿼카다운 밝고 친근한 칭찬 메시지:"
def generate_compliment(content, user_type, quality_level="medium"):
    """
    Bedrock을 사용하여 품질 기반 칭찬 메시지 생성
    """
    try:
        # 품질에 따른 맞춤 프롬프트 생성
        prompt = get_quality_based_prompt(content, user_type, quality_level)
        
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
                "max_new_tokens": 200,  # 한글 150자 + 충분한 여유분으로 잘림 방지
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
