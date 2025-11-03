#!/bin/bash
# Activate Destiny Team conda environment

echo "🚀 Activating Destiny Team environment..."
echo ""

# Activate conda
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate team

echo "✅ Environment 'team' activated!"
echo ""
echo "📊 Installed packages:"
echo "   • PostgreSQL (psycopg2-binary)"
echo "   • Neo4j (neo4j driver)"
echo "   • Qdrant (qdrant-client)"
echo "   • Redis (redis)"
echo "   • LM Studio (requests)"
echo "   • NumPy (numpy)"
echo ""
echo "🎯 Quick commands:"
echo "   python test_all_connections.py    # Test all services"
echo "   python project_manager.py list    # List projects"
echo "   python session_workflow.py        # Session management"
echo ""
echo "📚 Read: CO_TERAZ.md for next steps"
echo ""
