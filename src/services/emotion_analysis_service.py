import cv2
import numpy as np
from typing import List, Dict, Optional
from facenet_pytorch import MTCNN
from config.settings import Config
import base64
from PIL import Image
import io

# EmotiEffLib 경로 설정
Config.setup_emotiefflib_path()

from emotiefflib.facial_analysis import EmotiEffLibRecognizer

def init_models(device: str = "cpu", model_name: str = "enet_b0_8_best_afew"):
    """모델 초기화"""
    fer = EmotiEffLibRecognizer(engine="torch", model_name=model_name, device=device)
    mtcnn = MTCNN(keep_all=False, post_process=False, min_face_size=40, device=device)
    return fer, mtcnn

def recognize_faces(frame: np.ndarray, mtcnn: MTCNN) -> List[np.ndarray]:
    """얼굴 감지"""
    boxes, probs = mtcnn.detect(frame, landmarks=False)
    if probs is None or probs[0] is None:
        return []
    boxes = boxes[probs > 0.9]
    facial_images = []
    for box in boxes:
        x1, y1, x2, y2 = map(int, box[:4])
        facial_images.append(frame[y1:y2, x1:x2, :])
    return facial_images

def softmax_normalize_confidence(logit_scores):
    """logit 점수를 0-1 범위 확률로 변환"""
    # softmax 적용하여 확률로 변환
    exp_scores = np.exp(logit_scores - np.max(logit_scores))  # 수치적 안정성을 위해 최댓값 빼기
    probabilities = exp_scores / np.sum(exp_scores)
    return float(np.max(probabilities))

def analyze_image_emotion(image_data: str, device: str = "cpu") -> Optional[Dict]:
    """이미지 기반 감정 분석
    
    Args:
        image_data: base64 인코딩된 이미지 데이터
        device: 사용할 디바이스 (cpu/cuda)
    
    Returns:
        감정 분석 결과 딕셔너리 또는 None
    """
    try:
        fer, mtcnn = init_models(device=device)
        
        # base64 디코딩
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # PIL 이미지를 OpenCV 형식으로 변환
        image_np = np.array(image)
        if len(image_np.shape) == 3:
            # RGB to BGR for OpenCV
            if image_np.shape[2] == 3:
                rgb_frame = image_np
            else:
                rgb_frame = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
        else:
            print("❌ Invalid image format")
            return None
        
        # 얼굴 감지
        faces = recognize_faces(rgb_frame, mtcnn)
        
        if not faces:
            print("⚠️ No faces detected in image")
            return {
                "emotion": "Neutral",
                "confidence": 0.0,
                "face_detected": False
            }
        
        # 감정 분석 (첫 번째 얼굴만 사용)
        emotions, scores = fer.predict_emotions([faces[0]], logits=True)
        
        # logit 점수를 0-1 범위 확률로 변환
        confidence = softmax_normalize_confidence(scores[0])
        
        result = {
            "emotion": emotions[0],
            "confidence": round(confidence, 3),
            "face_detected": True
        }
        
        print(f"✅ Image emotion analysis: {result['emotion']} (confidence: {result['confidence']} = {round(confidence*100, 1)}%)")
        return result
        
    except Exception as e:
        print(f"❌ Image emotion analysis error: {str(e)}")
        return {
            "emotion": "Neutral",
            "confidence": 0.0,
            "face_detected": False,
            "error": str(e)
        }

def analyze_video_emotion(video_path: str, device: str = "cpu", frame_interval: int = 10) -> List[Dict]:
    """동영상 감정 분석"""
    fer, mtcnn = init_models(device=device)

    results = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_idx = 0

    print(f"🔍 Analyzing video: {video_path}")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        if frame_idx % frame_interval == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = recognize_faces(rgb_frame, mtcnn)

            if faces:
                emotions, scores = fer.predict_emotions(faces, logits=True)
                
                # logit 점수를 0-1 범위 확률로 변환
                confidence = softmax_normalize_confidence(scores[0])
                
                results.append({
                    "frame": frame_idx,
                    "time_sec": round(frame_idx / fps, 2),
                    "emotion": emotions[0],
                    "confidence": round(confidence, 3)
                })

        frame_idx += 1

    cap.release()
    print(f"✅ Finished analyzing. Total analyzed frames: {len(results)}")
    return results 