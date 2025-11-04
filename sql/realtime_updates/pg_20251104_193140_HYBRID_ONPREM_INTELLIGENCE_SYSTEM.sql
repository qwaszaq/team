INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/architecture/HYBRID_ONPREM_INTELLIGENCE_SYSTEM.md',
    'team_documentation',
    '🏗️ HYBRID ON-PREM INTELLIGENCE SYSTEM',
    '# 🏗️ HYBRID ON-PREM INTELLIGENCE SYSTEM
## Local LLM Workers + Cloud Supervisor Architecture

**Date:** 2025-11-04  
**Status:** Conceptual Design  
**Feasibility:** ✅ HIGH - All components available ',
    1054,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();