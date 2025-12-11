FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

# Копируем проект
COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

RUN chmod +x /app/scripts/entrypoint.sh
CMD ["sh", "/app/scripts/entrypoint.sh"]
