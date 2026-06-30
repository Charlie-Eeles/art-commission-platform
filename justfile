start-api:
    @uv run --directory=backend --env-file="$(pwd)/backend/.env" uvicorn app:app --reload

start-frontend:
    @cd frontend && pnpm install && pnpm dev
