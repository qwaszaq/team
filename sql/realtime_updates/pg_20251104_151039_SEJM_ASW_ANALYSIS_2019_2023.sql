INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/research/SEJM_ASW_ANALYSIS_2019_2023.md',
    'analysis',
    '🏛️ Analiza Pracy Komisji Administracji i Spraw Wewnętrznych',
    '# 🏛️ Analiza Pracy Komisji Administracji i Spraw Wewnętrznych

**Komisja:** Komisja Administracji i Spraw Wewnętrznych (ASW)  
**Kadencja:** IX (2019-2023)  
**Zakres:** 2019-11-14 do 2023-08-30  
**D',
    450,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();