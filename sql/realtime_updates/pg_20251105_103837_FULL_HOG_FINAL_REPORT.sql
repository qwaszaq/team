INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'FULL_HOG_FINAL_REPORT.md',
    'analysis',
    '🐗💨 FULL HOG MODE - FINAL REPORT',
    '# 🐗💨 FULL HOG MODE - FINAL REPORT

**Date:** 2025-11-05  
**Mission:** Complete Enterprise Analytical System  
**Status:** ✅ **MISSION ACCOMPLISHED - PRODUCTION READY**

---

## 🎯 EXECUTIVE SUMMARY

`',
    526,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();