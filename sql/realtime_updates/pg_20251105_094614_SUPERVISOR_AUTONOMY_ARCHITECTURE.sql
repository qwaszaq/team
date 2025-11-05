INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/architecture/SUPERVISOR_AUTONOMY_ARCHITECTURE.md',
    'architecture',
    '🎯 ARCHITEKTURA NADZORU I AUTONOMII - HYBRID SUPERVISION',
    '# 🎯 ARCHITEKTURA NADZORU I AUTONOMII - HYBRID SUPERVISION

**Data:** 2025-11-05  
**Architekt:** Aleksander Nowak + Katarzyna Wiśniewska  
**Cel:** System z progresywną autonomią pod nadzorem Claude

',
    949,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();