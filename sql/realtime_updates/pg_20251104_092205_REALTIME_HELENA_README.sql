
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
                'docs/team/REALTIME_HELENA_README.md',
                'team_documentation',
                '🚀 Real-Time Helena Document Processor',
                '# 🚀 Real-Time Helena Document Processor

## Czym to jest?

**Automatyczne przetwarzanie plików .md w czasie rzeczywistym.**

Zamiast czekać 4 godziny na cron, każdy plik `.md` który zapiszesz jest:
- ',
                302,
                NOW(),
                NOW(),
                'realtime_watcher'
            )
            ON CONFLICT (file_path) DO UPDATE SET
                document_type = EXCLUDED.document_type,
                title = EXCLUDED.title,
                content_preview = EXCLUDED.content_preview,
                indexed_at = NOW();
            