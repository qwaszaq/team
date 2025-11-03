#!/bin/bash

# ════════════════════════════════════════════════════════════════════
# CLEANUP SCRIPT - Remove Evaluation Test Remnants
# ════════════════════════════════════════════════════════════════════
#
# Purpose: Clean up test data and temporary files after evaluation
# Run: ./CLEANUP_AFTER_EVALUATION.sh
#
# Options:
#   full    - Complete cleanup (reset all databases)
#   soft    - Keep databases, only remove temp files
#   verify  - Check what will be deleted (dry run)
#
# ════════════════════════════════════════════════════════════════════

set -e

CLEANUP_TYPE="${1:-verify}"

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║           🧹 EVALUATION CLEANUP SCRIPT                             ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# ════════════════════════════════════════════════════════════════════
# FUNCTION: Show what will be cleaned
# ════════════════════════════════════════════════════════════════════

show_cleanup_plan() {
    echo "📋 CLEANUP PLAN:"
    echo "───────────────────────────────────────────────────────────────────"
    echo ""
    
    echo "🗑️  TEMPORARY FILES TO DELETE:"
    echo "   • /tmp/helena_test.log"
    echo "   • /tmp/pair_test.log"
    echo "   • /tmp/full_test_output.log"
    echo "   • /tmp/usage_test.log"
    echo "   • /tmp/capacity_test.log"
    echo ""
    
    if [ "$CLEANUP_TYPE" = "full" ]; then
        echo "🗄️  DATABASES TO RESET:"
        echo "   • PostgreSQL: Clear all tables (decisions, messages, agent_contexts)"
        echo "   • Neo4j: Delete all nodes and relationships"
        echo "   • Qdrant: Clear destiny-team-framework-master collection"
        echo "   • Redis: Flush all keys"
        echo ""
        echo "⚠️  WARNING: This will DELETE ALL PROJECT DATA!"
        echo "   Only use this if you want a COMPLETE reset."
    else
        echo "🗄️  DATABASES:"
        echo "   • Will NOT be modified (use 'full' cleanup to reset)"
    fi
    echo ""
    echo "───────────────────────────────────────────────────────────────────"
}

# ════════════════════════════════════════════════════════════════════
# FUNCTION: Remove temporary files
# ════════════════════════════════════════════════════════════════════

cleanup_temp_files() {
    echo ""
    echo "🧹 Cleaning temporary files..."
    echo "───────────────────────────────────────────────────────────────────"
    
    FILES=(
        "/tmp/helena_test.log"
        "/tmp/pair_test.log"
        "/tmp/full_test_output.log"
        "/tmp/usage_test.log"
        "/tmp/capacity_test.log"
    )
    
    for file in "${FILES[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            echo "   ✅ Deleted: $file"
        else
            echo "   ⏭️  Not found: $file"
        fi
    done
    
    echo ""
}

# ════════════════════════════════════════════════════════════════════
# FUNCTION: Reset databases (DESTRUCTIVE)
# ════════════════════════════════════════════════════════════════════

reset_databases() {
    echo ""
    echo "🗄️  Resetting databases..."
    echo "───────────────────────────────────────────────────────────────────"
    echo ""
    
    # PostgreSQL
    echo "📊 PostgreSQL: Clearing tables..."
    docker exec sms-postgres psql -U user -d destiny_team -c "
        TRUNCATE TABLE decisions CASCADE;
        TRUNCATE TABLE team_messages CASCADE;
        TRUNCATE TABLE agent_contexts CASCADE;
    " 2>/dev/null && echo "   ✅ PostgreSQL tables cleared" || echo "   ⚠️  PostgreSQL cleanup failed"
    
    # Neo4j
    echo ""
    echo "🕸️  Neo4j: Deleting all nodes..."
    docker exec sms-neo4j cypher-shell -u neo4j -p password "
        MATCH (n) DETACH DELETE n
    " 2>/dev/null && echo "   ✅ Neo4j nodes deleted" || echo "   ⚠️  Neo4j cleanup failed"
    
    # Qdrant
    echo ""
    echo "🔍 Qdrant: Clearing collection..."
    curl -s -X DELETE "http://localhost:6333/collections/destiny-team-framework-master" > /dev/null 2>&1
    # Recreate empty collection
    curl -s -X PUT "http://localhost:6333/collections/destiny-team-framework-master" \
        -H "Content-Type: application/json" \
        -d '{
            "vectors": {
                "size": 1024,
                "distance": "Cosine"
            }
        }' > /dev/null 2>&1 && echo "   ✅ Qdrant collection reset" || echo "   ⚠️  Qdrant cleanup failed"
    
    # Redis
    echo ""
    echo "⚡ Redis: Flushing cache..."
    docker exec kg-redis redis-cli FLUSHALL > /dev/null 2>&1 && \
        echo "   ✅ Redis cache flushed" || echo "   ⚠️  Redis cleanup failed"
    
    echo ""
}

# ════════════════════════════════════════════════════════════════════
# FUNCTION: Verify Docker containers
# ════════════════════════════════════════════════════════════════════

verify_docker() {
    echo ""
    echo "🐳 Verifying Docker containers..."
    echo "───────────────────────────────────────────────────────────────────"
    
    REQUIRED_CONTAINERS=("sms-postgres" "sms-neo4j" "kg-redis" "sms-qdrant")
    ALL_RUNNING=true
    
    for container in "${REQUIRED_CONTAINERS[@]}"; do
        if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
            echo "   ✅ $container: Running"
        else
            echo "   ❌ $container: NOT running"
            ALL_RUNNING=false
        fi
    done
    
    echo ""
    
    if [ "$ALL_RUNNING" = false ]; then
        echo "⚠️  WARNING: Some containers are not running."
        echo "   Start them with: docker-compose up -d"
        echo ""
        return 1
    fi
    
    return 0
}

# ════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ════════════════════════════════════════════════════════════════════

case "$CLEANUP_TYPE" in
    verify)
        echo "🔍 VERIFICATION MODE (dry run - nothing will be deleted)"
        echo ""
        show_cleanup_plan
        echo ""
        echo "To actually clean up, run:"
        echo "  ./CLEANUP_AFTER_EVALUATION.sh soft   (temp files only)"
        echo "  ./CLEANUP_AFTER_EVALUATION.sh full   (temp files + databases)"
        echo ""
        ;;
    
    soft)
        echo "🧹 SOFT CLEANUP (temp files only)"
        echo ""
        show_cleanup_plan
        echo ""
        read -p "Continue with cleanup? (y/N): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cleanup_temp_files
            echo ""
            echo "✅ Soft cleanup complete!"
            echo "   Databases remain unchanged."
        else
            echo "❌ Cleanup cancelled."
        fi
        ;;
    
    full)
        echo "🗑️  FULL CLEANUP (temp files + databases)"
        echo ""
        show_cleanup_plan
        echo ""
        echo "⚠️  WARNING: This will DELETE ALL DATA in databases!"
        echo ""
        read -p "Are you SURE you want to proceed? (yes/no): " -r
        echo ""
        if [[ $REPLY = "yes" ]]; then
            verify_docker || exit 1
            cleanup_temp_files
            reset_databases
            echo ""
            echo "✅ Full cleanup complete!"
            echo "   All test data removed."
            echo "   Databases reset to empty state."
        else
            echo "❌ Cleanup cancelled (must type 'yes' to confirm)."
        fi
        ;;
    
    *)
        echo "❌ Unknown cleanup type: $CLEANUP_TYPE"
        echo ""
        echo "Usage: ./CLEANUP_AFTER_EVALUATION.sh [verify|soft|full]"
        echo ""
        echo "  verify - Show what will be cleaned (default)"
        echo "  soft   - Remove temp files only"
        echo "  full   - Remove temp files AND reset databases"
        echo ""
        exit 1
        ;;
esac

echo ""
echo "───────────────────────────────────────────────────────────────────"
echo "🎯 Cleanup script finished."
echo "───────────────────────────────────────────────────────────────────"
echo ""
