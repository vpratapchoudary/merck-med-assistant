# Python base image
FROM python:3.12.1

# Set working directory
WORKDIR /app

# Disable development dependencies
ENV UV_NO_DEV=1

# Copy files and Install dependencies
RUN pip3 install uv
COPY pyproject.toml uv.lock ./
COPY src ./src
RUN uv sync --locked

# Create a non-root user and set permissions
RUN useradd -m -u 1000 user
RUN chown -R user:user /app
USER user
ENV HOME=/home/user \
	PATH=/app/.venv/bin:$PATH

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]