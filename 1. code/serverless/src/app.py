import json
from handlers.text_handler import handle_generate_text
from handlers.image_handler import handle_generate_image
from handlers.voice_handler import handle_generate_voice

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
        
        # 경로별 라우팅
        path = event.get('path', '')
        
        if path == '/generate/text':
            return handle_generate_text(event, headers)
        elif path == '/generate/image':
            return handle_generate_image(event, headers)
        elif path == '/generate/voice':
            return handle_generate_voice(event, headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not Found'})
            }
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
