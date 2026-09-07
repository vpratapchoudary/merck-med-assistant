from langchain_core.tools import tool

from backend.config import PINECONE_CFG
from backend.vectors.embedding import embed_query, load_embedding_model
from backend.vectors.retriever import query_pinecone_index
from backend.utils.logs import log_config

logger = log_config(__name__)


@tool
def get_context(
    query: str, 
    top_k: int = 5, 
    index_host: str = PINECONE_CFG["index_host"], 
    namespace: str = PINECONE_CFG["namespace"]
) -> dict:
    """
    Retrieve relevant context from the vector store based on the user's query.

    Args:
        query (str): The user's query.
        top_k (int): The number of top results to return.
        index_host (str): The host of the Pinecone index.
        namespace (str): The namespace to query within the index.
    """
    logger.info(f"Retrieving context for query: {query}")
    query_vector = embed_query(query, load_embedding_model())
    return query_pinecone_index(
        index_host=index_host,
        query_vector=query_vector,
        top_k=top_k,
        namespace=namespace
    )