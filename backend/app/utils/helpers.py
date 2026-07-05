import uuid
from datetime import datetime, timezone
from pathlib import Path

def generate_uuid() -> str:
    """Generates a UUID string."""
    return str(uuid.uuid4())

def get_file_extension(filename: str) -> str:
    """Gets the lowercase extension of a filename."""
    return Path(filename).suffix.lower()

def format_file_size(size_bytes: int) -> str:
    """Formats bytes into human readable string."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncates text and adds ellipsis if too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_utc_now() -> datetime:
    """Returns the current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)
