INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'GETTING_STARTED.md',
    'team_documentation',
    '🚀 GETTING STARTED - Destiny Analytical System',
    '# 🚀 GETTING STARTED - Destiny Analytical System

**Quick guide to get up and running in 5 minutes!**

---

## ⚡ FASTEST START (Recommended)

```bash
# 1. Run automated setup
./setup.sh

# 2. Add your ',
    357,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();