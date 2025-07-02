from flask import Blueprint, request, jsonify
import json
from services.transcribe_service import transcribe_wav

# Blueprint 생성
transcribe_bp = Blueprint('transcribe', __name__)

@transcribe_bp.route("/transcribe", methods=["POST"])
def transcribe():
    """음성 인식 API 엔드포인트"""
    try:
        # JSON 데이터 받기
        data = request.get_json()
        if not data or 'videoUrl' not in data:
            return jsonify({"error": "Video URL is required"}), 400

        video_url = data['videoUrl']
        
        try:
            # 음성 인식 수행
            transcript = transcribe_wav(video_url)
            
            return jsonify({
                "status": "success",
                "transcript": transcript
            }), 200
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            return jsonify({
                "status": "error",
                "message": str(e),
                "detail": "Error during transcription process"
            }), 500
            
    except Exception as e:
        print(f"Request handling error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "detail": "Error processing request"
        }), 500 