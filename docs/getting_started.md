# Getting Started

## Frontend
The frontend is a Nuxt app using pnpm as its package manager.

Follow these steps to run the frontend locally:
- Create a `.env` file at `./frontend/.env` and populate it with the following properties (None of these values are sensitive):

```env
# API
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000

# LogTo (Auth)
NUXT_PUBLIC_LOGTO_ENDPOINT="https://bph6vd.logto.app/"
NUXT_PUBLIC_LOGTO_APP_ID="l36zyeqf0hgj7bctcpm4j"
NUXT_PUBLIC_LOGTO_API_RESOURCE=https://api.art-commission-platform.com
```

- Navigate to the frontend dir at `./frontend`
- Run `pnpm install` to sync dependencies
- Run `pnpm run dev` to start a development server on `http://localhost:3000`


## Backend
The backend is a Fastapi app using a Postgres database.

Follow these steps to run the backend locally:
- Create a `.env` file at `./backend/.env` and populate it with the following properties (None of these are sensitive):

```env
# Fastapi
SECRET_KEY={{ generate a Fastapi secret key }}

# Database
POSTGRES_USER=local
POSTGRES_PASSWORD=password
POSTGRES_DB=art_commission_platform
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
DATABASE_URL="postgresql://local:password@localhost:5432/art_commission_platform?sslmode=disable"

# AWS
S3_BUCKET=portfolio-images
S3_ENDPOINT_URL=http://localhost:4566
S3_PUBLIC_BASE_URL=http://localhost:4566/portfolio-images
AWS_DEFAULT_REGION=eu-west-2
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test

# LogTo
LOGTO_ENDPOINT=https://bph6vd.logto.app
LOGTO_API_RESOURCE=https://api.art-commission-platform.com
```

- Start the database with docker `docker compose up -d`
- Navigate to `./backend`
- Run migrations with `dbmate --url='postgres://local:password@localhost:5432/art_commission_platform?sslmode=disable' migrate`
- Run `uv run --env-file .env uvicorn app:app --reload` to start a development server on `http://127.0.0.1:8000`
