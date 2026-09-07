from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool
from uuid import uuid4

from backend.api.schema import ChatRequest, ChatResponse
from backend.services.llm_chat import answer_query


router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
	return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
	session_id = request.session_id or str(uuid4())
	response = await run_in_threadpool(
		answer_query,
		query=request.message,
		session_id=session_id,
	)
	return ChatResponse(response=response, session_id=session_id)