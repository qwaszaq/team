
            INSERT INTO documents (
                file_path,
                document_type,
                title,
                content_preview,
                line_count,
                created_at,
                indexed_at,
                source
            ) VALUES (
                'docs/status/AUTOMATION_PROOF_COMPLETE.md',
                'general_documentation',
                'Kompletna Automatyzacja - Potwierdzenie',
                '# Kompletna Automatyzacja - Potwierdzenie

**Data:** Tue Nov  4 09:30:20 CET 2025  
**System:** Destiny Project Automation  
**Status:** Pełna automatyzacja aktywna

---

## Potwierdzenie Działania

T',
                51,
                NOW(),
                NOW(),
                'realtime_watcher'
            )
            ON CONFLICT (file_path) DO UPDATE SET
                document_type = EXCLUDED.document_type,
                title = EXCLUDED.title,
                content_preview = EXCLUDED.content_preview,
                indexed_at = NOW();
            