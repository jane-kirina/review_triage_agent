-- Database review_triage_agent

CREATE TABLE apps (
    app_id TEXT PRIMARY KEY,
    app_name TEXT NOT NULL,
    description TEXT,
    score NUMERIC,
    ratings_count INTEGER,
    downloads BIGINT,
    content_rating TEXT,
    section TEXT,
    categories TEXT
);


CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    app_id TEXT REFERENCES apps(app_id),
    review_text TEXT NOT NULL,
    review_score INTEGER,
    review_date TIMESTAMP,
    helpful_count INTEGER,
    review_hash TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE triage_runs (
    id SERIAL PRIMARY KEY,
    app_id TEXT REFERENCES apps(app_id),
    sample_size INTEGER,
    model_name TEXT,
    status TEXT DEFAULT 'running',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP
);

CREATE TABLE review_triage_run_results (
    id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES triage_runs(id),
    review_id INTEGER REFERENCES reviews(id),

    category TEXT NOT NULL,
    sentiment TEXT,
    severity TEXT,
    topic TEXT,
    summary TEXT,
    suggested_action TEXT,
    confidence NUMERIC,

    raw_llm_output JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);