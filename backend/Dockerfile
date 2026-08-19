FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /uvx /bin/

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY . .
RUN uv sync --locked --no-dev

CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8000", "--proxy-headers", "--forwarded-allow-ips=*"]
