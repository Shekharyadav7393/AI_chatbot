"""AI Customer Support Chatbot backend package."""

import os
from pathlib import Path

backend_dir = Path(__file__).resolve().parents[1]
hf_cache_dir = backend_dir / ".cache" / "huggingface"
hf_cache_dir.mkdir(parents=True, exist_ok=True)

os.environ.setdefault("HF_HOME", str(hf_cache_dir))
os.environ.setdefault("SENTENCE_TRANSFORMERS_HOME", str(hf_cache_dir / "sentence-transformers"))
