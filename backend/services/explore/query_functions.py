from uuid import UUID

from sqlalchemy import text

from database import DbSession


def get_public_portfolios_qf(
    db: DbSession,
    page: int = 1,
    page_size: int = 20,
    tags: list[str] | None = None,
):
    offset = (page - 1) * page_size

    res = db.execute(
        text(
            """
            --sql
            SELECT
                settings.id,
                settings.user_id,
                settings.description,
                settings.commission_slots,
                settings.created_at,
                settings.updated_at,
                COUNT(*) OVER () AS total_count,
                COALESCE(
                    (
                        SELECT JSONB_AGG(
                            TO_JSONB(image)
                            ORDER BY image.created_at DESC
                        )
                        FROM art.images AS image
                        WHERE image.user_id = settings.user_id
                    ),
                    '[]'::JSONB
                ) AS images,
                COALESCE(
                    (
                        SELECT JSONB_AGG(
                            JSONB_BUILD_OBJECT(
                                'id', tag.id,
                                'name', tag.name,
                                'created_at', tag.created_at
                            )
                            ORDER BY tag.name
                        )
                        FROM art.portfolio_tags AS portfolio_tag
                        JOIN art.tags AS tag
                            ON tag.id = portfolio_tag.tag_id
                        WHERE portfolio_tag.portfolio_id = settings.id
                    ),
                    '[]'::JSONB
                ) AS tags
            FROM art.portfolio_settings AS settings
            WHERE settings.is_public = TRUE
            AND (
                CAST(:tags AS TEXT[]) IS NULL
                OR EXISTS (
                    SELECT 1
                    FROM art.portfolio_tags AS portfolio_tag
                    JOIN art.tags AS tag
                        ON tag.id = portfolio_tag.tag_id
                    WHERE portfolio_tag.portfolio_id = settings.id
                        AND tag.name = ANY(CAST(:tags AS TEXT[]))
                )
            )
            ORDER BY settings.updated_at DESC
            LIMIT :page_size
            OFFSET :offset;
            """
        ),
        {
            "page_size": page_size,
            "offset": offset,
            "tags": tags or None,
        },
    )

    rows = res.mappings().all()
    total = rows[0]["total_count"] if rows else 0

    return {
        "items": rows,
        "page": page,
        "page_size": page_size,
        "total": total,
        "has_next": offset + len(rows) < total,
    }


def get_public_portfolio_by_id_qf(
    db: DbSession,
    portfolio_id: UUID,
):
    res = db.execute(
        text(
            """
            --sql
            SELECT
                settings.id,
                settings.user_id,
                settings.description,
                settings.commission_slots,
                settings.created_at,
                settings.updated_at,
                COALESCE(
                    (
                        SELECT JSONB_AGG(
                            TO_JSONB(image)
                            ORDER BY image.created_at DESC
                        )
                        FROM art.images AS image
                        WHERE image.user_id = settings.user_id
                    ),
                    '[]'::JSONB
                ) AS images,
                COALESCE(
                    (
                        SELECT JSONB_AGG(
                            JSONB_BUILD_OBJECT(
                                'id', tag.id,
                                'name', tag.name,
                                'created_at', tag.created_at
                            )
                            ORDER BY tag.name
                        )
                        FROM art.portfolio_tags AS portfolio_tag
                        JOIN art.tags AS tag
                            ON tag.id = portfolio_tag.tag_id
                        WHERE portfolio_tag.portfolio_id = settings.id
                    ),
                    '[]'::JSONB
                ) AS tags
            FROM art.portfolio_settings AS settings
            WHERE settings.id = :portfolio_id
                AND settings.is_public = TRUE;
            """
        ),
        {"portfolio_id": portfolio_id},
    )

    return res.mappings().one_or_none()
