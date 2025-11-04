
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
                'docs/status/SYSTEM_TEST_REPORT_20251104.md',
                'status_report',
                '🧪 System Test Report - Complete Pipeline Verification',
                '# 🧪 System Test Report - Complete Pipeline Verification

**Date:** 2025-11-04 09:14  
**Performed by:** AI Assistant + Artur  
**Test Type:** End-to-End Integration Test  
**Status:** ✅ **ALL TESTS PA',
                377,
                NOW(),
                NOW(),
                'realtime_watcher'
            )
            ON CONFLICT (file_path) DO UPDATE SET
                document_type = EXCLUDED.document_type,
                title = EXCLUDED.title,
                content_preview = EXCLUDED.content_preview,
                indexed_at = NOW();
            