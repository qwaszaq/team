INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'README.md',
    'protocol',
    '🤖 Destiny Team Framework - Helena Auto-Execution System',
    '# 🤖 Destiny Team Framework - Helena Auto-Execution System

**Multi-Agent AI Development Framework with Unlimited Context Memory**

A complete AI software development team that automatically propagates',
    473,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();