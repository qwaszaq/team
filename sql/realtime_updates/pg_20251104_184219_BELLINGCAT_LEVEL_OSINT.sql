INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/concepts/BELLINGCAT_LEVEL_OSINT.md',
    'architecture',
    '🔍 Bellingcat-Level OSINT System - Investigative Journalism & Intelligence',
    '# 🔍 Bellingcat-Level OSINT System - Investigative Journalism & Intelligence

**Inspired by:** Bellingcat, The Insider, ProPublica investigative methodologies  
**Prepared by:** Aleksander Nowak (Orche',
    1243,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();