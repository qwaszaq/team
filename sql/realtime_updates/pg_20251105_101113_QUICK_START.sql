INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'QUICK_START.md',
    'architecture',
    '🚀 QUICK START - Destiny Analytical System',
    '# 🚀 QUICK START - Destiny Analytical System

Get up and running in 5 minutes!

---

## ✅ Prerequisites

```bash
# 1. LMStudio running on 192.168.200.226:1234
#    - Model: openai/gpt-oss-20b OR gemma-',
    292,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();