import os
import sys
import tempfile
from pathlib import Path

# .env 파일 불러오기 (dotenv가 설치된 경우에만)
try:
    from dotenv import load_dotenv
    # src 폴더의 상위 폴더에서 .env 파일 찾기
    current_dir = os.path.dirname(os.path.abspath(__file__))  # config 폴더
    src_dir = os.path.dirname(current_dir)  # src 폴더
    project_root = os.path.dirname(src_dir)  # ai_interview 폴더
    env_path = os.path.join(project_root, '.env')
    load_dotenv(env_path)
except ImportError:
    print("Warning: python-dotenv not installed. Using system environment variables only.")

def _parse_server_address(server_address):
    """서버 주소를 HOST와 PORT로 분리"""
    try:
        # http:// 또는 https:// 프로토콜 제거
        if server_address.startswith(('http://', 'https://')):
            server_address = server_address.split('://', 1)[1]
        
        if ":" in server_address:
            host, port = server_address.rsplit(":", 1)
            return host, int(port)
        else:
            # 포트가 없으면 기본값 사용
            return server_address, 3002
    except (ValueError, AttributeError):
        # 파싱 실패시 기본값 사용
        return "0.0.0.0", 3002

class Config:
    """애플리케이션 설정"""
    
    # Flask 설정
    DEBUG = True
    
    # 서버 주소 파싱 (예: "localhost:3000" 또는 "0.0.0.0:3002")
    FLASK_URL = os.getenv("FLASK_URL", "0.0.0.0:3002")
    HOST, PORT = _parse_server_address(FLASK_URL)
    
    # 업로드 설정
    UPLOAD_FOLDER = tempfile.gettempdir()
    
    # API 키 설정
    SECRET_API_KEY = os.getenv("API_SECRET_KEY")
    SPEECH_TO_TEXT_API_KEY = os.getenv("SPEECH_TO_TEXT_API_KEY")
    
    # AWS 설정
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
    
    # EmotiEffLib 경로 설정
    PROJECT_ROOT = Path(__file__).parent.parent.parent  # ai_interview 디렉토리
    SRC_PATH = PROJECT_ROOT / "src"  # src 디렉토리
    EMOTIEFFLIB_PATH = PROJECT_ROOT / "EmotiEffLib"
    
    @classmethod
    def setup_emotiefflib_path(cls):
        """EmotiEffLib과 src 디렉토리를 Python path에 추가"""
        # src 디렉토리 추가 (config 모듈 등을 import하기 위해)
        src_str = str(cls.SRC_PATH)
        if src_str not in sys.path:
            sys.path.insert(0, src_str)
            print(f"src path added to sys.path: {src_str}")
            
        # EmotiEffLib 디렉토리 추가
        emotiefflib_str = str(cls.EMOTIEFFLIB_PATH)
        if emotiefflib_str not in sys.path:
            sys.path.insert(0, emotiefflib_str)
            print(f"EmotiEffLib path added to sys.path: {emotiefflib_str}") 