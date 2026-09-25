# Stage 1: Build virtualenv using uv
FROM python:3.11-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY pyproject.toml .
RUN uv sync --frozen --no-cache

# Stage 2: Runtime Container
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY app /app/app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]