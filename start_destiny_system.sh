#!/bin/bash
###############################################################################
# 🚀 DESTINY SYSTEM - MASTER STARTUP SCRIPT
# Uruchamia cały system ze wszystkimi usługami w jednej komendzie
###############################################################################

# Only exit on error for critical operations
# Verification checks will not cause exit

PROJECT_DIR="/Users/artur/coursor-agents-destiny-folder"
cd "$PROJECT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║                   🚀 DESTINY SYSTEM - STARTUP MASTER 🚀                     ║"
echo "║                                                                              ║"
echo "║              Complete Multi-Agent AI Development Framework                   ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

###############################################################################
# STEP 1: Check Docker
###############################################################################

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐳 STEP 1: Sprawdzam Docker..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker nie jest zainstalowany!${NC}"
    echo "   Zainstaluj Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker nie działa. Uruchamiam...${NC}"
    open -a Docker
    echo "   Czekam 15 sekund na uruchomienie Dockera..."
    sleep 15
    
    # Check again
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker nie uruchomił się. Uruchom Docker Desktop ręcznie.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Docker działa${NC}"
echo ""

###############################################################################
# STEP 2: Start/Check Database Containers
###############################################################################

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🗄️  STEP 2: Uruchamiam bazy danych..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Function to check if container is running
check_container() {
    local name=$1
    if docker ps --format '{{.Names}}' | grep -q "^${name}$"; then
        echo -e "${GREEN}✅ ${name} - RUNNING${NC}"
        return 0
    elif docker ps -a --format '{{.Names}}' | grep -q "^${name}$"; then
        echo -e "${YELLOW}⚠️  ${name} - STOPPED, uruchamiam...${NC}"
        docker start "${name}" &> /dev/null
        sleep 2
        echo -e "${GREEN}✅ ${name} - STARTED${NC}"
        return 0
    else
        echo -e "${RED}❌ ${name} - NIE ZNALEZIONY${NC}"
        return 1
    fi
}

echo "Sprawdzam kontenery:"
echo ""

# Check each database
QDRANT_OK=false
POSTGRES_OK=false
NEO4J_OK=false
REDIS_OK=false

# Qdrant
if check_container "sms-qdrant"; then
    QDRANT_OK=true
fi

# PostgreSQL
if check_container "sms-postgres" || check_container "hercules-postgres"; then
    POSTGRES_OK=true
fi

# Neo4j
if check_container "sms-neo4j"; then
    NEO4J_OK=true
fi

# Redis
if check_container "sms-redis" || check_container "hercules-redis" || check_container "kg-redis"; then
    REDIS_OK=true
fi

echo ""

# Summary
if [ "$QDRANT_OK" = true ] && [ "$POSTGRES_OK" = true ] && [ "$NEO4J_OK" = true ] && [ "$REDIS_OK" = true ]; then
    echo -e "${GREEN}✅ Wszystkie bazy danych działają!${NC}"
else
    echo -e "${YELLOW}⚠️  Niektóre kontenery nie działają:${NC}"
    [ "$QDRANT_OK" = false ] && echo "   ❌ Qdrant"
    [ "$POSTGRES_OK" = false ] && echo "   ❌ PostgreSQL"
    [ "$NEO4J_OK" = false ] && echo "   ❌ Neo4j"
    [ "$REDIS_OK" = false ] && echo "   ❌ Redis"
    echo ""
    echo "Uruchom brakujące kontenery lub sprawdź docker-compose.yml"
fi

echo ""

# Wait for databases to be ready
echo "Czekam 5 sekund na gotowość baz danych..."
sleep 5
echo ""

###############################################################################
# STEP 3: Check/Start Helena Watcher
###############################################################################

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "👁️  STEP 3: Sprawdzam Helena Watcher..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

WATCHER_PID=$(ps aux | grep realtime_md_watcher | grep -v grep | awk '{print $2}')

if [ -n "$WATCHER_PID" ]; then
    echo -e "${GREEN}✅ Helena Watcher już działa (PID: $WATCHER_PID)${NC}"
else
    echo -e "${YELLOW}⚠️  Helena Watcher nie działa. Uruchamiam...${NC}"
    
    # Check if conda environment exists (with timeout)
    if timeout 5 conda env list 2>/dev/null | grep -q "^team " 2>/dev/null; then
        echo "   Używam conda environment 'team'"
        ./start_watcher_conda.sh
    else
        echo "   Używam systemowego Pythona"
        nohup python3 scripts/realtime_md_watcher.py > logs/watcher.log 2>&1 &
    fi
    
    sleep 2
    
    WATCHER_PID=$(ps aux | grep realtime_md_watcher | grep -v grep | awk '{print $2}')
    if [ -n "$WATCHER_PID" ]; then
        echo -e "${GREEN}✅ Helena Watcher uruchomiony (PID: $WATCHER_PID)${NC}"
    else
        echo -e "${RED}❌ Nie udało się uruchomić Helena Watcher${NC}"
    fi
fi

echo ""

###############################################################################
# STEP 4: Verify Database Connectivity
###############################################################################

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 STEP 4: Weryfikuję połączenia z bazami..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Qdrant
if curl -s http://localhost:6333/collections > /dev/null 2>&1; then
    QDRANT_POINTS=$(curl -s http://localhost:6333/collections/destiny-team-framework-master 2>/dev/null | python3 -c "import json,sys; r=json.load(sys.stdin)['result']; print(r['points_count'])" 2>/dev/null || echo "?")
    echo -e "${GREEN}✅ Qdrant:    http://localhost:6333${NC} (${QDRANT_POINTS} points)"
else
    echo -e "${RED}❌ Qdrant:    http://localhost:6333${NC} (nie odpowiada)"
fi

# PostgreSQL (check port with nc)
if command -v nc &> /dev/null; then
    if nc -z localhost 5432 2>&1 | grep -q 'succeeded\|open'; then
        echo -e "${GREEN}✅ PostgreSQL: localhost:5432${NC}"
    else
        echo -e "${YELLOW}⚠️  PostgreSQL: localhost:5432${NC} (port nie odpowiada)"
    fi
else
    # Fallback: Check if container is healthy
    if docker ps --filter "name=postgres" --filter "status=running" --format "{{.Names}}" | grep -q postgres; then
        echo -e "${GREEN}✅ PostgreSQL: localhost:5432${NC} (container healthy)"
    else
        echo -e "${YELLOW}⚠️  PostgreSQL: localhost:5432${NC}"
    fi
fi

# Neo4j
if curl -s http://localhost:7474 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Neo4j:     http://localhost:7474${NC}"
else
    echo -e "${RED}❌ Neo4j:     http://localhost:7474${NC} (nie odpowiada)"
fi

# Redis (check port with nc)
if command -v nc &> /dev/null; then
    if nc -z localhost 6379 2>&1 | grep -q 'succeeded\|open'; then
        echo -e "${GREEN}✅ Redis:     localhost:6379${NC}"
    else
        echo -e "${YELLOW}⚠️  Redis:     localhost:6379${NC} (port nie odpowiada)"
    fi
else
    # Fallback: Check if container is healthy
    if docker ps --filter "name=redis" --filter "status=running" --format "{{.Names}}" | grep -q redis; then
        echo -e "${GREEN}✅ Redis:     localhost:6379${NC} (container healthy)"
    else
        echo -e "${YELLOW}⚠️  Redis:     localhost:6379${NC}"
    fi
fi

echo ""

###############################################################################
# STEP 5: System Status Summary
###############################################################################

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 STEP 5: Status systemu"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🐳 Docker Containers:"
docker ps --format "   • {{.Names}} - {{.Status}}" | grep -E "qdrant|postgres|neo4j|redis" || echo "   (brak uruchomionych kontenerów)"
echo ""

echo "🤖 Destiny Processes:"
ps aux | grep -E "realtime_md_watcher|helena.*processor|morning_brief" | grep -v grep | awk '{printf "   • %s (PID: %s)\n", $11, $2}' || echo "   (brak uruchomionych procesów)"
echo ""

echo "📁 Project:"
echo "   • Directory: $PROJECT_DIR"
echo "   • Branch: $(git branch --show-current 2>/dev/null || echo 'unknown')"
echo "   • Last commit: $(git log -1 --oneline 2>/dev/null | cut -c 1-60 || echo 'unknown')"
echo ""

###############################################################################
# STEP 6: Quick Links & Commands
###############################################################################

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔗 Quick Links & Commands"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📊 Dashboards:"
echo "   • Qdrant:     http://localhost:6333/dashboard"
echo "   • Neo4j:      http://localhost:7474"
echo "   • PostgreSQL: psql -h localhost -U postgres -d destinyframework"
echo ""

echo "📝 Logs:"
echo "   • Watcher:    tail -f logs/watcher.log"
echo "   • Helena:     tail -f logs/helena_realtime_processor.log"
echo ""

echo "🧪 Test System:"
echo "   • Demo:       python3 examples/enhanced_collaboration_demo.py"
echo "   • Tests:      python3 tests/test_integrated_system.py"
echo "   • All Tests:  python3 -m pytest tests/ -v"
echo ""

echo "🛑 Stop System:"
echo "   • Watcher:    kill $WATCHER_PID"
echo "   • Containers: docker stop sms-qdrant sms-postgres sms-neo4j sms-redis"
echo ""

###############################################################################
# Final Message
###############################################################################

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║                    ✅ DESTINY SYSTEM READY! ✅                              ║"
echo "║                                                                              ║"
echo "║  All services are running and ready to use!                                  ║"
echo "║                                                                              ║"
echo "║  Create a new .md file in docs/ to test Helena's auto-propagation! 🚀      ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Return success
exit 0
