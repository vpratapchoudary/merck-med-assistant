import click

from pathlib import Path
from merck_med_assistant.vectors.vectorizer import vectorize_store_pdf
from merck_med_assistant.config import VECTORIZER_CFG

@click.command()
@click.option('--input_file', type=click.Path(exists=True), required=True, help='Path to the input file to vectorize.')
def vectorize_pdf(input_file):
    """
    Command-line interface to vectorize a PDF file and store the embeddings in a Pinecone index.
    """

    pdf_path = Path(input_file)
    
    vectorize_store_pdf(
        pdf_path=pdf_path,
        index_name=VECTORIZER_CFG["index_name"],
        chunk_size=VECTORIZER_CFG["chunk_size"],
        chunk_overlap=VECTORIZER_CFG["chunk_overlap"],
        embed_model=VECTORIZER_CFG["embed_model"],
        vec_dim=VECTORIZER_CFG["vec_dim"],
        metric=VECTORIZER_CFG["metric"]
    )