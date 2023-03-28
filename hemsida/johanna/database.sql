CREATE TABLE saved_data (
    id TEXT PRIMARY KEY CHECK (id SIMILAR TO '[0-9]{10}'),
    velocity FLOAT,
    accuracy FLOAT
);