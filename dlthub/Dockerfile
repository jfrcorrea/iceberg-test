# Use Python 3.14 as requested
FROM python:3.14.2-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV CONTINUOUS=true
ENV INTERVAL_SECONDS=600

# Run the pipeline
CMD ["uv", "run", "python", "opensky_pipeline.py"]
