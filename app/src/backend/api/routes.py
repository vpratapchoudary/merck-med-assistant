from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool

from backend.api.schema import ChatRequest, ChatResponse
from backend.services.llm_chat import answer_query


router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
	return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
	response = await run_in_threadpool(answer_query, query=request.message)
	return ChatResponse(response=response)