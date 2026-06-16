from fastapi import APIRouter, Depends
from database import DbSession

from middleware.auth import get_current_user
from sqlalchemy import text

router = APIRouter()


@router.get("/")
def health():
    return {"healthy": True}


@router.get("/db")
def db_health(db: DbSession):
    res = db.execute(
        text(
            """
            SELECT
                1;
            """
        )
    ).scalar()
    return {"healthy": res == 1}
