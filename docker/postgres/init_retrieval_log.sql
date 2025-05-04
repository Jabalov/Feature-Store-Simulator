CREATE TABLE IF NOT EXISTS retrieval_log (
    id SERIAL PRIMARY KEY,
    source TEXT,
    entity_id TEXT,
    feature_name TEXT,
    retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    freshness_seconds FLOAT
);
