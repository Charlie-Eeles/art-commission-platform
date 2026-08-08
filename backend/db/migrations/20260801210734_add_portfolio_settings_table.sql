-- migrate:up
CREATE TABLE art.portfolio_settings (
    id uuid PRIMARY KEY DEFAULT uuidv4() NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL,
    commission_slots SMALLINT NOT NULL,
    user_id UUID NOT NULL UNIQUE REFERENCES accounts.users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- migrate:down
DROP TABLE art.portfolio_settings;
