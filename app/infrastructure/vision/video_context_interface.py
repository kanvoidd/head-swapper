from cv2 import VideoCapture, VideoWriter
from dataclasses import dataclass

@dataclass
class VideoContext:
    cap: VideoCapture
    frame_index: int
    fps: float
    frame_height: int
    frame_width: int
    writer: VideoWriter