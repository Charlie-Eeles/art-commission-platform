-- migrate:up
CREATE TYPE art.request_status AS ENUM (
    'pending',
    'in_progress',
    'rejected',
    'completed'
);

CREATE TABLE art.requests (
    id UUID PRIMARY KEY DEFAULT uuidv4() NOT NULL,
    requester_id UUID NOT NULL REFERENCES accounts.users(id) ON DELETE CASCADE,
    portfolio_id UUID NOT NULL REFERENCES art.portfolio_settings(id) ON DELETE CASCADE,
    status art.request_status NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- migrate:down
DROP TABLE art.requests;
DROP TYPE art.request_status;
