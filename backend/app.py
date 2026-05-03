from os import environ

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from urls import router


def create_app() -> FastAPI:
    app = FastAPI()

    app.state.secret_key = environ["SECRET_KEY"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app


app = create_app()
