TRUNCATE TABLE
    art.requests,
    art.portfolio_tags,
    art.tags,
    art.images,
    art.portfolio_settings,
    accounts.users
RESTART IDENTITY;

INSERT INTO accounts.users (id, email, auth_sub)
VALUES
    ('00000000-0000-0000-0000-000000000001', 'mickey.mouse@art-commission-platform.co.uk', 'nkusafcop3y3'),
    ('00000000-0000-0000-0000-000000000002', 'minnie.mouse@art-commission-platform.co.uk', 'seed|minnie-mouse'),
    ('00000000-0000-0000-0000-000000000003', 'donald.duck@art-commission-platform.co.uk', 'seed|donald-duck'),
    ('00000000-0000-0000-0000-000000000004', 'daisy.duck@art-commission-platform.co.uk', 'seed|daisy-duck'),
    ('00000000-0000-0000-0000-000000000005', 'goofy@art-commission-platform.co.uk', 'seed|goofy'),
    ('00000000-0000-0000-0000-000000000006', 'pluto@art-commission-platform.co.uk', 'seed|pluto'),
    ('00000000-0000-0000-0000-000000000007', 'cinderella@art-commission-platform.co.uk', 'seed|cinderella'),
    ('00000000-0000-0000-0000-000000000008', 'snow.white@art-commission-platform.co.uk', 'seed|snow-white'),
    ('00000000-0000-0000-0000-000000000009', 'peter.pan@art-commission-platform.co.uk', 'seed|peter-pan'),
    ('00000000-0000-0000-0000-000000000010', 'winnie.the.pooh@art-commission-platform.co.uk', 'seed|winnie-the-pooh');

INSERT INTO art.portfolio_settings (
    id,
    description,
    is_public,
    commission_slots,
    user_id
)
SELECT
    md5('portfolio-' || id::text)::uuid,
    'Portfolio for ' || replace(split_part(email, '@', 1), '.', ' '),
    true,
    3,
    id
FROM accounts.users;

INSERT INTO art.tags (id, name)
SELECT
    md5('tag-' || name)::uuid,
    name
FROM (
    VALUES
        ('Painting'),
        ('Portrait'),
        ('Landscape'),
        ('Illustration'),
        ('Printmaking')
) AS seed_tags(name);

INSERT INTO art.portfolio_tags (tag_id, portfolio_id)
SELECT
    md5('tag-' || assignments.tag_name)::uuid,
    portfolios.id
FROM (
    VALUES
        ('nkusafcop3y3', 'Painting'),
        ('seed|mickey-mouse', 'Portrait'),
        ('seed|minnie-mouse', 'Illustration'),
        ('seed|minnie-mouse', 'Portrait'),
        ('seed|donald-duck', 'Landscape'),
        ('seed|donald-duck', 'Painting'),
        ('seed|daisy-duck', 'Printmaking'),
        ('seed|daisy-duck', 'Illustration'),
        ('seed|goofy', 'Illustration'),
        ('seed|goofy', 'Landscape'),
        ('seed|pluto', 'Painting'),
        ('seed|pluto', 'Printmaking'),
        ('seed|cinderella', 'Portrait'),
        ('seed|cinderella', 'Painting'),
        ('seed|snow-white', 'Portrait'),
        ('seed|snow-white', 'Illustration'),
        ('seed|peter-pan', 'Landscape'),
        ('seed|peter-pan', 'Printmaking'),
        ('seed|winnie-the-pooh', 'Illustration'),
        ('seed|winnie-the-pooh', 'Painting')
) AS assignments(auth_sub, tag_name)
JOIN accounts.users AS users ON users.auth_sub = assignments.auth_sub
JOIN art.portfolio_settings AS portfolios ON portfolios.user_id = users.id;

INSERT INTO art.images (
    id,
    art_name,
    image_url,
    upload_id,
    user_id
)
SELECT
    md5('image-' || users.id::text || artwork.art_name)::uuid,
    artwork.art_name,
    'https://portfolio-images-458063641986-eu-west-2-an.s3.eu-west-2.amazonaws.com/seed-images/' || artwork.slug || '.png',
    md5('upload-' || users.id::text || artwork.art_name)::uuid,
    users.id
FROM accounts.users AS users
CROSS JOIN (
    VALUES
        ('The Starry Night', 'the-starry-night'),
        ('Mona Lisa', 'mona-lisa'),
        ('The Great Wave off Kanagawa', 'the-great-wave-off-kanagawa')
) AS artwork(art_name, slug);
