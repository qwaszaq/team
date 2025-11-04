INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'investigations/active/telus_cpk_real_001/FINAL_OSINT_REPORT.md',
    'analysis',
    'Raport OSINT: Robert Telus — CPK (real data)',
    '# Raport OSINT: Robert Telus — CPK (real data)

- **Zakres**: przegląd publicznych doniesień dot. powiązania sprawy działki pod CPK z Robertem Telusem; identyfikacja osi faktów, kontrowersji, ryzyk pr',
    96,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();