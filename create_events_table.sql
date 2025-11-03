-- Create events table for Destiny Team Framework
-- This fixes the "relation events does not exist" error

CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    project_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    importance FLOAT NOT NULL,
    made_by VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    additional_data JSONB
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_events_project_id ON events(project_id);
CREATE INDEX IF NOT EXISTS idx_events_made_by ON events(made_by);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);

-- Verify table was created
SELECT 'events table created successfully!' as status;
SELECT COUNT(*) as current_events FROM events;
