from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv  # ✅ 추가
from flask_cors import CORS  # 추가
import os
import uuid
import tempfile
import json

from analyze_video_emotion import analyze_video_emotion
from transcribe_audio import transcribe_wav
from text_to_speech import synthesize_speech

# ✅ .env 파일 불러오기
load_dotenv()

app = Flask(__name__)
CORS(app)  # CORS 추가
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# ✅ 환경변수에서 API 키 불러오기
SECRET_API_KEY = os.getenv("API_SECRET_KEY")

@app.before_request
def verify_api_key():
    client_key = request.headers.get("x-api-key")
    if client_key != SECRET_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    filename = secure_filename(video_file.filename)
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
    video_file.save(temp_path)

    try:
        results = analyze_video_emotion(temp_path, device="cpu")
        os.remove(temp_path)
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        # JSON 데이터 받기
        data = request.get_json()
        if not data or 'videoUrl' not in data:
            return jsonify({"error": "Video URL is required"}), 400

        video_url = data['videoUrl']
        
        try:
            # 음성 인식 수행
            transcript = transcribe_wav(video_url)
            
            return app.response_class(
                response=json.dumps({
                    "status": "success",
                    "transcript": transcript
                }, ensure_ascii=False),
                status=200,
                mimetype='application/json'
            )
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

@app.route("/synthesize", methods=["POST"])
def synthesize():
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002, debug=True)