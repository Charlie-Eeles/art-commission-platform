from uuid import UUID

from sqlalchemy import text

from database import DbSession


def create_image_qf(
    db: DbSession,
    art_name: str,
    image_url: str,
    upload_id: UUID,
    user_id: UUID,
):
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


def get_image_by_id_qf(
    db: DbSession,
    image_id: UUID,
    user_id: UUID,
):
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


def update_image_qf(
    db: DbSession,
    image_id: UUID,
    user_id: UUID,
    art_name: str,
):
    res = db.execute(
        text(
            """
            --sql
            UPDATE art.images
            SET
                art_name = :art_name,
                updated_at = NOW()
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


def delete_image_qf(
    db: DbSession,
    image_id: UUID,
    user_id: UUID,
):
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

    return res.mappings().one()


def set_portfolio_tags_qf(
    db: DbSession,
    portfolio_id: UUID,
    tag_ids: list[UUID],
):
    unique_tag_ids = list(dict.fromkeys(tag_ids))

    if unique_tag_ids:
        res = db.execute(
            text(
                """
                --sql
                SELECT id
                FROM art.tags
                WHERE id = ANY(CAST(:tag_ids AS UUID[]));
                """
            ),
            {"tag_ids": unique_tag_ids},
        )

        existing_tag_ids = set(res.scalars().all())
        missing_tag_ids = [
            tag_id
            for tag_id in unique_tag_ids
            if tag_id not in existing_tag_ids
        ]

        if missing_tag_ids:
            missing = ", ".join(str(tag_id) for tag_id in missing_tag_ids)
            raise ValueError(f"Unknown tag IDs: {missing}")

    db.execute(
        text(
            """
            --sql
            DELETE FROM art.portfolio_tags
            WHERE portfolio_id = :portfolio_id;
            """
        ),
        {"portfolio_id": portfolio_id},
    )

    if unique_tag_ids:
        db.execute(
            text(
                """
                --sql
                INSERT INTO art.portfolio_tags (
                    tag_id,
                    portfolio_id
                )
                SELECT
                    tag_id,
                    :portfolio_id
                FROM unnest(CAST(:tag_ids AS UUID[])) AS tag_id;
                """
            ),
            {
                "portfolio_id": portfolio_id,
                "tag_ids": unique_tag_ids,
            },
        )


def get_portfolio_settings_qf(
    db: DbSession,
    user_id: UUID,
):
    res = db.execute(
        text(
            """
            --sql
            SELECT
                ps.id,
                ps.description,
                ps.is_public,
                ps.commission_slots,
                ps.user_id,
                ps.created_at,
                ps.updated_at,
                COALESCE(
                    jsonb_agg(
                        jsonb_build_object(
                            'id', t.id,
                            'name', t.name,
                            'created_at', t.created_at
                        )
                        ORDER BY t.name
                    ) FILTER (WHERE t.id IS NOT NULL),
                    '[]'::jsonb
                ) AS tags
            FROM art.portfolio_settings AS ps
            LEFT JOIN art.portfolio_tags AS pt
                ON pt.portfolio_id = ps.id
            LEFT JOIN art.tags AS t
                ON t.id = pt.tag_id
            WHERE ps.user_id = :user_id
            GROUP BY
                ps.id,
                ps.description,
                ps.is_public,
                ps.commission_slots,
                ps.user_id,
                ps.created_at,
                ps.updated_at;
            """
        ),
        {"user_id": user_id},
    )

    return res.mappings().one_or_none()


def get_tags_qf(db: DbSession):
    res = db.execute(
        text(
            """
            --sql
            SELECT
                id,
                name,
                created_at
            FROM art.tags
            ORDER BY name;
            """
        ),
    )

    return res.mappings().all()
