INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-04/COMMIT_388327f_feature.md',
    'architecture',
    'Sejm API Analysis System - Real Data from Parliament',
    '# Sejm API Analysis System - Real Data from Parliament

**Auto-Generated Documentation**

**Date:** 2025-11-04 15:11:16
**Commit:** `388327f`
**Type:** Feature
**Author:** artur

---

## 📝 Commit Mess',
    224,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();