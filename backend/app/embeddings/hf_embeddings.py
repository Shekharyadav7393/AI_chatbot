"""Embedding service using Google Gemini's text-embedding-004 model.

This replaces the previous sentence-transformers based service that required
torch (~2GB). The Gemini embedding API is free-tier friendly and produces
768-dimensional embeddings with zero local ML dependencies.
"""

import httpx

from app.config.settings import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)


class EmbeddingService:
    """Generates text embeddings via the Gemini embedding API."""

    EMBED_MODEL = "models/text-embedding-004"
    BATCH_LIMIT = 100  # Gemini batch embed limit

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is required for the embedding service.")
        self._base_url = settings.GEMINI_API_BASE_URL

    def embed_text(self, text: str) -> list[float]:
        """Embed a single piece of text synchronously (blocking)."""
        url = f"{self._base_url}/{self.EMBED_MODEL}:embedContent"
        payload = {
            "model": self.EMBED_MODEL,
            "content": {"parts": [{"text": text}]},
            "taskType": "RETRIEVAL_DOCUMENT",
        }

        response = httpx.post(
            url,
            params={"key": settings.GEMINI_API_KEY},
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()["embedding"]["values"]

    def embed_query(self, text: str) -> list[float]:
        """Embed a query text (uses RETRIEVAL_QUERY task type for better search results)."""
        url = f"{self._base_url}/{self.EMBED_MODEL}:embedContent"
        payload = {
            "model": self.EMBED_MODEL,
            "content": {"parts": [{"text": text}]},
            "taskType": "RETRIEVAL_QUERY",
        }

        response = httpx.post(
            url,
            params={"key": settings.GEMINI_API_KEY},
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()["embedding"]["values"]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts using Gemini batch embed API."""
        if not texts:
            return []

        url = f"{self._base_url}/{self.EMBED_MODEL}:batchEmbedContents"
        all_embeddings: list[list[float]] = []

        # Process in batches of BATCH_LIMIT
        for i in range(0, len(texts), self.BATCH_LIMIT):
            batch = texts[i : i + self.BATCH_LIMIT]
            requests = [
                {
                    "model": self.EMBED_MODEL,
                    "content": {"parts": [{"text": t}]},
                    "taskType": "RETRIEVAL_DOCUMENT",
                }
                for t in batch
            ]

            response = httpx.post(
                url,
                params={"key": settings.GEMINI_API_KEY},
                json={"requests": requests},
                timeout=60.0,
            )
            response.raise_for_status()

            data = response.json()
            for emb in data.get("embeddings", []):
                all_embeddings.append(emb["values"])

        return all_embeddings


_embedding_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
