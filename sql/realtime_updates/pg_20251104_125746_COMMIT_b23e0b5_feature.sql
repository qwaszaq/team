INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-04/COMMIT_b23e0b5_feature.md',
    'general_documentation',
    'Add demo feature for live demonstration',
    '# Add demo feature for live demonstration

**Auto-Generated Documentation**

**Date:** 2025-11-04 12:57:45
**Commit:** `b23e0b5`
**Type:** Feature
**Author:** artur

---

## 📝 Commit Message

**feat: ',
    57,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();