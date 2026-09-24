import os
import re
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env if present
load_dotenv(BASE_DIR / ".env")


def _resolve_sqlite_uri(database_url: str | None) -> str:
    """Normalize SQLite file paths to the project-local database without breaking memory DB usage."""
    if not database_url:
        return f"sqlite:///{(BASE_DIR / 'careerprep.db').resolve()}"

    if database_url.startswith("sqlite:///:memory:") or database_url == "sqlite://":
        return database_url

    if database_url.startswith("sqlite:///"):
        candidate = database_url.replace("sqlite:///", "", 1)

        if candidate.startswith("/") and re.match(r"^/[A-Za-z]:", candidate):
            candidate = candidate[1:]

        if candidate in {":memory:", "", "/:memory:"}:
            return "sqlite:///:memory:"

        if not os.path.isabs(candidate):
            candidate = str((BASE_DIR / candidate).resolve())

        candidate = candidate.replace("\\", "/")
        return f"sqlite:///{candidate}"

    return database_url


class Config:
    """Application configuration settings."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-careerprep-2026")

    # SQLite Database
    SQLALCHEMY_DATABASE_URI = _resolve_sqlite_uri(os.getenv("DATABASE_URL"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Engine Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Demo Mode: True if explicitly set OR if API key is not provided
    _raw_demo = os.getenv("DEMO_MODE", "False").lower()
    DEMO_MODE = _raw_demo in ("true", "1", "yes") or not GEMINI_API_KEY

    # Uploads & Storage
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    AUDIO_FOLDER = UPLOAD_FOLDER / "recordings"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    
    # Allowed Extensions
    ALLOWED_RESUME_EXTENSIONS = {"pdf", "docx", "txt"}
    ALLOWED_AUDIO_EXTENSIONS = {"webm", "wav", "mp3", "ogg"}


# Ensure upload directories exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.AUDIO_FOLDER, exist_ok=True)
