
class VideoErrorValidator:

    def validate_video_capture(cap, path):
        if not cap.isOpened():
            raise ValueError(f"Failed to open video: {path}")

    def validate_video_writer(writer, path):
        if not writer.isOpened():
            writer.release()
            raise ValueError(f"Failed to write video: {path}")