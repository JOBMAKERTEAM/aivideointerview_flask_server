from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
import tempfile
from config.settings import Config

# EmotiEffLib 경로 설정 (emotion_analysis_service에서 필요)
Config.setup_emotiefflib_path()

from services.emotion_analysis_service import analyze_video_emotion

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