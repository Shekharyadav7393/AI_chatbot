"""RAG service — orchestrates retrieval-augmented generation.

Completely rewritten to remove langchain dependency. Uses plain Python
string formatting for prompts and the Gemini REST service for generation.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.embeddings.hf_embeddings import get_embedding_service
from app.models.message import MessageRole
from app.prompts.templates import (
    NO_CONTEXT_RESPONSE,
    SYSTEM_PROMPT,
    GENERAL_SYSTEM_PROMPT,
    RAG_PROMPT_TEMPLATE,
    GENERAL_PROMPT_TEMPLATE,
)
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.chat import ChatResponse
from app.schemas.message import MessageResponse
from app.services.gemini_service import get_gemini_llm_service
from app.utils.exceptions import NotFoundError, RAGError
from app.utils.helpers import truncate_text
from app.utils.logger import get_logger
from app.vectorstore.retriever import RetrieverService

settings = get_settings()
logger = get_logger(__name__)


class RAGService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_repo = ChatRepository(db)
        self.msg_repo = MessageRepository(db)
        self.retriever = RetrieverService()

    async def chat(self, message: str, chat_id: uuid.UUID | None, user_id: uuid.UUID) -> ChatResponse:
        chat_id, is_new_chat = await self._resolve_chat(message, chat_id, user_id)

        user_msg = await self.msg_repo.create(
            {
                "chat_id": chat_id,
                "role": MessageRole.user,
                "content": message,
            }
        )

        history_msgs = await self.msg_repo.get_recent_by_chat(chat_id, limit=10)
        chat_history = self._format_history([msg for msg in history_msgs if msg.id != user_msg.id])

        # Try to find relevant documents first
        try:
            embedding_service = get_embedding_service()
            query_embedding = embedding_service.embed_query(message)
            results = await self.retriever.similarity_search(
                query_embedding,
                top_k=settings.TOP_K_RESULTS,
                score_threshold=settings.RETRIEVAL_SCORE_THRESHOLD,
            )
        except Exception as exc:
            logger.warning("Retrieval failed, falling back to general answer: %s", exc)
            results = []

        if results:
            # Documents found — use RAG pipeline
            context = self._format_context(results)
            sources = [
                {
                    "document_id": res.get("document_id"),
                    "document": res["document_name"],
                    "chunk_index": res["chunk_index"],
                    "score": round(res["score"], 4),
                }
                for res in results
            ]

            try:
                assistant_response = await self._generate_rag_answer(context, chat_history, message)
            except Exception as exc:
                logger.error("RAG generation failed: %s, falling back to general...", exc)
                assistant_response = None

            if not assistant_response or assistant_response == NO_CONTEXT_RESPONSE:
                try:
                    assistant_response = await self._generate_general_answer(chat_history, message)
                    sources = []
                except Exception as exc:
                    logger.error("General fallback generation failed: %s", exc)
                    assistant_response = NO_CONTEXT_RESPONSE
        else:
            # No documents match — use general knowledge AI
            sources = []
            try:
                assistant_response = await self._generate_general_answer(chat_history, message)
            except Exception as exc:
                logger.error("General answer generation failed: %s", exc)
                assistant_response = NO_CONTEXT_RESPONSE

        assistant_msg = await self.msg_repo.create(
            {
                "chat_id": chat_id,
                "role": MessageRole.assistant,
                "content": assistant_response,
                "sources": sources,
            }
        )

        if not is_new_chat:
            await self.chat_repo.update(chat_id, {})

        return ChatResponse(chat_id=chat_id, message=MessageResponse.model_validate(assistant_msg))

    # ------------------------------------------------------------------ helpers

    async def _resolve_chat(
        self,
        message: str,
        chat_id: uuid.UUID | None,
        user_id: uuid.UUID,
    ) -> tuple[uuid.UUID, bool]:
        if not chat_id:
            chat = await self.chat_repo.create({"user_id": user_id, "title": truncate_text(message, max_length=50)})
            return chat.id, True

        chat = await self.chat_repo.get_by_id(chat_id)
        if not chat or chat.user_id != user_id:
            raise NotFoundError("Chat not found")
        return chat_id, False

    def _format_context(self, results: list[dict]) -> str:
        return "\n\n---\n\n".join(
            f"Document: {res['document_name']}\nChunk: {res['chunk_index']}\nContent:\n{res['chunk_text']}"
            for res in results
        )

    def _format_history(self, messages: list) -> str:
        if not messages:
            return "No previous conversation."
        formatted = []
        for msg in messages:
            role = "Customer" if msg.role == MessageRole.user else "Assistant"
            formatted.append(f"{role}: {truncate_text(msg.content, max_length=700)}")
        return "\n".join(formatted)

    async def _generate_rag_answer(self, context: str, chat_history: str, question: str) -> str:
        """Build RAG prompt and call Gemini."""
        prompt = RAG_PROMPT_TEMPLATE.format(
            system_prompt=SYSTEM_PROMPT,
            context=context,
            chat_history=chat_history,
            question=question,
        )
        llm = get_gemini_llm_service()
        return await llm.generate(prompt)

    async def _generate_general_answer(self, chat_history: str, question: str) -> str:
        """Build general prompt and call Gemini."""
        prompt = GENERAL_PROMPT_TEMPLATE.format(
            system_prompt=GENERAL_SYSTEM_PROMPT,
            chat_history=chat_history,
            question=question,
        )
        llm = get_gemini_llm_service()
        return await llm.generate(prompt)
