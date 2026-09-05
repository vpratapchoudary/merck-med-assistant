import json
import os
from pathlib import Path

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

from merck_med_assistant.vectors.preprocess import chunk_embed_pdf
from merck_med_assistant.utils.logs import logger

def vectorize_store_pdf(
        pdf_path: Path, 
        index_name: str,
        namespace: str = "",
        chunk_size: int = 500,
        chunk_overlap: int = 200,
        embed_model: str = "all-MiniLM-L6-v2",
        vec_dim: int = 384,
        metric: str = "cosine",
        pinecone_cloud: str = "aws",
        pinecone_region: str = "us-east-1",
        batch_size: int = 100,
        progress_file: Path | None = None
    ) -> None:
    """
    Vectorize a PDF file and store the embeddings in a Pinecone index.

    Args:
        pdf_path (Path): Path to the PDF file.
        index_name (str): Name of the Pinecone index to store the embeddings.
        namespace (str): The namespace to store the embeddings in.
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
    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )

    if not pc.has_index(index_name):
        logger.info(f"Creating Pinecone index: {index_name}")
        pc.indexes.create(
            name=index_name,
            vector_type="dense",
            dimension=vec_dim,
            metric=metric,
            spec=ServerlessSpec(
                cloud=pinecone_cloud,
                region=pinecone_region
            ),
            deletion_protection="disabled"
        )
    
    index = pc.Index(index_name)

    if batch_size < 1:
        raise ValueError("batch_size must be greater than zero")

    total = len(chunks_with_embeddings)
    progress_file = progress_file or pdf_path.with_suffix(".upsert-progress.json")
    start_index = 0
    if progress_file.exists():
        progress = json.loads(progress_file.read_text())
        if (progress.get("total") == total
                and progress.get("index_name") == index_name
                and progress.get("namespace") == namespace):
            start_index = min(progress.get("next_index", 0), total)
            logger.info(
                f"Resuming Pinecone upsert: {start_index}/{total} already confirmed; "
                f"{total - start_index} pending"
            )

    logger.info(
        f"Upserting {total} embeddings into Pinecone index: {index_name}; "
        f"{start_index} confirmed, {total - start_index} pending"
    )
    for batch_start in range(start_index, total, batch_size):
        batch_end = min(batch_start + batch_size, total)
        vectors = [
            (
                f"{pdf_path.stem}_{i}",
                item["embedding"],
                {"text": item["text"]}
            )
            for i, item in enumerate(chunks_with_embeddings[batch_start:batch_end], batch_start)
        ]
        try:
            index.upsert(vectors=vectors, namespace=namespace)
        except Exception:
            logger.exception(
                f"Upsert failed for chunks {batch_start}-{batch_end - 1}; "
                f"{batch_start} confirmed, {total - batch_start} pending"
            )
            raise

        progress_file.write_text(json.dumps({
            "index_name": index_name,
            "namespace": namespace,
            "total": total,
            "next_index": batch_end
        }))
        logger.info(
            f"Upsert progress: {batch_end}/{total} confirmed, "
            f"{total - batch_end} pending"
        )

    logger.info(f"Upsert complete: {total}/{total} chunks confirmed")