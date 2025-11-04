
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
                'docs/protocols/TEST_AUTO_WATCHER_20251104_091904.md',
                'protocol',
                'Test Auto-Watcher',
                '# Test Auto-Watcher

Utworzony: Tue Nov  4 09:19:04 CET 2025
Test: Sprawdzenie czy watcher automatycznie wykrywa zmiany

To jest dokument testowy utworzony aby zweryfikować że:
1. Watcher działa autom',
                11,
                NOW(),
                NOW(),
                'realtime_watcher'
            )
            ON CONFLICT (file_path) DO UPDATE SET
                document_type = EXCLUDED.document_type,
                title = EXCLUDED.title,
                content_preview = EXCLUDED.content_preview,
                indexed_at = NOW();
            