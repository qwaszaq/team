
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
                'docs/protocols/TEST_PROTOCOL_SYSTEM_CHECK.md',
                'protocol',
                'Test Protocol - System Check',
                '# Test Protocol - System Check

**Created:** 2025-11-04 09:13  
**Purpose:** Test end-to-end documentation processing  
**Status:** TEST DOCUMENT

---

## Test Objectives

This document tests the comp',
                55,
                NOW(),
                NOW(),
                'realtime_watcher'
            )
            ON CONFLICT (file_path) DO UPDATE SET
                document_type = EXCLUDED.document_type,
                title = EXCLUDED.title,
                content_preview = EXCLUDED.content_preview,
                indexed_at = NOW();
            