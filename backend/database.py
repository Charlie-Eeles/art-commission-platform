from os import environ
from typing import Annotated, TypeAlias

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session, sessionmaker

sqlalchemy_uri = URL.create(
    "postgresql+psycopg",
    host=environ["POSTGRES_HOST"],
    port=environ["POSTGRES_PORT"],
    database=environ["POSTGRES_DB"],
    username=environ["POSTGRES_USER"],
    password=environ["POSTGRES_PASSWORD"],
    query={"sslmode": "prefer"},
)

engine = create_engine(
    sqlalchemy_uri,
    pool_pre_ping=True,
    pool_recycle=150,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db():
    with SessionLocal() as session:
        yield session


DbSession: TypeAlias = Annotated[Session, Depends(get_db)]
