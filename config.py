from pathlib import Path

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