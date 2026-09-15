import mediapipe as mp

import cv2
from cv2 import VideoCapture

from config import BLAZE_FACE_MODEL_PATH, UPLOADS_DIR, LANDMARKS_RADIUS, LANDMARKS_COLOR, LANDMARKS_THICKNESS, DETECT_WIDTH

class FaceTracker:

    def __init__(self, video_path):
        self.video_path = video_path
        self.BaseOptions = mp.tasks.BaseOptions
        self.FaceLandmarker = mp.tasks.vision.FaceLandmarker
        self.FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        self.options = self.FaceLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path=str(BLAZE_FACE_MODEL_PATH)),
            running_mode=self.VisionRunningMode.VIDEO
        )

        self.landmarker = self.FaceLandmarker.create_from_options(self.options)


    def mark_face_landmarks(self):

        cap = VideoCapture(self.video_path)

        frame_index = 0

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_timestamp_ms = int(frame_index / fps * 1000)
                frame_index += 1

                processed_frame = self.process_frame(frame)
                landmarked = self.landmarker.detect_for_video(processed_frame, frame_timestamp_ms)

                landmarked_frame = self.draw_face_landmarks(
                    frame=frame, 
                    landmarked_frame=landmarked,
                    frame_height=frame_height,
                    frame_width=frame_width,
                    radius=LANDMARKS_RADIUS,
                    color=LANDMARKS_COLOR,
                    thickness=LANDMARKS_THICKNESS,
                )

                cv2.imshow('frame', landmarked_frame)
                if cv2.waitKey(5) == ord('q'):
                    break
        finally:                
            cap.release()
            self.landmarker.close()
            cv2.destroyAllWindows()


    def process_frame(self, frame):
        h, w = frame.shape[:2]
        scale = DETECT_WIDTH / w

        resized_frame = cv2.resize(frame, (DETECT_WIDTH, int(scale * h)))
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        return mp_frame

    def draw_face_landmarks(self, frame, landmarked_frame, frame_height, frame_width, radius=3, color=(255, 0, 0), thickness=1):

        # лицо не найдено, возвращаем кадр как есть
        if not landmarked_frame.face_landmarks:
            return frame

        face = landmarked_frame.face_landmarks[0]
        for lm in face:
            center = (int(lm.x * frame_width), int(lm.y * frame_height))
            frame = cv2.circle(frame, center, radius, color, thickness)

        return frame
            

if __name__ == "__main__":
    video_path = UPLOADS_DIR / "b2a5c2ef-0494-40e5-9bfd-c55a3db3ce04.mp4"
    face_tracker = FaceTracker(video_path=video_path)

    face_tracker.mark_face_landmarks()