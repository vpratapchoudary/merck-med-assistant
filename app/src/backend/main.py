from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from chainlit.utils import mount_chainlit

from backend.api.routes import router
from backend.vectors.embedding import load_embedding_model
from ui.chatbot import CL_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the embedding model at startup
    load_embedding_model()
    yield

app = FastAPI(
    title="Merck Medical Assistant",
    lifespan=lifespan
)

app.include_router(router)

mount_chainlit(
	app=app,
	target=str(CL_PATH),
	path="/ui",
)