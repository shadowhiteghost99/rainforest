FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY pyproject.toml .
COPY . /app
#ARG SERVICE_PATH="shufersal_stores_collector"
#CMD ["python3", "-m", "src.services.${SERVICE_PATH}"]
