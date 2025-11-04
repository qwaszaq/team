# 📁 Documentation Structure Protocol

**Created:** 2025-11-04  
**Status:** ACTIVE  
**Applies to:** ALL AGENTS  
**Critical:** YES - All agents must follow this structure

---

## 🎯 Purpose

This protocol defines where and how all documentation should be saved in the Destiny project.

**Problem Solved:**
- ❌ 168 .md files scattered in root directory
- ❌ Hard to find relevant documentation
- ❌ No organization or categorization
- ❌ Difficult for agents to discover knowledge

**Solution:**
- ✅ Organized `docs/` directory structure
- ✅ Clear categorization
- ✅ Automatic indexing
- ✅ Easy discovery

---

## 📂 Directory Structure

```
docs/
├── protocols/          # Process definitions, protocols, procedures
├── team/              # Team member profiles, agent definitions
├── status/            # Status reports, completion summaries
├── architecture/      # System design, framework docs
├── guides/            # Setup guides, tutorials, how-tos
├── analysis/          # Research, assessments, deep dives
├── tasks/             # Task definitions, challenges
├── general/           # Miscellaneous documentation
└── INDEX.md           # Auto-generated index (DO NOT EDIT)
```

---

## 📋 Where to Save What

### `docs/protocols/`
**Use for:**
- Process definitions (how things work)
- Protocols (rules and procedures)
- Monitoring procedures
- Data handling protocols
- Verification procedures

**Examples:**
- `DATA_LOADING_PROTOCOL.md`
- `ALEKSANDER_CONTINUOUS_MONITORING_PROTOCOL.md`
- `VERIFICATION_INTEGRATION_GUIDE.md`

**Naming:** `[TOPIC]_PROTOCOL.md` or `[TOPIC]_PROCESS.md`

---

### `docs/team/`
**Use for:**
- Agent profiles and definitions
- Team member information
- Collaboration patterns
- Agent responsibilities
- Team structure

**Examples:**
- `ALEKSANDER_HELENA_WORKING_RELATIONSHIP.md`
- `ANALYTICAL_TEAM_COMPLETE_SUMMARY.md`
- `CROSS_TEAM_COLLABORATION_MULTI_TURN.md`

**Naming:** `[AGENT_NAME]_[TOPIC].md` or `[TEAM]_[TOPIC].md`

---

### `docs/status/`
**Use for:**
- Daily/weekly status reports
- Project completion summaries
- Progress updates
- Milestone reports
- Morning briefs

**Examples:**
- `MORNING_BRIEF_20251104.md`
- `DAY_2_FINAL_STATUS.md`
- `ANALYTICAL_TEAM_FINAL_STATUS.md`

**Naming:** `[TOPIC]_STATUS.md` or `[DATE]_SUMMARY.md`

---

### `docs/architecture/`
**Use for:**
- System architecture documentation
- Framework descriptions
- Design patterns
- Integration patterns
- Technical architecture

**Examples:**
- `ARCHITECTURE_EXPLAINED.md`
- `SELF_ENFORCING_SYSTEM.md`
- `UNLIMITED_CONTEXT_ARCHITECTURE.md`

**Naming:** `[SYSTEM]_ARCHITECTURE.md` or `[COMPONENT]_DESIGN.md`

---

### `docs/guides/`
**Use for:**
- Setup instructions
- Installation guides
- Quick start guides
- Tutorials
- How-to documents

**Examples:**
- `CI_SETUP_GUIDE.md`
- `POSTGRES_SETUP_GUIDE.md`
- `ANALYTICAL_TEAM_QUICK_START.md`

**Naming:** `[TOPIC]_GUIDE.md` or `[TOPIC]_SETUP.md`

---

### `docs/analysis/`
**Use for:**
- Research documents
- Gap analysis
- Assessments
- Evaluations
- Deep dives

**Examples:**
- `ANALYTICAL_TOOLKITS_DEEP_DIVE.md`
- `CORE_ASSUMPTIONS_GAP_ANALYSIS.md`
- `DATA_QUALITY_CROSS_DATABASE_ASSESSMENT.md`

**Naming:** `[TOPIC]_ANALYSIS.md` or `[TOPIC]_ASSESSMENT.md`

---

### `docs/tasks/`
**Use for:**
- Task definitions
- Challenges
- Checklists
- Action items

**Examples:**
- `CHALLENGE_TASK.md`
- `IMMEDIATE_TASKS.md`
- `PRE_START_EXECUTION_CHECKLIST.md`

**Naming:** `[TOPIC]_TASK.md` or `[TOPIC]_CHECKLIST.md`

---

### `docs/general/`
**Use for:**
- Documents that don't fit other categories
- Miscellaneous documentation
- Experimental docs

**Default category** - Use this if you're unsure.

---

## 🤖 For Agents: How to Use This Structure

### When Creating New Documentation:

1. **Determine category** based on content type
2. **Choose appropriate directory** from above
3. **Use naming convention** for that category
4. **Save file** to correct location

**Example (Aleksander creating a new protocol):**
```bash
# Bad (old way)
echo "# New Protocol" > NEW_PROTOCOL.md

# Good (new way)
echo "# New Protocol" > docs/protocols/NEW_PROTOCOL.md
```

### When Referencing Documentation:

Always use relative paths from project root:

```markdown
See [Monitoring Protocol](docs/protocols/ALEKSANDER_CONTINUOUS_MONITORING_PROTOCOL.md)
See [Team Structure](docs/team/ANALYTICAL_TEAM_COMPLETE_SUMMARY.md)
See [Setup Guide](docs/guides/CI_SETUP_GUIDE.md)
```

### When Searching for Documentation:

1. **Check INDEX:** `docs/INDEX.md` (auto-generated, updated daily)
2. **Browse category:** Navigate to relevant `docs/[category]/`
3. **Use semantic search:** If integrated with Qdrant

---

## ⚡ Real-Time Processing

**All documentation saved to `docs/` is automatically:**

1. **Detected instantly** by file watcher
2. **Processed by Helena** within seconds
3. **Added to databases:**
   - PostgreSQL (metadata)
   - Neo4j (relationships)
   - Qdrant (semantic search)
   - Redis (cache)

**No manual action required!**

---

## 📊 Index Generation

The `docs/INDEX.md` file is **automatically generated** by:

```bash
python3 scripts/organize_documentation.py
```

**Do NOT edit INDEX.md manually** - it will be overwritten.

**Regenerate index:**
- Automatically: Daily via cron
- Manually: Run script above

---

## 🔍 Finding Documentation

### Method 1: Browse INDEX
```bash
cat docs/INDEX.md
# or
open docs/INDEX.md
```

### Method 2: Use grep
```bash
grep -r "topic" docs/
```

### Method 3: Use semantic search (if available)
```python
from qdrant_client import QdrantClient
client = QdrantClient(url="http://localhost:6333")
results = client.search(
    collection_name="destiny-docs",
    query_text="monitoring protocol"
)
```

---

## ⚠️ Migration

**Existing root-level .md files have been migrated:**

- ✅ 168 files organized into categories
- ✅ All moved to `docs/[category]/`
- ✅ Root directory cleaned up
- ✅ INDEX.md generated

**If you find a .md file in root:**
- Move it to appropriate `docs/[category]/`
- Or run: `python3 scripts/organize_documentation.py`

---

## 🎯 Benefits

### For Agents:
- ✅ Easy to find relevant documentation
- ✅ Clear where to save new docs
- ✅ Automatic processing to databases
- ✅ Semantic search enabled

### For Users:
- ✅ Organized structure
- ✅ No more clutter in root
- ✅ Quick navigation
- ✅ Professional appearance

### For System:
- ✅ Consistent structure
- ✅ Easier to index
- ✅ Better knowledge graph
- ✅ Scalable organization

---

## 📝 Examples

### Example 1: Helena creates database protocol
```python
protocol = """
# Database Update Protocol
...
"""

# Save to appropriate location
path = "docs/protocols/DATABASE_UPDATE_PROTOCOL.md"
with open(path, 'w') as f:
    f.write(protocol)

# Watcher detects it instantly
# Helena processes it automatically
# Added to all databases within 10 seconds
```

### Example 2: Aleksander creates team status
```python
status = """
# Team Status Report - 2025-11-04
...
"""

path = "docs/status/TEAM_STATUS_20251104.md"
with open(path, 'w') as f:
    f.write(status)
```

### Example 3: Sofia creates market analysis
```python
analysis = """
# Market Research - Q4 2025
...
"""

path = "docs/analysis/MARKET_RESEARCH_Q4_2025.md"
with open(path, 'w') as f:
    f.write(analysis)
```

---

## 🔄 Workflow Integration

### For Documentation Agent (Helena):
1. Monitor `docs/` for changes
2. Process new/modified files
3. Extract metadata
4. Propagate to all databases
5. Update knowledge graph

### For Orchestrator (Aleksander):
1. Receives morning brief from `docs/status/MORNING_BRIEF_*.md`
2. Reviews team docs in `docs/team/`
3. Checks protocols in `docs/protocols/`
4. Creates new status reports in `docs/status/`

### For All Agents:
1. **Read** documentation from appropriate category
2. **Create** new docs in correct location
3. **Reference** docs using relative paths
4. **Trust** that docs are auto-processed

---

## ✅ Compliance

**All agents MUST:**
- ✅ Save documentation to `docs/[category]/`
- ✅ Use proper naming conventions
- ✅ NOT save .md files to root (except README.md)
- ✅ Reference this protocol when uncertain

**This protocol is:**
- ✅ Automatically enforced by file watcher
- ✅ Part of morning brief
- ✅ Indexed in all databases

---

## 📚 Related Documentation

- [Real-Time Helena System](../team/REALTIME_HELENA_README.md)
- [Morning Brief Protocol](MORNING_BRIEF_PROTOCOL.md)
- [Helena Auto-Save Protocol](HELENA_AUTO_SAVE_PROTOCOL.md)

---

**Status:** ACTIVE  
**Last Updated:** 2025-11-04  
**Next Review:** Monthly or as needed

*This protocol ensures all project knowledge is organized, discoverable, and hot.*
