INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-04/COMMIT_300ea7b_feature.md',
    'general_documentation',
    'Transparency + Cross-Team Orchestration System (Option B+C)',
    '# Transparency + Cross-Team Orchestration System (Option B+C)

**Auto-Generated Documentation**

**Date:** 2025-11-04 13:26:25
**Commit:** `300ea7b`
**Type:** Feature
**Author:** artur

---

## 📝 Comm',
    361,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();