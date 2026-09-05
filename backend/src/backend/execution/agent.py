from langchain_groq import ChatGroq

from backend.execution.tools import get_context

def run_groq_chat_model(
    model_name: str,
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 512,
) -> str:
    """
    Run a chat model using the Groq API.

    Args:
        model_name (str): The name of the Groq model to use.
        messages (list[dict]): A list of message dictionaries, each containing 'role' and 'content'.
        temperature (float): Sampling temperature for the model.
        max_tokens (int): Maximum number of tokens to generate.

    Returns:
        str: The generated response from the model.
    """
    chat_model = ChatGroq(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens
    ).bind_tools([get_context])
    response = chat_model.invoke(messages)
    return response.content