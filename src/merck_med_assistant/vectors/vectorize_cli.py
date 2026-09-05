import click

from pathlib import Path
from merck_med_assistant.vectors.vectorizer import vectorize_store_pdf
from merck_med_assistant.config import VECTORIZER_CFG, PINECONE_CFG
from merck_med_assistant.utils.logs import logger

@click.command()
@click.option('--input-file', type=click.Path(exists=True), required=True, help='Path to the input file to vectorize.')
@click.option('--batch-size', type=click.IntRange(min=1), default=100, show_default=True,
              help='Number of vectors sent in each Pinecone upsert request.')
@click.option('--progress-file', type=click.Path(path_type=Path), default=None,
              help='JSON file used to resume confirmed upsert batches.')
def vectorize_pdf(input_file, batch_size, progress_file):
    """
    Command-line interface to vectorize a PDF file and store the embeddings in a Pinecone index.
    """

    logger.info(f"Starting vectorization for file: {input_file}")
    pdf_path = Path(input_file)
    
    vectorize_store_pdf(
        pdf_path=pdf_path,
        index_name=PINECONE_CFG["index_name"],
        namespace=PINECONE_CFG["namespace"],
        chunk_size=VECTORIZER_CFG["chunk_size"],
        chunk_overlap=VECTORIZER_CFG["chunk_overlap"],
        embed_model=VECTORIZER_CFG["embed_model"],
        vec_dim=VECTORIZER_CFG["vec_dim"],
        metric=VECTORIZER_CFG["metric"],
        pinecone_cloud=PINECONE_CFG["cloud"],
        pinecone_region=PINECONE_CFG["region"],
        batch_size=batch_size,
        progress_file=progress_file
    )