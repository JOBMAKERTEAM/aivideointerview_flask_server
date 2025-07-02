from flask import Flask
from flask_cors import CORS
from config.settings import Config
from middleware.auth_middleware import verify_api_key
from routes.transcribe_routes import transcribe_bp

def create_app():
    """Flask 애플리케이션 팩토리 함수"""
    app = Flask(__name__)
    
    # 설정 로드
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
    
    # CORS 설정
    CORS(app)
    
    # 미들웨어 등록
    app.before_request(verify_api_key)
    
    # Blueprint 등록
    app.register_blueprint(transcribe_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)