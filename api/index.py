import sys
from pathlib import Path

# Add root directory to python path
file_path = Path(__file__).resolve().parent.parent
sys.path.append(str(file_path))

from app import app

# Vercel entrypoint
app = app