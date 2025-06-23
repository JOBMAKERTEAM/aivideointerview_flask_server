import os
import requests
import base64

def synthesize_speech(text, voice_type):
    api_key = os.getenv("SPEECH_TO_TEXT_API_KEY")
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
    
    # voice_type이 이미 전체 이름으로 전달됨
    payload = {
        "input": {
            "text": text
        },
        "voice": {
            "languageCode": "ko-KR",
            "name": voice_type
        },
        "audioConfig": {
            "audioEncoding": "LINEAR16"
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()["audioContent"]
        else:
            error_detail = response.json().get('error', {}).get('message', 'Unknown error')
            raise Exception(f"Synthesis failed: {error_detail}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
