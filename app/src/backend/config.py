VECTORIZER_CFG = {
    "embed_model": "all-MiniLM-L6-v2",
    "chunk_size": 500,
    "chunk_overlap": 200,
    "vec_dim": 384,
    "metric": "cosine",
}

PINECONE_CFG = {
    "cloud": "aws",
    "region": "us-east-1",
    "index_name": "med-assistant-index",
    "namespace": "merck-manual",
    "index_host": "https://med-assistant-index-dtdp5ws.svc.aped-4627-b74a.pinecone.io"
}

LLM_CFG = {
    "model_name": "qwen/qwen3.8-27b",
    "temperature": 0.0,
    "max_tokens": 512
}