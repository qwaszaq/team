INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'README.md',
    'architecture',
    '🚀 Destiny Analytical System - Hybrid Multi-Agent Platform',
    '# 🚀 Destiny Analytical System - Hybrid Multi-Agent Platform

**Enterprise-grade analytical system combining local LLM (privacy) with Claude supervision (quality)**

---

## 🎯 Overview

Hybrid multi-ag',
    282,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();