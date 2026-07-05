from langchain_core.prompts import PromptTemplate

# ---------------------------------------------------------------------------
# RAG (Knowledge Retrieval) Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an advanced AI Support Desk Assistant.
Answer the customer's query using the provided company document context.
Analyze the context carefully to find the answer.
If the context does not contain the answer, or only partially answers the query, reply with:
"I'm sorry, but I couldn't find that information in the uploaded company documents."
Do not make up facts or use outside knowledge when using this mode.
Keep the tone professional, polite, and helpful."""

RAG_PROMPT_TEMPLATE = """{system_prompt}

Below is the conversation history (if any):
---------------------
{chat_history}
---------------------

Company document context:
---------------------
{context}
---------------------

Current User Question: {question}

Please provide a helpful and direct answer to the Current User Question based on the context and conversation history.

Grounded Answer:"""

NO_CONTEXT_RESPONSE = "I'm sorry, but I couldn't find that information in the uploaded company documents."

def get_rag_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)


# ---------------------------------------------------------------------------
# General Knowledge Fallback Prompts (Rule 2 & 3)
# ---------------------------------------------------------------------------

GENERAL_SYSTEM_PROMPT = """You are an advanced AI Support Desk Assistant.
Answer the user's queries clearly and accurately using your baseline training knowledge.
Fully understand and reply in the same language the user uses.
If the user asks in Hinglish (e.g., "python kya hai"), understand their intent perfectly and reply in clear, helpful, and natural Hinglish.
Format your responses nicely with proper markdown when appropriate.
Maintain a professional, polite, and helpful support desk tone at all times."""

GENERAL_PROMPT_TEMPLATE = """{system_prompt}

Below is the conversation history (if any):
---------------------
{chat_history}
---------------------

Current User Question: {question}

Please provide a helpful and direct answer to the Current User Question based on the conversation context.

Helpful Answer:"""

def get_general_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(GENERAL_PROMPT_TEMPLATE)
