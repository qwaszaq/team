-- Database initialization for Destiny Analytical System
-- Paweł Kowalski - Data Engineer
-- 2025-11-05

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Document embeddings table
CREATE TABLE IF NOT EXISTS document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id VARCHAR(100) NOT NULL,
    document_id VARCHAR(100) NOT NULL,
    chunk_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1024),  -- Both models use 1024 dimensions
    model_used VARCHAR(100) NOT NULL,
    text_hash VARCHAR(32) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_chunk UNIQUE (document_id, chunk_id)
);

-- Create indexes
CREATE INDEX idx_embeddings_case ON document_embeddings(case_id);
CREATE INDEX idx_embeddings_document ON document_embeddings(document_id);
CREATE INDEX idx_embeddings_hash ON document_embeddings(text_hash);
CREATE INDEX idx_embeddings_vector ON document_embeddings USING ivfflat (embedding vector_cosine_ops);

-- Agent tasks table
CREATE TABLE IF NOT EXISTS agent_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id VARCHAR(100) NOT NULL,
    task_id VARCHAR(100) NOT NULL,
    agent_name VARCHAR(100) NOT NULL,
    agent_role VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    task_data JSONB,
    result_data JSONB,
    confidence_score FLOAT,
    tokens_used INTEGER,
    time_taken FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    CONSTRAINT unique_task UNIQUE (task_id)
);

CREATE INDEX idx_tasks_case ON agent_tasks(case_id);
CREATE INDEX idx_tasks_agent ON agent_tasks(agent_role);
CREATE INDEX idx_tasks_status ON agent_tasks(status);

-- Cases table
CREATE TABLE IF NOT EXISTS cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    case_type VARCHAR(100),
    status VARCHAR(20) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_cases_id ON cases(case_id);
CREATE INDEX idx_cases_status ON cases(status);

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id VARCHAR(100) NOT NULL,
    document_id VARCHAR(100) UNIQUE NOT NULL,
    filename VARCHAR(500) NOT NULL,
    document_type VARCHAR(100),
    file_size INTEGER,
    content TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_documents_case ON documents(case_id);
CREATE INDEX idx_documents_type ON documents(document_type);

-- Quality reviews table (for Claude supervision)
CREATE TABLE IF NOT EXISTS quality_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id VARCHAR(100) NOT NULL,
    reviewer VARCHAR(100) NOT NULL,  -- 'claude' or 'manual'
    grade VARCHAR(10),
    quality_score FLOAT,
    strengths TEXT[],
    gaps TEXT[],
    suggestions TEXT[],
    approved BOOLEAN,
    review_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reviews_task ON quality_reviews(task_id);
CREATE INDEX idx_reviews_grade ON quality_reviews(grade);

-- Performance metrics table
CREATE TABLE IF NOT EXISTS performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_type VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    metadata JSONB,
    recorded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_metrics_type ON performance_metrics(metric_type);
CREATE INDEX idx_metrics_time ON performance_metrics(recorded_at);

-- Insert initial test data
INSERT INTO cases (case_id, title, description, case_type, status) VALUES
('case_001', 'Test Case - Financial Analysis', 'Initial test case for system validation', 'financial', 'active');

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO destiny;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO destiny;
