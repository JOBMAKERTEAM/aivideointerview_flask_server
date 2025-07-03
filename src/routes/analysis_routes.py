from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
import tempfile
from config.settings import Config

# EmotiEffLib 경로 설정 (emotion_analysis_service에서 필요)
Config.setup_emotiefflib_path()

from services.emotion_analysis_service import analyze_video_emotion, analyze_image_emotion

# Blueprint 생성
analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route("/analyze", methods=["POST"])
def analyze():
    """동영상 감정 분석 API 엔드포인트 (현재 사용하지 않음)"""
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    filename = secure_filename(video_file.filename)
    temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}_{filename}")
    video_file.save(temp_path)

    try:
        results = analyze_video_emotion(temp_path, device="cpu")
        os.remove(temp_path)
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@analysis_bp.route("/analyze-image", methods=["POST"])
def analyze_image():
    """이미지 감정 분석 API 엔드포인트"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
        
        image_data = data['image']
        frame_number = data.get('frame', 0)
        capture_time = data.get('captureTime', 0.0)
        
        # base64 prefix 제거 (data:image/jpeg;base64, 등)
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # 감정 분석 수행
        result = analyze_image_emotion(image_data, device="cpu")
        
        if result is None:
            return jsonify({"status": "error", "message": "Failed to analyze image"}), 500
        
        # 응답 데이터 구성
        response_data = {
            "status": "success",
            "frame": frame_number,
            "captureTime": capture_time,
            "emotion": result["emotion"],
            "confidence": result["confidence"],
            "faceDetected": result["face_detected"]
        }
        
        if "error" in result:
            response_data["warning"] = result["error"]
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Image analysis API error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500 