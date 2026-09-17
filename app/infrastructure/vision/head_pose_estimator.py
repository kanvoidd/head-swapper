import numpy as np
import cv2

from .face_tracker import FaceTracker
from config import UPLOADS_DIR, OBJECT_POINTS, NOSE_INDEX, CHIN_INDEX, LEFT_EYE_INDEX, RIGHT_EYE_INDEX, LEFT_MOUTH_INDEX, RIGHT_MOUTH_INDEX, ASSUMED_FOCAL_LENGTH_FACTOR, DIST_COEFFS

class HeadPoseEstimator:

    def __init__(self):

        self.face_tracker = FaceTracker()

        self.object_points = OBJECT_POINTS

        self.factor = ASSUMED_FOCAL_LENGTH_FACTOR
        self.dist_coeffs = DIST_COEFFS

        self.landmarks_idxs = [NOSE_INDEX, CHIN_INDEX, LEFT_EYE_INDEX, RIGHT_EYE_INDEX, LEFT_MOUTH_INDEX, RIGHT_MOUTH_INDEX]


    def estimate_head_pose(self, frame, frame_timestamp, camera_matrix, video_resolution: tuple):

        # Получаем нормализованные координаты точек лица
        landmarks = self.face_tracker.detect_face_landmarks(frame, frame_timestamp)

        # Отбираем нужные координаты лица + переводим их в пиксели
        image_points = self.get_image_points(
            landmarks,
            video_width=video_resolution[0],
            video_height=video_resolution[1]
        )

        if image_points is None:
            return None

        success, rvec, tvec = cv2.solvePnP(
            objectPoints=self.object_points,
            imagePoints=image_points,
            cameraMatrix=camera_matrix,
            distCoeffs=self.dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success: 
            raise ValueError("Failed to estimate pose.")

        yaw, pitch, roll = self.get_head_angles(rvec)

        return {
            "rvec": rvec,
            "tvec": tvec,
            "yaw": yaw,
            "pitch": pitch,
            "roll": roll,
        }
        


    def get_camera_matrix(self, video_width, video_height):

        fx, fy = video_width * self.factor, video_width * self.factor

        cx = video_width / 2
        cy = video_height / 2

        camera_matrix = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0,  0,  1]
        ], dtype=np.float64)

        return camera_matrix


    def get_image_points(self, landmarks, video_width, video_height):

        try:
            face = landmarks.face_landmarks[0]
        except IndexError:
            return None

        image_points = []

        for idx in self.landmarks_idxs:
            lm = face[idx]
            X, Y = lm.x * video_width, lm.y * video_height
            image_points.append([X, Y])

        return np.array(image_points, dtype=np.float64)

    def get_head_angles(self, rvec):

        rotation_matrix, _ = cv2.Rodrigues(rvec)
        angles, *_ = cv2.RQDecomp3x3(rotation_matrix)
        yaw, pitch, roll = angles

        return yaw, pitch, roll



if __name__ == "__main__":
    head_pose_estimator = HeadPoseEstimator()

    video_path = UPLOADS_DIR / "b2a5c2ef-0494-40e5-9bfd-c55a3db3ce04.mp4"
    cap = cv2.VideoCapture(video_path)
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_index = 0
    
    camera_matrix = head_pose_estimator.get_camera_matrix(frame_width, frame_height)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_timestamp_ms = int(frame_index / fps * 1000)
        frame_index += 1

        print(head_pose_estimator.estimate_head_pose(frame, frame_timestamp_ms, camera_matrix, (frame_width, frame_height)))