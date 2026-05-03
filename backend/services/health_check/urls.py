from fastapi import APIRouter
from database import DbSession

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
