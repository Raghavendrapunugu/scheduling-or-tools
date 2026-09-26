# Stage 1: Builder
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# 1. Copy project metadata files (both lockfile and pyproject.toml are required for --frozen)
COPY pyproject.toml uv.lock README.md* ./

# 2. Sync dependencies without installing the root project package yet
RUN uv sync --frozen --no-install-project --no-cache

# 3. Copy application source code and install the root project
COPY app /app/app
RUN uv sync --frozen --no-cache

# Stage 2: Runtime Container
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv
COPY app /app/app

# Set environment path to use virtual environment binaries
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]