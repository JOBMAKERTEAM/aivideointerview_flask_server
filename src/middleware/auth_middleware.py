from flask import request, jsonify
from config.settings import Config

def verify_api_key():
    """API 키 검증 미들웨어"""
    client_key = request.headers.get("x-api-key")
    if client_key != Config.SECRET_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401 