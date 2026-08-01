from uuid import UUID
from sqlalchemy import text

from database import DbSession


def create_image_qf(db: DbSession, art_name: str, image_url: str, upload_id: UUID, user_id: UUID):
    res = db.execute(
        text(
            """
            --sql
            INSERT INTO art.images (
                art_name,
                image_url,
                upload_id,
                user_id
            )
            VALUES (
                :art_name,
                :image_url,
                :upload_id,
                :user_id
            )
            RETURNING
                id,
                art_name,
                image_url,
                upload_id,
                user_id,
                created_at,
                updated_at;
            """
        ),
        {
            "art_name": art_name,
            "image_url": image_url,
            "upload_id": upload_id,
            "user_id": user_id,
        },
    )

    row = res.mappings().one()
    db.commit()
    return row

def get_user_images_qf(db: DbSession, user_id: UUID):
    res = db.execute(
        text(
            """
            --sql
            SELECT
                id,
                art_name,
                image_url,
                upload_id,
                user_id,
                created_at,
                updated_at
            FROM art.images
            WHERE user_id = :user_id
            ORDER BY created_at DESC;
            """
        ),
        {"user_id": user_id},
    )

    return res.mappings().all()

def get_image_by_id_qf(db: DbSession, image_id: UUID, user_id: UUID):
    res = db.execute(
        text(
            """
            --sql
            SELECT
                id,
                art_name,
                image_url,
                upload_id,
                user_id,
                created_at,
                updated_at
            FROM art.images
            WHERE id = :image_id
              AND user_id = :user_id;
            """
        ),
        {
            "image_id": image_id,
            "user_id": user_id,
        },
    )

    return res.mappings().one_or_none()

def update_image_qf(db: DbSession, image_id: UUID, user_id: UUID, art_name: str):
    res = db.execute(
        text(
            """
            --sql
            UPDATE art.images
            SET
                art_name = :art_name,
                updated_at = now()
            WHERE id = :image_id
              AND user_id = :user_id
            RETURNING
                id,
                art_name,
                image_url,
                upload_id,
                user_id,
                created_at,
                updated_at;
            """
        ),
        {
            "image_id": image_id,
            "user_id": user_id,
            "art_name": art_name,
        },
    )

    return res.mappings().one_or_none()

def delete_image_qf(db: DbSession, image_id: UUID, user_id: UUID):
    res = db.execute(
        text(
            """
            --sql
            DELETE FROM art.images
            WHERE id = :image_id
              AND user_id = :user_id
            RETURNING image_url;
            """
        ),
        {
            "image_id": image_id,
            "user_id": user_id,
        },
    )

    return res.mappings().one_or_none()

def save_portfolio_settings_qf(
    db: DbSession,
    description: str,
    is_public: bool,
    commission_slots: int,
    user_id: UUID,
):
    res = db.execute(
        text(
            """
            --sql
            INSERT INTO art.portfolio_settings (
                description,
                is_public,
                commission_slots,
                user_id
            )
            VALUES (
                :description,
                :is_public,
                :commission_slots,
                :user_id
            )
            ON CONFLICT (user_id) DO UPDATE
            SET
                description = EXCLUDED.description,
                is_public = EXCLUDED.is_public,
                commission_slots = EXCLUDED.commission_slots,
                updated_at = NOW()
            RETURNING
                id,
                description,
                is_public,
                commission_slots,
                user_id,
                created_at,
                updated_at;
            """
        ),
        {
            "description": description,
            "is_public": is_public,
            "commission_slots": commission_slots,
            "user_id": user_id,
        },
    )

    row = res.mappings().one()
    db.commit()
    return row

def get_portfolio_settings_qf(db: DbSession, user_id: UUID):
    res = db.execute(
        text(
            """
            --sql
            SELECT
                id,
                description,
                is_public,
                commission_slots,
                user_id,
                created_at,
                updated_at
            FROM art.portfolio_settings
            WHERE user_id = :user_id;
            """
        ),
        {"user_id": user_id},
    )

    return res.mappings().one_or_none()
