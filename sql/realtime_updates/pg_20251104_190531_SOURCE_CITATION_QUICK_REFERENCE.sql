INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'SOURCE_CITATION_QUICK_REFERENCE.md',
    'general_documentation',
    '📚 SOURCE CITATION - QUICK REFERENCE CARD',
    '# 📚 SOURCE CITATION - QUICK REFERENCE CARD

**🔴 MANDATORY for ALL investigative & research agents**

---

## 🎯 THE RULE

```
NO SOURCE = NO CLAIM
```

If you can''t cite it, don''t claim it.

---

## ✅ ',
    100,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();