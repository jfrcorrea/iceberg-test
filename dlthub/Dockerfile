# Stage 1: Builder
FROM python:3.14.2-alpine AS builder

# Install build dependencies
RUN apk add --no-cache build-base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a specific directory
# We use --target to install directly into /app/deps, avoiding venv symlink issues
RUN uv export --frozen --no-dev -o requirements.txt && \
    uv pip install -r requirements.txt --target /app/deps

# Stage 2: Final
FROM python:3.14.2-alpine

WORKDIR /app

# Copy the dependencies from the builder
COPY --from=builder /app/deps /app/deps

# Copy source code
COPY . .

# Set environment variables
# add /app/deps to PYTHONPATH so python can find the installed packages
ENV PYTHONPATH="/app/deps" \
    PYTHONUNBUFFERED=1 \
    CONTINUOUS=true \
    INTERVAL_SECONDS=600

# Run the pipeline using the system python
CMD ["python", "opensky_pipeline.py"]
