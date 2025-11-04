INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-04/COMMIT_5e8b9d8_feature.md',
    'architecture',
    'Automatic documentation generation for ALL code changes',
    '# Automatic documentation generation for ALL code changes

**Auto-Generated Documentation**

**Date:** 2025-11-04 12:44:44
**Commit:** `5e8b9d8`
**Type:** Feature
**Author:** artur

---

## 📝 Commit M',
    163,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();