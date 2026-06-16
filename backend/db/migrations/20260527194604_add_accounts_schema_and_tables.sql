-- migrate:up
CREATE SCHEMA IF NOT EXISTS accounts;

CREATE TABLE accounts.users (
    id uuid PRIMARY KEY DEFAULT uuidv4() NOT NULL,
    email text NOT NULL,
    auth_sub text NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- migrate:down
DROP TABLE accounts.users;

DROP SCHEMA accounts;
