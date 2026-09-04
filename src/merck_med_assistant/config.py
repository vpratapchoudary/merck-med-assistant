VECTORIZER_CFG = {
    "embed_model": "all-MiniLM-L6-v2",
    "chunk_size": 500,
    "chunk_overlap": 200,
    "vec_dim": 384,
    "metric": "cosine",
    "index_name": "merck_manual_index"
}

PINECONE_CFG = {
    "cloud": "aws",
    "region": "us-east-1"
}