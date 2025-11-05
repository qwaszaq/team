INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/plans/ROLE_BASED_IMPLEMENTATION_PLAN.md',
    'team_documentation',
    '📋 PLAN IMPLEMENTACJI - PODZIAŁ NA ROLE',
    '# 📋 PLAN IMPLEMENTACJI - PODZIAŁ NA ROLE

**Data:** 2025-11-05  
**Koordynator:** Aleksander Nowak  
**Cel:** Jasny podział zadań dla systemu multiagentowego

---

## 🎯 OVERVIEW - 3 TYGODNIE DO MVP

`',
    439,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();