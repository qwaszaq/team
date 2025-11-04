INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/guides/TROUBLESHOOTING.md',
    'general_documentation',
    '🔧 Troubleshooting Guide - Helena Auto-Execution System',
    '# 🔧 Troubleshooting Guide - Helena Auto-Execution System

**Common issues and their solutions**

---

## 📋 Table of Contents

1. [Watcher Issues](#watcher-issues)
2. [Qdrant Issues](#qdrant-issues)
3.',
    641,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();