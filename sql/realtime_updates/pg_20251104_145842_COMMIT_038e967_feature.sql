INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-04/COMMIT_038e967_feature.md',
    'team_documentation',
    'Deep Research Agents - Complete System Design',
    '# Deep Research Agents - Complete System Design

**Auto-Generated Documentation**

**Date:** 2025-11-04 14:58:42
**Commit:** `038e967`
**Type:** Feature
**Author:** artur

---

## 📝 Commit Message

**',
    263,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();