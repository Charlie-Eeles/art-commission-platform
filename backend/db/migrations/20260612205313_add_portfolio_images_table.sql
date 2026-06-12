-- migrate:up
CREATE SCHEMA IF NOT EXISTS art;

CREATE TABLE art.images (
    id uuid PRIMARY KEY DEFAULT uuidv4() NOT NULL,
    art_name TEXT NOT NULL,
    image_url TEXT NOT NULL,
    upload_id UUID NOT NULL,
    user_id UUID NOT NULL REFERENCES accounts.users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- migrate:down
DROP TABLE art.images;

DROP SCHEMA art;
