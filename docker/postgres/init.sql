CREATE TABLE IF NOT EXISTS feature_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    owner VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS features (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    feature_group_id INTEGER REFERENCES feature_groups(id),
    data_type VARCHAR(100) NOT NULL,
    description TEXT,
    transformation TEXT,
    source_table VARCHAR(255),
    version INTEGER DEFAULT 1,
    ttl_days INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feature_lineage (
    id SERIAL PRIMARY KEY,
    feature_id INTEGER REFERENCES features(id),
    upstream_table VARCHAR(255),
    upstream_column VARCHAR(255)
);
