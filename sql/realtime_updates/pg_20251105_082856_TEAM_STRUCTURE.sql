INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/team/TEAM_STRUCTURE.md',
    'team_documentation',
    '👥 Destiny Team - Complete Structure',
    '# 👥 Destiny Team - Complete Structure

## 🎯 Full Team (10 Agents)

### **Coordination Layer**

#### 1. **Aleksander Nowak** - Orchestrator 🎯
- **Model:** Claude Sonnet 4.5
- **Role:** Project coordina',
    375,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();