
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
                'docs/protocols/DOCUMENTATION_STRUCTURE_PROTOCOL.md',
                'protocol',
                '📁 Documentation Structure Protocol',
                '# 📁 Documentation Structure Protocol

**Created:** 2025-11-04  
**Status:** ACTIVE  
**Applies to:** ALL AGENTS  
**Critical:** YES - All agents must follow this structure

---

## 🎯 Purpose

This pro',
                402,
                NOW(),
                NOW(),
                'realtime_watcher'
            )
            ON CONFLICT (file_path) DO UPDATE SET
                document_type = EXCLUDED.document_type,
                title = EXCLUDED.title,
                content_preview = EXCLUDED.content_preview,
                indexed_at = NOW();
            