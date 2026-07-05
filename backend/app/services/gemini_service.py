import httpx

from app.config.settings import get_settings
from app.utils.exceptions import RAGError
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)


class GeminiLLMService:
    """Gemini REST client used by the RAG chain when GEMINI_API_KEY is set."""

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise RAGError("GEMINI_API_KEY is required when AI_PROVIDER is set to gemini.")

    async def generate(self, prompt: str) -> str:
        model = settings.GEMINI_MODEL
        model_path = model if model.startswith("models/") else f"models/{model}"
        url = f"{settings.GEMINI_API_BASE_URL}/{model_path}:generateContent"
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=settings.GEMINI_TIMEOUT_SECONDS) as client:
                response = await client.post(
                    url,
                    params={"key": settings.GEMINI_API_KEY},
                    json=payload,
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error("Gemini API returned %s: %s", exc.response.status_code, exc.response.text)
            raise RAGError("Gemini API request failed. Check GEMINI_API_KEY and GEMINI_MODEL.") from exc
        except httpx.HTTPError as exc:
            logger.error("Gemini API request failed: %s", exc)
            raise RAGError("Could not reach Gemini API.") from exc

        data = response.json()
        candidates = data.get("candidates") or []
        if not candidates:
            block_reason = data.get("promptFeedback", {}).get("blockReason")
            raise RAGError(f"Gemini API returned no candidates. Block reason: {block_reason or 'unknown'}")

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts)
        return text.strip()


def get_gemini_llm_service() -> GeminiLLMService:
    return GeminiLLMService()
