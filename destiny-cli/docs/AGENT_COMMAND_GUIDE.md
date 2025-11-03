# 🤖 destiny-agent Command Guide

**Author:** Piotr Nowicki (DevOps Engineer)  
**Purpose:** Agent management and coordination  
**Version:** 1.0

## 📖 Overview

`destiny-agent` is a CLI tool for managing and monitoring the 9 specialized agents in the Destiny Team Framework. It provides visibility into agent status, workload distribution, performance metrics, and task assignment capabilities.

## 🎯 Commands

### **1. list** - Show All Agents

List all available agents with their current status.

**Usage:**
```bash
destiny agent list [OPTIONS]
```

**Options:**
- `--role, -r TEXT` - Filter by role (developer, qa, ux, etc.)
- `--status, -s TEXT` - Filter by status (idle, busy, error)
- `--verbose, -v` - Show detailed information

**Examples:**
```bash
# List all agents
destiny agent list

# Filter by role
destiny agent list --role developer

# Show detailed info
destiny agent list --verbose

# Filter by status
destiny agent list --status idle
```

**Output:**
```
🤖 DESTINY TEAM AGENTS

┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ ID             ┃ Name                     ┃ Role               ┃ Status      ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ tomasz         │ Tomasz Kamiński          │ Senior Developer   │ 🟢 Idle     │
│ anna           │ Anna Lewandowska         │ QA Engineer        │ 🟢 Idle     │
│ magdalena      │ Magdalena Wiśniewska     │ UX Designer        │ 🟢 Idle     │
│ michal         │ Michał Kowalczyk         │ Software Architect │ 🟢 Idle     │
│ katarzyna      │ Katarzyna Zielińska      │ Product Manager    │ 🟢 Idle     │
│ piotr          │ Piotr Nowicki            │ DevOps Engineer    │ 🟢 Idle     │
│ joanna         │ Joanna Mazur             │ Data Scientist     │ 🟢 Idle     │
│ dr_joanna      │ Dr. Joanna Kowalska      │ Research Lead      │ 🟢 Idle     │
│ aleksander     │ Aleksander Nowak         │ Technical Lead     │ 🟢 Idle     │
└────────────────┴──────────────────────────┴────────────────────┴─────────────┘

✅ 9 agent(s) shown
```

---

### **2. info** - Agent Details

Show detailed information about a specific agent.

**Usage:**
```bash
destiny agent info AGENT_ID [OPTIONS]
```

**Arguments:**
- `AGENT_ID` - Agent identifier (tomasz, anna, michal, etc.)

**Options:**
- `--history, -h` - Show recent task history

**Examples:**
```bash
# Basic info
destiny agent info tomasz

# With task history
destiny agent info anna --history

# Other agents
destiny agent info michal
destiny agent info katarzyna
```

**Output:**
```
🤖 AGENT INFORMATION

╔═══════════════════════════════════════════════════════════╗
║              Tomasz Kamiński                              ║
╠═══════════════════════════════════════════════════════════╣
║ Name: Tomasz Kamiński                                     ║
║ Role: Senior Developer                                    ║
║ Status: 🟢 Available                                      ║
║ Specialties: Python, Backend, API, Implementation        ║
║                                                           ║
║ Agent class: TomaszAgent                                  ║
║ Module: agents.specialized.tomasz_agent                   ║
╚═══════════════════════════════════════════════════════════╝

📊 Statistics:
  Total Tasks       27
  Completed         25
  Failed            2
  Success Rate      92.6%
  Avg Completion    45.2 minutes
  Last Active       2025-11-03 10:15
```

---

### **3. workload** - Team Workload Overview

Show current workload distribution across all agents.

**Usage:**
```bash
destiny agent workload [OPTIONS]
```

**Options:**
- `--sort, -s TEXT` - Sort by: tasks, name, success_rate (default: tasks)
- `--limit, -n INTEGER` - Number of agents to show (default: 9)

**Examples:**
```bash
# Default view
destiny agent workload

# Sort by success rate
destiny agent workload --sort success_rate

# Top 5 busiest
destiny agent workload --limit 5

# Sort by name
destiny agent workload --sort name
```

**Output:**
```
📊 AGENT WORKLOAD OVERVIEW

┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Agent                   ┃ Role               ┃ Tasks ┃ Completed ┃ Failed┃ Success    ┃ Workload      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Tomasz Kamiński         │ Senior Developer   │ 27    │ 25        │ 2     │ 92.6%      │ ▓▓▓░░ Busy    │
│ Anna Lewandowska        │ QA Engineer        │ 23    │ 22        │ 1     │ 95.7%      │ ▓▓▓░░ Busy    │
│ Aleksander Nowak        │ Technical Lead     │ 18    │ 17        │ 1     │ 94.4%      │ ▓▓░░░ Medium  │
│ Michał Kowalczyk        │ Software Architect │ 15    │ 15        │ 0     │ 100.0%     │ ▓▓░░░ Medium  │
│ Katarzyna Zielińska     │ Product Manager    │ 12    │ 11        │ 1     │ 91.7%      │ ▓▓░░░ Medium  │
│ Magdalena Wiśniewska    │ UX Designer        │ 10    │ 10        │ 0     │ 100.0%     │ ▓░░░░ Light   │
│ Piotr Nowicki           │ DevOps Engineer    │ 8     │ 8         │ 0     │ 100.0%     │ ▓░░░░ Light   │
│ Joanna Mazur            │ Data Scientist     │ 6     │ 6         │ 0     │ 100.0%     │ ▓░░░░ Light   │
│ Dr. Joanna Kowalska     │ Research Lead      │ 4     │ 4         │ 0     │ 100.0%     │ ░░░░░ Idle    │
└─────────────────────────┴────────────────────┴───────┴───────────┴───────┴────────────┴───────────────┘

Team Summary:
  Total Tasks: 123
  Completed: 118 (95.9%)
  Failed: 5
```

---

### **4. stats** - Performance Statistics

Show agent performance statistics over time.

**Usage:**
```bash
destiny agent stats [OPTIONS]
```

**Options:**
- `--agent, -a TEXT` - Specific agent ID
- `--days, -d INTEGER` - Time period in days (default: 30)

**Examples:**
```bash
# All agents, last 30 days
destiny agent stats

# Specific agent
destiny agent stats --agent tomasz

# Custom period
destiny agent stats --days 7

# Specific agent, custom period
destiny agent stats --agent anna --days 14
```

**Output (specific agent):**
```
📈 AGENT PERFORMANCE STATISTICS

Agent: Tomasz
Period: Last 30 days

Tasks: 27
Completed: 25 (92.6%)
Failed: 2 (7.4%)
Avg Time: 45.2 minutes
```

**Output (all agents):**
```
📈 AGENT PERFORMANCE STATISTICS

Period: Last 30 days

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Agent                        ┃ Tasks ┃ Completed ┃ Success    ┃ Avg Time ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Michał Kowalczyk             │ 15    │ 15        │ 100.0%     │ 38.5 min │
│ Magdalena Wiśniewska         │ 10    │ 10        │ 100.0%     │ 42.1 min │
│ Anna Lewandowska             │ 23    │ 22        │ 95.7%      │ 51.3 min │
│ Aleksander Nowak             │ 18    │ 17        │ 94.4%      │ 35.7 min │
│ Tomasz Kamiński              │ 27    │ 25        │ 92.6%      │ 45.2 min │
└──────────────────────────────┴───────┴───────────┴────────────┴──────────┘
```

---

### **5. assign** - Assign Task

Assign a new task to a specific agent.

**Usage:**
```bash
destiny agent assign AGENT_ID TASK [OPTIONS]
```

**Arguments:**
- `AGENT_ID` - Agent to assign to (tomasz, anna, etc.)
- `TASK` - Task description (quoted string)

**Options:**
- `--priority, -p INTEGER` - Priority 1-5 (default: 3)
- `--deadline, -d DATE` - Deadline in YYYY-MM-DD format

**Examples:**
```bash
# Basic assignment
destiny agent assign tomasz "Implement login feature"

# With priority
destiny agent assign anna "Test checkout flow" --priority 5

# With deadline
destiny agent assign michal "Design architecture" --deadline 2025-12-01

# High priority with deadline
destiny agent assign katarzyna "Review PRD" --priority 4 --deadline 2025-11-05
```

**Output:**
```
📝 ASSIGNING TASK

╔═══════════════════════════════════════════════════════════╗
║                  ✅ Task Assigned                         ║
╠═══════════════════════════════════════════════════════════╣
║ Task: Implement login feature                             ║
║ Assigned to: Tomasz Kamiński (Senior Developer)          ║
║ Priority: 🔥🔥🔥 (3/5)                                     ║
║ Status: ⏳ Pending                                         ║
║ Created: 2025-11-03 12:30                                 ║
║                                                           ║
║ Task ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890            ║
╚═══════════════════════════════════════════════════════════╝
```

---

### **6. performance** - Performance Trends

Show agent performance trends over time (placeholder for future enhancement).

**Usage:**
```bash
destiny agent performance [OPTIONS]
```

**Options:**
- `--agent, -a TEXT` - Specific agent ID
- `--metric, -m TEXT` - Metric: success_rate, speed, volume

**Examples:**
```bash
# All agents
destiny agent performance

# Specific agent
destiny agent performance --agent tomasz

# Specific metric
destiny agent performance --metric speed
```

**Output:**
```
📊 AGENT PERFORMANCE OVER TIME

Metric: success_rate
Scope: All Agents

📈 Performance visualization coming soon!
This would show performance trends, graphs, and comparisons

Available metrics:
  • success_rate - Task completion rate over time
  • speed - Average task completion speed
  • volume - Number of tasks completed
```

---

## 🚀 Installation

```bash
# From destiny-cli directory
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
source .venv/bin/activate

# Commands are immediately available
destiny agent --help
```

---

## 📋 Common Workflows

### **Daily Standup**

```bash
# Check team status
destiny agent list

# See workload distribution
destiny agent workload

# Check busiest agents
destiny agent workload --sort tasks --limit 5
```

### **Task Assignment**

```bash
# Assign to specific agent
destiny agent assign tomasz "Fix authentication bug" --priority 4

# Check if accepted
destiny agent info tomasz --history
```

### **Performance Review**

```bash
# See all agent stats
destiny agent stats

# Specific agent performance
destiny agent stats --agent anna --days 90

# Compare workload
destiny agent workload --sort success_rate
```

### **Load Balancing**

```bash
# Find least busy agent
destiny agent workload --sort tasks

# Assign work to idle agents
destiny agent assign joanna "Analyze user data"
```

---

## 🔧 Integration

### **Works With:**

- **destiny-memory** - See agent memories
  ```bash
  destiny memory agent tomasz
  destiny agent info tomasz
  ```

- **destiny-status** - Quick team overview
  ```bash
  destiny status
  destiny agent list
  ```

- **destiny-task** - Task management
  ```bash
  destiny agent assign tomasz "task"
  destiny task list
  ```

---

## 💡 Tips & Best Practices

1. **Check workload before assigning:**
   ```bash
   destiny agent workload
   destiny agent assign <least-busy-agent> "task"
   ```

2. **Use priority appropriately:**
   - 1-2: Nice to have
   - 3: Normal priority
   - 4-5: High/Critical (use sparingly)

3. **Monitor performance regularly:**
   ```bash
   destiny agent stats --days 7  # Weekly review
   ```

4. **Balance workload:**
   ```bash
   destiny agent workload --sort tasks
   # Assign to agents with lower task counts
   ```

5. **Check agent specialties:**
   ```bash
   destiny agent info <agent>
   # Assign tasks matching their specialties
   ```

---

## 🐛 Troubleshooting

### **"No workload data available"**

**Fix:**
```bash
destiny setup init
```

### **"Agent not found"**

**Check available agents:**
```bash
destiny agent list
```

### **"Database connection failed"**

**Check setup:**
```bash
destiny setup check
destiny memory health
```

---

## 📚 Related Commands

- `destiny status` - Quick agent status
- `destiny memory agent <name>` - Agent memories
- `destiny task list` - View all tasks
- `destiny setup check` - Verify installation

---

**Built with ❤️ by the Destiny Team Framework**
