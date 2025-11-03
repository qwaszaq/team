# 🚀 destiny-cli Installation Guide

**Making destiny-cli comfortable for end users!**

---

## 🎯 **RECOMMENDED SETUP FOR END USERS**

### **Goal: Type `destiny` anywhere and it just works!**

```bash
# From anywhere in the system:
destiny memory stats
destiny status
destiny task list

# No activation, no paths, no hassle!
```

---

## 📦 **INSTALLATION OPTIONS**

### **Option 1: Install from Source** ⭐ Recommended for Development

```bash
# 1. Navigate to the project
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli

# 2. Install in editable mode (changes reflect immediately)
pip3 install -e .

# 3. Done! Now you can use it anywhere:
destiny --help
destiny memory stats
destiny status
```

**Pros:**
- ✅ Available globally (no venv activation)
- ✅ Type `destiny` from anywhere
- ✅ Changes to code reflect immediately
- ✅ Easy development workflow

**Cons:**
- ⚠️ Installs globally (may conflict with other projects)

---

### **Option 2: Install in Virtual Environment** ⭐ Recommended for Users

```bash
# 1. Create and activate virtual environment
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
python3 -m venv venv
source venv/bin/activate

# 2. Install the package
pip install -e .

# 3. Use it (while venv is active):
destiny memory stats
destiny status
```

**Pros:**
- ✅ Isolated from system Python
- ✅ No conflicts with other projects
- ✅ Clean uninstall

**Cons:**
- ⚠️ Must activate venv each time (can be automated)

---

### **Option 3: Install with pipx** ⭐ BEST for End Users

```bash
# 1. Install pipx (if not already installed)
brew install pipx
pipx ensurepath

# 2. Install destiny-cli
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
pipx install .

# 3. Use it anywhere, anytime:
destiny memory stats
destiny status
```

**Pros:**
- ✅ Available globally
- ✅ Completely isolated
- ✅ No venv activation needed
- ✅ Easy updates: `pipx upgrade destiny-cli`
- ✅ Easy uninstall: `pipx uninstall destiny-cli`

**Cons:**
- None! This is the BEST option for end users.

---

## 🔧 **STEP-BY-STEP INSTALLATION**

### **For End Users (pipx method):**

```bash
# Step 1: Install pipx (one-time setup)
brew install pipx
pipx ensurepath

# Step 2: Install destiny-cli
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
pipx install .

# Step 3: Verify installation
destiny --help

# Step 4: Test it!
destiny memory stats
destiny status
```

**Expected output:**
```
✅ destiny-cli installed successfully!

Available commands:
  - destiny status          # Agent & task status
  - destiny task           # Task management
  - destiny memory         # Memory exploration
  - destiny agent          # Agent management (future)
  - destiny demo           # Demo runner (future)
```

---

## 📝 **AFTER INSTALLATION**

### **How Users Will Use It:**

```bash
# From ANYWHERE in the system:
cd ~/Documents
destiny memory stats

cd ~/Projects/other-project
destiny status

cd /tmp
destiny memory search "bug"

# It just works! ✅
```

---

## 🎨 **MAKING IT EVEN MORE COMFORTABLE**

### **1. Add Aliases (Optional)**

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Destiny CLI shortcuts
alias dm='destiny memory'
alias ds='destiny status'
alias dt='destiny task'

# Now you can type:
dm stats              # instead of destiny memory stats
ds                    # instead of destiny status
dt list               # instead of destiny task list
```

Reload shell:
```bash
source ~/.zshrc
```

---

### **2. Enable Tab Completion (Optional)**

```bash
# For zsh (add to ~/.zshrc)
eval "$(_DESTINY_COMPLETE=zsh_source destiny)"

# For bash (add to ~/.bashrc)
eval "$(_DESTINY_COMPLETE=bash_source destiny)"

# Reload shell
source ~/.zshrc
```

Now you can:
```bash
destiny <TAB>          # Shows: status, task, memory, agent, demo
destiny memory <TAB>   # Shows: stats, search, agent, relationships, health, cleanup
```

---

### **3. Create a Helper Script (Optional)**

Create `/usr/local/bin/destiny-quick`:

```bash
#!/bin/bash
# Quick destiny commands

case "$1" in
  "check")
    destiny memory health && destiny status
    ;;
  "search")
    destiny memory search "$2"
    ;;
  "report")
    echo "=== Destiny Team Daily Report ==="
    date
    echo ""
    destiny status
    echo ""
    destiny memory stats
    ;;
  *)
    destiny "$@"
    ;;
esac
```

Make it executable:
```bash
chmod +x /usr/local/bin/destiny-quick
```

Use it:
```bash
destiny-quick check           # Health + Status
destiny-quick search "bug"    # Quick search
destiny-quick report          # Daily report
```

---

## 🔄 **UPDATING destiny-cli**

### **When you make changes to the code:**

**If installed with `-e` (editable):**
```bash
# No action needed! Changes reflect immediately.
# Just use the commands:
destiny memory stats
```

**If installed with pipx:**
```bash
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
pipx upgrade destiny-cli --force
```

**If installed with pip:**
```bash
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
pip install --upgrade --force-reinstall .
```

---

## 🗑️ **UNINSTALLING**

### **If installed with pipx:**
```bash
pipx uninstall destiny-cli
```

### **If installed with pip:**
```bash
pip uninstall destiny-cli
```

### **If installed globally:**
```bash
pip3 uninstall destiny-cli
```

---

## 🧪 **TESTING THE INSTALLATION**

### **Verification Checklist:**

```bash
# 1. Check command is available
which destiny
# Should show: /usr/local/bin/destiny or similar

# 2. Check version
destiny --version
# Should show: destiny-cli version 0.1.0

# 3. Check help
destiny --help
# Should show all available commands

# 4. Test each command
destiny status
destiny memory stats
destiny memory health
destiny task list

# 5. Test from different directory
cd ~
destiny memory stats
# Should work!
```

---

## 🎯 **RECOMMENDED WORKFLOW FOR YOUR PROJECT**

### **For Development (You):**

```bash
# One-time setup
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
pip3 install -e .

# Daily use (from anywhere):
destiny memory stats
destiny status

# Make code changes, test immediately
# (no reinstall needed with -e flag)
```

---

### **For End Users (Evaluator, Team Members):**

```bash
# One-time setup
brew install pipx
pipx install /path/to/destiny-cli

# Daily use (from anywhere):
destiny memory stats
destiny status
destiny memory search "authentication"

# Update when new version available
pipx upgrade destiny-cli
```

---

## 📊 **COMPARISON TABLE**

| Method | Global Access | No Activation | Easy Updates | Isolated | Best For |
|--------|--------------|---------------|--------------|----------|----------|
| **pipx** | ✅ | ✅ | ✅ | ✅ | **End Users** ⭐ |
| **pip install -e** | ✅ | ✅ | ✅ (automatic) | ❌ | **Developers** ⭐ |
| **venv + pip** | ❌ | ❌ | ✅ | ✅ | Testing |
| **Manual run** | ❌ | ❌ | ❌ | ✅ | Development only |

---

## 🚨 **TROUBLESHOOTING**

### **Issue: "destiny: command not found"**

**Solution:**
```bash
# Check if installed
pip3 list | grep destiny-cli

# If not found, install:
pip3 install -e /Users/artur/coursor-agents-destiny-folder/destiny-cli

# Check PATH
echo $PATH
# Make sure Python bin directory is in PATH
```

---

### **Issue: "ModuleNotFoundError"**

**Solution:**
```bash
# Reinstall with all dependencies
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
pip3 install --upgrade --force-reinstall .
```

---

### **Issue: Changes not reflecting**

**Solution:**
```bash
# If NOT installed with -e flag, reinstall:
pip3 install --force-reinstall -e .

# Or use pipx:
pipx upgrade destiny-cli --force
```

---

## ✅ **FINAL RECOMMENDATION**

### **For Maximum Comfort:**

**1. Install with pipx or pip -e**
```bash
# Choose one:
pipx install .              # For users
pip3 install -e .           # For developers
```

**2. Add aliases**
```bash
alias dm='destiny memory'
alias ds='destiny status'
```

**3. Enable tab completion**
```bash
eval "$(_DESTINY_COMPLETE=zsh_source destiny)"
```

**Result:** Ultra-comfortable CLI experience! 🎉

```bash
# From anywhere:
dm stats              # Quick memory check
ds                    # Quick status check
destiny <TAB>         # See all commands
```

---

## 🎯 **QUICK START FOR NEW USERS**

### **Copy-paste this:**

```bash
# Install pipx
brew install pipx
pipx ensurepath

# Install destiny-cli
cd /Users/artur/coursor-agents-destiny-folder/destiny-cli
pipx install .

# Add aliases (optional but recommended)
echo "alias dm='destiny memory'" >> ~/.zshrc
echo "alias ds='destiny status'" >> ~/.zshrc
source ~/.zshrc

# Test it!
destiny --help
dm stats
ds

# Done! 🎉
```

---

## 📖 **DOCUMENTATION**

For complete command reference, see:
- `MEMORY_COMMAND_GUIDE.md` - destiny-memory documentation
- `README.md` - Project overview
- `destiny --help` - Built-in help

---

**The goal: Type `destiny` and it just works, anywhere, anytime!** ✨
