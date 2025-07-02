from flask import Blueprint, request, jsonify
from services.text_to_speech_service import synthesize_speech

# Blueprint 생성
synthesis_bp = Blueprint('synthesis', __name__)

@synthesis_bp.route("/synthesize", methods=["POST"])
def synthesize():
    """음성 합성 API 엔드포인트 (현재 사용하지 않음)"""
    try:
        # JSON 데이터 받기
        data = request.get_json()
        if not data or 'text' not in data or 'voice' not in data:
            return jsonify({"error": "Text and voice name are required"}), 400

        text = data['text']
        voice_type = data['voice']
        
        try:
            # 음성 합성 수행
            audio_content = synthesize_speech(text, voice_type)
            
            return jsonify({
                "status": "success",
                "audioContent": audio_content
            })
        except Exception as e:
            print(f"Synthesis error: {str(e)}")
            return jsonify({
                "status": "error",
                "message": str(e),
                "detail": "Error during speech synthesis"
            }), 500
            
    except Exception as e:
        print(f"Request handling error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "detail": "Error processing request"
        }), 500 