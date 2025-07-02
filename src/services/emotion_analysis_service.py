import cv2
import numpy as np
from typing import List, Dict
from facenet_pytorch import MTCNN
from config.settings import Config

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
                results.append({
                    "frame": frame_idx,
                    "time_sec": round(frame_idx / fps, 2),
                    "emotion": emotions[0],
                    "confidence": round(float(np.max(scores[0])), 3)
                })

        frame_idx += 1

    cap.release()
    print(f"✅ Finished analyzing. Total analyzed frames: {len(results)}")
    return results 