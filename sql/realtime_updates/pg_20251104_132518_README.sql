INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'orchestration/README.md',
    'general_documentation',
    '🎯 Orchestration System',
    '# 🎯 Orchestration System

**Complete transparency and coordination tools for Destiny Team**

---

## What''s This?

Tools that help YOU (as orchestrator) coordinate Core Team + Analytical Team effectiv',
    90,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();