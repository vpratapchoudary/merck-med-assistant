import os
from contextlib import asynccontextmanager

import uvicorn
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


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)