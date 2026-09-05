from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.vectors.embedding import load_embedding_model
from backend.utils.logs import logger

def chunk_embed_pdf(
        pdf_path: Path, 
        chunk_size: int = 500, 
        chunk_overlap: int = 200,
        embed_model: str = "all-MiniLM-L6-v2"
    ) -> list[dict]:
    """
    Chunk and embed a PDF file.

    Args:
        pdf_path (Path): Path to the PDF file.
        chunk_size (int): Size of each chunk in characters.
        chunk_overlap (int): Overlap between chunks in characters.
        embed_model (str): Name of the embedding model to use.

    Returns:
        List[dict]: A list of dictionaries containing the text chunks and their embeddings.
    """
    # Load the PDF
    logger.info(f"Loading PDF from {pdf_path}")
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    # Split the text into chunks
    logger.info(f"Splitting text into chunks of size {chunk_size} with overlap {chunk_overlap}")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    model = load_embedding_model(embed_model)

    # Embed each chunk
    logger.info(f"Embedding chunks with model: {embed_model}")
    embeddings = model.encode(chunks)

    # Create a list of dictionaries with text and embeddings
    result = [{"text": chunk, "embedding": embedding.tolist()} for chunk, embedding in zip(chunks, embeddings)]

    return result