from sqlalchemy import text

from database import DbSession


def get_user(auth_sub: str, db: DbSession):
    with db.begin():
        return db.execute(
            text("""
            SELECT
                u.id,
                u.email,
                u.auth_sub,
                u.created_at,
                u.updated_at
            FROM
                accounts.users u
            WHERE
                u.auth_sub = :auth_sub;
            """),
            {"auth_sub": auth_sub},
        ).mappings().fetchone()


def create_new_user(auth_sub: str, email: str, db: DbSession):
    with db.begin():
        return db.execute(
            text("""
            INSERT INTO
                accounts.users (
                    auth_sub,
                    email
                )
            VALUES (
                :auth_sub,
                :email
            )
            RETURNING
                id,
                email,
                auth_sub,
                created_at,
                updated_at;
            """),
            {
                "auth_sub": auth_sub,
                "email": email,
            },
        ).mappings().fetchone()
