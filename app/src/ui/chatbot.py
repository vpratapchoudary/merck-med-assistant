from pathlib import Path

import chainlit as cl
from starlette.concurrency import run_in_threadpool

from backend.services.llm_chat import answer_query

CL_PATH = Path(__file__)

@cl.on_chat_start
async def start_chat():
    await cl.Message(
        content="Hello! I am your medical assistant. How can I help you today?"
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    response_text = await run_in_threadpool(answer_query, query=message.content)

    # Send the model's response back to the user
    await cl.Message(content=response_text).send()