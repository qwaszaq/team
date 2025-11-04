INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/orchestration/QUICK_START.md',
    'general_documentation',
    '🚀 Quick Start: Transparency System',
    '# 🚀 Quick Start: Transparency System

**5-minute guide to using the new orchestration tools**

---

## ⚡ Instant Demo

```bash
cd /Users/artur/coursor-agents-destiny-folder/orchestration
python3 test_',
    235,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();