#!/bin/bash
echo "AI Interview 음성 처리 전용 환경 설치..."

# 1. 시스템 패키지 설치
sudo apt-get update
sudo apt-get install -y python3.9 python3.9-dev python3.9-venv python3-pip ffmpeg

# 2. Python 가상환경 생성
python3.9 -m venv ai_speech_env
source ai_speech_env/bin/activate

# 3. 초경량 Python 패키지 설치
pip install --upgrade pip

pip install flask==2.3.3
pip install flask-cors==6.0.0  
pip install requests==2.32.3
pip install python-dotenv==1.1.0
pip install boto3==1.38.22

echo "flask 서버 설치 완료!"
echo "flask 환경 활성화: source ai_speech_env/bin/activate"