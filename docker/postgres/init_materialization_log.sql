CREATE TABLE IF NOT EXISTS materialization_log (
    id SERIAL PRIMARY KEY,
    feature_name TEXT NOT NULL,
    run_id TEXT,
    status TEXT CHECK (status IN ('success', 'failed')) DEFAULT 'success',
    materialized_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_seconds FLOAT,
    error_message TEXT
);
