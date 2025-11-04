
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
                'docs/status/AUTOSTART_SYSTEM_STATUS.md',
                'status_report',
                '✅ Auto-Start System - Status Report',
                '# ✅ Auto-Start System - Status Report

**Data:** 2025-11-04 09:18  
**Status:** 🟢 OPERATIONAL

---

## 🎯 System Auto-Start - Aktywny

Wszystkie komponenty systemu uruchamiają się **automatycznie przy ',
                349,
                NOW(),
                NOW(),
                'realtime_watcher'
            )
            ON CONFLICT (file_path) DO UPDATE SET
                document_type = EXCLUDED.document_type,
                title = EXCLUDED.title,
                content_preview = EXCLUDED.content_preview,
                indexed_at = NOW();
            