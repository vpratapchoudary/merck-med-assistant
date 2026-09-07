# Python base image
FROM python:3.12.1

# Set the working directory inside the container to /app
WORKDIR /app

# Copy all files from the current directory on the host to the container's /app directory
COPY . .

# Disable development dependencies
ENV UV_NO_DEV=1

# Install Python dependencies
RUN pip3 install uv
RUN uv sync --locked

# Create a non-root user and switch to that user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

# Define the command to run the app
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0"]