import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import cv2
from cv2 import VideoCapture

from config import BLAZE_FACE_MODEL_PATH, UPLOADS_DIR

test_img = UPLOADS_DIR / "photo_example.jpg"

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(BLAZE_FACE_MODEL_PATH)),
    running_mode=VisionRunningMode.VIDEO
)


def mark_face_landmarks(video_path: str):

    cap = VideoCapture(video_path)

    frame_index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Внутренняя константа OpenCv CAP_PROP_POS_MSEC нередко возвращает 0 или некорректно рассчитывает время
        # Поэтому считаем timestamp вручную
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_timestamp_ms = int(frame_index / fps * 1000)
        frame_index += 1
        
        landmarked_frame = track_face_landmarks(frame, frame_timestamp_ms)
        # cv2.imshow('frame', landmarked_frame)
        #if cv2.waitKey(33) == ord('q'):
            #break
        face = landmarked_frame.face_landmarks[0]
        for i, lm in enumerate(face):
            X = lm.x
            Y = lm.y
            Z = lm.z
            print(f"landmark {i}:\nX: {X}\nY: {Y}\nZ: {Z}\n\n")

    cap.release()


def track_face_landmarks(frame, frame_timestamp_ms):
    
    mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    with FaceLandmarker.create_from_options(options) as landmarker:
        lm_res = landmarker.detect_for_video(mp_frame, frame_timestamp_ms)

    return lm_res

if __name__ == "__main__":
    mark_face_landmarks(UPLOADS_DIR / "b2a5c2ef-0494-40e5-9bfd-c55a3db3ce04.mp4")

