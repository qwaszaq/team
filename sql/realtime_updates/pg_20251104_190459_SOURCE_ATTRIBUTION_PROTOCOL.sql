INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/protocols/SOURCE_ATTRIBUTION_PROTOCOL.md',
    'protocol',
    '📚 SOURCE ATTRIBUTION PROTOCOL - Mandatory for All Investigations',
    '# 📚 SOURCE ATTRIBUTION PROTOCOL - Mandatory for All Investigations

**Status:** 🔴 MANDATORY - NO EXCEPTIONS  
**Applies to:** ALL Investigative & Research Agents  
**Standard:** Bellingcat-level sourc',
    680,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();