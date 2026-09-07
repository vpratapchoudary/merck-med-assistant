# Python base image
FROM python:3.12.1

WORKDIR /app

# Disable development dependencies
ENV UV_NO_DEV=1

RUN pip3 install uv
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --locked

RUN useradd -m -u 1000 user
RUN chown -R user:user /app
USER user
ENV HOME=/home/user \
	PATH=/app/.venv/bin:$PATH

CMD ["sh", "-c", "exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000}"]