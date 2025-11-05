INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/team/PAWEL_DATA_ENGINEER_PROFILE.md',
    'team_documentation',
    '🔧 Paweł Kowalski - Data Engineer',
    '# 🔧 Paweł Kowalski - Data Engineer

**Date:** 2025-11-05  
**Status:** ✅ Operational  
**Team:** Destiny Team Framework (Agent #8)

---

## 🎯 Role & Specialization

**Paweł Kowalski** is the **Data En',
    378,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();