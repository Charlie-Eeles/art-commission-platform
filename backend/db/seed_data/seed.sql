INSERT INTO accounts.users (id, email, auth_sub)
VALUES
    (
        '00000000-0000-0000-0000-000000000001',
        'mickey.mouse@art-commission-platform.com',
        'seed|mickey-mouse'
    ),
    (
        '00000000-0000-0000-0000-000000000002',
        'minnie.mouse@art-commission-platform.com',
        'seed|minnie-mouse'
    ),
    (
        '00000000-0000-0000-0000-000000000003',
        'donald.duck@art-commission-platform.com',
        'seed|donald-duck'
    ),
    (
        '00000000-0000-0000-0000-000000000004',
        'daisy.duck@art-commission-platform.com',
        'seed|daisy-duck'
    ),
    (
        '00000000-0000-0000-0000-000000000005',
        'goofy@art-commission-platform.com',
        'seed|goofy'
    ),
    (
        '00000000-0000-0000-0000-000000000006',
        'pluto@art-commission-platform.com',
        'seed|pluto'
    ),
    (
        '00000000-0000-0000-0000-000000000007',
        'cinderella@art-commission-platform.com',
        'seed|cinderella'
    ),
    (
        '00000000-0000-0000-0000-000000000008',
        'snow.white@art-commission-platform.com',
        'seed|snow-white'
    ),
    (
        '00000000-0000-0000-0000-000000000009',
        'peter.pan@art-commission-platform.com',
        'seed|peter-pan'
    ),
    (
        '00000000-0000-0000-0000-000000000010',
        'winnie.the.pooh@art-commission-platform.com',
        'seed|winnie-the-pooh'
    );

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
FROM accounts.users
WHERE auth_sub LIKE 'seed|%';

INSERT INTO
    art.images (
        id,
        art_name,
        image_url,
        upload_id,
        user_id
    )
SELECT
    md5('image-' || users.id::text || artwork.art_name)::uuid,
    artwork.art_name,
    'http://localhost:4566/portfolio-images/' || artwork.slug || '.png',
    md5('upload-' || users.id::text || artwork.art_name)::uuid,
    users.id
FROM
    accounts.users AS users
CROSS JOIN
    (
        VALUES
            ('The Starry Night', 'the-starry-night'),
            ('Mona Lisa', 'mona-lisa'),
            (
                'The Great Wave off Kanagawa',
                'the-great-wave-off-kanagawa'
            )
    ) AS artwork(art_name, slug)
WHERE
    users.auth_sub LIKE 'seed|%';
