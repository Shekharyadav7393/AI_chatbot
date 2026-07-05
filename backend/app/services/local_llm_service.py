import asyncio
import os
from functools import lru_cache

from transformers import pipeline

from app.config.settings import get_settings
from app.utils.exceptions import RAGError
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)


class LocalLLMService:
    """Offline Hugging Face generator used by the RAG chain."""

    def __init__(self) -> None:
        os.environ["TRANSFORMERS_OFFLINE"] = "1" if settings.TRANSFORMERS_OFFLINE else "0"
        os.environ["HF_HUB_OFFLINE"] = "1" if settings.TRANSFORMERS_OFFLINE else "0"
        try:
            self.generator = pipeline(
                task=settings.LOCAL_LLM_TASK,
                model=settings.LOCAL_LLM_MODEL,
                tokenizer=settings.LOCAL_LLM_MODEL,
            )
            logger.info("Loaded local LLM model %s", settings.LOCAL_LLM_MODEL)
        except Exception as exc:
            logger.error("Failed to load local LLM %s: %s", settings.LOCAL_LLM_MODEL, exc)
            raise RAGError(
                "Local AI model is not available. Download/cache the configured Hugging Face model or set LOCAL_LLM_MODEL to a local model path."
            ) from exc

    async def generate(self, prompt: str) -> str:
        return await asyncio.to_thread(self._generate_sync, prompt)

    def _generate_sync(self, prompt: str) -> str:
        kwargs = {
            "max_new_tokens": settings.LOCAL_LLM_MAX_NEW_TOKENS,
            "do_sample": settings.LOCAL_LLM_TEMPERATURE > 0,
        }
        if settings.LOCAL_LLM_TEMPERATURE > 0:
            kwargs["temperature"] = settings.LOCAL_LLM_TEMPERATURE

        output = self.generator(prompt, **kwargs)[0]
        text = output.get("generated_text") or output.get("summary_text") or output.get("translation_text") or ""
        if text.startswith(prompt):
            text = text[len(prompt):]
        return text.strip()


@lru_cache()
def get_local_llm_service() -> LocalLLMService:
    return LocalLLMService()
