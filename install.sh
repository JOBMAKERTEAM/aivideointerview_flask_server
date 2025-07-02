#!/bin/bash
echo "AI Interview 음성 처리 전용 환경 설치..."

# 1. 시스템 패키지 설치
sudo apt-get update
sudo apt-get install -y python3.9 python3.9-dev python3.9-venv python3-pip ffmpeg

# 2. Python 가상환경 생성
python3.9 -m venv ai_speech_env
source ai_speech_env/bin/activate

# 3. pip 업그레이드
pip install --upgrade pip

# 4. Flask 웹 프레임워크
pip install flask==2.3.3
pip install flask-cors==6.0.0  
pip install werkzeug==3.1.3

# 5. 환경변수 관리
pip install python-dotenv==1.1.0

# 6. HTTP 요청 라이브러리
pip install requests==2.32.3

# 7. AWS SDK
pip install boto3==1.38.22
pip install botocore==1.38.22

# 8. Google Cloud Speech API
pip install google-cloud-speech==2.32.0
pip install google-api-core==2.24.2
pip install google-auth==2.40.2
pip install googleapis-common-protos==1.70.0
pip install grpcio==1.72.0rc1
pip install grpcio-status==1.72.0rc1
pip install proto-plus==1.26.1
pip install protobuf==6.31.0

# 9. 컴퓨터 비전 및 이미지 처리
pip install opencv-python==4.11.0.86
pip install opencv-python-headless==4.11.0.86
pip install numpy==1.26.3
pip install pillow==10.2.0

# 10. 딥러닝 프레임워크 (PyTorch)
pip install torch==2.2.2
pip install torchvision==0.17.2
pip install torchaudio==2.2.2

# 11. 얼굴 인식
pip install facenet-pytorch==2.6.0

# 12. 감정 분석 라이브러리
pip install emotiefflib==1.0

# 13. 유틸리티 라이브러리들
pip install tqdm==4.67.1
pip install pyyaml==6.0.2
pip install coloredlogs==15.0.1
pip install humanfriendly==10.0

# 14. 기타 의존성
pip install certifi==2025.4.26
pip install charset-normalizer==3.4.2
pip install idna==3.10
pip install urllib3==1.26.20
pip install six==1.17.0
pip install python-dateutil==2.9.0.post0
pip install jmespath==1.0.1
pip install s3transfer==0.13.0
pip install packaging==25.0
pip install filelock==3.13.1
pip install fsspec==2024.6.1
pip install huggingface-hub==0.31.2
pip install safetensors==0.5.3
pip install sympy==1.13.3
pip install networkx==3.2.1
pip install mpmath==1.3.0
pip install typing-extensions==4.12.2

echo ""
echo "====================================="
echo "✅ AI Interview Flask 서버 설치 완료!"
echo "====================================="
echo ""
echo "🚀 사용 방법:"
echo "1. 가상환경 활성화: source ai_speech_env/bin/activate"
echo "2. 서버 시작: cd src && python app.py"
echo ""
echo "📋 설치된 주요 기능:"
echo "- Flask 웹 서버"
echo "- Google Cloud Speech-to-Text API"
echo "- AWS S3 연동"
echo "- 컴퓨터 비전 (OpenCV)"
echo "- 딥러닝 (PyTorch)"
echo "- 얼굴 인식 (FaceNet)"
echo "- 감정 분석 (EmotiEffLib)"
echo ""
echo "⚠️  주의사항:"
echo "- .env 파일에 API 키 설정 필요"
echo "- ffmpeg는 시스템 패키지로 설치됨"