INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/kickoff/IMPLEMENTATION_KICKOFF.md',
    'architecture',
    '🚀 KICK-OFF IMPLEMENTACJI - HYBRID ANALYTICAL SYSTEM',
    '# 🚀 KICK-OFF IMPLEMENTACJI - HYBRID ANALYTICAL SYSTEM

**Data:** 2025-11-05  
**Status:** IMPLEMENTATION STARTED  
**Koordynator:** Aleksander Nowak

---

## 🎯 MISJA

Zbudować w 3 tygodnie hybrydowy s',
    194,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();