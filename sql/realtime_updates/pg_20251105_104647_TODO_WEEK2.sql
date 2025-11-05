INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'TODO_WEEK2.md',
    'general_documentation',
    '📋 TODO - Week 2 Priorities',
    '# 📋 TODO - Week 2 Priorities

## 🔴 HIGH PRIORITY

### 1. Database Integration (5 days)
- [ ] PostgreSQL setup script
  - [ ] Create destiny user
  - [ ] Initialize database
  - [ ] Run schema migratio',
    69,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();