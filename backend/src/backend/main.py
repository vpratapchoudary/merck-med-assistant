from fastapi import FastAPI

from backend.api.routes import router


app = FastAPI(title="Merck Medical Assistant")
app.include_router(router)
