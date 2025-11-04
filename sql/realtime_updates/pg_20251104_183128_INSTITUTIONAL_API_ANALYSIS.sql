INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/capabilities/INSTITUTIONAL_API_ANALYSIS.md',
    'analysis',
    '🌐 Institutional API Analysis Capability',
    '# 🌐 Institutional API Analysis Capability

**Date:** 2025-11-04  
**Status:** ✅ VERIFIED IN PRODUCTION  
**Evidence:** Sejm API Analysis (197 meetings analyzed)  

---

## 🎯 Overview

Agenci Destiny T',
    287,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();