import os

from pinecone.grpc import PineconeGRPC as Pinecone

from merck_med_assistant.utils.logs import logger

def query_pinecone_index(
        index_host: str, 
        query_vector: list, 
        top_k: int = 3, 
        namespace: str = "__default__"):
    """
    Query a Pinecone index with a given vector.

    Args:
        index_host (str): The host of the Pinecone index.
        query_vector (list): The vector to query against the index.
        top_k (int): The number of top results to return.
        namespace (str): The namespace to query within the index.

    Returns:
        dict: The query results from Pinecone.
    """
    logger.info(f"Querying Pinecone index at host: {index_host}")
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(host=index_host)

    response = index.query(
        namespace=namespace,
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        include_values=False
    )
    return response