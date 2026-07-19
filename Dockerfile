FROM python:3.14

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --in-project

COPY . /app
ENV SERVICE_PATH="shufersal_stores_collector"
CMD ["sh", "-c", "python3 -m src.services.${SERVICE_PATH}"]
