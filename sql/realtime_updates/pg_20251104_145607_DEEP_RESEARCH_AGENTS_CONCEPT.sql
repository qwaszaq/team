INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/concepts/DEEP_RESEARCH_AGENTS_CONCEPT.md',
    'team_documentation',
    '🔬 Deep Research Agents - Complete Concept',
    '# 🔬 Deep Research Agents - Complete Concept

**Project:** Multi-Agent Deep Research System  
**Date:** 2025-11-04  
**Teams:** Analytical Team + Core Team  
**Status:** ✅ Concept Complete

---

## 📋 E',
    950,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();