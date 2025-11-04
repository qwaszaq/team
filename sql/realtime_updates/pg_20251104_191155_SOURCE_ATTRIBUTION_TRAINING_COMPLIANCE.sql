INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/team/SOURCE_ATTRIBUTION_TRAINING_COMPLIANCE.md',
    'team_documentation',
    '✅ SOURCE ATTRIBUTION PROTOCOL - Training Compliance Record',
    '# ✅ SOURCE ATTRIBUTION PROTOCOL - Training Compliance Record

**Document Type:** Compliance Certification  
**Date:** 2025-11-04  
**Protocol:** SOURCE ATTRIBUTION PROTOCOL (Mandatory)  
**Status:** ✅',
    577,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();