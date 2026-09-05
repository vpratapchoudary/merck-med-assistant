from backend.config import LLM_CFG
from backend.execution.agent import run_groq_chat_model
from backend.execution.prompts import SYSTEM_MESSAGE
from backend.utils.logs import logger


def answer_query(query: str) -> str:
    """
    Answer a user's query using the Groq chat model.

    Args:
        query (str): The user's query.

    Returns:
        str: The model's response to the query.
    """
    messages = [
        {
            "role": "system", 
            "content": SYSTEM_MESSAGE
        }, 
        {
            "role": "user", 
            "content": query
        }
    ]
    
    response = run_groq_chat_model(
        model_name=LLM_CFG["model_name"],
        messages=messages,
        temperature=LLM_CFG["temperature"],
        max_tokens=LLM_CFG["max_tokens"],
    )
    
    return response