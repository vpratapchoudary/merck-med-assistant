from functools import lru_cache

import os

from sentence_transformers import SentenceTransformer

from backend.config import VECTORIZER_CFG
from backend.utils.logs import logger


@lru_cache(maxsize=None)
def load_embedding_model(model_name: str = VECTORIZER_CFG["embed_model"]) -> SentenceTransformer:
    """Load an embedding model once and reuse it for the application's lifetime."""
    logger.info(f"Loading embedding model: {model_name}")
    return SentenceTransformer(
        model_name_or_path=model_name,
        token=os.getenv("HF_TOKEN"),
    )


def embed_query(query: str, model: SentenceTransformer | None = None) -> list[float]:
    """Embed one user query using the application's configured model."""
    if not query.strip():
        raise ValueError("Query must not be empty")

    model = model or load_embedding_model()
    embedding = model.encode(query)
    return embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)