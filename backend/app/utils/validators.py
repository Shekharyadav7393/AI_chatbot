import re
from pathlib import Path
from app.config.settings import get_settings

settings = get_settings()

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

def validate_file_type(filename: str) -> bool:
    """Validate if the file extension is allowed."""
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS

def validate_file_size(size: int) -> bool:
    """Validate if the file size is within limits."""
    return size <= settings.MAX_UPLOAD_SIZE

def validate_email(email: str) -> bool:
    """Basic email validation regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength (min 8 chars)."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    return True, ""

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal or invalid characters."""
    return re.sub(r'[^a-zA-Z0-9_\.-]', '_', filename)
