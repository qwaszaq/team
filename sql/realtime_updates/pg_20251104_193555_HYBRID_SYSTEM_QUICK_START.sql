INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/guides/HYBRID_SYSTEM_QUICK_START.md',
    'architecture',
    '🚀 HYBRID ON-PREM SYSTEM - Quick Start Guide',
    '# 🚀 HYBRID ON-PREM SYSTEM - Quick Start Guide

**Local LLM Worker + Cloud Supervisor = Professional Intelligence**

---

## 🎯 What This System Does

**Problem:** Cloud LLMs are expensive, raise privac',
    588,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();