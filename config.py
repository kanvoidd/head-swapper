from pathlib import Path
import numpy as np

# --------------------------------------------------
# Constants
# --------------------------------------------------

MAX_VIDEO_SIZE_MB = 512
MAX_MODEL_SIZE_MB = 1024

BYTES_IN_MB = 1024 * 1024

ALLOWED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
}

ALLOWED_MODEL_EXTENSIONS = {
    ".glb",
    ".gltf",
    ".obj",
    ".fbx"
}

LANDMARKS_RADIUS = 3
LANDMARKS_COLOR = (255, 0, 0)
LANDMARKS_THICKNESS = 2

DETECT_WIDTH = 640

# --------------------------------------------------
# Head Pose Constants
# --------------------------------------------------

# Object points
CANONICAL_3D_FACE_MODEL = [
    [0.0,   0.0,   0.0],      # nose
    [0.0,  -63.6, -12.5],     # chin
    [-43.3, 32.7, -26.0],     # left eye
    [43.3,  32.7, -26.0],     # right eye
    [-28.9, -28.9, -24.1],    # left mouth
    [28.9,  -28.9, -24.1],    # right mouth
]

OBJECT_POINTS = np.array(CANONICAL_3D_FACE_MODEL, dtype=np.float64)

# MediaPipe landmarks
NOSE_INDEX = 1
CHIN_INDEX = 152
LEFT_EYE_INDEX = 263
RIGHT_EYE_INDEX = 33
LEFT_MOUTH_INDEX = 291
RIGHT_MOUTH_INDEX = 61


# Camera approximation
ASSUMED_FOCAL_LENGTH_FACTOR = 1.0


# Distortion
DIST_COEFFS = np.zeros((4, 1), dtype=np.float64)

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent  # Указывает на корень проекта

FRONTEND_DIR = BASE_DIR / "frontend"
STORAGE_DIR = BASE_DIR / "app/infrastructure/storage"

UPLOADS_DIR = STORAGE_DIR / "uploads"
PROCESSING_DIR = STORAGE_DIR / "processing"
RESULTS_DIR = STORAGE_DIR / "results"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSING_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


BLAZE_FACE_MODEL_PATH = BASE_DIR / "app/infrastructure/storage/models/face_landmarker.task"