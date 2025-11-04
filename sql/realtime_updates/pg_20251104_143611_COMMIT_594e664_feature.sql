INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-04/COMMIT_594e664_feature.md',
    'architecture',
    'Cross-Team Review - face_recognition Library Deep Dive',
    '# Cross-Team Review - face_recognition Library Deep Dive

**Auto-Generated Documentation**

**Date:** 2025-11-04 14:36:10
**Commit:** `594e664`
**Type:** Feature
**Author:** artur

---

## 📝 Commit Me',
    222,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();