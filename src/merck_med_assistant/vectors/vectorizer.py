import os
from pathlib import Path

from pinecone import Pinecone, ServerlessSpec

from merck_med_assistant.vectors.preprocess import chunk_embed_pdf
from merck_med_assistant.utils.logs import logger

def vectorize_store_pdf(
        pdf_path: Path, 
        index_name: str,
        chunk_size: int = 500,
        chunk_overlap: int = 200,
        embed_model: str = "all-MiniLM-L6-v2",
        vec_dim: int = 384,
        metric: str = "cosine",
        pinecone_cloud: str = "aws",
        pinecone_region: str = "us-east-1"
    ) -> None:
    """
    Vectorize a PDF file and store the embeddings in a Pinecone index.

    Args:
        pdf_path (Path): Path to the PDF file.
        index_name (str): Name of the Pinecone index to store the embeddings.
    """
    logger.info(f"Vectorizing PDF: {pdf_path}")
    # Chunk and embed the PDF
    chunks_with_embeddings = chunk_embed_pdf(
        pdf_path=pdf_path,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        embed_model=embed_model
    )

    # Initialize Pinecone client
    pinecone = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )

    # Create or connect to the index
    if index_name not in pinecone.list_indexes():
        logger.info(f"Creating Pinecone index: {index_name}")
        pinecone.create_index(
            index_name, 
            dimension=vec_dim, 
            metric=metric, 
            serverless=ServerlessSpec(
                cloud=pinecone_cloud,
                region=pinecone_region
            )
        )
    
    index = pinecone.Index(index_name)

    # Upsert embeddings into the index
    logger.info(f"Upserting {len(chunks_with_embeddings)} embeddings into Pinecone index: {index_name}")
    for i, item in enumerate(chunks_with_embeddings):
        index.upsert(
            vectors=(
                [(f"{pdf_path.stem}_{i}", 
                      item["embedding"], 
                      {"text": item["text"]})
                ]
            )
        )