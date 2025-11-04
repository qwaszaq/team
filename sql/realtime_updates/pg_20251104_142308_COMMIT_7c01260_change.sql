INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-04/COMMIT_7c01260_change.md',
    'architecture',
    'research: Face Recognition Open Source Software Analysis',
    '# research: Face Recognition Open Source Software Analysis

**Auto-Generated Documentation**

**Date:** 2025-11-04 14:23:08
**Commit:** `7c01260`
**Type:** Change
**Author:** artur

---

## 📝 Commit M',
    185,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();