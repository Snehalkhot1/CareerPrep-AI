"""Speech and audio file utilities."""
import os
import uuid
from werkzeug.utils import secure_filename
from config import Config


def is_allowed_audio_file(filename):
    """Checks if audio filename has an allowed extension."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in Config.ALLOWED_AUDIO_EXTENSIONS


def save_audio_file(file_storage):
    """Saves uploaded audio file safely and returns the saved filename."""
    if not file_storage or file_storage.filename == "":
        return None

    original_filename = secure_filename(file_storage.filename)
    ext = original_filename.rsplit(".", 1)[1].lower() if "." in original_filename else "webm"
    unique_filename = f"audio_{uuid.uuid4().hex[:12]}.{ext}"
    
    file_path = os.path.join(Config.AUDIO_FOLDER, unique_filename)
    file_storage.save(file_path)
    return unique_filename
