INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/research/RESEARCH_DELIVERY_SUMMARY.md',
    'status_report',
    '📦 Research Delivery Summary',
    '# 📦 Research Delivery Summary

**Task ID:** RESEARCH-FACE-REC-001  
**Date:** 2025-11-04  
**Delivered By:** Analytical Team (Viktor Kovalenko)  
**Delivered To:** User (Artur)

---

## ✅ Mission Comp',
    239,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();