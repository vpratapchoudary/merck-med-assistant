from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage

from backend.execution.tools import get_context
from backend.utils.logs import log_config

logger = log_config(__name__)

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
    conversation = list(messages)

    for _ in range(3):
        response = chat_model.invoke(conversation)
        conversation.append(response)

        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:
            tool_result = get_context.invoke(tool_call["args"])
            conversation.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"],
                    name=tool_call["name"],
                )
            )

    raise RuntimeError("The model exceeded the maximum number of tool calls")