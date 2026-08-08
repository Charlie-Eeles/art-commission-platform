-- migrate:up
CREATE TABLE art.tags (
    id uuid PRIMARY KEY DEFAULT uuidv4() NOT NULL,
    name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO art.tags (name)
VALUES
    ('Anime'),
    ('Cartoon'),
    ('Realism'),
    ('Semi-Realism'),
    ('Pixel Art'),
    ('Chibi'),
    ('Watercolor'),
    ('Digital Painting'),
    ('Comic Book'),
    ('Line Art');

CREATE TABLE art.portfolio_tags (
    tag_id UUID NOT NULL REFERENCES art.tags(id) ON DELETE CASCADE,
    portfolio_id UUID NOT NULL REFERENCES art.portfolio_settings(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tag_id, portfolio_id)
);

-- migrate:down
DROP TABLE art.portfolio_tags;
DROP TABLE art.tags;
