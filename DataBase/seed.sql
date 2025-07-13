-- Insert admin user
INSERT INTO users (
    id, first_name, last_name, email, password, is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LCF7rrsOa3KAd2dQQv0rROAsgAHrMpxDRU4uxqgLTHAxltNj4cz7y', -- hashed "admin1234"
    TRUE
);

-- Insert initial amenities
INSERT INTO amenities (id, name) VALUES
    ('a1a11111-1111-1111-1111-111111111111', 'WiFi'),
    ('b2b22222-2222-2222-2222-222222222222', 'Swimming Pool'),
    ('c3c33333-3333-3333-3333-333333333333', 'Air Conditioning');
