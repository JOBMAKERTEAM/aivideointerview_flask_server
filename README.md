# AI Interview - Speech Processing API

AI 면접 시스템을 위한 음성 처리 API 서버입니다. 음성을 텍스트로 변환하고, 텍스트를 음성으로 합성하는 기능을 제공합니다.

## 🎯 주요 기능

### 1. 음성 인식 (Speech-to-Text)
- 비디오/오디오 파일에서 음성을 텍스트로 변환
- Google Cloud Speech-to-Text API 사용
- 한국어 음성 인식 지원
- WebM, WAV 등 다양한 오디오 형식 지원

### 2. 음성 합성 (Text-to-Speech)
- 텍스트를 자연스러운 음성으로 변환
- Google Cloud Text-to-Speech API 사용
- 한국어 음성 합성 지원
- 다양한 음성 타입 선택 가능

### 3. API 보안
- API 키 기반 인증 시스템
- CORS 지원으로 웹 애플리케이션 연동

## 🛠 기술 스택

- **Backend**: Python 3.9, Flask
- **Speech Processing**: Google Cloud Speech/Text-to-Speech API
- **Audio Processing**: FFmpeg
- **Cloud Storage**: AWS S3 (선택적)
- **Dependencies**: 6개 핵심 패키지로 최적화

## 📋 시스템 요구사항

### 필수 시스템 패키지
- Python 3.9+
- FFmpeg (오디오 변환용)

### Python 패키지
```txt
flask==2.3.3
flask-cors==6.0.0
requests==2.32.3
python-dotenv==1.1.0
boto3==1.38.22
werkzeug==3.1.3
```

## 🚀 설치 및 실행

### 1. Repository 클론
```bash
git clone <repository-url>
cd ai_interview
```

### 2. 시스템 패키지 설치 (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3.9 python3.9-dev python3.9-venv python3-pip ffmpeg
```

### 3. Python 가상환경 설정
```bash
python3.9 -m venv ai_speech_env
source ai_speech_env/bin/activate  # Linux/Mac
# ai_speech_env\Scripts\activate    # Windows
```

### 4. 패키지 설치
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. 환경변수 설정
`.env` 파일을 생성하고 다음 내용을 입력:
```env
# API 보안 키
API_SECRET_KEY=your-secret-api-key

# Google Cloud API 키
SPEECH_TO_TEXT_API_KEY=your-google-cloud-api-key

# AWS 설정 (선택적)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=your-aws-region
AWS_S3_BUCKET=your-s3-bucket-name
```

### 6. 서버 실행
```bash
cd src
python app.py
```

서버가 `http://localhost:3002`에서 실행됩니다.

## 📚 API 사용법

### 인증
모든 API 요청에는 헤더에 API 키가 필요합니다:
```
x-api-key: your-secret-api-key
```

### 1. 음성 인식 API

**POST** `/transcribe`

비디오/오디오 URL에서 음성을 텍스트로 변환합니다.

```bash
curl -X POST http://localhost:3002/transcribe \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key" \
  -d '{
    "videoUrl": "https://example.com/video.webm"
  }'
```

**응답 예시:**
```json
{
  "status": "success",
  "transcript": "안녕하세요. 면접에 참여해주셔서 감사합니다."
}
```

### 2. 음성 합성 API

**POST** `/synthesize`

텍스트를 음성으로 변환합니다.

```bash
curl -X POST http://localhost:3002/synthesize \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key" \
  -d '{
    "text": "안녕하세요. 면접을 시작하겠습니다.",
    "voice": "ko-KR-Standard-A"
  }'
```

**응답 예시:**
```json
{
  "status": "success",
  "audioContent": "base64-encoded-audio-data"
}
```

## 🐳 Docker 배포

### Dockerfile
```dockerfile
FROM python:3.9-slim

# FFmpeg 설치
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY src/ .

# 포트 노출
EXPOSE 3002

# 앱 실행
CMD ["python", "app.py"]
```

### Docker 실행
```bash
# 이미지 빌드
docker build -t ai-interview-api .

# 컨테이너 실행
docker run -p 3002:3002 --env-file .env ai-interview-api
```

## ☁️ AWS 배포

### EC2 배포
```bash
# EC2 인스턴스에서
sudo apt-get update
sudo apt-get install python3.9 python3.9-venv python3-pip ffmpeg

python3.9 -m venv ai_speech_env
source ai_speech_env/bin/activate
pip install -r requirements.txt

# PM2로 프로세스 관리 (선택적)
npm install -g pm2
pm2 start app.py --interpreter python3
```

### ECS/Fargate 배포
1. Docker 이미지를 ECR에 푸시
2. ECS 태스크 정의 생성
3. 서비스 배포

## 🔧 개발 환경 설정

### 개발용 실행
```bash
# 개발 모드로 실행 (자동 재시작)
export FLASK_ENV=development
python app.py
```

### 로그 확인
```bash
# 실시간 로그 확인
tail -f app.log

# 또는 Docker 로그
docker logs -f container-name
```

## 🔍 트러블슈팅

### 일반적인 문제들

**1. FFmpeg not found 오류**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

**2. Google Cloud API 키 오류**
- Google Cloud Console에서 Speech-to-Text, Text-to-Speech API 활성화
- API 키 생성 및 권한 확인
- `.env` 파일의 API 키 확인

**3. 메모리 부족 오류**
- 큰 오디오 파일 처리 시 발생
- 서버 메모리 증설 또는 파일 크기 제한 설정

### 로그 메시지
```
✅ 정상: "Starting transcription for video_url: ..."
❌ 오류: "Failed to download video: 404"
❌ 오류: "WAV conversion failed"
```

## 📊 성능 최적화

### 권장 서버 사양
- **개발환경**: CPU 2코어, RAM 4GB
- **운영환경**: CPU 4코어, RAM 8GB
- **디스크**: SSD 권장

### 최적화 팁
- 임시 파일 자동 정리 (구현됨)
- 동시 요청 수 제한
- 로드 밸런서 사용 (다중 인스턴스)

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

## 🔗 관련 링크

- [Google Cloud Speech-to-Text API](https://cloud.google.com/speech-to-text)
- [Google Cloud Text-to-Speech API](https://cloud.google.com/text-to-speech)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)

---

**버전**: v1.0.0  
**최종 업데이트**: 2024년  
**문의**: [your-email@example.com] 

## 🔄 주요 개선사항

1. **관심사의 분리**: 라우터, 서비스, 설정, 미들웨어를 각각 분리
2. **Blueprint 패턴**: Flask Blueprint를 사용한 모듈식 라우팅
3. **애플리케이션 팩토리**: `create_app()` 함수로 앱 생성
4. **중앙집중식 설정**: 모든 환경변수를 `config/settings.py`에서 관리
5. **확장성**: 새로운 기능 추가가 쉬워짐

## 💾 기존 파일 백업

기존 파일들은 `.bak` 확장자로 백업되어 있습니다:
- `transcribe_audio.py.bak`
- `text_to_speech.py.bak`  
- `analyze_video_emotion.py.bak`

## 🚀 사용 방법

**서버 실행:**
```bash
cd ai_interview/src
python app.py
```

**새로운 기능 추가시 (예: 음성 합성 활성화):**
```python
# app.py에 추가
from routes.synthesis_routes import synthesis_bp
app.register_blueprint(synthesis_bp)
```

## 📚 추가 문서

프로젝트 구조에 대한 자세한 설명은 `ai_interview/ARCHITECTURE.md` 파일에서 확인할 수 있습니다.

이제 코드가 훨씬 더 체계적이고 관리하기 쉬운 구조로 변경되었습니다! 🎯 