from app.utils.logger import get_logger
from app.vectorstore.chroma_store import ChromaVectorStore

logger = get_logger(__name__)


class RetrieverService:
    def __init__(self) -> None:
        self.vector_store = ChromaVectorStore()

    async def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        score_threshold: float = 0.7,
    ) -> list[dict]:
        try:
            return self.vector_store.similarity_search(query_embedding, top_k, score_threshold)
        except Exception as e:
            logger.error("Error in vector store similarity search: %s", e)
            raise
