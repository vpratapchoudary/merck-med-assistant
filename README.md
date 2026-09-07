# Merck Medical Assistant

A medical knowledge assistant built with FastAPI, Chainlit, LangChain, Pinecone, and Groq. The app loads medical PDFs into a vector store, retrieves relevant context for user questions, and answers using a Groq-hosted LLM with tool calling.

## Overview

This project provides a lightweight RAG (retrieval-augmented generation) workflow for medical reference material. It is designed to:

- ingest PDF documents into a vector database
- embed text using a sentence transformer model
- retrieve highly relevant chunks at query time
- answer questions with grounded context from indexed content
- expose both a browser UI and an API

## Architecture

The application is organized into a few main layers:

- API layer: FastAPI app in `app/src/backend/main.py`
- UI layer: Chainlit chatbot in `app/src/ui/chatbot.py`
- Retrieval layer: vector search and embedding logic under `app/src/backend/vectors/`
- LLM orchestration: Groq + tool calling in `app/src/backend/execution/`
- Service layer: session memory and chat orchestration in `app/src/backend/services/`

## Tech Stack

- Python 3.12
- FastAPI
- Chainlit
- LangChain Core / LangChain Groq
- SentenceTransformers
- Pinecone vector database
- pypdf for PDF extraction
- uv for dependency and environment management

## Project Structure

```text
merck-med-assistant/
├── app/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── src/
│       ├── backend/
│       │   ├── api/
│       │   ├── execution/
│       │   ├── services/
│       │   ├── utils/
│       │   ├── vectors/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── main.py
│       └── ui/
│           └── chatbot.py
└── README.md
```

## Configuration

Core configuration is in `app/src/backend/config.py`.

Important defaults include:

- embedding model: `all-MiniLM-L6-v2`
- chunk size: `500`
- chunk overlap: `200`
- Pinecone cloud: `aws`
- Pinecone region: `us-east-1`
- Pinecone index: `med-assistant-index`
- namespace: `merck-manual`
- Groq model: `qwen/qwen3.8-27b`

## Requirements

Before running the app, set the following environment variables:

- `PINECONE_API_KEY`
- `HF_TOKEN` for Hugging Face model downloads
- `GROQ_API_KEY` for the Groq model client

Example:

```bash
export PINECONE_API_KEY="your_pinecone_key"
export HF_TOKEN="your_huggingface_token"
export GROQ_API_KEY="your_groq_key"
```

## Local Setup

From the project root:

```bash
cd app
uv sync
```

This installs the dependencies defined in `app/pyproject.toml`.

## Run the Application

Start the FastAPI service:

```bash
cd app
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

The app mounts the Chainlit interface at:

- http://localhost:8000/ui

The FastAPI API also exposes:

- GET `/health`
- POST `/chat`

## Populate the Vector Store

Use the built-in CLI to chunk and ingest a PDF into Pinecone:

```bash
cd app
uv run vectorize-pdf --input-file /path/to/your/document.pdf --batch-size 100 --progress-file /path/to/progress.json
```

This command:

1. reads the PDF
2. splits it into chunks
3. embeds each chunk
4. creates the Pinecone index if needed
5. upserts vectors into the configured namespace

## How the Assistant Works

The runtime flow is:

1. a user asks a question in the UI or API
2. the query is embedded with the configured sentence-transformer model
3. Pinecone retrieves the closest matching chunks
4. the Groq model receives the user message plus retrieved context
5. the model produces a grounded answer with relevant supporting material

## Docker

A Docker image is included in `app/Dockerfile`.

Build:

```bash
docker build -t merck-med-assistant ./app
```

Run:

```bash
docker run -p 10000:10000 -e PINECONE_API_KEY="..." -e HF_TOKEN="..." -e GROQ_API_KEY="..." merck-med-assistant
```

## Notes

- The app expects a prebuilt or newly created Pinecone index before it is queried.
- Retrieval quality depends on the PDF content, chunk size, and vector index configuration.
- The app currently uses a single configured namespace and index name, which can be updated in `app/src/backend/config.py`.
- The Chainlit UI is mounted under `/ui`, while the API remains available at the standard FastAPI routes.

## Development Notes

If you want to customize behavior, the most relevant files are:

- `app/src/backend/config.py` for model and vector settings
- `app/src/backend/execution/tools.py` for Pinecone retrieval tool logic
- `app/src/backend/execution/agent.py` for Groq tool-calling orchestration
- `app/src/backend/vectors/vectorizer.py` for PDF ingestion into Pinecone
- `app/src/ui/chatbot.py` for the browser chat interface

## License

This project is currently provided as a local application template and has no explicit license file yet.
