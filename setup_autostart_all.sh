#!/bin/bash
###############################################################################
# Setup Complete Auto-Start System
# Uruchamia wszystkie komponenty automatycznie przy starcie systemu
###############################################################################

echo "========================================================================"
echo "         🚀 SETUP AUTO-START - Wszystkie Komponenty"
echo "========================================================================"
echo ""

PROJECT_DIR="/Users/artur/coursor-agents-destiny-folder"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

# Tworzenie katalogów
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$LAUNCH_AGENTS_DIR"

echo "📦 Przygotowanie katalogów..."
echo "   ✅ logs/"
echo "   ✅ LaunchAgents/"
echo ""

# Make scripts executable
chmod +x "$PROJECT_DIR/scripts/morning_brief_for_aleksander.py"
chmod +x "$PROJECT_DIR/scripts/realtime_md_watcher.py"
chmod +x "$PROJECT_DIR/scripts/helena_realtime_processor.py"
chmod +x "$PROJECT_DIR/start_realtime_helena.sh"

echo "✅ Skrypty wykonywalne"
echo ""

###############################################################################
# 1. MORNING BRIEF AGENT
###############################################################################

echo "1️⃣  Konfiguracja Morning Brief Agent..."

MORNING_BRIEF_PLIST="$LAUNCH_AGENTS_DIR/com.destiny.morningbrief.plist"

cat > "$MORNING_BRIEF_PLIST" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.destiny.morningbrief</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/artur/coursor-agents-destiny-folder/scripts/morning_brief_for_aleksander.py</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StartInterval</key>
    <integer>28800</integer>
    
    <key>StandardOutPath</key>
    <string>/Users/artur/coursor-agents-destiny-folder/logs/morning_brief.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/artur/coursor-agents-destiny-folder/logs/morning_brief_error.log</string>
    
    <key>WorkingDirectory</key>
    <string>/Users/artur/coursor-agents-destiny-folder</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF

# Unload if exists
launchctl unload "$MORNING_BRIEF_PLIST" 2>/dev/null

# Load
launchctl load "$MORNING_BRIEF_PLIST"

if [ $? -eq 0 ]; then
    echo "   ✅ Morning Brief Agent - AKTYWNY"
    echo "      • Uruchamia się przy starcie systemu"
    echo "      • Powtarza co 8 godzin"
    echo "      • Log: logs/morning_brief.log"
else
    echo "   ⚠️  Morning Brief Agent - Problem z załadowaniem"
fi
echo ""

###############################################################################
# 2. REAL-TIME WATCHER
###############################################################################

echo "2️⃣  Konfiguracja Real-Time Watcher..."

WATCHER_PLIST="$LAUNCH_AGENTS_DIR/com.destiny.watcher.plist"

cat > "$WATCHER_PLIST" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.destiny.watcher</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/artur/coursor-agents-destiny-folder/scripts/realtime_md_watcher.py</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/artur/coursor-agents-destiny-folder/logs/watcher.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/artur/coursor-agents-destiny-folder/logs/watcher_error.log</string>
    
    <key>WorkingDirectory</key>
    <string>/Users/artur/coursor-agents-destiny-folder</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
    
    <key>ThrottleInterval</key>
    <integer>10</integer>
</dict>
</plist>
EOF

# Unload if exists
launchctl unload "$WATCHER_PLIST" 2>/dev/null

# Load
launchctl load "$WATCHER_PLIST"

if [ $? -eq 0 ]; then
    echo "   ✅ Real-Time Watcher - AKTYWNY"
    echo "      • Uruchamia się przy starcie systemu"
    echo "      • Działa cały czas (KeepAlive)"
    echo "      • Monitoruje pliki .md"
    echo "      • Log: logs/watcher.log"
else
    echo "   ⚠️  Real-Time Watcher - Problem z załadowaniem"
fi
echo ""

###############################################################################
# SUMMARY
###############################################################################

echo "========================================================================"
echo "                      ✅ SETUP ZAKOŃCZONY"
echo "========================================================================"
echo ""
echo "🎯 Skonfigurowane komponenty:"
echo ""
echo "1. Morning Brief Agent"
echo "   └─ Automatyczny brief dla Aleksandra"
echo "   └─ Uruchamia się: Przy starcie + co 8h"
echo "   └─ Status: $(launchctl list | grep morningbrief > /dev/null && echo '✅ RUNNING' || echo '❌ NOT RUNNING')"
echo ""
echo "2. Real-Time Watcher"
echo "   └─ Monitoruje dokumentację .md"
echo "   └─ Uruchamia się: Przy starcie"
echo "   └─ Status: $(launchctl list | grep destiny.watcher > /dev/null && echo '✅ RUNNING' || echo '❌ NOT RUNNING')"
echo ""
echo "========================================================================"
echo "📋 WERYFIKACJA"
echo "========================================================================"
echo ""
echo "Sprawdź czy usługi działają:"
echo "   launchctl list | grep destiny"
echo ""
echo "Zobacz logi:"
echo "   tail -f logs/morning_brief.log"
echo "   tail -f logs/watcher.log"
echo ""
echo "Zatrzymaj usługi (jeśli potrzeba):"
echo "   launchctl unload $MORNING_BRIEF_PLIST"
echo "   launchctl unload $WATCHER_PLIST"
echo ""
echo "Uruchom usługi ponownie:"
echo "   launchctl load $MORNING_BRIEF_PLIST"
echo "   launchctl load $WATCHER_PLIST"
echo ""
echo "========================================================================"
echo "🎉 SYSTEM GOTOWY!"
echo "========================================================================"
echo ""
echo "Od teraz przy każdym uruchomieniu systemu:"
echo "  ✅ Morning Brief będzie generowany automatycznie"
echo "  ✅ Watcher będzie monitorować pliki .md"
echo "  ✅ Helena będzie przetwarzać zmiany w czasie rzeczywistym"
echo ""
echo "Zapisz nowy dokument .md w docs/ i zobacz magię! ✨"
echo ""

# Test watchdog installation
echo "📦 Sprawdzanie watchdog..."
python3 -c "import watchdog" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Instaluję watchdog..."
    pip3 install watchdog
    echo "✅ Watchdog zainstalowany"
fi

echo ""
echo "========================================================================"
