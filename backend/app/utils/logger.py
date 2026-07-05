import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.config.settings import get_settings

settings = get_settings()

class JsonFormatter(logging.Formatter):
    def format(self, record):
        import json
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage()
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    app_logger = logging.getLogger("app")
    app_logger.setLevel(settings.LOG_LEVEL)
    
    # Avoid duplicate logs if run multiple times
    if app_logger.handlers:
        return
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # File handler
    file_handler = RotatingFileHandler(
        log_dir / "app.log", maxBytes=10485760, backupCount=5
    )
    file_handler.setFormatter(JsonFormatter())
    
    app_logger.addHandler(console_handler)
    app_logger.addHandler(file_handler)
    
    # Also set for root logger
    logging.getLogger().setLevel(settings.LOG_LEVEL)
    logging.getLogger().addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"app.{name}")
