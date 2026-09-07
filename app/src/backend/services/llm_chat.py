from backend.config import LLM_CFG
from backend.execution.agent import run_groq_chat_model
from backend.execution.prompts import SYSTEM_MESSAGE
from backend.services.conversation import conversation_store
from backend.utils.logs import log_config

logger = log_config(__name__)


def answer_query(query: str, session_id: str) -> str:
    """
    Answer a user's query using the Groq chat model.

    Args:
        query (str): The user's query.
        session_id (str): The stable ID for the user's conversation.

    Returns:
        str: The model's response to the query.
    """
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    messages.extend(conversation_store.get(session_id))
    messages.append({"role": "user", "content": query})

    logger.info(f"Running Groq chat model with query: {query}")
    response = run_groq_chat_model(
        model_name=LLM_CFG["model_name"],
        messages=messages,
        temperature=LLM_CFG["temperature"],
        max_tokens=LLM_CFG["max_tokens"],
    )
    
    conversation_store.append(
        session_id=session_id,
        user_message=query,
        assistant_message=response,
    )
    return response