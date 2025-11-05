#!/bin/bash
# Destiny Analytical System - Quick Setup Script
# Team Destiny - 2025-11-05

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     DESTINY ANALYTICAL SYSTEM - QUICK SETUP                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo "1. Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    echo -e "${GREEN}✅ Python: ${PYTHON_VERSION}${NC}"
else
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

# Check Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d ' ' -f 3 | cut -d ',' -f 1)
    echo -e "${GREEN}✅ Docker: ${DOCKER_VERSION}${NC}"
else
    echo -e "${YELLOW}⚠️  Docker not found (optional for databases)${NC}"
fi

# Check Docker Compose
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✅ Docker Compose: Available${NC}"
else
    echo -e "${YELLOW}⚠️  Docker Compose not found (optional)${NC}"
fi

echo ""
echo "2. Setting up Python environment..."

# Install dependencies
echo "   Installing Python dependencies..."
if pip3 install -r requirements.txt --break-system-packages -q 2>/dev/null || \
   pip3 install -r requirements.txt -q 2>/dev/null; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  Some dependencies may need manual installation${NC}"
fi

echo ""
echo "3. Configuring environment..."

# Create .env if doesn't exist
if [ ! -f .env ]; then
    echo "   Creating .env from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env and add your ANTHROPIC_API_KEY${NC}"
    echo -e "${YELLOW}   Run: nano .env${NC}"
else
    echo -e "${GREEN}✅ .env already exists${NC}"
fi

# Create logs directory
mkdir -p logs
echo -e "${GREEN}✅ Logs directory created${NC}"

echo ""
echo "4. Testing core components..."

# Test LLM client
echo "   Testing LLM client..."
if python3 -c "from src.llm.lmstudio_client import LMStudioLLMClient; print('OK')" 2>/dev/null; then
    echo -e "${GREEN}✅ LLM client: OK${NC}"
else
    echo -e "${RED}❌ LLM client: Error${NC}"
fi

# Test embeddings
echo "   Testing embeddings..."
if python3 -c "from src.data.embedding_pipeline import DualEmbeddingSystem; print('OK')" 2>/dev/null; then
    echo -e "${GREEN}✅ Embeddings: OK${NC}"
else
    echo -e "${RED}❌ Embeddings: Error${NC}"
fi

# Test agents
echo "   Testing agents..."
if python3 -c "from src.agents.base_agent import FinancialAnalystAgent; print('OK')" 2>/dev/null; then
    echo -e "${GREEN}✅ Agents: OK${NC}"
else
    echo -e "${RED}❌ Agents: Error${NC}"
fi

echo ""
echo "5. Database setup (optional)..."

# Ask about starting databases
read -p "   Start databases with Docker Compose? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   Starting databases..."
    docker-compose up -d
    echo -e "${GREEN}✅ Databases starting...${NC}"
    echo "   Waiting for databases to be ready (15 seconds)..."
    sleep 15
else
    echo -e "${YELLOW}⚠️  Skipping database startup${NC}"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    SETUP COMPLETE!                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your ANTHROPIC_API_KEY"
echo "  2. Test the system: python3 demo.py"
echo "  3. Run integration tests: python3 tests/integration/test_end_to_end.py"
echo "  4. Check health: python3 health_check.py"
echo ""
echo "Documentation:"
echo "  - README.md - Main documentation"
echo "  - QUICK_START.md - 5-minute guide"
echo "  - COMPLETE_SYSTEM_OVERVIEW.md - Full architecture"
echo ""
echo "Happy analyzing! 🚀"
