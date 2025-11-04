INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/status/COMPLETE_AUTOMATION_SUMMARY_20251104.md',
    'status_report',
    '✅ COMPLETE AUTOMATION SUMMARY - 2025-11-04',
    '# ✅ COMPLETE AUTOMATION SUMMARY - 2025-11-04

**Status:** OBOWIĄZKOWA AUTOMATYZACJA ZAIMPLEMENTOWANA  
**Helena:** Automatycznie propaguje do wszystkich baz danych

---

## 🎉 CO ZOSTAŁO OSIĄGNIĘTE

##',
    182,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();