# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Install system dependencies for psycopg2 and other tools
RUN apt-get update && apt-get install -y --no-install-recommends 
    build-essential 
    libpq-dev 
    curl 
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a multi-stage build
ENV UV_LINK_MODE=copy

# Install the project's dependencies
# Use --no-dev to exclude development dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application
COPY src ./src
COPY .env.example .env

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
