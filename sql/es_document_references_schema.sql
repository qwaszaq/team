-- Elasticsearch Document References Schema
-- Lightweight reference table instead of full document replication

-- 1. Document Reference Table
-- Purpose: Track ES documents without duplicating content
CREATE TABLE IF NOT EXISTS es_document_references (
    id SERIAL PRIMARY KEY,
    es_index TEXT NOT NULL,
    es_doc_id TEXT NOT NULL UNIQUE,
    doc_type TEXT,
    issuer TEXT,
    report_url TEXT,
    filename TEXT,
    file_size BIGINT,
    sha256 TEXT,
    indexed_at TIMESTAMP DEFAULT NOW(),
    data_classification TEXT DEFAULT 'public',
    investigation_id TEXT,
    tags TEXT[],
    metadata JSONB,
    CONSTRAINT valid_classification CHECK (data_classification IN ('public', 'confidential', 'internal', 'restricted'))
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_es_doc_refs_index ON es_document_references(es_index);
CREATE INDEX IF NOT EXISTS idx_es_doc_refs_investigation ON es_document_references(investigation_id);
CREATE INDEX IF NOT EXISTS idx_es_doc_refs_issuer ON es_document_references(issuer);
CREATE INDEX IF NOT EXISTS idx_es_doc_refs_tags ON es_document_references USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_es_doc_refs_metadata ON es_document_references USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_es_doc_refs_indexed_at ON es_document_references(indexed_at DESC);

-- 2. Document Usage Log (Audit Trail)
-- Purpose: Track access for GDPR compliance
CREATE TABLE IF NOT EXISTS es_document_usage_log (
    id SERIAL PRIMARY KEY,
    es_doc_id TEXT NOT NULL,
    accessed_by TEXT NOT NULL,
    access_timestamp TIMESTAMP DEFAULT NOW(),
    query_used TEXT,
    access_purpose TEXT,
    session_id TEXT,
    results_count INTEGER,
    response_time_ms FLOAT,
    FOREIGN KEY (es_doc_id) REFERENCES es_document_references(es_doc_id) ON DELETE CASCADE
);

-- Indexes for audit queries
CREATE INDEX IF NOT EXISTS idx_usage_log_doc ON es_document_usage_log(es_doc_id);
CREATE INDEX IF NOT EXISTS idx_usage_log_user ON es_document_usage_log(accessed_by);
CREATE INDEX IF NOT EXISTS idx_usage_log_timestamp ON es_document_usage_log(access_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_usage_log_purpose ON es_document_usage_log(access_purpose);

-- 3. Document Access Stats (Materialized View)
-- Purpose: Quick stats for monitoring
CREATE MATERIALIZED VIEW IF NOT EXISTS es_document_access_stats AS
SELECT 
    r.es_doc_id,
    r.issuer,
    r.investigation_id,
    COUNT(l.id) as total_accesses,
    COUNT(DISTINCT l.accessed_by) as unique_users,
    MAX(l.access_timestamp) as last_accessed,
    AVG(l.response_time_ms) as avg_response_time_ms
FROM es_document_references r
LEFT JOIN es_document_usage_log l ON r.es_doc_id = l.es_doc_id
GROUP BY r.es_doc_id, r.issuer, r.investigation_id;

CREATE UNIQUE INDEX IF NOT EXISTS idx_doc_stats_doc_id ON es_document_access_stats(es_doc_id);

-- Refresh function for stats
CREATE OR REPLACE FUNCTION refresh_document_stats()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY es_document_access_stats;
END;
$$ LANGUAGE plpgsql;

-- 4. Helper Functions

-- Get available sources for an investigation
CREATE OR REPLACE FUNCTION get_investigation_sources(p_investigation_id TEXT)
RETURNS TABLE(
    issuer TEXT,
    doc_count BIGINT,
    total_size BIGINT,
    all_tags TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.issuer,
        COUNT(*) as doc_count,
        SUM(r.file_size) as total_size,
        ARRAY_AGG(DISTINCT tag) as all_tags
    FROM es_document_references r,
         UNNEST(r.tags) as tag
    WHERE r.investigation_id = p_investigation_id
    GROUP BY r.issuer;
END;
$$ LANGUAGE plpgsql;

-- Get recent document access by agent
CREATE OR REPLACE FUNCTION get_agent_recent_access(
    p_agent_name TEXT,
    p_days INTEGER DEFAULT 7
)
RETURNS TABLE(
    es_doc_id TEXT,
    filename TEXT,
    issuer TEXT,
    access_count BIGINT,
    last_access TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.es_doc_id,
        r.filename,
        r.issuer,
        COUNT(l.id) as access_count,
        MAX(l.access_timestamp) as last_access
    FROM es_document_references r
    JOIN es_document_usage_log l ON r.es_doc_id = l.es_doc_id
    WHERE l.accessed_by = p_agent_name
      AND l.access_timestamp >= NOW() - (p_days || ' days')::INTERVAL
    GROUP BY r.es_doc_id, r.filename, r.issuer
    ORDER BY last_access DESC;
END;
$$ LANGUAGE plpgsql;

-- Audit trail query
CREATE OR REPLACE FUNCTION get_document_audit_trail(
    p_es_doc_id TEXT,
    p_days INTEGER DEFAULT 90
)
RETURNS TABLE(
    accessed_by TEXT,
    access_timestamp TIMESTAMP,
    query_used TEXT,
    access_purpose TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        l.accessed_by,
        l.access_timestamp,
        l.query_used,
        l.access_purpose
    FROM es_document_usage_log l
    WHERE l.es_doc_id = p_es_doc_id
      AND l.access_timestamp >= NOW() - (p_days || ' days')::INTERVAL
    ORDER BY l.access_timestamp DESC;
END;
$$ LANGUAGE plpgsql;

-- Comments for documentation
COMMENT ON TABLE es_document_references IS 'Lightweight references to Elasticsearch documents (no content duplication)';
COMMENT ON TABLE es_document_usage_log IS 'Audit trail for GDPR compliance - tracks document access';
COMMENT ON MATERIALIZED VIEW es_document_access_stats IS 'Aggregated access statistics per document';
COMMENT ON FUNCTION get_investigation_sources IS 'Get summary of available sources for an investigation';
COMMENT ON FUNCTION get_agent_recent_access IS 'Get documents recently accessed by an agent';
COMMENT ON FUNCTION get_document_audit_trail IS 'Get full audit trail for a specific document';
