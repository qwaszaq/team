
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
                'docs/protocols/AUTO_PROPAGATION_VERIFICATION.md',
                'general_documentation',
                'Automatyczna Propagacja - Weryfikacja',
                '# Automatyczna Propagacja - Weryfikacja

**Data:** Tue Nov  4 09:27:25 CET 2025
**Status:** Produkcyjny dokument

## Opis

Ten dokument służy do weryfikacji że system automatyzacji działa w 100%.

## ',
                34,
                NOW(),
                NOW(),
                'realtime_watcher'
            )
            ON CONFLICT (file_path) DO UPDATE SET
                document_type = EXCLUDED.document_type,
                title = EXCLUDED.title,
                content_preview = EXCLUDED.content_preview,
                indexed_at = NOW();
            