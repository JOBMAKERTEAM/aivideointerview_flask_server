import os
import base64
import json
import requests
import boto3
import tempfile
from botocore.exceptions import ClientError
from config.settings import Config

def transcribe_wav(video_url, language_code="ko-KR"):
    """비디오 URL에서 음성을 인식하여 텍스트로 변환"""
    temp_webm_path = None
    temp_wav_path = None
    try:
        print(f"Starting transcription for video_url: {video_url}")
        
        # presigned URL에서 파일 다운로드
        response = requests.get(video_url)
        if response.status_code != 200:
            raise Exception(f"Failed to download video: {response.status_code}")
        
        # 임시 webm 파일 저장
        temp_webm_path = tempfile.NamedTemporaryFile(delete=False, suffix='.webm').name
        with open(temp_webm_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded webm file to: {temp_webm_path}")
        
        # webm을 wav로 변환
        temp_wav_path = temp_webm_path.replace('.webm', '.wav')
        convert_command = f'ffmpeg -y -i "{temp_webm_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{temp_wav_path}"'
        print(f"Converting with command: {convert_command}")
        os.system(convert_command)
        
        if not os.path.exists(temp_wav_path):
            raise Exception("WAV conversion failed")
            
        print(f"Converted to WAV: {temp_wav_path}")
        
        # WAV 파일을 base64로 인코딩
        with open(temp_wav_path, 'rb') as audio_file:
            audio_content = base64.b64encode(audio_file.read()).decode('utf-8')

        # 임시 파일들 삭제
        if temp_webm_path and os.path.exists(temp_webm_path):
            os.unlink(temp_webm_path)
        if temp_wav_path and os.path.exists(temp_wav_path):
            os.unlink(temp_wav_path)

        # 요청 payload 구성
        request_body = {
            "config": {
                "encoding": "LINEAR16",
                "sampleRateHertz": 16000,
                "languageCode": language_code
            },
            "audio": {
                "content": audio_content
            }
        }

        # 환경변수에서 API 키 가져오기
        api_key = Config.SPEECH_TO_TEXT_API_KEY
        if not api_key:
            raise Exception("SPEECH_TO_TEXT_API_KEY 환경변수가 설정되어 있지 않습니다.")

        url = f"https://speech.googleapis.com/v1/speech:recognize?key={api_key}"
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }

        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(request_body)
        )

        if response.status_code == 200:
            data = response.json()
            transcript = ""
            for result in data.get('results', []):
                transcript += result['alternatives'][0]['transcript']
            return transcript
        else:
            raise Exception(f"Speech-to-Text API error: {response.text}")

    except Exception as e:
        # 임시 파일들이 존재하면 삭제
        if temp_webm_path and os.path.exists(temp_webm_path):
            os.unlink(temp_webm_path)
        if temp_wav_path and os.path.exists(temp_wav_path):
            os.unlink(temp_wav_path)
        raise e

def download_from_s3(s3_key):
    """S3에서 파일 다운로드"""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_REGION
    )
    bucket_name = Config.AWS_S3_BUCKET
    
    if not all([Config.AWS_ACCESS_KEY_ID, Config.AWS_SECRET_ACCESS_KEY, bucket_name]):
        raise Exception("AWS credentials or bucket name not properly configured")

    # 임시 파일 생성
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
    try:
        # HeadObject 체크를 건너뛰고 바로 다운로드 시도
        print(f"Downloading from bucket: {bucket_name}, key: {s3_key}")
        s3_client.download_file(
            Bucket=bucket_name,
            Key=s3_key,
            Filename=temp_file.name,
            ExtraArgs={'RequestPayer': 'requester'}  # 필요한 경우에만 추가
        )
        return temp_file.name
    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        raise Exception(f"S3 download failed: {str(e)}") 